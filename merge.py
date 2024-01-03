import pandas as pd
import datetime as dt
import plotly.graph_objects as go

### PRIMEIRA TAREFA

## Chamar as tabelas csv como um dataframe no pandas
content = pd.read_csv('Content.csv')
reactions = pd.read_csv('Reactions.csv')
reac_types = pd.read_csv('ReactionTypes.csv')

## Retirar as colunas não necessarias para a analise 
content = content.drop(columns=['Unnamed: 0', 'URL','User ID']).dropna(how='any') 
reactions = reactions.drop(columns=['Unnamed: 0','User ID']).dropna(how='any')
reac_types = reac_types.drop(columns=['Unnamed: 0']).dropna(how='any')

## Renomear uma coluna de interesse que apresenta o mesmo nome de outra coluna(que não apresenta os mesmos dados)
content = content.rename(columns={"Type": "Content Type"})

## Junção dos dataframes, automaticamente, utilizando os nomes iguais que foram encontrados entre os dataframes utilizados 
df_merge = pd.merge(reactions,reac_types)
df_merge = pd.merge(content,df_merge)

## Limpeza de dados da coluna Category, retirando as marcas de citação e tornando todas as letras em letras minuscula para um futuro agrupamento de maneira correta
df_merge['Category'] = df_merge['Category'].apply(lambda s: s.replace('"',''))
df_merge['Category'] = df_merge['Category'].str.lower()

## Transformar as datas da coluna Datetime em datas
df_merge['Datetime'] = df_merge['Datetime'].apply(lambda s: dt.datetime.strptime(s,"%Y-%m-%d %H:%M:%S"))

## Obtenção das cinco maiores categorias segundo o score dado pelas reações e salva este resultado em um tabela de excel com o nome de 'result'
df_merge.groupby(['Category'])['Score'].sum().sort_values(ascending=False).head(5).to_excel('result.xlsx')

### SEGUNDA TAREFA - ANALISE DE DADOS E GRAFICOS

## Numero total de Categorias
len(df_merge['Category'].unique())

## Numero de reações para a categoria mais popular
df_merge.groupby(['Category'])['Score'].sum().sort_values(ascending=False).head(1)

df_animals = df_merge[df_merge['Category']== 'animals'] 
len(df_animals['Type'])

## As 5 reações mais comuns para a categoria mais popular
df_animals['Type'].value_counts(ascending=False).head(5)

## As porcentagens de cada reação para a categioria mais popular
df_porct = pd.DataFrame(df_animals['Type'].value_counts(ascending=False)).reset_index()
df_porct['porcentagem'] = df_porct['count']/df_porct['count'].sum() 

## Contagem dos numeros de tipos de conteúdo 
df_merge['Content Type'].value_counts(ascending=False)

## Contagem dos numeros de tipos de conteúdo para a categoria mais popular  
df_animals['Content Type'].value_counts(ascending=False)

## Obtendo o mês e ano mais populares(e um grafico)
df_merge['data_formatada'] = df_merge['Datetime'].dt.strftime('%B-%Y')
df_graph = pd.DataFrame(df_merge['data_formatada'].value_counts(ascending=False)).reset_index()
df_graph['data_sort'] = df_graph['data_formatada'].apply(lambda s: dt.datetime.strptime(s,'%B-%Y'))
df_graph = df_graph.sort_values(by='data_sort')

fig = go.Figure()
fig.add_trace(go.Bar(x=df_graph['data_formatada'], y= df_graph['count'],
                marker_color='rgb(26, 118, 255)',
                text=df_graph['count'],hoverinfo='none'))
fig.update_layout({"paper_bgcolor": "rgba(0, 0, 0, 0)",
        "plot_bgcolor": "rgba(0, 0, 0, 0)",})
fig.update_layout(xaxis=dict(type='category',))
fig.update_yaxes(visible=False, showticklabels=False)
fig.show()