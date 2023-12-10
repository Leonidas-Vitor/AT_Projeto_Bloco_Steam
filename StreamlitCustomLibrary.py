import streamlit as st
import json
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

def SetPageConfig(title='AT'):
    st.set_page_config(
        #page_title=title,
        layout="wide")

def SetTheme():
    if 'sb_theme' not in st.session_state:
        with open("seabornTheme.json", 'r') as j:
            st.session_state['sb_theme'] = json.load(j)
    sb.set_theme(palette= st.session_state['sb_theme']['palette'],style= st.session_state['sb_theme']['style'])
    plt.rcParams.update(st.session_state['sb_theme']['plt_rcParams'])

def ReadCSV(name,path):
    if name not in st.session_state:
        st.session_state[name] = pd.read_csv(path,engine='pyarrow')
    return st.session_state[name]

def PreserveCSV(name,df):
    if name in st.session_state:
        st.session_state[name] = df
    return st.session_state[name]

def ReadJson(name,path):
    if name not in st.session_state:
        st.session_state[name] = pd.read_json(path)
    return st.session_state[name]

def PreserveJson(name,df):
    if name in st.session_state:
        st.session_state[name] = df
    return st.session_state[name]

def GetBasicTextMarkdown(font_size: float, text: str, align = 'center'):
    return f"""<p style='text-align: {align}; font-size:{font_size}px;'><b>{text}</b></p>"""
