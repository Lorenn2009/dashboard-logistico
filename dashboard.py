import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
page_title="Dashboard Logístico",
page_icon="🚚",
layout="wide"
)

st.title("🚚 Dashboard de Análise Logística")

# Carrega a planilha

dados = pd.read_excel("planilha_dashboard_logistica.xlsx")

# Cria o status automaticamente

dados["Status"] = dados.apply(
lambda x: "Atrasada"
if x["dias_reais"] > x["prazo_dias"]
else "Entregue",
axis=1
)

# Calcula atraso

dados["atraso"] = (
dados["dias_reais"] - dados["prazo_dias"]
)

# Filtro de região

regioes = ["Todas"] + list(dados["regiao"].unique())

regiao_selecionada = st.sidebar.selectbox(
"Selecione a Região",
regioes
)

if regiao_selecionada != "Todas":
    dados = dados[dados["regiao"] == regiao_selecionada]

# Métricas

total_entregas = len(dados)

atrasadas = len(
dados[dados["Status"] == "Atrasada"]
)

taxa_atraso = (
atrasadas / total_entregas * 100
if total_entregas > 0
else 0
)

media_atraso = (
dados["atraso"].clip(lower=0).mean()
)

col1, col2, col3, col4 = st.columns(4)

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

with col4:
    st.metric(
        "⏱️ Média de Atraso",
        f"{media_atraso:.1f} dias"
)

if taxa_atraso > 20:
    st.error(
        "⚠️ Atenção! A taxa de atraso está acima de 20%."
)

# Gráfico por transportadora

st.subheader("🚚 Entregas por Transportadora")

grafico_transportadora = (
dados.groupby("transportadora")
.size()
.reset_index(name="Quantidade")
)

fig1 = px.bar(
grafico_transportadora,
x="transportadora",
y="Quantidade",
color="transportadora",
template="plotly_white",
title="Quantidade de Entregas por Transportadora"
)

st.plotly_chart(
fig1,
use_container_width=True
)

# Gráfico por região

st.subheader("🌎 Distribuição por Região")

grafico_regiao = (
dados.groupby("regiao")
.size()
.reset_index(name="Quantidade")
)

fig2 = px.pie(
grafico_regiao,
names="regiao",
values="Quantidade",
title="Distribuição das Entregas"
)

st.plotly_chart(
fig2,
use_container_width=True
)

# Status das entregas

st.subheader("📈 Status das Entregas")

status_df = (
dados.groupby("Status")
.size()
.reset_index(name="Quantidade")
)

fig3 = px.bar(
status_df,
x="Status",
y="Quantidade",
color="Status",
template="plotly_white"
)

st.plotly_chart(
fig3,
use_container_width=True
)

# Entregas atrasadas

st.subheader("🚨 Entregas Atrasadas")

atrasos = dados[
dados["Status"] == "Atrasada"
]

st.dataframe(atrasos)

# Base completa

st.subheader("📋 Base Completa")

st.dataframe(dados)
