import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def formatar_numero(valor, prefixo=''):
    for unidade in ['','mil']:
        if valor <1000:
            return f'{prefixo}{valor:.2f} {unidade}'
        valor /=1000
    return f'{prefixo}{valor:.2f} Milhoes'

st.title('DASHBOARD DE VENDAS :shopping_cart:')

url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

coluna1 , coluna2 = st.columns(2)
with coluna1:
    st.metric('Receita',formatar_numero(dados['preco'].sum()), 'R$')
with coluna2:
    st.metric('quantidade de vendas',formatar_numero(dados.shape[0]))





st.dataframe(dados)

