import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import streamlit as st
import StreamlitCustomLibrary as at_lib

at_lib.SetPageConfig()
at_lib.SetTheme()

st.header('Análise exploratória',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(25,
    '''
    Finalmente com o dataset limpo e pronto para ser utilizado, podemos começar a análise exploratória e identificar\
    as variáveis independentes que mais influenciam na variável dependente, que é o número total de reviews.
    '''),unsafe_allow_html=True)

df_steam = pd.read_csv('SteamDatasetForStreamlitCleaned.csv',engine='pyarrow')

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

df_steam.set_index('id',inplace=True)
st.dataframe(df_steam,height=250)

st.divider()

#st.dataframe(df_steam.describe(),height=250,hide_index=True)

#nCols = ['total_duration','total_achievements','total_supported_languages','positive_reviews_percent','price', 'self_published_percent','commercialization_days']
df_steam_numerics = df_steam.drop(columns=['name','release_date','tags','main_genre','hasSingleplayer','hasMultiplayer','hasCoop','self_published_percent'])


x_plots = 2
y_plots = 3

st.subheader('Filtros',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(25,
    '''
    Aqui estão alguns controladores para filtrar os dados, removendo outliers de cada coluna. Mais abaixo estão os gráficos\
    que permitem visualizar os dados filtrados. 
    '''),unsafe_allow_html=True)
#É importante que essa filtragem seja feita já pensando no tipo de jogo que se\
 #   quer prever, por exemplo, RPGs tendem a ter uma duração maior que jogos de plataforma, portanto eliminar os outliers superiores\
   # pode não ser uma ideia adequada cas

min_max_total_reviews = st.slider("Número total de reviews:", value=(df_steam_numerics['total_reviews'].min(), df_steam_numerics['total_reviews'].max()))
df_steam_numerics = df_steam_numerics[(df_steam_numerics['total_reviews'] >= min_max_total_reviews[0]) & (df_steam_numerics['total_reviews'] <= min_max_total_reviews[1])]

cols = st.columns(3)
with cols[0]:
    min_max_duration = st.slider("Duração total:", value=(df_steam_numerics['total_duration'].min(), df_steam_numerics['total_duration'].max()))
    df_steam_numerics = df_steam_numerics[(df_steam_numerics['total_duration'] >= min_max_duration[0]) & (df_steam_numerics['total_duration'] <= min_max_duration[1])]
    min_max_positive_reviews_percent = st.slider("Porcentagem de reviews positivas:", value=(df_steam_numerics['positive_reviews_percent'].min(), df_steam_numerics['positive_reviews_percent'].max()))
    df_steam_numerics = df_steam_numerics[(df_steam_numerics['positive_reviews_percent'] >= min_max_positive_reviews_percent[0]) & (df_steam_numerics['positive_reviews_percent'] <= min_max_positive_reviews_percent[1])]
with cols[1]:
    min_max_commercialization_days = st.slider("Dias de comercialização:", value=(df_steam_numerics['commercialization_days'].min(), df_steam_numerics['commercialization_days'].max()))
    df_steam_numerics = df_steam_numerics[(df_steam_numerics['commercialization_days'] >= min_max_commercialization_days[0]) & (df_steam_numerics['commercialization_days'] <= min_max_commercialization_days[1])]
    min_max_total_supported_languages = st.slider("Número de idiomas suportados:", value=(df_steam_numerics['total_supported_languages'].min(), df_steam_numerics['total_supported_languages'].max()))
    df_steam_numerics = df_steam_numerics[(df_steam_numerics['total_supported_languages'] >= min_max_total_supported_languages[0]) & (df_steam_numerics['total_supported_languages'] <= min_max_total_supported_languages[1])]
with cols[2]:
    min_max_price = st.slider("Faixa de preço:", value=(df_steam_numerics['price'].min(), df_steam_numerics['price'].max()))
    df_steam_numerics = df_steam_numerics[(df_steam_numerics['price'] >= min_max_price[0]) & (df_steam_numerics['price'] <= min_max_price[1])]
    min_max_total_achievements = st.slider("Número de conquistas:", value=(df_steam_numerics['total_achievements'].min(), df_steam_numerics['total_achievements'].max()))
    df_steam_numerics = df_steam_numerics[(df_steam_numerics['total_achievements'] >= min_max_total_achievements[0]) & (df_steam_numerics['total_achievements'] <= min_max_total_achievements[1])]

st.markdown(at_lib.GetBasicTextMarkdown(25,f'''Quantidade de jogos restantes no dataset: {df_steam_numerics.shape[0]}'''),unsafe_allow_html=True)
st.subheader('Boxplot',divider=True)

fig, axs = plt.subplots(x_plots,y_plots,figsize=(15, 10))

i  = 0
for r in range(x_plots):
    for c in range(y_plots):
        colName = df_steam_numerics.columns[i]
        if colName == 'total_reviews':
            i = i + 1
            colName = df_steam_numerics.columns[i]
        sb.boxplot(data=df_steam_numerics[colName],  ax=axs[r, c], orient='v',color=sb.color_palette()[i % len(sb.color_palette())])
        i = i + 1
        
plt.subplots_adjust(wspace=0.3, hspace=0.0)
st.pyplot(fig)
st.subheader('Dispersão',divider=True)

fig, axs = plt.subplots(x_plots,y_plots,figsize=(15, 10))

i  = 0
for r in range(x_plots):
    for c in range(y_plots):
        if df_steam_numerics.columns[i] == 'total_reviews':
            i += 1
        sb.regplot(data=df_steam_numerics, x=df_steam_numerics.columns[i], y='total_reviews', ax=axs[r, c],
        color= sb.color_palette()[i % len(sb.color_palette())],line_kws={'color':'red'})
        i += 1
        
plt.subplots_adjust(wspace=0.3, hspace=0.3)
st.pyplot(fig)
st.subheader('Mapa de calor',divider=True)
fig, ax = plt.subplots(figsize=(15, 5))

nOrder = list(df_steam_numerics.columns)
nOrder.remove('total_reviews')
nOrder.append('total_reviews')

df_steam_numerics = df_steam_numerics[nOrder]

df_steam_corr = df_steam_numerics.corr()
sb.heatmap(df_steam_corr, annot=True, fmt='.2f',cmap=sb.color_palette("coolwarm", as_cmap=True), ax=ax, mask=np.triu(df_steam_corr, k=1),vmin=-1, vmax=1)
ax.axhline(6, color='yellow', linewidth=2)
ax.axhline(7, color='yellow', linewidth=4)

st.pyplot(fig)

#df_steam.drop(columns=['hasSingleplayer','hasMultiplayer','hasCoop','self_published_percent','main_genre','tags','name'],inplace=True)

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam_numerics.shape[0]} linhas e {df_steam_numerics.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam_numerics,height=250)

st.download_button(
    label="Baixar o dataset preparado",
    data=df_steam_numerics.to_csv(index=True),
    file_name='SteamDatasetForStreamlitReadyForRegression.csv',
    mime='text/csv',
)
