import streamlit as st
import numpy as np
import pandas as pd

# custom imports
import hero_core
import utils

rpc_address = "https://api.harmony.one"

class hero:
    def __init__(self, heroId, rpc_address):
        raw_details = hero_core.get_hero(heroId, rpc_address)
        self.details = hero_core.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
    
    def genes_df(self, d0, r1, r2, r3):
        D0 =  ["D0", d0["class"], d0["subClass"], d0["profession"], d0["statBoost1"], d0["statBoost2"]]
        R1 =  ["R1", r1["class"], r1["subClass"], r1["profession"], r1["statBoost1"], r1["statBoost2"]]
        R2 =  ["R2", r2["class"], r2["subClass"], r2["profession"], r2["statBoost1"], r2["statBoost2"]]
        R3 =  ["R3", r3["class"], r3["subClass"], r3["profession"], r3["statBoost1"], r3["statBoost2"]]

        df = pd.DataFrame(
            data = [
                D0, R1, R2, R3
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
        return df

def unweighted_class_chances(class1, class2):
    p = {}
    if (class1 == "warrior" and class2 == "knight") or (class1 == "knight" and class2 == "warrior"):
        p["paladin"] = 0.25
        p[class1] = 0.375
        p[class2] = 0.375
    elif (class1 == "archer" and class2 == "thief") or (class1 == "thief" and class2 == "archer"):
        p["darkKnight"] = 0.25
        p[class1] = 0.375
        p[class2] = 0.375
    elif (class1 == "pirate" and class2 == "monk") or (class1 == "monk" and class2 == "pirate"):
        p["ninja"] = 0.25
        p[class1] = 0.375
        p[class2] = 0.375  
    elif (class1 == "wizard" and class2 == "priest") or (class1 == "priest" and class2 == "wizard"):
        p["summoner"] = 0.25
        p[class1] = 0.375
        p[class2] = 0.375  
    elif (class1 == "paladin" and class2 == "darkKnight") or (class1 == "darkKnight" and class2 == "paladin"):
        p["dragoon"] = 0.25
        p[class1] = 0.375
        p[class2] = 0.375
    elif (class1 == "ninja" and class2 == "summoner") or (class1 == "summoner" and class2 == "ninja"):
        p["sage"] = 0.25
        p[class1] = 0.375
        p[class2] = 0.375
    elif (class1 == "dragoon" and class2 == "sage") or (class1 == "sage" and class2 == "dragoon"):
        p["sage"] = 0.125
        p[class1] = 0.4375
        p[class2] = 0.4375
    else:
        if class1 == class2: p[class1] = 1
        else:
            p[class1] = 0.5
            p[class2] = 0.5
    return p

class summon:       
    def __init__(self):
        self.hero_class = {
            "warrior": [0,0],
            "knight": [0,0],
            "thief": [0,0],
            "archer": [0,0],
            "priest": [0,0],
            "wizard": [0,0],
            "monk": [0,0],
            "pirate": [0,0],
            "paladin": [0,0],
            "darkKnight": [0,0],
            "summoner": [0,0],
            "ninja": [0,0],
            "dragoon": [0,0],
            "sage": [0,0],
            "dreadKnight": [0,0]
        }
        self.hero_profession = {
            "mining": 0,
            "gardening": 0,
            "fishing": 0,
            "foraging": 0,
        }
        self.statBoost = {
            "STR": [0,0],
            "END": [0,0],
            "VIT": [0,0],
            "WIS": [0,0],
            "AGI": [0,0],
            "LCK": [0,0],
            "DEX": [0,0],
            "INT": [0,0]
        }

    def check_same_grandparents(self, hero1, hero2):
        hero1_parents = [hero1.details['summoningInfo']['summonerId'], hero1.details['summoningInfo']['assistantId']]
        hero2_parents = [hero2.details['summoningInfo']['summonerId'], hero2.details['summoningInfo']['assistantId']]
        return (hero1_parents[0] in hero2_parents) and (hero1_parents[1] in hero2_parents)
        

    def calculate_genes_probability(self, df1, df2):
        total_main = 0
        total_sub = 0
        for i in range(4):  #D0, R1, R2, R3

            weighting = [
                0.75,       
                0.1875, 
                0.046875,   
                0.015625
            ]

            p_mainClass = unweighted_class_chances(df1.loc[:,"Class"][i],df2.loc[:,"Class"][i])

            
            for key in p_mainClass.keys():
                total_main += p_mainClass[key] * weighting[i]
                self.hero_class[key][0] += p_mainClass[key] * weighting[i]

            
            p_subClass = unweighted_class_chances(df1.loc[:,"SubClass"][i],df2.loc[:,"SubClass"][i])
            for key in p_subClass.keys():
                self.hero_class[key][1] += p_subClass[key] * weighting[i]
                total_sub += p_subClass[key] * weighting[i]
            
            profession1 = df1.loc[:,"Prof"][i]
            self.hero_profession[profession1] += 0.5 * weighting[i]

            profession2 = df2.loc[:,"Prof"][i]
            self.hero_profession[profession2] += 0.5 * weighting[i]

            statBoost1 = df1.loc[:,"GreenStat"][i]
            statBoost1 = df2.loc[:,"GreenStat"][i]
            self.statBoost[utils.short_stat(statBoost1)][0] += 0.5 * weighting[i]
            self.statBoost[utils.short_stat(statBoost1)][0] += 0.5 * weighting[i]

            statBoost2 = df1.loc[:,"BlueStat"][i]
            statBoost2 = df2.loc[:,"BlueStat"][i]
            self.statBoost[utils.short_stat(statBoost1)][1] += 0.5 * weighting[i]
            self.statBoost[utils.short_stat(statBoost1)][1] += 0.5 * weighting[i]


def app():

    st.title('Summoning Guru')

    with st.container():
        col1, col2 = st.columns((1,1))
        hero_id1 = int(col1.text_input('Hero 1', value=118630))
        hero_id2 = int(col2.text_input('Hero 2', value=105293))

        hero1 = hero(hero_id1, rpc_address)
        hero2 = hero(hero_id2, rpc_address)
        offspring = summon()
        cantBorn = offspring.check_same_grandparents(hero1, hero2)

    
    if st.button('Search'):

        if cantBorn == True:
            st.write("Both heroes have the same parents, please try a different pair of heroes.")
            return

        df1 = hero1.genes_df(
            hero1.details['info']['statGenes'],
            hero1.details['info']['statGenes']['r1'],
            hero1.details['info']['statGenes']['r2'],
            hero1.details['info']['statGenes']['r3']
        )

        df2 = hero2.genes_df(
            hero2.details['info']['statGenes'],
            hero2.details['info']['statGenes']['r1'],
            hero2.details['info']['statGenes']['r2'],
            hero2.details['info']['statGenes']['r3']
        )

        
        with st.container():

            st.header("Probability")
            col1, col2 = st.columns((1,1)) 
            offspring.calculate_genes_probability(df1,df2)

            df3 = pd.DataFrame.from_dict(data=offspring.hero_class, orient='index', columns=['MainClass', 'SubClass'])
            df4 = pd.DataFrame.from_dict(data=offspring.hero_profession, orient='index', columns=['Profession'])
            df5 = pd.DataFrame.from_dict(data=offspring.statBoost, orient='index', columns=['GreenStat', 'BlueStat'])
            
            col1.markdown("**Class**")
            col1.dataframe(df3.style.format(subset=['MainClass', 'SubClass'], formatter="{:.2%}"), height=1500)

            col2.markdown("**StatBoost**")
            col2.dataframe(df5.style.format(subset=['GreenStat', 'BlueStat'], formatter="{:.2%}"), height=1500)

            col2.markdown("**Profession**")
            col2.dataframe(df4.style.format(subset=['Profession'], formatter="{:.2%}"), height=1500)

            with st.container():

                st.header("Parent Genes")

                col1, col2 = st.columns((1,1))
                col1.markdown("**Hero 1 Genes**")
                col1.write(df1)

                col2.markdown("**Hero 2 Genes**")
                col2.write(df2)

            with st.container():

                st.header("\nCalculation Details")

                st.markdown("""
                1. Summoned hero has 50/50 chance to get each parent genes (D0, R1, R2, R3)
                2. Weighting of each genes: 
                    D0 - 75%
                    R1 - 18.75%
                    R2 - 4.6875%
                    R3 - 1.5625%
                3. If parent genes match, 25% mutation chance into higher tier class, halved for DreadKnight
                """)

