from dataclasses import dataclass
import pandas as pd

DESTINOS_VALIDOS = {"reuso", "reciclagem", "aterro", "armazenado"}


@dataclass(frozen=True)
class KPIResultado:
    massa_recebida_kg: float
    massa_reuso_kg: float
    massa_reciclagem_kg: float
    massa_aterro_kg: float
    taxa_reaproveitamento_pct: float
    desvio_aterro_pct: float
    valor_recuperado_rs: float


def validar_df(df: pd.DataFrame) -> None:
    colunas = {"data", "ponto_coleta", "categoria", "massa_kg", "destino"}
    faltando = colunas - set(df.columns)

    if faltando:
        raise ValueError(f"CSV faltando colunas: {sorted(faltando)}")


def calcular_kpis(df: pd.DataFrame, valor_por_kg=None):

    recebida = df["massa_kg"].sum()

    reuso = df[df["destino"] == "reuso"]["massa_kg"].sum()
    reciclagem = df[df["destino"] == "reciclagem"]["massa_kg"].sum()
    aterro = df[df["destino"] == "aterro"]["massa_kg"].sum()

    taxa = ((reuso + reciclagem) / recebida) * 100 if recebida else 0
    desvio = (1 - (aterro / recebida)) * 100 if recebida else 0

    valor = 0
    if valor_por_kg:
        reaproveitados = df[df["destino"].isin(["reuso", "reciclagem"])]

        for i, row in reaproveitados.iterrows():
            valor += row["massa_kg"] * valor_por_kg.get(row["categoria"], 0)

    return KPIResultado(
        recebida,
        reuso,
        reciclagem,
        aterro,
        taxa,
        desvio,
        valor
    )
