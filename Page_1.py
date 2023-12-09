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
        with open("seabornTheme.json", 'r') as j:
            st.session_state['sb_theme'] = json.load(j)
    sb.set_theme(palette= st.session_state['sb_theme']['palette'],style= st.session_state['sb_theme']['style'])
    plt.rcParams.update(st.session_state['sb_theme']['plt_rcParams'])

SetTheme()

def GetBasicTextMarkdown(font_size: float, text: str, align = 'center'):
    return f"""<p style='text-align: {align}; font-size:{font_size}px;'><b>{text}</b></p>"""
st.header('Obtenção dos de dados',divider=True)
