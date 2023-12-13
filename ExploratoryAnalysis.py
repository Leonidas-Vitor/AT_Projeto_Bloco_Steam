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

st.dataframe(df_steam,hide_index=True,height=250)

st.divider()

#nCols = ['total_duration','total_achievements','total_supported_languages','positive_reviews_percent','price', 'self_published_percent','commercialization_days']
df_steam_numerics = df_steam.drop(columns=['name','id','release_date','tags','main_genre','hasSingleplayer','hasMultiplayer','hasCoop','self_published_percent'])


x_plots = 2
y_plots = 3

st.subheader('Boxplot',divider=True)

fig, axs = plt.subplots(x_plots,y_plots,figsize=(15, 15))

i  = 0
for r in range(x_plots):
    for c in range(y_plots):
        colName = df_steam_numerics.columns[i]
        if colName == 'total_reviews':
            i += 1
            colName = df_steam_numerics.columns[i]
        sb.boxplot(data=df_steam_numerics[colName],  ax=axs[r, c], orient='h',color=sb.color_palette()[i % len(sb.color_palette())])
        i += 1
        
plt.subplots_adjust(wspace=0.3, hspace=0.3)
st.pyplot(fig)
st.subheader('Dispersão',divider=True)

fig, axs = plt.subplots(x_plots,y_plots,figsize=(15, 10))

i  = 0
for r in range(x_plots):
    for c in range(y_plots):
        if df_steam_numerics.columns[i] == 'total_reviews':
            i += 1
        sb.regplot(data=df_steam_numerics, x=df_steam_numerics.columns[i], y='total_reviews', ax=axs[r, c], line_kws={'color':'red'})
        i+= 1
        
plt.subplots_adjust(wspace=0.3, hspace=0.3)
st.pyplot(fig)
st.subheader('Mapa de calor',divider=True)
fig, ax = plt.subplots(figsize=(15, 5))

nOrder = list(df_steam_numerics.columns)
nOrder.remove('total_reviews')
nOrder.append('total_reviews')

df_steam_numerics = df_steam_numerics[nOrder]

df_steam_corr = df_steam_numerics.corr()
sb.heatmap(df_steam_corr, annot=True, fmt='.2f',cmap=sb.color_palette("coolwarm", as_cmap=True), ax=ax, mask=np.triu(df_steam_corr, k=1))
ax.axhline(6, color='white', linewidth=2)
ax.axhline(7, color='white', linewidth=4)

st.pyplot(fig)
