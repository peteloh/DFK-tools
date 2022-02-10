import streamlit as st
import pandas as pd
import matplotlib.pyplot as pl

# custom imports
import hero_core
import auction_core
import pandas as pd
from dfk_contracts import serendale_contracts

ideal_class_profession = {
    "warrior": "mining",
    "knight": "mining",
    "archer": "foraging",
    "thief": "fishing",
    "pirate": "mining",
    "monk": "mining",
    "wizard": "gardening",
    "priest": "gardening",
    "paladin": "mining",
    "darkknight": "mining",
    "ninja": "fishing",
    "summoner": "gardening",
    "dragoon": "mining",
    "sage": "gardening",
    "dreadknight": "mining"
}

ideal_professsion_stats = {
    "mining": ["strength", "endurance"],
    "gardening": ["wisdom", "vitality"],
    "foraging": ["intelligence", "dexterity"],
    "fishing": ["agility", "luck"]
}

short_stat = {
    "agility": "AGI",
    "strength": "STR",
    "endurance": "END",
    "luck": "LCK",
    "dexterity": "DEX",
    "wisdom": "WIS",
    "intelligence": "INT",
    "vitality": "VIT"
}

data = {
    "ID": [],
    "Gen": [],
    "SumLeft": [],
    "SumMax": [],
    "Rarity" : [],
    "Class": [],
    "SubClass": [],
    "Prof": [],
    "ProfStat1": [],
    "ProfStat2": [],
    "ValStat1": [],
    "ValStat2": [],
    "SumStats": [],
    "Level": []
}

auction_address = "0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892"
rpc_address = "https://api.harmony.one"

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

st.set_page_config(
            page_title="dfk tools",
            layout='wide'
    )

def app():

    st.header('My Heroes')

    col1, col2 = st.columns((1,2))
    n_wallets = col1.number_input('Number of wallets to track', min_value=1, value=1)
    user_addresses = []

    for i in range(n_wallets):
        if i == 0: user_addresses += [col1.text_input('0x Wallet {} Address'.format(i+1), value = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F")]
        elif i == 1: user_addresses += [col1.text_input('0x Wallet {} Address'.format(i+1), value = "0xc4b35c78e83b598cf8e60f87e380731457eb824f")]
        else: user_addresses += [col1.text_input('0x Wallet {} Address'.format(i+1), value="")]
    
    if col1.button('Search'):

        if len(user_addresses) == 1:
            user_heroes_in_wallet = hero_core.get_users_heroes(user_addresses[0], rpc_address)
            user_heroes_in_auctions = auction_core.get_user_auctions(auction_address, user_addresses[0], rpc_address)
            user_heroes = sorted(user_heroes_in_wallet + user_heroes_in_auctions)
        else:
            user_heroes = []
            for i in range(len(user_addresses)):
                user_heroes += hero_core.get_users_heroes(user_addresses[i], rpc_address)
                user_heroes += auction_core.get_user_auctions(auction_address, user_addresses[i], rpc_address)

        user_heroes = sorted(user_heroes)

        count = 0

        pg_bar_holder = col1.empty()
        pg_bar = pg_bar_holder.progress(0)

        for hero in user_heroes:
            count+=1
            percentage = count / len(user_heroes)
            pg_bar_holder.progress(percentage)
            raw_details = hero_core.get_hero(hero, rpc_address)
            details = hero_core.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
            data["ID"] += [details["id"]]
            data["Gen"] += [details["info"]["generation"]]

            maxSummons = details["summoningInfo"]["maxSummons"]
            data["SumLeft"] += [maxSummons - details["summoningInfo"]["summons"]]
            data["SumMax"] += [maxSummons]

            data["Rarity"] += [details["info"]["rarity"]]
            data["Class"] += [details["info"]["statGenes"]["class"]]
            data["SubClass"] += [details["info"]["statGenes"]["subClass"]]

            profession = details["info"]["statGenes"]["profession"]
            # print(profession)
            data["Prof"] += [profession]

            # data["statBoost1"] += [short_stat[details["info"]["statGenes"]["statBoost1"]]]
            # data["statBoost2"] += [short_stat[details["info"]["statGenes"]["statBoost2"]]]

            prof_stats = ideal_professsion_stats[profession]
            data["ProfStat1"] += [short_stat[prof_stats[0]]]
            data["ProfStat2"] += [short_stat[prof_stats[1]]]

            profStat1_val = details["stats"][prof_stats[0]]
            profStat2_val = details["stats"][prof_stats[1]]
            data["ValStat1"] += [profStat1_val]
            data["ValStat2"] += [profStat2_val]
            data["SumStats"] += [profStat1_val + profStat2_val]

            data["Level"] += [details["state"]["level"]]

        pg_bar_holder.empty() 
        
        df = pd.DataFrame(data=data)
        st.dataframe(df,height=3000)


        csv = convert_df(df)
        filename = "dfk_heroes.csv"
        st.download_button(
            label="Export CSV",
            data=csv,
            file_name=filename,
            mime='text/csv',
        )

