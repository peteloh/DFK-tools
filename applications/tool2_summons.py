import streamlit as st
import numpy as np
import pandas as pd

# custom imports
from core import hero_core, utils

rpc_address = "https://api.harmony.one"

class hero:
    def __init__(self, heroId, rpc_address):
        raw_details = hero_core.get_hero(heroId, rpc_address)
        self.details = hero_core.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
    
    def get_stats(self, details):
        data = {}
        data["ID"] = [details["id"]]
        data["Gen"] = [details["info"]["generation"]]
        data["Level"] = [details["state"]["level"]]
        maxSummons = details["summoningInfo"]["maxSummons"]
        data["SumLeft"] = [maxSummons - details["summoningInfo"]["summons"]]
        data["SumMax"] = [maxSummons]
        data["Rarity"] = [details["info"]["rarity"]]
        data["Class"] = [details["info"]["statGenes"]["class"]]
        data["SubClass"] = [details["info"]["statGenes"]["subClass"]]
        profession = details["info"]["statGenes"]["profession"]
        data["Prof"] = [profession]

        prof_stats = utils.ideal_professsion_stats(profession)
        data["ProfStat1"] = [prof_stats[0]]
        data["ProfStat2"] = [prof_stats[1]]
        profStat1_val = details["stats"][utils.long_stat(prof_stats[0])]
        profStat2_val = details["stats"][utils.long_stat(prof_stats[1])]
        data["ValStat1"] = [profStat1_val]
        data["ValStat2"] = [profStat2_val]
        data["GreenStat"] = [details["info"]["statGenes"]["statBoost1"]]
        data["BlueStat"] = [details["info"]["statGenes"]["statBoost2"]]
        self.stats = data

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
    
    def check_is_parent_child(self, hero1, hero2):
        hero1_ID = hero1.details["id"]
        hero2_ID = hero1.details["id"]
        hero1_parents = [hero1.details['summoningInfo']['summonerId'], hero1.details['summoningInfo']['assistantId']]
        hero2_parents = [hero2.details['summoningInfo']['summonerId'], hero2.details['summoningInfo']['assistantId']]
        if hero1_parents[0] == hero2_ID or hero1_parents[1] == hero2_ID: 
            return True
        elif hero2_parents[0] == hero1_ID or hero2_parents[1] == hero1_ID: 
            return True
        else: 
            return False
        

    def calculate_genes_probability(self, df1, df2):
        weighting = [
            0.75,       
            0.1875, 
            0.046875,   
            0.015625
        ]

        for i in range(4):  # Hero1 D0, R1, R2, R3
            for j in range(4): # Hero2 D0, R1, R2, R3
                
                p_mainClass = unweighted_class_chances(df1.loc[:,"Class"][i],df2.loc[:,"Class"][j])
                p_subClass = unweighted_class_chances(df1.loc[:,"SubClass"][i],df2.loc[:,"SubClass"][j])

                for key in p_mainClass.keys():
                    self.hero_class[key][0] += p_mainClass[key] * weighting[i] * weighting[j]
                
                p_subClass = unweighted_class_chances(df1.loc[:,"SubClass"][i],df2.loc[:,"SubClass"][i])
                for key in p_subClass.keys():
                    self.hero_class[key][1] += p_subClass[key] * weighting[i] * weighting[j]

                profession1 = df1.loc[:,"Prof"][i]
                profession2 = df2.loc[:,"Prof"][j]
                self.hero_profession[profession1] += 0.5 * weighting[i] * weighting[j]
                self.hero_profession[profession2] += 0.5 * weighting[i] * weighting[j]

                hero1_statBoost1 = df1.loc[:,"GreenStat"][i]
                hero2_statBoost1 = df2.loc[:,"GreenStat"][j]
                self.statBoost[hero1_statBoost1][0] += 0.5 * weighting[i] * weighting[j]
                self.statBoost[hero2_statBoost1][0] += 0.5 * weighting[i] * weighting[j]

                hero1_statBoost2 = df1.loc[:,"BlueStat"][i]
                hero2_statBoost2 = df2.loc[:,"BlueStat"][j]
                self.statBoost[hero1_statBoost2][1] += 0.5 * weighting[i] * weighting[j]
                self.statBoost[hero2_statBoost2][1] += 0.5 * weighting[i] * weighting[j]

def app():

    st.title('Summoning Guru')

    with st.container():
        col1, col2 = st.columns((1,1))
        col1.subheader("Hero 1")
        col2.subheader("Hero 2")
        hero_id1 = int(col1.text_input("Input",value=118630))
        hero_id2 = int(col2.text_input("Input",value=105293))

        hero1 = hero(hero_id1, rpc_address)
        hero2 = hero(hero_id2, rpc_address)
        offspring = summon()

        hero1.get_stats(hero1.details)
        hero2.get_stats(hero2.details)

        
    with st.container():
        col1, col2, col5, col6 = st.columns((1,1,1,1))

        col1.text("Hero ID")
        col2.text(str(hero1.stats["ID"][0]))
        col5.text("Hero ID")
        col6.text(str(hero2.stats["ID"][0]))

        col1.text("Generation")
        col2.text(str(hero1.stats["Gen"][0]))
        col5.text("Generation")
        col6.text(str(hero2.stats["Gen"][0]))

        col1.text("Summons")
        col2.text(str(hero1.stats["SumLeft"][0]) + "/" + str(hero1.stats["SumMax"][0]))
        col5.text("Summons")
        col6.text(str(hero2.stats["SumLeft"][0]) + "/" + str(hero2.stats["SumMax"][0]))

        col1.text("Rarity")
        col2.text(str(hero1.stats["Rarity"][0]))
        col5.text("Rarity")
        col6.text(str(hero2.stats["Rarity"][0]))

        col1.text("Class")
        col2.text(str(hero1.stats["Class"][0]))
        col5.text("Class")
        col6.text(str(hero2.stats["Class"][0]))

        col1.text("SubClass")
        col2.text(str(hero1.stats["SubClass"][0]))
        col5.text("SubClass")
        col6.text(str(hero2.stats["SubClass"][0]))

        col1.text("Profession")
        col2.text(str(hero1.stats["Prof"][0]))
        col5.text("Profession")
        col6.text(str(hero2.stats["Prof"][0]))

        col1.text("GreenStat")
        col2.text(str(hero1.stats["GreenStat"][0]))
        col5.text("GreenStat")
        col6.text(str(hero2.stats["GreenStat"][0]))

        col1.text("BlueStat")
        col2.text(str(hero1.stats["BlueStat"][0]))
        col5.text("BlueStat")
        col6.text(str(hero2.stats["BlueStat"][0]))
    
    with st.container():
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

        col1, col2 = st.columns((1,1))
        col1.markdown("**Genes**")
        col1.write(df1)

        col2.markdown("**Genes**")
        col2.write(df2)

    
    if offspring.check_same_grandparents(hero1, hero2) == True or offspring.check_is_parent_child(hero1, hero2) == True:
        st.write("Incest is not allowed, please try a different pair of heroes.")

    else:
        if st.button('Search'):

            with st.container():

                st.header("Probability")
                offspring.calculate_genes_probability(df1,df2)
                
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((1,1,1,1,1,1,1,1)) 

                col1.markdown("**Classes**")
                col2.markdown("**MainClass**")
                col3.markdown("**SubClass**")

                df3 = pd.DataFrame.from_dict(data=offspring.hero_class, orient='index', columns=['MainClass', 'SubClass'])
                df3_array = df3.to_numpy() * 100

                for key in offspring.hero_class.keys():
                    col1.text(str(key))

                for i in range(len(df3_array)):
                    if df3_array[i,0] == 0: col2.text("-")
                    else: col2.text(str(round(df3_array[i,0],2))+"%")
                    if df3_array[i,1] == 0: col3.text("-")
                    else: col3.text(str(round(df3_array[i,1],2))+"%")

                col5.markdown("**StatBoost**")
                col6.markdown("**GreenStat**")
                col7.markdown("**BlueStat**")

                df4 = pd.DataFrame.from_dict(data=offspring.statBoost, orient='index', columns=['GreenStat', 'BlueStat'])
                df4_array = df4.to_numpy() * 100

                for key in offspring.statBoost.keys():
                    col5.text(str(key))
                
                for i in range(len(df4_array)):
                    if df4_array[i,0] == 0: col6.text("-")
                    else: col6.text(str(round(df4_array[i,0],2))+"%")
                    if df4_array[i,1] == 0: col7.text("-")
                    else: col7.text(str(round(df4_array[i,1],2))+"%")
                
                col5.markdown("____________________________________________________________")
                col6.markdown("____________________________________________________________")
                col7.markdown("____________________________________________________________")

                col5.markdown("**Profession**")
                col6.markdown("**Chances**")

                df5 = pd.DataFrame.from_dict(data=offspring.hero_profession, orient='index', columns=['Profession'])
                df5_array = df5.to_numpy() * 100

                for key in offspring.hero_profession.keys():
                    col5.text(str(key))
                for i in range(len(df5_array)):
                    if df5_array[i,0] == 0: col6.text("-")
                    else: col6.text(str(round(df5_array[i,0],2))+"%")
            
                
                # col5.markdown("**StatBoost**")
                # col6.write("GreenStat")
                # col7.write("BlueStat")

                # col1.text(offspring.hero_class[0][])
                # col2.text(df3[0,1])
                # col3.text(df3[0,2])
                # col5.text("**StatBoost**")
                # col6.text("GreenStat")
                # col7.text("BlueStat")



                # col1.markdown("**Class**")
                # col1.dataframe(df3.style.format(subset=['MainClass', 'SubClass'], formatter="{:.2%}"), height=1500)

                # col2.markdown("**StatBoost**")
                # col2.dataframe(df5.style.format(subset=['GreenStat', 'BlueStat'], formatter="{:.2%}"), height=1500)

                # col2.markdown("**Profession**")
                # col2.dataframe(df4.style.format(subset=['Profession'], formatter="{:.2%}"), height=1500)

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
    
