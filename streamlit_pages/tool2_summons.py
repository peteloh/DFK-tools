import streamlit as st
import hero_core
import numpy as np
import pandas as pd

rpc_address = "https://api.harmony.one"

class genes_table:
    def __init__(self, d0, r1, r2, r3):
        self.D0 =  ["Dominant", d0["class"], d0["subClass"], d0["profession"], d0["statBoost1"], d0["statBoost2"]]
        self.R1 =  ["R1",       r1["class"], r1["subClass"], r1["profession"], r1["statBoost1"], r1["statBoost2"]]
        self.R2 =  ["R2",       r2["class"], r2["subClass"], r2["profession"], r2["statBoost1"], r2["statBoost2"]]
        self.R3 =  ["R3",       r3["class"], r3["subClass"], r3["profession"], r3["statBoost1"], r3["statBoost2"]]
    


def app():

    
    st.header('Summoning Guru')
    r1col1, r1col2, r1col3, r1col4 = st.columns((1,1,1,1))
    hero1 = int(r1col1.text_input('Hero 1', value=118630))
    hero2 = int(r1col2.text_input('Hero 2', value=105293))

    r2col1, r2col2 = st.columns((1,1))
    if r1col1.button('Search'):

        hero_1_raw_details = hero_core.get_hero(hero1, rpc_address)
        hero_1_details = hero_core.human_readable_hero(hero_1_raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)

        hero1_d0 = hero_1_details['info']['statGenes']
        hero1_r1 = hero_1_details['info']['statGenes']['r1']
        hero1_r2 = hero_1_details['info']['statGenes']['r2']
        hero1_r3 = hero_1_details['info']['statGenes']['r3']

        hero1_genes = genes_table(hero1_d0, hero1_r1, hero1_r2, hero1_r3)
        df1 = pd.DataFrame(
            data = [
                hero1_genes.D0, hero1_genes.R1, hero1_genes.R2, hero1_genes.R3
            ],
            columns = [
                "Genes",
                "Class",
                "SubClass",
                "Prof",
                "GreenStat",
                "BlueStat"
            ]
        )
        
        hero_2_raw_details = hero_core.get_hero(hero2, rpc_address)
        hero_2_details = hero_core.human_readable_hero(hero_2_raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)

        hero2_d0 = hero_2_details['info']['statGenes']
        hero2_r1 = hero_2_details['info']['statGenes']['r1']
        hero2_r2 = hero_2_details['info']['statGenes']['r2']
        hero2_r3 = hero_2_details['info']['statGenes']['r3']

        hero2_genes = genes_table(hero2_d0, hero2_r1, hero2_r2, hero2_r3)
        df2 = pd.DataFrame(
            data = [
                hero2_genes.D0, hero2_genes.R1, hero2_genes.R2, hero2_genes.R3
            ],
            columns = [
                "Genes",
                "Class",
                "SubClass",
                "Prof",
                "GreenStat",
                "BlueStat"
            ]
        )

        r2col1.subheader("Hero 1 Genes")
        r2col1.write(df1)

        r2col2.subheader("Hero 2 Genes")
        r2col2.write(df2)
        
    r3col1, r3col2 = st.columns((1,1)) 
    
    st.markdown("""

    **Calculation Details** \n
    1. Summoned hero has 50/50 chance to get each parent genes (D0, R1, R2, R3)
    2. Weighting of each genes: 
        D0 - 75%
        R1 - 18.75%
        R2 - 4.6875%
        R3 - 1.5625%
    3. If parent genes match, 25% mutation chance into higher tier class, halved for DreadKnight
    """)

