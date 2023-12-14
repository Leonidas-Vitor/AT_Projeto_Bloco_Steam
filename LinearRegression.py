import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import StreamlitCustomLibrary as at_lib
import plotly.graph_objects as go

at_lib.SetPageConfig()
at_lib.SetTheme()

st.header('Regressão linear',divider=True)

#st.warning('''
#    O dataset pode demorar um pouco para ser carregado pois se ele não foi processado nas outras páginas ele será todo\
#    processado agora.
#    ''', icon="⚠️")

#st.markdown(at_lib.GetBasicTextMarkdown(25,
#    '''
#    Teste2
#    '''),unsafe_allow_html=True)

df_steam = pd.read_csv('SteamDatasetForStreamlitReadyForRegressionLog.csv',engine='pyarrow')

#with st.expander('Dataset não filtrado'):
st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)
    
st.dataframe(df_steam,height=250,use_container_width=True)


#---------------- Faltou lugar para upar um novo csv

with st.expander('Dataset preparado'):
    st.markdown(at_lib.GetBasicTextMarkdown(20,
        f'''
        O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
        '''),unsafe_allow_html=True)
        
    st.dataframe(df_steam,hide_index=True,height=250)

st.table(df_steam.describe())


x = df_steam[['total_duration','price','total_supported_languages', 'total_achievements']]
y = df_steam['total_reviews']

num_repeats = 1000

st.subheader('Modelo de regressão',divider=True)
st.markdown(at_lib.GetBasicTextMarkdown(20,
f'''
Os dados estão sendo separados em 70% para treino e 30% para teste, sendo escalonados com o MinMaxScaler. \
O modelo utilizado é o LinearRegression do sklearn e a métrica utilizada é o MSE, RMSE e o MAE médios \
de {num_repeats} repetições. O processo pode demorar um pouco, por favor aguarde.
'''),unsafe_allow_html=True)

mse_scores = []
rmse_scores = []
mae_scores = []

reviews = []

game_example = pd.DataFrame({'total_duration': [15], 'price': [14.99], 
'total_supported_languages': [3], 'total_achievements': [100]})

MinMax_scaler = MinMaxScaler()



for _ in range(num_repeats):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    # Aplicando o Scaler
    x_train_scaled = MinMax_scaler.fit_transform(x_train)
    game_example_scaled = MinMax_scaler.transform(game_example)

    x_test_scaled =  MinMax_scaler.fit_transform(x_test)

    modelo_regressao = LinearRegression()
    modelo_regressao.fit(x_train_scaled, y_train)


    y_pred = modelo_regressao.predict(x_test_scaled)
    
    #st.write(y_pred)

    mse = mean_squared_error(y_test, y_pred)
    mse_scores.append(mse)

    rmse = np.sqrt(mse)
    rmse_scores.append(rmse)

    mae = mean_absolute_error(y_test, y_pred)
    mae_scores.append(mae)

    reviews.append(modelo_regressao.predict(game_example_scaled))

#with st.expander('Grupos de treino e teste escalonados'):
#    columns = st.columns([0.5,0.5])
#    with columns[0]:
#        st.text('Grupo de treino escalonado')
#        st.table(x_train_scaled)
#    with columns[1]:
#        st.text('Grupo de teste escalonado')
#        st.table(x_test_scaled)
#st.dataframe(x_train_scaled,hide_index=True,height=250)

#st.table(reviews)

#st.text(f"Mean Squared Error: {mse}")

cols = st.columns([0.15,0.3,0.3,0.3])
#Possui dados de categoria?
with cols[1]:
    st.metric(label=f"MSE médio de {num_repeats} repetições", value=f'{np.mean(np.exp(mse_scores)):.2f}')
with cols[2]:
    st.metric(label=f"RMSE de {num_repeats} repetições", value=f'{np.mean(np.exp(rmse_scores)):.2f}')
with cols[3]:
    st.metric(label=f"MAE de {num_repeats} repetições", value=f'{np.mean(np.exp(mae_scores)):.2f}')
st.subheader('Estimativa de faturamento',divider=True)

predReviews = int(np.mean(np.exp(reviews))-1)
st.markdown(at_lib.GetBasicTextMarkdown(25,f'''Previsão de reviews: {predReviews}'''),unsafe_allow_html=True)

##Explicar a regra dos 30

cT = st.slider('Taxa de conversão: Quanto cada review é convertido em vendas?',min_value=1,max_value=100,value=30,step=1)

pT = st.slider('Taxa da publicadora: Quantos porcentos do faturamento pertence a publicadora? (%)',min_value=0,max_value=100,value=0,step=1)

steamCut = predReviews*cT*0.7
euaTaxCut = steamCut * 0.7
publisherCut = euaTaxCut * (1-(pT/100))
brTaxCut = publisherCut * 0.845

data = {##Falta IOF, e SPread
    'Etapa': ['Steam - 30%', 'EUA Imposto - 30%', f'Publicadora - {pt}%', 'Imposto sob faturamento - 15,5%'],
    'Quantidade': [steamCut, euaTaxCut, publisherCut, brTaxCut]
}

# Cria um gráfico de funil
fig = go.Figure(go.Funnel(
    y = data['Etapa'],
    x = data['Quantidade'],
    #textinfo = "value+percent initial",
    marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal"],
    "line": {"width": [4, 2, 2, 3, 1], "color": ["wheat", "wheat", "blue", "wheat"]}},
    connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3},"fillcolor":'white'},
))

st.plotly_chart(fig, use_container_width=True)
st.subheader('Gráficos de avaliação do modelo',divider=True)

with st.expander('Gráficos de Dispersão'):
    for col in x_test.columns:
        if col == '':
            continue
        fig, ax = plt.subplots(figsize=(10,5))
        sb.scatterplot(x=x_test[col], y=y_test, color='yellow', label='Real',ax = ax,alpha=0.5)
        sb.scatterplot(x=x_test[col], y=y_pred, color='blue', label='Previsto',ax = ax,alpha=0.5)
        ax.ticklabel_format(style='plain', axis='both')
        st.pyplot(fig)

with st.expander('Gráficos de regressão'):
    for col in x_test.columns:
        if col == '':
            continue
        st.text(col)
        fig, ax = plt.subplots(figsize=(10,5))
        df_resultado = pd.DataFrame({col: x_test[col], 'Real': y_test, 'Previsto': y_pred})
        t = sb.lmplot(data=df_resultado,x=col, y='Previsto', aspect=2, height=6)
        sb.scatterplot(x=x_test[col], y=y_test, color='yellow', label='Real',ax = t.ax,alpha=0.5)
        st.pyplot(t)

with st.expander('Gráfico de Resíduos'):
    for col in x_test.columns:
        if col == '':
            continue
        fig, ax = plt.subplots(figsize=(10,5))
        residuos = y_test - y_pred
        sb.scatterplot(x=x_test[col], y=residuos,ax = ax)
        st.pyplot(fig)
