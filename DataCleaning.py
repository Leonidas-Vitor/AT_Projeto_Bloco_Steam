import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import streamlit as st
import ast
import StreamlitCustomLibrary as at_lib

at_lib.SetPageConfig()
at_lib.SetTheme()

st.header('Preparação dos dados',divider=True)

st.text(
    '''
    Agora que os dados foram estruturados e pré-preparados iremos fazer algumas investigações e limpezas, pois ainda temos apps\
    inadequados para gerar um modelo de regressão linear adequado. 
    ''')

df_steam = pd.read_csv('SteamDatasetForStreamlitClean.csv',engine='pyarrow')

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam,hide_index=True,height=250)

st.divider()
st.subheader('Remoção de não jogos',divider=True)
