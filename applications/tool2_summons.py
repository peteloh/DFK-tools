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
        data["ID"] = details["id"]
        data["Gen"] = details["info"]["generation"]
        data["Level"] = details["state"]["level"]
        maxSummons = details["summoningInfo"]["maxSummons"]
        data["SumLeft"] = maxSummons - details["summoningInfo"]["summons"]
        data["SumMax"] = maxSummons
        data["Rarity"] = details["info"]["rarity"]
        data["Class"] = details["info"]["statGenes"]["class"]
        data["SubClass"] = details["info"]["statGenes"]["subClass"]
        profession = details["info"]["statGenes"]["profession"]
        data["Prof"] = profession

        prof_stats = utils.ideal_professsion_stats(profession)
        data["ProfStat1"] = prof_stats[0]
        data["ProfStat2"] = prof_stats[1]
        profStat1_val = details["stats"][utils.long_stat(prof_stats[0])]
        profStat2_val = details["stats"][utils.long_stat(prof_stats[1])]
        data["ValStat1"] = profStat1_val
        data["ValStat2"] = profStat2_val
        data["GreenStat"] = details["info"]["statGenes"]["statBoost1"]
        data["BlueStat"] = details["info"]["statGenes"]["statBoost2"]
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
        p["dreadKnight"] = 0.125
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

def convert_to_percent(decimal):
    if not isinstance(decimal, float): return "-"
    if decimal == 0: return "-"
    else: return str(round((decimal * 100),2))+"%"


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
        col2.text(str(hero1.stats["ID"]))
        col5.text("Hero ID")
        col6.text(str(hero2.stats["ID"]))

        col1.text("Generation")
        col2.text(str(hero1.stats["Gen"]))
        col5.text("Generation")
        col6.text(str(hero2.stats["Gen"]))

        col1.text("Summons")
        col2.text(str(hero1.stats["SumLeft"]) + "/" + str(hero1.stats["SumMax"]))
        col5.text("Summons")
        col6.text(str(hero2.stats["SumLeft"]) + "/" + str(hero2.stats["SumMax"]))

        col1.text("Rarity")
        col2.text(str(hero1.stats["Rarity"]))
        col5.text("Rarity")
        col6.text(str(hero2.stats["Rarity"]))

        col1.text("Class")
        col2.text(str(hero1.stats["Class"]))
        col5.text("Class")
        col6.text(str(hero2.stats["Class"]))

        col1.text("SubClass")
        col2.text(str(hero1.stats["SubClass"]))
        col5.text("SubClass")
        col6.text(str(hero2.stats["SubClass"]))

        col1.text("Profession")
        col2.text(str(hero1.stats["Prof"]))
        col5.text("Profession")
        col6.text(str(hero2.stats["Prof"]))

        col1.text("GreenStat")
        col2.text(str(hero1.stats["GreenStat"]))
        col5.text("GreenStat")
        col6.text(str(hero2.stats["GreenStat"]))

        col1.text("BlueStat")
        col2.text(str(hero1.stats["BlueStat"]))
        col5.text("BlueStat")
        col6.text(str(hero2.stats["BlueStat"]))
    
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
            
            st.header("Probability")
            st.subheader("Basic Statistics")
            with st.container():

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
            
            st.markdown('#')

            st.subheader("Advanced Statistics")
            with st.container():
                col1, col2, col3, col4, col5 = st.columns((1,1,1,1,1))

                col1.markdown('**Class**')
                col2.markdown('**Match Prof + 2 StatBoosts**')
                col3.markdown('**Match Prof + 1 StatBoosts**')
                col4.markdown('**Match Prof + 0 StatBoosts**')
                col5.markdown('**Mismatched Prof**')
    
                # prob_class = offspring.hero_class
                table = []

                for key in offspring.hero_class.keys():

                    prob_mainclass = offspring.hero_class[key][0]

                    matching_prof = utils.ideal_class_profession(key)
                    prob_matching_prof = offspring.hero_profession[matching_prof]
                    prob_not_matching_prof = 1 - prob_matching_prof

                    matching_stats = utils.ideal_professsion_stats(matching_prof)
                    matching_stat1 = matching_stats[0]
                    matching_stat2 = matching_stats[1]

                    prob_matching_stat1 = offspring.statBoost[matching_stat1][0] + offspring.statBoost[matching_stat2][0]
                    prob_not_matching_stat1 = 1 - prob_matching_stat1
                    prob_matching_stat2 = offspring.statBoost[matching_stat1][1] + offspring.statBoost[matching_stat2][1]
                    prob_not_matching_stat2 = 1 - prob_matching_stat2

                    table += [[
                        key,
                        prob_mainclass * prob_matching_prof * prob_matching_stat1 * prob_matching_stat2,
                        prob_mainclass * prob_matching_prof * prob_matching_stat1 * prob_not_matching_stat2 + prob_mainclass * prob_matching_prof * prob_not_matching_stat1 * prob_matching_stat2,
                        prob_mainclass * prob_matching_prof * prob_not_matching_stat1 * prob_not_matching_stat2,
                        prob_mainclass * prob_not_matching_prof,
                        prob_mainclass
                    ]]
                total = [0,0,0,0]
                for row in table:

                    col1.text(row[0])
                    col2.text(convert_to_percent(row[1]))
                    col3.text(convert_to_percent(row[2]))
                    col4.text(convert_to_percent(row[3]))
                    col5.text(convert_to_percent(row[4]))
                    total[0] += row[1]
                    total[1] += row[2]
                    total[2] += row[3]
                    total[3] += row[4]
                
                col1.markdown("**Total**")
                col2.markdown("**"+convert_to_percent(total[0])+"**")
                col3.markdown("**"+convert_to_percent(total[1])+"**")
                col4.markdown("**"+convert_to_percent(total[2])+"**")
                col5.markdown("**"+convert_to_percent(total[3])+"**")

            # st.markdown('#')
            # st.subheader("Expected Returns")
            # with st.container(): 
            #     col1, gap, col2, col3, col4 = st.columns((1,0.5,1,1,1))
            #     col2.markdown("**Costs**")
            #     # col2.markdown("** **")

            #     col1.markdown("**Potential Rewards**")
            #     # col4.markdown("** **")

            # with st.container():
                
            #     col3, gap, col1, col2, col4 = st.columns((1,0.5,1,1,1))
            #     valid_classes = []
            #     floor_prices = []

            #     for key in offspring.hero_class.keys():
            #         if offspring.hero_class[key][0] != 0:
            #             valid_classes += [key]
                
            #     for c in valid_classes:
            #         floor_prices += [col3.number_input(f"{c} est. floor price")]

            #     cost_hero1 = col1.number_input(f"Cost of Hero 1")               
            #     cost_hero2 = col1.number_input(f"Cost of Hero 2")

            #     hero1_sale = col2.number_input(f"Sale Price Hero 1 (0 Summon)")
            #     hero2_sale = col2.number_input(f"Sale Price Hero 2 (0 Summon)")
                
            #     net_hero_cost = cost_hero1 + cost_hero2 - hero1_sale - hero2_sale

            #     col1.markdown(f"**Net Hero Cost   =   {net_hero_cost}**")

            #     col1.markdown("____________________________________________________________")

            #     maxSummons = min(hero1.stats["SumLeft"], hero2.stats["SumLeft"])
            #     col1.markdown(f"This pair has {maxSummons} summon(s) left")

            #     hero1_summoned =hero1.stats["SumMax"] - hero1.stats["SumLeft"]
            #     hero2_summoned =hero2.stats["SumMax"] - hero2.stats["SumLeft"]

            #     total_summoning_cost = 0
            #     for i in range(maxSummons):
            #         hero1_cost = utils.summoning_cost(hero1.stats["Gen"], hero1_summoned)
            #         hero1_summoned += 1
            #         hero2_cost = utils.summoning_cost(hero2.stats["Gen"], hero2_summoned)
            #         hero2_summoned += 1

            #         summon_cost = hero1_cost + hero2_cost
            #         total_summoning_cost += summon_cost
            #         col1.markdown(f"Summon {i+1} = {hero1_cost} + {hero2_cost} = {summon_cost}")
                
            #     col1.markdown(f"**Total Summoning Costs   =   {total_summoning_cost}**")

            #     col1.markdown("____________________________________________________________")

            #     total_costs = net_hero_cost + total_summoning_cost
            #     col1.markdown(f"**Overall Cost   =   {total_costs} Jewels**")

            
            # if st.button("Calculate"):
            #     with st.cointainer():

            #         col1, col2, col3, col4 = columns((1,1,1,1))
            #         offspring_EV = 0

            #         col1.markdown("**Main Class**")
            #         col2.markdown("**Probabiliy**")
            #         col3.markdown("**Floor Price**")
            #         col4.markdown("**Class EV (Per Summon)**")
                    
            #         for i in range(valid_classes):
            #             col1.write(valid_classes[i])
            #             col2.write(offspring.hero_class[key][0])
            #             col3.write(floor_prices[i])
            #             col4.write(offspring.hero_class[key][0] * floor_prices[i] * maxSummons)
            #             offspring_EV += offspring.hero_class[key][0] * floor_prices[i]
                        
            #         st.write("EV per summon = " + str(offspring_EV))
            #         st.write("Max number of summons = " + str(maxSummons))
            #         st.write("Total Summons EV = " + str(offspring_EV * maxSummons))
            #         st.write("Total Costs = " + str(total_costs))
            #         st.markdown(f"**Expected Value = {offspring_EV * maxSummons - total_costs}**")
                    

                    
            st.header("\nCalculation Details")
            with st.container():

                st.markdown("""
                1. Summoned hero has 50/50 chance to get each parent genes (D0, R1, R2, R3)
                2. Weighting of each genes: 
                    D0 - 75%
                    R1 - 18.75%
                    R2 - 4.6875%
                    R3 - 1.5625%
                3. If parent genes match, 25% mutation chance into higher tier class, halved for DreadKnight
                """)

                st.markdown("""
                For advanced probabilities, 4 main scenarios were considered:
                1. Main Class match with profession and 2 stat boost
                2. Main Class match with profession and 1 stat boost
                3. Main Class match with profession and 0 stat boost
                4. Main Class not match with profession.
                """)
    
