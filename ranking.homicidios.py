# Importação de Bibliotecas

import streamlit as st
import pandas as pd
import plotly.express as px


# Ranking Homicídios 2026

df = pd.DataFrame({
    "ranking_regional": [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
        12, 13, 14, 15, 16, 17, 18, 19, 20, 21
    ],

    "ranking_nacional": [
        1834, 2535, 2709, 2842, 2914, 3117, 3133, 3275, 3325, 3383, 3694,
        3881, 3987, 4400, 4408, 4435, 4450, 4505, 4541, 4553, 4703
    ],

    "municipio": [
        "Novo Cruzeiro", "Santa Maria do Suaçuí", "Ladainha", "Angelândia",
        "Capelinha", "Setubinha", "São Sebastião do Maranhão", "Itamarandiba",
        "Virgem da Lapa", "Água Boa", "Turmalina", "José Gonçalves de Minas",
        "Minas Novas", "Aricanduva", "Berilo", "Carbonita", "Chapada do Norte",
        "Francisco Badaró", "Jenipapo de Minas", "Leme do Prado", "Veredinha"
    ],

    "homicidios_registrados": [
        6, 2, 2, 1, 5, 1, 1, 3, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],

    "populacao": [
        27453, 12898, 14399, 7860, 41536, 10032, 10244, 34137, 11867, 12545, 20650,
        3993, 24191, 4820, 9769, 8633, 10024, 7208, 6124, 4387, 5257
    ],

    "taxa_homicidios_registrados": [
        21.9, 15.5, 13.9, 12.7, 12.0, 10.0, 9.8, 8.8, 8.4, 8.0, 4.8,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]
})


# Título do painel

st.title("Ranking de Homicídios - Gazeta dos Vales")


# FILTRO SLIDER POR TAXA DE HOMICÍDIOS

st.subheader("Gráfico de barras por homicídios")


taxa_minima = float(df["taxa_homicidios_registrados"].min())
taxa_maxima = float(df["taxa_homicidios_registrados"].max())

filtro_taxa = st.slider(
    "Selecione a taxa mínima de homicídios registrados:",
    min_value=taxa_minima,
    max_value=taxa_maxima,
    value=taxa_minima,
    step=0.1
)

df_filtrado_taxa = df[
    df["taxa_homicidios_registrados"] >= filtro_taxa
]


# Ordenar pela maior taxa

df_filtrado_taxa = df_filtrado_taxa.sort_values(
    by="taxa_homicidios_registrados",
    ascending=False
)


# Gráfico

fig = px.bar(
    df_filtrado_taxa,
    x="taxa_homicidios_registrados",
    y="municipio",
    orientation="h",
    text="taxa_homicidios_registrados",
    title="Taxa de Homicídios Registrados",
    hover_data=[
        "ranking_regional",
        "ranking_nacional",
        "homicidios_registrados",
        "populacao"
    ]
)

fig.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    },
    height=700,
    xaxis_title="Taxa de Homicídios Registrados",
    yaxis_title="Município"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(fig, use_container_width=True)

# RANKING POR TAMANHO DA POPULAÇÃO - BARRAS

st.subheader("Gráfico de barras por população")

df_populacao = df.sort_values(
    by="populacao",
    ascending=False
).copy()

df_populacao["ranking_populacao"] = range(1, len(df_populacao) + 1)

fig_populacao = px.bar(
    df_populacao,
    x="municipio",
    y="populacao",
    text="populacao",
    title="Ranking dos Municípios por Tamanho da População",
    hover_data=[
        "ranking_populacao",
        "ranking_regional",
        "ranking_nacional",
        "homicidios_registrados",
        "taxa_homicidios_registrados"
    ]
)

fig_populacao.update_layout(
    height=700,
    xaxis_title="Município",
    yaxis_title="População",
    xaxis_tickangle=-45
)

fig_populacao.update_traces(
    textposition="outside"
)

st.plotly_chart(fig_populacao, use_container_width=True)

# ==============================
# FILTRO MULTISELECT POR MUNICÍPIO
# ==============================

st.subheader("Selectbox de município")

municipios_selecionados = st.multiselect(
    "Selecione os municípios",
    options=df["municipio"].tolist(),
    default=["Novo Cruzeiro", "Capelinha"]
)

if municipios_selecionados:
    filtrado = df[df["municipio"].isin(municipios_selecionados)]

    filtrado = filtrado[
        [
            "ranking_regional",
            "ranking_nacional",
            "municipio",
            "homicidios_registrados",
            "taxa_homicidios_registrados"
        ]
    ]

    st.dataframe(
        filtrado,
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("Selecione ao menos um município.")