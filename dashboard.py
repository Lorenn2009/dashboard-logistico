import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Dashboard de Análise Logística")



dados = pd.read_excel("planilha_dashboard_logistica.xlsx")


regioes = ["Todas"] + list(dados["Regiao"].unique())

regiao_selecionada = st.sidebar.selectbox(
    "Selecione a Região",
    regioes
)

if regiao_selecionada != "Todas":
    dados = dados[dados["Regiao"] == regiao_selecionada]


total_entregas = len(dados)

atrasadas = len(
    dados[dados["Status"] == "Atrasada"]
)

taxa_atraso = (
    atrasadas / total_entregas * 100
    if total_entregas > 0
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📦 Total de Entregas",
        total_entregas
    )

with col2:
    st.metric(
        "🚨 Entregas Atrasadas",
        atrasadas
    )

with col3:
    st.metric(
        "📊 Taxa de Atraso",
        f"{taxa_atraso:.1f}%"
    )


if taxa_atraso > 20:
    st.error(
        "⚠️ Atenção! A taxa de atraso está acima de 20%."
    )


st.subheader("🚚 Entregas por Transportadora")

grafico_transportadora = (
    dados.groupby("Transportadora")
    .size()
    .reset_index(name="Quantidade")
)

fig1 = px.bar(
      grafico_transportadora,
    x="Transportadora",
    y="Quantidade",
    color="Transportadora",
    template="plotly_white",
    title="Quantidade de Entregas por Transportadora",
    color_discrete_map={
        "LogFast": "#4CAF50",
        "RapidoSul": "#2196F3",
        "ExpressoBr": "#FF9800"
    }
)

st.plotly_chart(
    fig1,
    use_container_width=True
)



st.subheader("🌎 Distribuição por Região")

grafico_regiao = (
    dados.groupby("Regiao")
    .size()
    .reset_index(name="Quantidade")
)

fig2 = px.pie(
     grafico_regiao,
    names="Regiao",
    values="Quantidade",
    title="Distribuição das Entregas",
    color="Regiao",
    color_discrete_map={
        "Sul": "#4CAF50",
        "Sudeste": "#2196F3",
        "Nordeste": "#FF9800",
        "Norte": "#9C27B0",
        "Centro-Oeste": "#F44336"
    }
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


st.subheader("🚨 Entregas Atrasadas")

atrasos = dados[
    dados["Status"] == "Atrasada"
]

st.dataframe(atrasos)

st.subheader("📋 Base Completa")

st.dataframe(dados)