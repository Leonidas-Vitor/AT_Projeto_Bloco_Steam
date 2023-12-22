import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
import streamlit as st
import ast
import StreamlitCustomLibrary as at_lib
import json

at_lib.SetPageConfig()
at_lib.SetTheme()

st.header('Preparação dos dados',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(25,
    '''
    Agora iremos estruturar os dados de forma que fique mais fácil de utilizá-los com eles.\
    \nPara isso iremos criar novas colunas, remover colunas que não serão mais utilizadas e tratar\
    os problemas de qualidade mais evidente, na próxima página continuaremos a tratar de\
    problemas de qualidade.
    '''),unsafe_allow_html=True)


df_steam = pd.read_csv('SteamDatasetForStreamlitInspected.csv',engine='pyarrow')

#df_steam.drop(df_steam[df_steam['scrap_status'] != 'Scrap_Sucess'].index,inplace=True)
#df_steam.drop(df_steam[df_steam['type'] != 'game'].index,inplace=True)

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam,hide_index=True,height=250)

st.divider()

cols = st.columns([0.45,0.55])
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    1º Serão removidas as colunas que não nos servem para mais nada.
    ''',align = 'left'),unsafe_allow_html=True)

    st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    2º Removeremos linhas que não atendem as premissas do estudo.
    ''',align = 'left'),unsafe_allow_html=True)
    
    st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    3º Criaremos novas colunas para facilitar a manipulação dos dados.
    ''',align = 'left'),unsafe_allow_html=True)

    st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    4º Uma última limpeza nos dados, baseado nas colunas novas.
    ''',align = 'left'),unsafe_allow_html=True)

    st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    5º Por fim, algumas visualizações e análises após a preparação dos dados.
    ''',align = 'left'),unsafe_allow_html=True)

with cols[1]:
    st.markdown('''
| Coluna         | Justificativa                                                                       |
|----------------|-------------------------------------------------------------------------------------|
| scrap_status   | Já utilizamos essa coluna para remover linhas sem dados                             |
| type           | Já utilizamos essa coluna para remover as linhas que não eram de jogos              |
| required_age   | Pela imensa quantidade de dados faltantes nessa coluna ela será desconsiderada      |
| spy_status     | Tem o mesmo valor que o scrap_status                                                |
| hltb_status    | Se a duração for nan ou 0 já significa que não há dados de duração para aquele jogo |
| hltb_name      | Não iremos trabalhar essa coluna                                                    |
| recommendations| Iremos utilizar as colunas positive e negativa ao invés dessa                       |
    ''')

df_steam.drop(columns=['scrap_status','type','required_age','spy_status','hltb_status','hltb_name',
    'recommendations'],inplace=True)

st.divider()

#st.markdown(at_lib.GetBasicTextMarkdown(25,
#    '''
#    Agora removeremos diversas linhas que não atendem as premissas do estudo.
#    '''),unsafe_allow_html=True)

#%%writefile -a 'C:\Users\leoni\OneDrive\Documentos\AT_Projeto_Bloco_Streamlit\DataPreparation.py'
st.subheader('Remoção de alguns apps indesejados',divider=True)

cols = st.columns([0.5,0.2,0.3])
#É Gratuito?
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
        '''
        O jogo não deve ser gratuito, pois estamos analisando jogos que serão comercializados no modelo premium,\
        ou seja, os jogos tem um preço para serem adquiridos/jogados.
        '''),unsafe_allow_html=True)
with cols[2]:
    freeGames = df_steam[(df_steam['is_free'] == True)]['steam_appid'].count()
    freeGamesPercent = (freeGames/df_steam['steam_appid'].count())*100
    st.metric(label="Jogos removidos", value=f'{freeGames}', delta=f'-{freeGamesPercent:.2f}%')

with st.expander('Amostra dos apps removidos'):
    st.dataframe(df_steam[(df_steam['is_free'] == True)].sample(5),use_container_width=True)
df_steam = df_steam[(df_steam['is_free'] == False)]

st.divider()
cols = st.columns([0.5,0.2,0.3])
#Já lançado?
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Jogos não lançados não podem ser analisados, pois ainda não foram comercializados tendo como data referência 2023/11/08
    '''),unsafe_allow_html=True)
with cols[2]:
    df_steam['release_date'] = df_steam['release_date'].apply(ast.literal_eval)
    notLaunched = df_steam[(df_steam['release_date'].str['coming_soon'] == True) | (df_steam['release_date'].str['date'] == '')]['steam_appid'].count()
    notLaunchedPercent = (notLaunched/df_steam['steam_appid'].count())*100
    st.metric(label="Jogos removidos", value=f'{notLaunched}', delta=f'-{notLaunchedPercent:.2f}%')

with st.expander('Amostra dos apps removidos'):
    st.dataframe(df_steam[(df_steam['release_date'].str['coming_soon'] == True) | (df_steam['release_date'].str['date'] == '')].sample(5),use_container_width=True)

df_steam = df_steam[(df_steam['release_date'].str['coming_soon'] == False) & (df_steam['release_date'].str['date'] != '')]

st.divider()
cols = st.columns([0.5,0.2,0.3])
#Possui dados de tag?
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Jogos sem tags não podem ser comparados e/ou categorizados, portanto terão de ser removidos, contudo,\
    em outro momento se for necessário é possível obter as tags diretamente na página do jogos na loja Steam.
    '''),unsafe_allow_html=True)
with cols[2]:
    noTag = df_steam[df_steam['tags'].apply(lambda x: len(ast.literal_eval(x)) == 0)]['steam_appid'].count()
    notTagPercent = (noTag/df_steam['steam_appid'].count())*100
    st.metric(label="Jogos removidos", value=f'{noTag}', delta=f'-{notTagPercent:.2f}%')

with st.expander('Amostra dos apps removidos'):
    st.dataframe(df_steam[df_steam['tags'].apply(lambda x: len(ast.literal_eval(x)) == 0)].sample(5),use_container_width=True)

df_steam = df_steam[df_steam['tags'].apply(lambda x: len(ast.literal_eval(x)) > 0)]


st.divider()
cols = st.columns([0.5,0.2,0.3])
#Possui dados de preço?
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    O preço é um dado bem importante para o estudo e por serem poucos jogos sem essa informação, eles serão\
    removidos.
    '''),unsafe_allow_html=True)
with cols[2]:
    noPrice = df_steam[df_steam['price_overview'] == '']['steam_appid'].count()
    notPricePercent = (noPrice/df_steam['steam_appid'].count())*100
    st.metric(label="Jogos removidos", value=f'{noPrice}', delta=f'-{notPricePercent:.2f}%')

with st.expander('Amostra dos apps removidos'):
    st.dataframe(df_steam[df_steam['price_overview'] == ''].sample(5),use_container_width=True)

df_steam = df_steam[df_steam['price_overview'] != '']

st.divider()
cols = st.columns([0.5,0.2,0.3])
#Possui dados de categoria?
with cols[0]:
    st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Algumas linhas não tinham dados na coluna categories e após uma breve investigação foi constatado que são ferramentas\
    para desenvolvedores, apps temporários (Playtest) e jogos sem uma data de lançamento definida, portanto serão removidos.
    '''),unsafe_allow_html=True)
with cols[2]:
    noCat = df_steam[df_steam['categories'] == '']['steam_appid'].count()
    notCatPercent = (noCat/df_steam['steam_appid'].count())*100
    st.metric(label="Jogos removidos", value=f'{noCat}', delta=f'-{notCatPercent:.2f}%')

with st.expander('Amostra dos apps removidos'):
    st.dataframe(df_steam[df_steam['categories'] == ''].sample(5),use_container_width=True)

df_steam = df_steam[df_steam['categories'] != '']

#st.divider()

st.subheader('Criação de novas colunas',divider=True)

st.markdown(at_lib.GetBasicTextMarkdown(25,
    '''
    Agora serão criadas as novas colunas que tornarão mais fácil a manipulação dos dados, além de remover colunas\
    que não serão mais utilizadas. O dataset resultante terá as seguintes colunas:
    '''),unsafe_allow_html=True)

cols = st.columns([0.2,0.8])
with cols[1]:
    st.markdown('''
    | Coluna                    | Descrição                                                              | Tipo              |
    |---------------------------|------------------------------------------------------------------------|-------------------|
    | id                        | ID do jogo na loja steam                                               | Numérico discreto |
    | name                      | Nome do jogo                                                           | Textual           |
    | main_genre                | Principal gênero do jogo                                               | Textural          |
    | tags                      | Lista de tags do jogo                                                  | Lista textual     |
    | isEarlyAcess              | Se um jogo está ou não em acesso antecipado                            | Booleana          |
    | release_date              | Data de lançamento do jogo                                             | Datetime          |
    | commercialization_days    | Total de dias em comercialização até o dia em que o dataset foi criado | Numérico discreto |
    | price                     | Preço em dólares do jogo                                               | Numérico contínuo |
    | hasSingle-player          | Se um jogo tem ou não modo single-player                               | Booleana          |
    | hasMulti-player           | Se um jogo tem ou não modo Multi-player                                | Booleana          |
    | hasCo-op                  | Se um jogo tem ou não modo co-op                                       | Booleana          |
    | total_reviews             | Quantidade total de avaliações do jogo                                 | Numérico discreto |
    | positive_reviews_percent  | Porcentagem das avaliações que foram positivas                         | Numérico contínuo |
    | total_supported_languages | Total de línguas suportadas                                            | Numérico discreto |
    | self_published_percent    | Estimativa do grau de auto-publicação do jogo                          | Numérico contínuo |
    | total_duration            | Duração média da campanha do jogo                                      | Numérico contínuo |
    | total_achievements        | Quantidade de conquistas                                               | Numérico discreto |
    ''')

st.divider()
#st.warning(''' Para evitar um consumo excessivo de memória RAM, os dados serão manipulados diretamente no dataset.
#''', icon="⚠️")

#cols = st.columns([0.5,0.5])
#------------ Coluna main_genre
#Online Party Game não foi identificado
#VR será tratado como uma característica do jogo e não como um gênero
generosValidos = [
    'Roguelike Deckbuilder','4X',
    'Simulation','Management', #=> Esses dois são juntos
    'Open World Survival Craft','City Builder','RPG','Rogue-like','Metroidvania','Dungeon Crawler','Souls-like',
    'Visual Novel','Twin Stick Shooter','Horror','Sexual Content','Card Battler','Beat \'em up','FPS','Shoot \'Em Up'
    'Tower Defense','Match 3','Puzzle-Platformer','Puzzle','2D Platformer','3D Platformer','Battle Royale']

#with cols[0]:
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Criação da coluna main_genre, ela é criada apartir da coluna tags, pegando a tag mais \"votada\" que estiver\
    dentro da nossa lista de gêneros válidos. A lista de gêneros válidos foi baseada em artigos de pesquisas\
    realizadas na loja steam. 
    '''),unsafe_allow_html=True)
    #st.table(generosValidos)

html_p = """<p style='text-align: center; font-size:%spx;'><b>%s</b></p>"""
link = 'https://howtomarketagame.com/2022/04/18/what-genres-are-popular-on-steam-in-2022/'
st.markdown(html_p % tuple([15,f'Referência: <a href={link}>Link para o artigo</a>']),unsafe_allow_html = True)

def GetMainGenre(tags):
    if (type(tags) == str):
        tags = ast.literal_eval(tags)
    if (type(tags) == dict):
        #return max(tags, key=tags.get)
        main_genre = {}
        try:
            for chave,valor in tags.items():
                if (chave in generosValidos):
                    main_genre[chave] = valor
            try:
                return max(main_genre, key=main_genre.get)
            except Exception as e:
                return 'Others'#max(tags, key=tags.get)
        except Exception as e:
            print(tags)
            return 'Erro'
    else:
        return 'NoTags'

df_steam = df_steam.assign(main_genre = df_steam['tags'].apply(lambda tags: GetMainGenre(tags)))

#with cols[1]:
st.dataframe(df_steam[['main_genre']].value_counts().reset_index().rename(columns={0:'count'}),use_container_width=True)

#------------ Organização das tags

def OrganizeTags(tags):
    if (type(tags) == str):
        tags= ast.literal_eval(tags)

    newList = []
    for tag in tags:
        newList.append(tag)
    return newList

df_steam['tags'] = df_steam['tags'].apply(lambda tags: OrganizeTags(tags))

#st.dataframe(df_steam['tags'],use_container_width=True)

#------------ Acesso antecipado
st.markdown(at_lib.GetBasicTextMarkdown(20,
        '''
        Criação da coluna isEarlyAcess, ela foi apartir da busca da palavra \'Early Access\' na coluna genres
        '''),unsafe_allow_html=True)

def IsEarlyAcess(genres):
    if (type(genres) == str and genres != ''):
        try:
            genres = ast.literal_eval(genres)
        except Exception as e:
            st.text(genres)
            pass
    try:
        for g in genres:
            if g['description'] == 'Early Access':
                return True
        return False
    except TypeError as te:
        #jogo não possui tags
        return False
    except Exception as e:
        return False
    
#Criação de uma coluna que identifica se um jogo está ou não em acesso antecipado
df_steam = df_steam.assign(isEarlyAcess = df_steam['genres'].apply(lambda genres: IsEarlyAcess(genres)))

st.table(df_steam[['isEarlyAcess']].value_counts().reset_index().rename(columns={0:'count'}))

#------------ Data de lançamento
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Coluna release_date agora está em formato datetime
    '''),unsafe_allow_html=True)

columns = st.columns([0.5,0.5])
with columns[0]:
    st.dataframe(df_steam['release_date'].head(50),use_container_width=True)

df_steam['release_date'] = pd.to_datetime(df_steam['release_date'].str['date'].apply(lambda d: np.nan if len(d) == 0 else d[:3] + ' 15, ' + d[4:8] if len(d) <= 8  else d))
df_steam.dropna(inplace=True,subset='release_date')
#df_steam['release_date'].dropna(inplace=True)

with columns[1]:
    st.dataframe(df_steam['release_date'].head(50),use_container_width=True)
#------------ Dias em comercialização
df_steam['commercialization_days'] = (pd.Timestamp('2023/11/08') - df_steam['release_date']).dt.days
#----------- Preço
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Coluna price agora está em formato numérico
    '''),unsafe_allow_html=True)

df_steam['price_overview'] = df_steam['price_overview'].apply(ast.literal_eval)
df_steam['price'] = df_steam['price_overview'].str['initial']/100

columns = st.columns([0.5,0.5])
with columns[0]:
    st.dataframe(df_steam['price_overview'].head(50),use_container_width=True)

with columns[1]:
    st.dataframe(df_steam['price'].head(50),use_container_width=True)

df_steam.drop(columns=['price_overview'],inplace=True)

#----------- Modos de jogo
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Colunas hasSingleplayer, hasMultiplayer e hasCoop são criadas apartir da coluna categories que é composta por dicts.
    '''),unsafe_allow_html=True)

def ContainsTargetCategory(categories, target_category):
    try:
        for category in categories:
            for value in category.values():
                if value == target_category:
                    return True
        return False
    except TypeError as te:
        #o jogo não possui categorias
        return False

df_steam['categories'] = df_steam['categories'].apply(ast.literal_eval)

df_steam['hasSingleplayer'] = df_steam['categories'].apply(lambda s : ContainsTargetCategory(s,'Single-player'))
df_steam['hasMultiplayer'] = df_steam['categories'].apply(lambda s : ContainsTargetCategory(s,'Multi-player'))
df_steam['hasCoop'] = df_steam['categories'].apply(lambda s : ContainsTargetCategory(s,'Co-op'))

st.dataframe(df_steam[['name','hasSingleplayer','hasMultiplayer','hasCoop']].sample(5),use_container_width=True)
#----------- Avaliações
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    As total_reviews e positive_revirews_percent são criadas apartir das colunas positive e negative, que são a quantidade\
    de avaliações positivas e negativas respectivamente. A coluna total_reviews é a soma das duas colunas e a coluna\
    positive_reviews_percent é a porcentagem de avaliações positivas.
    '''),unsafe_allow_html=True)

df_steam['total_reviews'] = df_steam['positive'].copy() + df_steam['negative'].copy()
df_steam['positive_reviews_percent'] = df_steam['positive'].copy()/df_steam['total_reviews']
df_steam['positive_reviews_percent'].fillna(0,inplace=True)

st.dataframe(df_steam[['name','total_reviews','positive_reviews_percent']].sample(5),use_container_width=True)
#----------- Línguas suportadas
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    A coluna total_supported_languages é criada apartir da coluna supported_languages, que é uma lista de\
    línguas suportadas pelo jogo.
    '''),unsafe_allow_html=True)

df_steam['total_supported_languages'] = df_steam.supported_languages.str.split(',')
df_steam['total_supported_languages'] = df_steam['total_supported_languages'].fillna('')
df_steam['total_supported_languages'] = df_steam['total_supported_languages'].apply(lambda languages: len(languages))

st.dataframe(df_steam[['name','supported_languages','total_supported_languages']].sample(5),use_container_width=True)
#----------- Auto publicação
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    A coluna de self_published_percent é uma estimativa do grau de auto publicação do jogo, ou seja, quanto maior\
    o valor, maior a probabilidade do jogo ser auto publicado. Essa coluna é criada apartir da comparação entre\
    as colunas developers e publishers, se um desenvolvedor for igual a um publicador, então o jogo é auto publicado.
    '''),unsafe_allow_html=True)

def Is_sef_published(developers,publishers):
    try:
        publisherPercent = 1/len(publishers)
        totalPublisher = 0
        for developer in developers:
            for publisher in publishers:
                if developer.strip() == publisher.strip():
                    totalPublisher += publisherPercent
        return totalPublisher if totalPublisher <= 1 else 1
    except TypeError as te:
        #print(te)
        #Ocorre quando não há dado de publicadora e/ou desenvolvedor (Nan)
        return 0

def ParseData(d):
    try:
        return ast.literal_eval(d)
    except Exception as e:
        return {}

df_steam['developers'] = df_steam['developers'].apply(ParseData)
df_steam['publishers'] = df_steam['publishers'].apply(ParseData)

df_steam['self_published_percent'] = df_steam.apply(lambda x: Is_sef_published(x.developers,x.publishers),axis=1)

df_steam['developers'] = df_steam['developers'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

st.dataframe(df_steam[['name','developers','publishers','self_published_percent']].sample(5),use_container_width=True)

#----------- Conquistas
st.markdown(at_lib.GetBasicTextMarkdown(20,
    '''
    Como não dá para saber se os desenvolvedores implementaram ou não conquista no jogo, iremos completar com 0\
    os dados faltantes. Uma vez que se o desenvolver tivesse implementado conquistas provavelmente os dados estariam\
    disponíveis.
    '''),unsafe_allow_html=True)

df_steam['achievements'] = df_steam['achievements'].apply(ParseData)
#df_steam['achievements'] = df_steam['achievements'].apply(json.loads)
df_steam['total_achievements'] = df_steam['achievements'].str['total']

df_steam['total_achievements'].fillna(0)

df_steam['total_achievements'] = df_steam['total_achievements'].apply(lambda x: 0 if np.isnan(x) else x)

st.dataframe(df_steam[['name','achievements','total_achievements']].sample(5),use_container_width=True)

#----------- Rename das colunas

df_steam.rename(columns={'steam_appid':'id','hltb_main_story':'total_duration'},inplace=True)

st.divider()

df_steam.drop(columns=['is_free','genres','supported_languages','categories','positive','negative',
    'developers','publishers','achievements','steamspy_owners',''],inplace=True)


try:
    df_steam['id'] = df_steam['id'].astype(int)
except Exception as e:
    print(e)
    pass

try:
    df_steam['total_reviews'] = df_steam['total_reviews'].astype(int)
except Exception as e:
    print(e)
    pass

try:
    df_steam['total_supported_languages'] = df_steam['total_supported_languages'].astype(int) 
except Exception as e:
    print(e)
    pass

try:
    df_steam['total_achievements'] = df_steam['total_achievements'].astype(int)
except Exception as e:
    print(e)
    pass

try:
    df_steam['release_date'] = df_steam['release_date'].astype('datetime64[ns]')
except Exception as e:
    print(e)
    pass

st.markdown(at_lib.GetBasicTextMarkdown(20,
    f'''
    O dataset atualmente possui {df_steam.shape[0]} linhas e {df_steam.shape[1]} colunas.
    '''),unsafe_allow_html=True)

st.dataframe(df_steam,hide_index=True,height=250)

st.table(df_steam.dtypes.astype(str))

st.download_button(
    label="Baixar o dataset preparado",
    data=df_steam.to_csv(index=False),
    file_name='SteamDatasetForStreamlitPrepared.csv',
    mime='text/csv',
)
#st.table(df_steam.dtypes)
# Visualizar/Analisar os dados resultantes


# Dados faltantes identificas (copiar tabela do TP7)
with st.expander('Dados faltantes e problemas identificados'):
    st.markdown('''
    | Coluna | Identificação | Motivo | Decisão
    |--------|---------------|--------|---------|
    |genres|Erro ao tentar percorrer os gêneros na tentativa de identificar se o jogo está ou não em acesso antecipado|Não conhecido até o momento|Inicialmente não seriam removidos, mas foram encontrados durante jogos em acesso antecipado sem a coluna genre, portanto, foi decidido remover todos os jogos sem valores em genres|
    |hltb_main_story|No .sample() foi observado algumas durações com valor 0, mas como nenhum jogo pode ter duração 0, é totalmente razoável assumir que isso é um dado faltante|Normalmente são jogos pouco populares e portanto ninguém postou essa informação no site|Pela importância desse dado para a análise em questão, serão removidos jogos com duração zerada|
    |release_date|Ao tentar passar a release_date para formato de data ocorria erros de formato indicando uma entrada sem dia, após uma pequena análise foram identificados outras entradas do mesmo jeito|Alguns jogos por motivos não totalmente compreendidos não possuem dia de lançamento, apenas mês e ano|Será inferido que eles foram lançados no dia 15 do mês e ano que já temos, é esperado que alguns dias de discrepância (+ ou - 15 dias) no tempo de comercialização não acarrete em grandes impactos na análise em andamanto  
    |required_age|No .sample() foi observado muitas idades mínimas com valor 0, suspeitando do grau de incidência foi feita uma contagem mostrando uma predominância imensa de idade mínima 0, o que não parece condizer com a realidade|Provavelmente esse dado só é crítico de ser colocado na loja para jogos de conteúdo adulto e/ou violento, portanto é muito negligêncido|A coluna min_age inicialmente prevista será desconsiderada pois há dados faltantes demais|
    |tags|No .sample() foi observado foi observado algumas entradas de tag com uma lista vazia|Não conhecido até o momento, suspeita-se de que jogos de baixa popularidade sofram dessa falta de dados|Ou serão ignorados para acelerar uma análise preliminar ou o dado será obtido através de um webscrapping da frontpage da loja steam|
    |price|Ao usar um describe na coluna foi observado uma contagem inferior ao esperado|Aparentemente se tratam de jogos por assinatura ou que não estão mais disponíveis para compra na loja|Por serem menos de 200 jogos, serão removidos em um primeiro momento
    |commercialization_days|Ao usar um describe na coluna foi observado uma contagem inferior ao esperado|Não está claro o porque de alguns jogos não terem informação de data de lançamento|Por serem menos de 31 jogos, serão removidos em um primeiro momento
    |supported_languages|Um jogo não possuia nenhuma linguagem suportada|Desconhecido|Substituir por zero|
    ''')

    st.divider()

    # Problemas na base e dimensões de qualidade afetadas (copiar tabela do TP7)
    st.markdown('''
    | Problema                                                                                                                                                                                                                                                                                                                                                                                  | Dimensões de qualidade afetados |
    |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
    | Muitos jogos receberam um dado equivocado de duração vinda do HowLongToBeat (HLTB), para minimizar isso foi estabelecido que a similaridade do nome pesquisado com o resultado deve ser maior que 90%, aplicar um filtro 100% poderia remover vários títulos que estão com os dados corretos mas que por mudanças de nome na loja não tem um nome perfeitamente igual ao presente no HLTB | Confiabilidade                  |
    | Vários jogos até possuem cadastro no HLTB mas ninguém submeteu durações para eles, o que irá inutilizar a análise pois nenhum jogo tem duração zero, portanto foi imposto que a duração deve no mínimo superior a zero para ser um jogo válida para essa análise                                                                                                                          | Completude                      |
    | Foi identificado que alguns jogos não possuem dia de lançamento, foi inferido o dia 15, pois limitaria o erro em + ou - 15 dias                                                                                                                                                                                                                                                           | Integridade                     |
    | Constatado também que jogos que não estão mais disponíveis na loja, não possuem uma data de lançamento, serão excluídos pois não se sabe a data em que foram excluídos                                                                                                                                                                                                                    | Integridade                     |
    | Inconsistência nas reviews de um jogo, os dados do steamSPY apontam um valor e a api da Steam outro, foi escolhido seguir com os dados do SteamSpy pois refletem os dados na front page da loja                                                                                                                                                                                           | Consistência                    |
    | Alguns jogos, cerca de 20 possuem tempo de comercialização negativo pois os dados foram coletados ao longo de 10 dias, usar a data de quando a coleta foi finalizada resolveria o problema                                                                                                                                                                                                | Atualidade                      |
    | O nome da publicadora ter um espaço de diferença em relação ao mesmo nome na coluna desenvolvedor                                                                                                                                                                                                                   | Consistência                    |
    | Vários apps marcados como "game" na coluna type, na versão são softwares diversos, inicialmente a crença de que apps sem valor na coluna "categories" seriam todos softwares se mostrou equivocada. A solução será montar uma lista de tags "proibidas" e remover todos os apps que possuam tais tags| Confiabilidade |
    ''')
