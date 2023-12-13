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

st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Jogos em acesso antecipado possuem um comportamento próprio, pois ainda estão em desenvolvimento e atraem um tipo de público\
    diferente dos jogos já lançados. Por isso, iremos remover esses jogos do dataset, pois não queremos que eles influenciem\
    o modelo de regressão linear será focado para jogos totalmente lançados.
    '''),unsafe_allow_html=True)

with st.expander('Jogos em acesso antecipado'):
    st.dataframe(df_steam[df_steam['isEarlyAcess']==True][['name','id','isEarlyAcess']],hide_index=True,height=250,use_container_width=True)

earlyAcessCount = df_steam[df_steam['isEarlyAcess']==True]['id'].count()
earlyAcessPercent = (earlyAcessCount/df_steam['id'].count())*100
st.metric(label="Jogos removidos", value=f'{earlyAcessCount}', delta=f'-{earlyAcessPercent:.2f}%')
st.subheader('Remoção de não jogos',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset ainda possui apps que não são jogos, como softwares de modelagem 3D e utilitários, e por serem classificados\
    pela loja como \"game\" na antiga coluna \"type\" eles ainda estão presentes no dataset. Iremos remove-los utilizando uma\
    lista de tags normalmente associdas a esses tipos de apps.
    '''),unsafe_allow_html=True)

forbiddenTags = ['Animation & Modeling','Game Development','Video Production', 'Utilities','Photo Editing','Software','VR']
df_steam['ContainForbiddenTag'] = df_steam['tags'].apply(lambda x: any(tag in x for tag in forbiddenTags))

cols = st.columns([0.7,0.3])
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(15,
        f'''
        Lista de tags indevidas:
        {forbiddenTags}
        A tag VR foi incluída pois não estamos interessados em jogos de realidade virtual para esse projeto, então aproveitamos\
        a operação para já retirar esse tipo de app do dataset.
        '''),unsafe_allow_html=True)

forbiddenTagCount = df_steam[df_steam['ContainForbiddenTag']==True]['id'].count()
forbiddenTagPercent = (forbiddenTagCount/df_steam['id'].count())*100
with cols[1]:
    st.metric(label="Jogos removidos", value=f'{forbiddenTagCount}', delta=f'-{forbiddenTagPercent:.2f}%')

with st.expander('Apps com tags indevidas'):
    st.dataframe(df_steam[df_steam['ContainForbiddenTag']==True][['name','id','tags']],hide_index=True,height=250,use_container_width=True)


st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam,hide_index=True,height=250)

st.table(df_steam.set_index('id').describe())

st.download_button(
    label="Baixar o dataset preparado",
    data=df_steam.to_csv(index=False),
    file_name='SteamDatasetForStreamlitClean.csv',
    mime='text/csv',
)
