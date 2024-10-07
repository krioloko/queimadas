import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from folium.plugins import HeatMap


# Carregando os dados
@st.cache_data
def load_data():
    df = pd.read_csv('focos_qmd_inpe_2024-01-01_2024-08-30_47.520706.csv', parse_dates=['DataHora'])
    return df

df = load_data()

# Interface do Usuário
st.title('Análise de Focos de Incêndio na Área Metropolitana de Campinas')

# Menu de seleção
option = st.selectbox(
    'Selecione uma opção:',
    ('Mapa de Focos de Incêndio', 'Análise Temporal')
)

if option == 'Mapa de Focos de Incêndio':
    st.subheader('Mapa de Focos de Incêndio')

    # Criando o mapa base centrado em Campinas
    mapa = folium.Map(location=[-22.90, -47.06], zoom_start=10)

    # Criando um mapa de calor
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(mapa)

    # Exibindo o mapa no Streamlit
    st.markdown("### Mapa Interativo")
    st.components.v1.html(mapa._repr_html_(), height=600)

elif option == 'Análise Temporal':
    st.subheader('Análise Temporal dos Focos de Incêndio')

    # Convertendo a coluna DataHora
    df['Data'] = df['DataHora'].dt.date

    # Contagem de focos por data
    focos_por_data = df.groupby('Data').size()

    # Plotando o gráfico
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=focos_por_data.index, y=focos_por_data.values)
    plt.title('Focos de Incêndio por Data')
    plt.xlabel('Data')
    plt.ylabel('Número de Focos de Incêndio')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Exibindo os dados em uma tabela
st.subheader('Dados dos Focos de Incêndio')
st.dataframe(df)