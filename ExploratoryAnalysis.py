import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import streamlit as st
import StreamlitCustomLibrary as at_lib

at_lib.SetPageConfig()
at_lib.SetTheme()

st.header('Análise exploratória',divider=True)

df_steam = pd.read_csv('SteamDatasetForStreamlitClean.csv',engine='pyarrow')

st.dataframe(df_steam.describe())

st.divider()

fig, ax = plt.subplots(figsize=(15, 5))

df_steam_corr = df_steam.corr()
sb.heatmap(df_steam_corr, annot=True, fmt='.2f', ax=ax, mask=np.triu(df_steam_corr, k=1))

st.divider()

fig, axs = plt.subplots(3,3,figsize=(15, 10))

nCols = ['total_duration','total_achievements','total_supported_languages','positive_reviews_percent','price',
'self_published_percent','commercialization_days']

for index, col in enumerate(nCols):
    sb.regplot(data=df_steam, x=col, y='total_reviews', ax=axs[index//3, index%3], line_kws={'color':'red'})
plt.subplots_adjust(wspace=0.3, hspace=0.3)

st.pyplot(fig)

st.divider()

fig, ax = plt.subplots(figsize=(15, 5))
sb.boxplot(data=df_steam[nCols], ax=ax)

st.pyplot(fig)

