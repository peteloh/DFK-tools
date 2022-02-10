import streamlit as st
import functions
import numpy as np
import pandas as pd

rpc_address = "https://api.harmony.one"

def app():
    st.header('My Heroes')
    user_address = st.text_input('0x Wallet Address', value ='0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F')

    if st.button('Search'):
        user_heroes = functions.get_users_heroes(user_address, rpc_address)

        df = pd.DataFrame(
            user_heroes,
            columns=["Hero ID"]
        )
        st.table(df)