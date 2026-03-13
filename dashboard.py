import streamlit as st
import pandas as pd
from kpis import calcular_kpis

st.set_page_config(page_title="Chipper Recycling", layout="wide")

st.title("Chipper Recycling ♻️")

VALOR_POR_KG = {
    "smartphone": 120,
    "notebook": 90,
    "tablet": 75,
    "perifericos": 30
}

arquivo = st.file_uploader("Carregar CSV", type=["csv"])

if arquivo:
    df = pd.read_csv(arquivo)
else:
    df = pd.read_csv("data_sample.csv")

resultado = calcular_kpis(df, VALOR_POR_KG)

st.metric("Massa recebida", f"{resultado.massa_recebida_kg:.2f} kg")
st.metric("Taxa reaproveitamento", f"{resultado.taxa_reaproveitamento_pct:.2f}%")
st.metric("Desvio de aterro", f"{resultado.desvio_aterro_pct:.2f}%")
st.metric("Valor recuperado", f"R$ {resultado.valor_recuperado_rs:.2f}")

st.bar_chart(df.groupby("destino")["massa_kg"].sum())