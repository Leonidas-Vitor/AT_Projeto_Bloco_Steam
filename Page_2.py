import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import streamlit as st
import json
import os

def SetPageConfig(title='AT'):
    st.set_page_config(
        #page_title=title,
        layout="wide")

SetPageConfig()

def SetTheme():
    if 'sb_theme' not in st.session_state:
        with open('seabornTheme.json', 'r') as j:
            st.session_state['sb_theme'] = json.load(j)
    sb.set_theme(palette= st.session_state['sb_theme']['palette'],style= st.session_state['sb_theme']['style'])
    plt.rcParams.update(st.session_state['sb_theme']['plt_rcParams'])

SetTheme()

def GetBasicTextMarkdown(font_size: float, text: str, align = 'center'):
    return f"""<p style='text-align: {align}; font-size:{font_size}px;'><b>{text}</b></p>"""

st.header('Conhecendo a base de dados',divider=True)

st.warning('''
    Devido ao tamanho original do dataset diversas colunas não relevantes para esse estudo foram 
    removidas e o dataset foi salvo em um novo arquivo que o streamlit permite carregar.
    As colunas removidas foram: short_description, appid, fullgame, hltb_main_extra,
    hltb_completionist, hltb_all_styles, ext_user_account_notice, 
    metacritic, drm_notice, alternate_appid, pc_requirements, 
    platforms, controller_support, demos, hltb_id, hltb_alias
    ''', icon="⚠️")

with st.expander("Colunas do dataset original"):
    markdown = '''
    |Coluna|Descrição|Tipo|
    |------|---------|----|
    |appid|Id de identificação na loja steam|Numérico discreto
    |name|Nome do jogo|Textual
    |scrap_status|Estado do processo de scrap|Textual categórica
    |type|Se é um jogo, demo ou dlc|Categorico
    |steam_appid|Id de identificação na loja steam, o nome da coluna é diferente quando o dado é extraído via API da steam|Numérico discreto
    |required_age|Idade mínima recomendada para o jogo|Numérico discreto
    |is_free|Se é um jogo gratuito|Booleano
    |short_description|Descrição breve do jogo|Textual
    |fullgame|Endereçamento para o jogo completo caso seja uma demo| Dicionário com id e nome do jogo completo
    |supported_languages|Lista de linguas suportadas pelo jogo|Textual
    |pc_requirements|Dicionário dos requisitos para "rodar" o jogo|Textual
    |developers|Nome da desenvolvedora|Textual
    |publishers|Nome da publicadora|Textual
    |platforms|Dicionário relacionando a plataforma e se o jogo está disponível nela|Booleano
    |categories|Dicionário de macro características do jogo|Textual categórica
    |release_date|Dicionário relacionando se o jogo já foi lançada e qual a data de lançamento|Temporal
    |controller_support|Tipo de suporte a controles|Textual categórica
    |positive|Quantidade de avaliações positivas|Numérico discreto
    |negative|Quantidade de avaliações negativas|Numérico discreto
    |tags|Tags do jogo|Textual categórica
    |steamspy_owners|Faixa estimada de proprietários de um jogo|Textual categórica
    |spy_status|Estado do processo de scrap dos dados do SteamSpy|Textual categórica
    |hltb_status|Estado do processo de scrap dos dados do HowLongToBeat|Textual categórica
    |genres|Lista de gêneros do jogo|Textual categórica
    |achievements|Quantidade de conquistas e o nome de algumas delas|Numérico discreta e Textual
    |price_overview|Dicionário contendo os dados de preço e promoções em dólar|Numérico contínuo
    |demos|Endereçamento para a demo caso possua| Dicionário com id e nome da demo
    |hltb_id|Id de identificação no HowLongToBeat|Numérico discreto
    |hltb_name|Nome do jogo no HowLongToBeat|Textual
    |hltb_alias|Apelido do jogo no HowLongToBeat|Textual
    |hltb_similarity|Grau de similaridade entre o nome do jogo buscado e o nome do jogo encontrado no HLTB|Numérico contínuo
    |hltb_main_story|Duração dos objetivos principais do jogo em hrs|Numérico contínuo
    |hltb_main_extra|Duração dos extras do jogo em hrs|Numérico contínuo
    |hltb_completionist|Duração dos objetivos principais, extras e outros em hrs|Numérico contínuo
    |hltb_all_styles|Duração em hrs levando em consideração todos os tipos de jogadores|Numérico contínuo
    |ext_user_account_notice|Desconhecido|Textual
    |recommendations|Quantidade de avaliações do jogo na loja steam|Numérico discreto
    |metacritic|Nota do jogo no site metacritic|Numérico discreto
    |drm_notice|Tipo de DRM do jogo|Textual
    |alternate_appid|Desconhecido|Numérico discreto
    '''

    st.markdown(markdown)


#path_json = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Datasets", "SteamDataset_w_HLTB.json")
#st.text(path_json)

with st.expander("Amostra do dataset original"):
    df_sample = pd.read_csv('SteamDatasetRawSample.csv',engine='pyarrow')
    st.dataframe(df_sample,hide_index=True)

st.subheader('Dataset reduzido')

#try:
#    df_redux = st.session_state['df_redux'].copy()
#except Exception as e:
#    df_redux = at_lib.ReadCSV('df_redux','SteamDatasetForStreamlit.csv').copy()

df_redux = pd.read_csv('SteamDatasetForStreamlit.csv',engine='pyarrow')
    
#= at_lib.ReadCSV('df_redux','SteamDatasetForStreamlit.csv')
st.dataframe(df_redux,hide_index=True,height=250)

#buffer = io.StringIO()
#df_redux.info(buf=buffer)
#s = buffer.getvalue()

st.markdown(GetBasicTextMarkdown(20,
    f'''
    O dataset reduzido possui {df_redux.shape[0]} linhas e {df_redux.shape[1]} colunas, sendo que\
    {(df_redux['scrap_status'] != 'Scrap_Sucess').sum()} linhas não possuem dados, indicando um\
    problema de integridade na qualidade de dados. Como não há como recuperar esses dados, eles serão removidos.
    '''),unsafe_allow_html=True)

df_redux.drop(df_redux[df_redux['scrap_status'] != 'Scrap_Sucess'].index,inplace=True)

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Esses são os tipos de cada coluna do dataset nesse momento:
    '''),unsafe_allow_html=True)
    
st.table(df_redux.dtypes)

st.markdown(GetBasicTextMarkdown(20,
    '''
    É possível observar que muitas colunas são do tipo object e além disso algumas delas são do tipo dicionário, o que\
    dificulta a manipulação dos dados. Na próxima página iremos gerar novas colunas para facilitar a manipulação\
    dos dados além de remover colunas que não serão mais utilizadas.
    '''),unsafe_allow_html=True)

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Vamos observar como está a distribuição dos dados de acordo com o tipo de app.
    '''),unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,5))
sb.histplot(df_redux,x=df_redux['type'], hue=df_redux['type'],ax=ax, alpha=1.0,shrink=0.85)

st.pyplot(fig)

st.markdown(GetBasicTextMarkdown(20,
    '''
    Podemos observar que temos muitas DLCs e demos, além de outros tipos de apps que não são jogos e portanto\
    iremos remove-los também pois não são relevantes para o estudo.
    '''),unsafe_allow_html=True)

df_redux.drop(df_redux[df_redux['type'] != 'game'].index,inplace=True)

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Agora a distribuição das idades recomendadas para os jogos.
    '''),unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,5))
sb.histplot(df_redux,x=df_redux['required_age'], hue=df_redux['required_age'],ax=ax, alpha=1.0,shrink=0.85)

st.pyplot(fig)

st.markdown(GetBasicTextMarkdown(20,
    f'''
    Há uma esmadora predominância de idades recomenda 0 anos, algo que é extremamente improvável. Provavelmente\
    esse dado só é crítico de ser colocado na loja para jogos de conteúdo adulto e/ou violento, portanto é muito\
    negligêncido, sendo então um problema confiabilidade desses dados. Infelizmente devido a natureza de publicação\
    da loja Steam não há como buscar dados em quantidade suficiente de outra fonte, portanto não há como utilizar a\
    classificação indicativa nesses estudo.
    '''),unsafe_allow_html=True)

st.divider()
cols = st.columns([0.2,0.3,0.3])
with cols[1]:
    freePercent = (df_redux['is_free'].sum()/df_redux['is_free'].count())*100
    st.metric(label="Jogos gratuitos", value=f'{freePercent:.2f}%')
with cols[2]:
    freePercent = ((df_redux['is_free'].count()-df_redux['is_free'].sum())/df_redux['is_free'].count())*100
    st.metric(label="Jogos pagos", value=f'{freePercent:.2f}%')

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Vamos ver quais desenvolvedores fizeram mais jogos
    '''),unsafe_allow_html=True)
dev_df = df_redux['developers'].value_counts().nlargest(10).reset_index()
dev_df.columns = ['developers','count']
st.table(dev_df)

dev_df = df_redux['developers'].value_counts()

cols = st.columns([0.1,0.2,0.2,0.2])
with cols[1]:
    st.metric(label="Média", value=f'{dev_df.mean():.2f}')
with cols[2]:
    st.metric(label="Mediana", value=f'{dev_df.median()}')
with cols[3]:
    st.metric(label="Desvio Padrão", value=f'{dev_df.std():.2f}')


st.markdown(GetBasicTextMarkdown(20,
    '''
    Apesar do top 10 de desenvolvedores terem feito mais de 100 jogos, a média de jogos por desenvolvedor é de\
    apenas 1.65 e a mediana ainda mais baixa de 1 jogo por desenvolvedor, o que indica uma grande oscilação nos dados\
    algo confirmado pela elavado desvio padrão de 13.86.
    '''),unsafe_allow_html=True)

st.markdown(GetBasicTextMarkdown(20,
    '''
    Além disso é bem curioso que tenhamos 3309 de jogos \"Sem\" desenvolvedora, vamos ver quais são esses jogos.
    '''),unsafe_allow_html=True)

st.dataframe(df_redux[df_redux['developers'] == ''])

st.markdown(GetBasicTextMarkdown(20,
    '''
    Olhando alguns exemplares diretamente na loja steam só é possível inferir que por algum motivo o desenvoveldor\
    preferiu não ser identificado, e não há como saber o motivo.
    '''),unsafe_allow_html=True)

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Agora vamos dar uma olhada nas publicadoras
    '''),unsafe_allow_html=True)
dev_df = df_redux['publishers'].value_counts().nlargest(10).reset_index()
dev_df.columns = ['publishers','count']
st.table(dev_df)

dev_df = df_redux['publishers'].value_counts()

cols = st.columns([0.1,0.2,0.2,0.2])
with cols[1]:
    st.metric(label="Média", value=f'{dev_df.mean():.2f}')
with cols[2]:
    st.metric(label="Mediana", value=f'{dev_df.median()}')
with cols[3]:
    st.metric(label="Desvio Padrão", value=f'{dev_df.std():.2f}')

st.markdown(GetBasicTextMarkdown(20,
    '''
    Curiosamente tivemos um retrato bem parecido com a dos desenvolvedores, isso deve indicar que há muitas autopublicações\
    na loja Steam. Algo que teremos como confirmar mais a frente quando criamos a coluna self_published.
    '''),unsafe_allow_html=True)

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Agora vamos olhar um pouco para as avaliações dos jogos, afinal uma das premissas para esse estudo é de que\
    há uma boa relação entre quantidade de avaliações e as vendas de um jogo. Para isso foi feito um gráfico de dispersão\
    usando as avaliações positivas e negativas como eixos x e y respectivamente e a quantidade de proprietários como\
    a cor dos pontos.
    '''),unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,5))
sb.scatterplot(df_redux,x='positive', y='negative',hue='steamspy_owners',ax=ax)
#ax.tick_params(axis='x',rotation=45)
ax.ticklabel_format(style='plain', axis='both')
st.pyplot(fig)

st.markdown(GetBasicTextMarkdown(25,
    '''
    É possível observar alguns outliers que estão distorcendo a escala do gráfico, contudo, é possível observar que\
    há uma relação entre a quantidade de avaliações positivas e negativas, o que é esperado, afinal quanto mais\
    avaliações positivas um jogo tem, mais avaliações negativas ele tende a ter. Além disso é possível observar que\
    a maioria dos jogos tem poucas avaliações, o que é esperado, afinal a maioria dos jogos não são muito populares.\
    Também é possível observar uma boa correlação entre a quantidade de avaliações e a quantidade de proprietários,\
    o que fortalece a premissa de que há uma boa relação entre a quantidade de avaliações e as vendas de um jogo.
    '''),unsafe_allow_html=True)

st.divider()

st.markdown(GetBasicTextMarkdown(25,
    '''
    Por fim vamos olhar os dados a respeito de duração dos jogos.
    '''),unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,5))
sb.kdeplot(df_redux[df_redux['hltb_status'] == 'Found'],x=df_redux['hltb_main_story'],ax=ax,fill=True)
st.pyplot(fig)

st.markdown(GetBasicTextMarkdown(20,
    '''
    É possível observar a presença de algun(s) outliers bem fora da curva, o que está distorcendo muito o gráfico, vamos\
    colocar um limite de 200hrs máxima e refazer o gráfico.
    '''),unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,5))
sb.kdeplot(df_redux[(df_redux['hltb_status'] == 'Found') & (df_redux['hltb_main_story'] < 200) & 
(df_redux['hltb_main_story'] > 0)],
x='hltb_main_story',ax=ax,fill=True)
st.pyplot(fig)

st.markdown(GetBasicTextMarkdown(20,
    '''
    Agora é possível observar que a maioria dos jogos tem uma duração entre 0 e 20 horas.
    '''),unsafe_allow_html=True)

cols = st.columns([0.2,0.3,0.3])
with cols[1]:
    foundPercent = (df_redux[df_redux['hltb_status'] == 'Found']['hltb_status'].count()/df_redux['hltb_status'].count())*100
    st.metric(label="Jogos com dados no HTLB", value=f'{foundPercent:.2f}%')
with cols[2]:
    notFoundPercent = 100-foundPercent
    st.metric(label="Jogos sem dados no HTLB", value=f'{notFoundPercent:.2f}%')

st.markdown(GetBasicTextMarkdown(20,
    '''
    Infelizmente a amostra de jogos com dados no HTLB é bem pequena, apenas 37.21% dos jogos possuem dados no HTLB,\
    o que irá nos exigir decidir entre inferir os dados faltantes ou remover os jogos sem dados no HTLB. Parte dessa\
    ausência de dados pode ser explicada por alterações de nome do jogo entre a loja Steam e o HTLB, como por exemplo\
    Divinity Original Sin 2, que na Steam está como Divinity: Original Sin 2 - Definitive Edition e no HTLB está\
    apenas Divinity Original Sin 2, o que inviabilizou a busca automática dos dados. Outra parte dessa ausência de\
    dados pode ser explicada pela baixa popularidade do jogo. Também suspeita-se de que haja uma correlação entre\
    preço e a probabilidade de ter dados no HLTB.
    '''),unsafe_allow_html=True)

st.divider()

st.markdown(GetBasicTextMarkdown(20,
    '''
    Além de termos poucos dados a respeito de duração, será que podemos confiar neles?
    '''),unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,5))
sb.histplot(df_redux,x='hltb_similarity', ax=ax, alpha=1.0,shrink=0.85,bins=10)

st.pyplot(fig)

cols = st.columns([0.4,0.6])
with cols[0]:
    perfectSimilarity = (df_redux[df_redux['hltb_similarity'] == 1]['hltb_status'].count()/df_redux['hltb_similarity'].count())*100
    st.metric(label="Jogos com nome \"perfeitamente\" similar", value=f'{perfectSimilarity:.2f}%')
    st.text('''
        No geral quando a similaridade do HLTB é igual a 1 temos uma 
        correlação entre os nomes dos jogos. Contudo, é possível observar 
        algumas inconsistências, como por exemplo, que apesar de serem 
        identificados como iguais, mas não são, como é o caso com
        Master of the Monster Lair e Dungeon Maker. O nos leva a ter 
        menos confiança nesses dados, porém por serem casos bem isolados 
        iremos tolerá-los, já que é difícil identificar esses casos de 
        forma automática. Ao lado temos um recorte onde esses casos são 
        mais prováveis ocorrerem, pois o nome da coluna \'name\' é 
        diferente do nome na coluna \'hltb_name\'.
        ''')
with cols[1]:
    st.dataframe(df_redux[
        (df_redux['hltb_similarity'] == 1) & (df_redux['name'].str.lower() != df_redux['hltb_name'].str.lower())
        ][['hltb_similarity','hltb_name','name']],use_container_width=True,hide_index=True)

st.divider()


### Incluir a comparação entre scrap sucess e steamspy scrap sucess, para provar que quando acha em um acha no outro

st.markdown(GetBasicTextMarkdown(25,
    '''
    Na próxima página iremos preparar os dados para a modelagem.
    '''),unsafe_allow_html=True)
    
st.dataframe(df_redux,hide_index=True,height=250)

st.markdown(GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_redux.shape[0]} linhas e {df_redux.shape[1]} colunas.
    '''),unsafe_allow_html=True)
