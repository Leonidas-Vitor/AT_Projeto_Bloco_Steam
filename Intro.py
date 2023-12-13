import seaborn as sb
import matplotlib.pyplot as plt
from st_pages import Page, show_pages, add_page_title
import streamlit as st
import StreamlitCustomLibrary as at_lib

at_lib.SetPageConfig()
at_lib.SetTheme()

#st.text(__file__)
    
#add_page_title()
show_pages(
    [
        Page('Intro.py','Introdução',":memo:"),
#        Page('DataAcquisition.py','Aquisição de dados',":building_construction:"),
        Page('DataInspection.py','Conhecendo a base de dados',":mag:"),
        Page('DataPreparation.py','Preparação dos dados',":wrench:"),
        Page('DataCleaning.py','Limpeza dos dados',':broom:'),
        Page('ExploratoryAnalysis.py','Análise exploratória',":bar_chart:"),
        Page('LinearRegression.py','Regressão linear',":bulb:"),
    ]
)

html_p = """<p style='text-align: center; font-size:%spx;'><b>%s</b></p>"""

st.markdown('''<h1 style='text-align: center; '><b>INSTITUTO INFNET</b></h1>''',unsafe_allow_html = True)
st.markdown(html_p % tuple([35,"ESCOLA SUPERIOR DE TECNOLOGIA"]),unsafe_allow_html=True)
st.markdown(html_p % tuple([35,"AT - Projeto de Bloco II"]),unsafe_allow_html=True)
st.divider()

github_link = '''https://github.com/Leonidas-Vitor/Steam_Scrapper.git'''
email = '''leonidas.almeida@al.infnet.edu.br'''

columns = st.columns([0.6,0.4])
with columns[0]:
    st.markdown(html_p % tuple([25,'Aluno: Leônidas Almeida']),unsafe_allow_html = True)
    st.markdown(html_p % tuple([25,f'E-mail: <a href= mailto:{email}>{email}</a>']),unsafe_allow_html = True)
    st.markdown(html_p % tuple([25,f'GitHub: <a href={github_link}>Link para o repositório</a>']),unsafe_allow_html = True)
    st.markdown(html_p % tuple([25,'Introdução:']),unsafe_allow_html = True)
    st.text('''
        Esta aplicação foi criada com o propósito de analisar os jogos da loja Steam e então estimar 
        quantas  vendas um novo jogo hipotético teria, baseado em suas principais características e 
        então avaliar se vale o investimento nele ou não.
        ''')
    st.text('''
    O modelo de regressão linear foi escolhido por ser um modelo simples e de fácil interpretação, 
    a avaliação do modelo será feita através das métricas de MSE, RMSE e MAE.
    ''')
with columns[1]:
    st.image('Infnet_logo.png',width=400)

#at_lib.ReadCSV('df_redux','SteamDatasetForStreamlit.csv')

tabs = st.tabs(['Informes','Navegação','Observações'])
with tabs[0]:
    st.write('''Para tornar a aplicação mais rápida os dados são carregados apenas uma vez e então manipulados\
        e armazenados na memória, por isso aplicar um rerun irá modificar gráficos, tabelas e valores, pois os\
        dados já foram modificados anteriormente e o rerun não os carrega novamente. Recomenda-se atualizar a página\
        (F5) ao invés de aplicar um rerun.''')
with tabs[1]:
    st.write('''A aplicação foi organizada em páginas, que podem ser acessadas pela barra lateral à esquerda.''')
with tabs[2]:
    st.markdown('''<p>
    Infelizmente não foi possível terminar totalmente esse trabalho/estudo a tempo, por isso algumas funcionalidades\
    não estão disponíveis, como a página sobre a aquisição dos dados e algumas funcionalidades da página de regressão linear.
    O trabalho será aprimorado nos próximos dias/semanas para que atinja o nível esperado.
    </P>
    ''',unsafe_allow_html=True)
#st.divider()
