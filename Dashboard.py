import streamlit as st
import requests
import pandas as pd
import plotly.express as px


##Configuração da página
st.set_page_config( layout='wide')
st.set_page_config(page_title = 'Dashboard de Vendas')


## Função para formatar números
def formatar_numero(valor, prefixo=''):
    for unidade in ['','mil']:
        if valor <1000:
            return f'{prefixo}{valor:.2f} {unidade}'
        valor /=1000
    return f'{prefixo}{valor:.2f} Milhoes'

# Título do Dashboard
st.title('DASHBOARD DE VENDAS :shopping_cart:')

## Criação de Abas do Dashboard
aba1, aba2, aba3 = st.tabs(['Receita','Quantidade de Vendas','vendedores'])

url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format= '%d/%m/%Y')

## tabela de dados:

### Tabela de Receitas
receitas_estados = dados.groupby('Local da Compra')['Preço'].sum()
receitas_estados = receitas_estados.drop_duplicates(subset='Local da Compra')[['Local da Compra', 'lat','lon']].merge(receitas_estados, left_on='Local da Compra', right_index=True).sort_values(by='preco', ascending=False)

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categoria = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by='Preço', ascending=False)

### Tabelas de Quantidade de vendas

vendas_estados = pd.DataFrame(dados.groupby('Local da compra')['Preço'].count())
vendas_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra','lat', 'lon']].merge(vendas_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)

vendas_mensal = pd.DataFrame(dados.set_index('Data da Compra').groupby(pd.Grouper(freq = 'M'))['Preço'].count()).reset_index()
vendas_mensal['Ano'] = vendas_mensal['Data da Compra'].dt.year
vendas_mensal['Mes'] = vendas_mensal['Data da Compra'].dt.month_name()

vendas_categorias = pd.DataFrame(dados.groupby('Categoria do Produto')['Preço'].count().sort_values(ascending = False))

### Tabelas de Vendedores
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))



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


## graficos de quantidade de vendas

fig_mapa_vendas = px.scatter_geo(vendas_estados, 
                     lat = 'lat', 
                     lon= 'lon', 
                     scope = 'south america', 
                     #fitbounds = 'locations', 
                     template='seaborn', 
                     size = 'Preço', 
                     hover_name ='Local da compra', 
                     hover_data = {'lat':False,'lon':False},
                     title = 'Vendas por estado',
                     )


fig_vendas_mensal = px.line(vendas_mensal, 
              x = 'Mes',
              y='Preço',
              markers = True, 
              range_y = (0,vendas_mensal.max()), 
              color = 'Ano', 
              line_dash = 'Ano',
              title = 'Quantidade de vendas mensal')

fig_vendas_mensal.update_layout(yaxis_title='Quantidade de vendas')



fig_vendas_estados = px.bar(vendas_estados.head(),
                             x ='Local da compra',
                             y = 'Preço',
                             text_auto = True,
                             title = 'Top 5 estados'
)

fig_vendas_estados.update_layout(yaxis_title='Quantidade de vendas')


fig_vendas_categorias = px.bar(vendas_categorias, 
                                text_auto = True,
                                title = 'Vendas por categoria')
fig_vendas_categorias.update_layout(showlegend=False, yaxis_title='Quantidade de vendas')

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
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', formatar_numero(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_vendas, use_container_width = True)
        st.plotly_chart(fig_vendas_estados, use_container_width = True)

    with coluna2:
        st.metric('Quantidade de vendas', formatar_numero(dados.shape[0]))
        st.plotly_chart(fig_vendas_mensal, use_container_width = True)
        st.plotly_chart(fig_vendas_categorias, use_container_width = True)


##Criação de colunas aba 3
with aba3:
    qtde_vedendores = st.number_input('Quantidade de vendedores', min_value=2, max_value=10, value=5)
    coluna1 , coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita',formatar_numero(dados['Preço'].sum()), 'R$')
        fig_receita_vendedores = px.bar(vendedores[['sum']].sort_values(by='sum', ascending=False).head(qtde_vedendores),
                                        x='sum',
                                        y=vendedores[['sum']].sort_values(by='sum', ascending=False).head(qtde_vedendores).index,
                                        text_auto=True,
                                        title=f'Top {qtde_vedendores} vendedores por receita')
        st.plotly_chart(fig_receita_vendedores, use_container_width=True)                                

    with coluna2:
        st.metric('quantidade de vendas',formatar_numero(dados.shape[0]))
        fig_vendas_vendedores = px.bar(vendedores[['count']].sort_values(by='count', ascending=False).head(qtde_vedendores),
                                        x='count',
                                        y=vendedores[['count']].sort_values(by='count', ascending=False).head(qtde_vedendores).index,
                                        text_auto=True,
                                        title=f'Top {qtde_vedendores}  por quantidade de vendas')
        st.plotly_chart(fig_vendas_vendedores, use_container_width=True)  

#st.dataframe(dados)

