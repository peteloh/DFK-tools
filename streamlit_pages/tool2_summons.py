import streamlit as st
import hero_core
import numpy as np
import pandas as pd

rpc_address = "https://api.harmony.one"

def app():
    st.header('Summoning Guru')
    col1, col2 = st.columns(2)
    col1.text_input('Hero 1')
    col2.text_input('Hero 2')

