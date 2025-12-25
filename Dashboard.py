import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config( layout='wide')

def formatar_numero(valor, prefixo=''):
    for unidade in ['','mil']:
        if valor <1000:
            return f'{prefixo}{valor:.2f} {unidade}'
        valor /=1000
    return f'{prefixo}{valor:.2f} Milhoes'

st.title('DASHBOARD DE VENDAS :shopping_cart:')

aba1, aba2, aba3 = st.tabs(['Receita','Quantidade de Vendas','vendedores'])

url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format= '%d/%m/%Y')

## tabela de dados
receitas_estados = dados.groupby('Local da Compra')['Preço'].sum()
receitas_estados = receitas_estados.drop_duplicates(subset='Local da Compra')[['Local da Compra', 'lat','lon']].merge(receitas_estados, left_on='Local da Compra', right_index=True).sort_values(by='preco', ascending=False)

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()


receita_categoria = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by='Preço', ascending=False)


## Criação de Graficos
fig_mapa_receita = px.scatter_geo(receitas_estados,
                                  lat= 'lat',
                                  lon= 'lon',
                                  scope='south america',
                                  size='Preço',
                                  template='seaborn',
                                  hover_name='Local da Compra',
                                  hover_data= {'lat':False, 'lon':False},
                                  title='Receita por estado')

fig_receita_mensal = px.line(receita_mensal,
                             x='Mes',
                             y='Preço',
                             markers=True,
                             range_y=(0, receita_mensal.max()),
                             color='Ano',
                             line_dash='Ano',
                             title='Receita Mensal')
fig_receita_mensal.update_layout(yaxis_title='Receita')


fig_receita_estados = px.bar(receitas_estados.head(),
                             x='Local da Compra',
                             y='Preço',
                             text_auto=True,
                             title='Top 5 estados por receita')
fig_receita_estados.update_layout(yaxis_title='Receita')

fig_receita_categoria = px.bar(receita_categoria,
                               text_auto=True,
                               title='Receita por categoria de produto')
fig_receita_estados.update_layout(yaxis_title='Receita')


## Visualizações no Streamlit

## Criação de Abas
##aba1, aba2, aba3 = st.tabs(['Receita','Quantidade de Vendas','vendedores'])


##Criação de colunas aba 1
with aba1:
     coluna1 , coluna2 = st.columns(2)
     with coluna1:
         st.metric('Receita',formatar_numero(dados['Preço'].sum()), 'R$')
         st.plotly_chart(fig_mapa_receita, use_container_width=True)
         st.plotly_chart(fig_receita_estados, use_container_width=True)

     with coluna2:
         st.metric('quantidade de vendas',formatar_numero(dados.shape[0]))
         st.plotly_chart(fig_receita_mensal, use_container_width=True)
         st.plotly_chart(fig_receita_categoria, use_container_width=True)


##Criação de colunas aba 2
with aba2:
    coluna1 , coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita',formatar_numero(dados['Preço'].sum()), 'R$')


    with coluna2:
        st.metric('quantidade de vendas',formatar_numero(dados.shape[0]))

##Criação de colunas aba 3
with aba3:
    coluna1 , coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita',formatar_numero(dados['Preço'].sum()), 'R$')


    with coluna2:
        st.metric('quantidade de vendas',formatar_numero(dados.shape[0]))




#st.dataframe(dados)

