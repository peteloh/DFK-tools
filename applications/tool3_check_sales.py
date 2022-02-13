import streamlit as st
import numpy as np
import pandas as pd

# custom imports
from core import hero_core, auction_core, utils
from applications import tool1_heroes

RPC_ADDRESS = "https://api.harmony.one"
AUCTION_ADDRESS = "0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892"

def heroes_string_to_list(heroes_string):
    old_list = heroes_string.split()
    for i in range(len(old_list)):
        old_list[i] = int(old_list[i])
    return old_list

my_heroes = """
    32436
    43124
    52654
    57763
    59353
    62625
    65456
    67570
    68109
    70142
    70722
    71631
    72734
    73805
    78384
    80331
    80335
    81764
    83525
    88002
    99260
    101896
    106105
    108143
    111688
    112548
    116164
    116183
    116595
    117394
    117484
    118630
    120121
    120274
    121351
    122037
    122043
    124852
    125145
    125148
    125725
    126097
    126524
    126530
"""


def app():

    st.header('Check Sales')
    
    st.subheader('Wallets')
    col1, col2 = st.columns((1,1))
    n_wallets = col1.number_input('Number of wallets to track', min_value=1, value=1)
    user_addresses = []

    for i in range(n_wallets):
        if i == 0: user_addresses += [col1.text_input('0x Wallet {} Address'.format(i+1), value = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F")]
        elif i == 1: user_addresses += [col1.text_input('0x Wallet {} Address'.format(i+1), value = "0xc4b35c78e83b598cf8e60f87e380731457eb824f")]
        else: user_addresses += [col1.text_input('0x Wallet {} Address'.format(i+1), value="")]
    
    st.subheader('Previous Heroes')
    heroes_string = st.text_input('Heroes List',value=my_heroes)

    with st.expander('Heroes List Help'):
        st.markdown("**Step 1** - Copy column of hero IDs")
        st.image('./images/hero_list_guide.png')
        st.markdown("**Step 2** - Paste as it is")
        st.image('./images/hero_list_guide2.png')
        st.markdown("**Step 3** - Press Search")
    
    st.subheader('Hero Sales')
    if st.button('Search'):
        old_list = sorted(heroes_string_to_list(heroes_string))

        if len(user_addresses) == 1:
            user_heroes_in_wallet = hero_core.get_users_heroes(user_addresses[0], RPC_ADDRESS)
            user_heroes_in_auctions = auction_core.get_user_auctions(AUCTION_ADDRESS, user_addresses[0], RPC_ADDRESS)
            user_heroes = sorted(user_heroes_in_wallet + user_heroes_in_auctions)
        else:
            user_heroes = []
            for i in range(len(user_addresses)):
                user_heroes += hero_core.get_users_heroes(user_addresses[i], RPC_ADDRESS)
                user_heroes += auction_core.get_user_auctions(AUCTION_ADDRESS, user_addresses[i], RPC_ADDRESS)

        current_list = sorted(user_heroes)

        hero_sold = []
        new_hero = []
        

        for i in range(len(old_list)):
            if old_list[i] not in current_list:
                hero_sold += [old_list[i]]

        for i in range(len(current_list)):
            if current_list[i] not in old_list:
                new_hero += [current_list[i]]

        with st.container():
            col1,col2,col3 = st.columns((1,1,1))
            col1.markdown("**Number**")
            col2.markdown("**Hero Sold**")
            col3.markdown("**New Hero**")

            if hero_sold == []: col2.write("No Hero(s) Sold")
            if new_hero == []: col3.write("No New Hero(s)")

            else:
                for i in range(max(len(hero_sold), len(new_hero))):
                    col1.write(str(i+1))

                for hero in hero_sold:
                    col2.write(str(hero))
                
                for hero in new_hero:
                    col3.write(str(hero))

        st.write("#")  
        
        st.header("Calculations")  
        st.write("Hero sold is the the list heroes that existed in the input_list but in the list pulled from the blockchain")
        st.write("New Hero is the the list heroes that exists on the blockchian but not in the input_list")
