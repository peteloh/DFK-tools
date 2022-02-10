import streamlit as st
import functions
import pandas as pd
import numpy as np

rpc_address = "https://api.harmony.one"

# Custom imports 
from streamlit_multipage import MultiPage
from streamlit_pages import tool1_heros, tool2_summons # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("DFK Tools")

# Add all your applications (pages) here
app.add_page("Heros Tracker", tool1_heros.app)
app.add_page("Summoning Guru", tool2_summons.app)

# The main app
app.run()

# if __name__ == '__main__': 
#     startup = True
#     st.sidebar.title('Please Select')
#     if st.sidebar.button('My Heroes') or startup == True:
#         startup = False
#         st.title('My Heroes')
#         user_address = st.text_input('0x Wallet Address', value ='0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F')

#         if st.button('Search'):
#             user_heroes = functions.get_users_heroes(user_address, rpc_address)

#             df = pd.DataFrame(
#                 user_heroes,
#                 columns=["Hero ID"]
#             )
#             st.table(df)

#     if st.sidebar.button('Summoning Guru'):
#         startup = False
#         st.title('Summoning Guru')
#         col1, col2 = st.columns(2)
#         col1.text_input('Hero 1')
#         col2.text_input('Hero 2')


    
    

    