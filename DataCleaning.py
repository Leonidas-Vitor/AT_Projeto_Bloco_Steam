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

st.markdown(at_lib.GetBasicTextMarkdown(25,
    '''
    Agora que os dados foram estruturados e pré-preparados iremos fazer algumas investigações e limpezas, pois ainda temos apps\
    inadequados para gerar um modelo de regressão linear adequado.
    '''),unsafe_allow_html=True)

df_steam = pd.read_csv('SteamDatasetForStreamlitPrepared.csv',engine='pyarrow')
st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam,hide_index=True,height=250)

st.divider()
st.subheader('Remoção de jogos em acesso antecipado',divider=True)

cols = st.columns([0.9,0.1])
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
        '''
        Jogos em acesso antecipado possuem um comportamento próprio, pois ainda estão em desenvolvimento e atraem um tipo de público\
        diferente dos jogos já lançados. Por isso, iremos remover esses jogos do dataset, pois não queremos que eles influenciem\
        o modelo de regressão linear será focado para jogos totalmente lançados.
        '''),unsafe_allow_html=True)
with cols[1]:
    earlyAcessCount = df_steam[df_steam['isEarlyAcess']==True]['id'].count()
    earlyAcessPercent = (earlyAcessCount/df_steam['id'].count())*100
    st.metric(label="Jogos removidos", value=f'{earlyAcessCount}', delta=f'-{earlyAcessPercent:.2f}%')

with st.expander('Jogos em acesso antecipado'):
    st.dataframe(df_steam[df_steam['isEarlyAcess']==True][['name','id','isEarlyAcess']],hide_index=True,height=250,use_container_width=True)

df_steam = df_steam[df_steam['isEarlyAcess']==False]
st.subheader('Remoção de apps VR',divider=True)

forbiddenTag = ['VR']
df_steam['ContainForbiddenTag'] = df_steam['tags'].apply(lambda x: any(tag in x for tag in forbiddenTag))
cols = st.columns([0.9,0.1])
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
        '''
        Esse modelo de regressão não irá contemplar jogos/apps de realidade virtual portanto iremos remove-los do dataset.
        '''),unsafe_allow_html=True)

with cols[1]:
    forbiddenTagCount = df_steam[df_steam['ContainForbiddenTag']==True]['id'].count()
    forbiddenTagPercent = (forbiddenTagCount/df_steam['id'].count())*100
    st.metric(label="Jogos removidos", value=f'{forbiddenTagCount}', delta=f'-{forbiddenTagPercent:.2f}%')

with st.expander('Apps vr removidos'):
    st.dataframe(df_steam[df_steam['ContainForbiddenTag']==True][['name','id','tags']],hide_index=True,height=250,use_container_width=True)

df_steam = df_steam[df_steam['ContainForbiddenTag']==False]
st.subheader('Remoção de não jogos',divider=True)

forbiddenTags = ['Game Development', 'Utilities','Software'] #'Animation & Modeling','Photo Editing','Video Production'
df_steam['ContainForbiddenTag'] = df_steam['tags'].apply(lambda x: any(tag in x for tag in forbiddenTags))

cols = st.columns([0.9,0.1])
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
        f'''
        O dataset ainda possui apps que não são jogos, como softwares de modelagem 3D e utilitários, e por serem classificados\
        pela loja como \"game\" na antiga coluna \"type\" eles ainda estão presentes no dataset. Iremos remove-los utilizando uma\
        lista de tags normalmente associdas a esses tipos de apps.
        '''),unsafe_allow_html=True)
    st.markdown(at_lib.GetBasicTextMarkdown(15,
        f'''
        {forbiddenTags}
        '''),unsafe_allow_html=True)

with cols[1]:
    forbiddenTagCount = df_steam[df_steam['ContainForbiddenTag']==True]['id'].count()
    forbiddenTagPercent = (forbiddenTagCount/df_steam['id'].count())*100
    st.metric(label="Jogos removidos", value=f'{forbiddenTagCount}', delta=f'-{forbiddenTagPercent:.2f}%')

with st.expander('Apps com tags indevidas'):
    st.dataframe(df_steam[df_steam['ContainForbiddenTag']==True][['name','id','tags']],hide_index=True,height=250,use_container_width=True)

df_steam = df_steam[df_steam['ContainForbiddenTag']==False]
st.subheader('Preenchendo as durações ausentes',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Existe uma grande ausência de dados de duração, para resolver esse problema iremos inferir os dados faltantes\
    através da mediana da duração dos jogos do mesmo gênero. Jogos que tiverem uma similaridade de nome menor que\
    0.9 também serão substituídos pela mediana do gênero, já que seus dados não são confiáveis. A inputação desses dados\
    faltantes está sendo feita nesse momento pois já removemos a maioria dos apps que poderiam influênciar na mediana\
    dos gêneros (ex.: VR).
    '''),unsafe_allow_html=True)

df_duration_median = df_steam[(df_steam['total_duration'] > 0) & (~np.isnan(df_steam['total_duration'])) &
    (df_steam['hltb_similarity'] > 0.9)].copy()

df_duration_median = df_duration_median[['main_genre','total_duration']]
df_duration_median = df_duration_median.groupby('main_genre').median().reset_index()

st.dataframe(df_duration_median,use_container_width=True)


#def FillDuration(df):
#    mask = (df['total_duration'] == 0) | df['total_duration'].isna() | df['total_duration'].apply(type) == str
#    genres = df.loc[mask, 'main_genre']
#    df.loc[mask, 'total_duration'] = df_duration_median.set_index('main_genre').loc[genres, 'total_duration'].values
#    return df

#df_steam = FillDuration(df_steam)

def FillDuration(row):
   if (row['total_duration'] == 0 or np.isnan(row['total_duration']) or type(row['total_duration']) == str):
        row['total_duration'] = df_duration_median[df_duration_median['main_genre'] == row['main_genre']].copy()['total_duration'].values[0]
    return row

df_steam = df_steam.apply(FillDuration,axis=1)

df_steam.drop(columns=['ContainForbiddenTag','isEarlyAcess','hltb_similarity'],inplace=True)

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam,hide_index=True,height=250)

st.table(df_steam.set_index('id').describe())

st.download_button(
    label="Baixar o dataset preparado",
    data=df_steam.to_csv(index=False),
    file_name='SteamDatasetForStreamlitCleaned.csv',
    mime='text/csv',
)
st.subheader('Preenchendo as durações ausentes',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Existe uma grande ausência de dados de duração, para resolver esse problema iremos inferir os dados faltantes\
    através da mediana da duração dos jogos do mesmo gênero. Jogos que tiverem uma similaridade de nome menor que\
    0.9 também serão substituídos pela mediana do gênero, já que seus dados não são confiáveis. A inputação desses dados\
    faltantes está sendo feita nesse momento pois já removemos a maioria dos apps que poderiam influênciar na mediana\
    dos gêneros (ex.: VR).
    '''),unsafe_allow_html=True)

df_duration_median = df_steam[(df_steam['total_duration'] > 0) & (~np.isnan(df_steam['total_duration'])) &
    (df_steam['hltb_similarity'] > 0.9)].copy()

df_duration_median = df_duration_median[['main_genre','total_duration']]
df_duration_median = df_duration_median.groupby('main_genre').median().reset_index()

st.dataframe(df_duration_median,use_container_width=True)


#def FillDuration(df):
#    mask = (df['total_duration'] == 0) | df['total_duration'].isna() | df['total_duration'].apply(type) == str
#    genres = df.loc[mask, 'main_genre']
#    df.loc[mask, 'total_duration'] = df_duration_median.set_index('main_genre').loc[genres, 'total_duration'].values
#    return df

#df_steam = FillDuration(df_steam)

def FillDuration(row):
   if (row['total_duration'] == 0 or np.isnan(row['total_duration']) or type(row['total_duration']) == str):
        row['total_duration'] = df_duration_median[df_duration_median['main_genre'] == row['main_genre']]['total_duration'].values[0]
    return row.copy()

df_steam = df_steam.apply(FillDuration,axis=1)
