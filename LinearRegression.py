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

df_redux = pd.read_csv('SteamDatasetForStreamlitClean.csv',engine='pyarrow')

#with st.expander('Dataset não filtrado'):
st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_redux.shape[0]} linhas e {df_redux.shape[1]} colunas.
    '''),unsafe_allow_html=True)
    
st.dataframe(df_redux,hide_index=True,height=250)

option = st.selectbox(
    'Escolha o gênero do jogo para gerar a regressão linear',(
    'Roguelike Deckbuilder','4X',
    'Simulation','Management', #=> Esses dois são juntos
    'Open World Survival Craft','City Builder','RPG','Rogue-like','Metroidvania','Dungeon Crawler','Souls-like',
    'Visual Novel','Twin Stick Shooter','Horror','Sexual Content','Card Battler','Beat \'em up','FPS','Shoot \'Em Up'
    'Tower Defense','Match 3','Puzzle-Platformer','Puzzle','2D Platformer','3D Platformer','Battle Royale'),index=7)

df_filtred = df_redux[df_redux['main_genre'] == option]

#---------------- Faltou lugar para upar um novo csv

with st.expander('Dataset preparado'):
    st.markdown(at_lib.GetBasicTextMarkdown(20,
        f'''
        O dataset atualmente possui {df_filtred.shape[0]} linhas e {df_filtred.shape[1]} colunas.
        '''),unsafe_allow_html=True)
        
    st.dataframe(df_filtred,hide_index=True,height=250)

st.table(df_filtred.describe())

x = df_filtred.drop(columns=['total_reviews','tags','id','name','release_date','main_genre','isEarlyAcess',
'hasSingleplayer','hasMultiplayer','hasCoop',''])
y = df_filtred['total_reviews']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

MinMax_scaler = MinMaxScaler()

# Aplicando o Scaler
x_train_scaled = MinMax_scaler.fit_transform(x_train)
x_test_scaled =  MinMax_scaler.fit_transform(x_test)


with st.expander('Grupos de treino e teste escalonados'):
    columns = st.columns([0.5,0.5])
    with columns[0]:
        st.text('Grupo de treino escalonado')
        st.table(x_train_scaled)
    with columns[1]:
        st.text('Grupo de teste escalonado')
        st.table(x_test_scaled)
#st.dataframe(x_train_scaled,hide_index=True,height=250)

modelo_regressao = LinearRegression()
modelo_regressao.fit(x_train_scaled, y_train)

y_pred = modelo_regressao.predict(x_test_scaled)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
#st.text(f"Mean Squared Error: {mse}")

cols = st.columns([0.15,0.3,0.3,0.3])
#Possui dados de categoria?
with cols[1]:
    st.metric(label="MSE", value=f'{mse:.2f}')
with cols[2]:
    st.metric(label="RMSE", value=f'{rmse:.2f}')
with cols[3]:
    st.metric(label="MAE", value=f'{mae:.2f}')

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
