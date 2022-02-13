import streamlit as st
import pandas as pd
import matplotlib.pyplot as pl

# custom imports
from core import hero_core, auction_core, utils
from core.dfk_contracts import serendale_contracts

auction_address = "0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892"
rpc_address = "https://api.harmony.one"

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def app():

    data = {
    "ID": [],
    "Gen": [],
    "SumLeft": [],
    "SumMax": [],
    "Rarity" : [],
    "Class": [],
    "SubClass": [],
    "Profession": [],
    "ProfStat1": [],
    "ProfStat2": [],
    "ValStat1": [],
    "ValStat2": [],
    "SumStats": [],
    "Level": []
    }

    st.header('My Heroes')

    col1, col2 = st.columns((1,1))
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

        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14 = st.columns((1,0.5,0.5,0.5,1,1,1,1,0.8,0.8,0.7,0.5,0.5,0.5))
        col1.markdown("**ID**")
        col2.markdown("**Gen**")
        col3.markdown("**SumLeft**")
        col4.markdown("**SumMax**")
        col5.markdown("**Rarity**")
        col6.markdown("**Class**")
        col7.markdown("**SubClass**")
        col8.markdown("**Profession**")
        col9.markdown("**ProfStat1**")
        col10.markdown("**ProfStat2**")
        col11.markdown("**Val1**")
        col12.markdown("**Val2**")
        col13.markdown("**ΣStats**")
        col14.markdown("**Lvl**")

        for hero in user_heroes:
            count+=1
            
            percentage = count / len(user_heroes)
            pg_bar_holder.progress(percentage)

            raw_details = hero_core.get_hero(hero, rpc_address)
            details = hero_core.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
            heroId = details["id"]
            data["ID"] += [heroId]
            col1.text(heroId)
            
            generation = details["info"]["generation"]
            data["Gen"] += [generation]
            col2.text(generation)

            maxSummons = details["summoningInfo"]["maxSummons"]
            sumLeft = maxSummons - details["summoningInfo"]["summons"]
            data["SumLeft"] += [sumLeft]
            col3.text(sumLeft)
            data["SumMax"] += [maxSummons]
            col4.text(maxSummons)

            rarity = details["info"]["rarity"]
            data["Rarity"] += [rarity]
            col5.text(rarity)
            mainClass = details["info"]["statGenes"]["class"]
            data["Class"] += [mainClass]
            col6.text(mainClass)
            subClass = details["info"]["statGenes"]["subClass"]
            data["SubClass"] += [subClass]
            col7.text(subClass)

            profession = details["info"]["statGenes"]["profession"]
            data["Profession"] += [profession]
            col8.text(profession)

            prof_stats = utils.ideal_professsion_stats(profession)
            data["ProfStat1"] += [prof_stats[0]]
            col9.text(prof_stats[0])
            data["ProfStat2"] += [prof_stats[1]]
            col10.text(prof_stats[1])

            profStat1_val = details["stats"][utils.long_stat(prof_stats[0])]
            profStat2_val = details["stats"][utils.long_stat(prof_stats[1])]
            data["ValStat1"] += [profStat1_val]
            col11.text(profStat1_val)
            data["ValStat2"] += [profStat2_val]
            col12.text(profStat2_val)
            sumStats = profStat1_val + profStat2_val
            data["SumStats"] += [sumStats]
            col13.text(sumStats)

            level = details["state"]["level"]
            data["Level"] += [level]
            col14.text(level)

        pg_bar_holder.empty() 
        df = pd.DataFrame(data=data)
        # st.dataframe(df,height=3000)



        csv = convert_df(df)
        filename = "dfk_heroes.csv"
        st.download_button(
            label="Export CSV",
            data=csv,
            file_name=filename,
            mime='text/csv',
        )

