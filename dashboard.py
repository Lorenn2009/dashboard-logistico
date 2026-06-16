import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="📦",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC;
}
</style>
""", unsafe_allow_html=True)


dados = pd.read_excel(
    "planilha_dashboard_logistica.xlsx"
)


total_entregas = len(dados)

atrasadas = len(
    dados[dados["Status"] == "Atrasada"]
)

taxa = (
    atrasadas / total_entregas
) * 100



st.title("📦 Dashboard Logístico")

st.markdown("""
<div style="
background-color:#E3F2FD;
padding:20px;
border-radius:15px;
border-left:8px solid #1E88E5;
margin-bottom:20px;
">

<h3>🚚 Monitoramento de Entregas</h3>

<p>
Este dashboard apresenta informações sobre entregas,
atrasos, desempenho das transportadoras e distribuição
regional das operações.
</p>

</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

col1.metric(
    "📦 Total de Entregas",
    total_entregas
)

col2.metric(
    "🚨 Entregas Atrasadas",
    atrasadas
)

col3.metric(
    "📊 Taxa de Atraso",
    f"{taxa:.1f}%"
)

st.divider()



if taxa > 20:

    st.markdown(f"""
    <div style="
    background-color:#FFEBEE;
    padding:15px;
    border-radius:10px;
    border-left:8px solid red;
    margin-bottom:20px;
    ">

    <h4>🚨 Atenção</h4>

    <p>
    A taxa de atraso atual é de
    <b>{taxa:.1f}%</b>.
    Recomenda-se investigar as causas.
    </p>

    </div>
    """, unsafe_allow_html=True)


atrasos_transportadora = (
    dados[dados["Status"] == "Atrasada"]
    ["Transportadora"]
    .value_counts()
    .reset_index()
)

atrasos_transportadora.columns = [
    "Transportadora",
    "Atrasos"
]

menor = atrasos_transportadora["Atrasos"].min()
maior = atrasos_transportadora["Atrasos"].max()

def categoria(valor):

    if valor == menor:
        return "Melhor"

    elif valor == maior:
        return "Pior"

    else:
        return "Intermediária"

atrasos_transportadora["Categoria"] = (
    atrasos_transportadora["Atrasos"]
    .apply(categoria)
)

fig1 = px.bar(
    atrasos_transportadora,
    x="Transportadora",
    y="Atrasos",
    color="Categoria",
    title="🚚 Atrasos por Transportadora",
    color_discrete_map={
        "Melhor": "green",
        "Intermediária": "gold",
        "Pior": "red"
    }
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

melhor_transportadora = (
    atrasos_transportadora
    .sort_values("Atrasos")
    .iloc[0]["Transportadora"]
)

st.markdown(f"""
<div style="
background-color:#E8F5E9;
padding:15px;
border-radius:10px;
border-left:8px solid green;
margin-bottom:20px;
">

<h4>🏆 Melhor Desempenho</h4>

<p>
A transportadora
<b>{melhor_transportadora}</b>
apresentou o menor número de atrasos.
</p>

</div>
""", unsafe_allow_html=True)

regioes = (
    dados["Regiao"]
    .value_counts()
    .reset_index()
)

regioes.columns = [
    "Regiao",
    "Quantidade"
]

fig2 = px.pie(
    regioes,
    names="Regiao",
    values="Quantidade",
    title="📍 Distribuição por Região"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

st.subheader("🚨 Entregas Atrasadas")

st.dataframe(
    dados[dados["Status"] == "Atrasada"]
)

st.divider()

st.subheader("📋 Base Completa")

st.dataframe(dados)