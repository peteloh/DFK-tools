import functions
import pandas as pd

user_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"
rpc_address = "https://api.fuzz.fi"

user_heroes = functions.get_users_heroes(user_address, rpc_address)

# print(user_heroes)
# print(len(user_heroes))

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
    "heroId": [],
    "generation": [],
    "summons": [],
    "maxSummons": [],
    "mainClass": [],
    "subClass": [],
    "profession": [],
    "statBoost1": [],
    "statBoost2": [],
    "profStat1": [],
    "profStat2": [],
    "totalProfStats": [],
    "level": []
}

for hero in user_heroes:
    raw_details = functions.get_hero(hero, rpc_address)
    details = functions.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
    data["heroId"] += [details["id"]]
    data["generation"] += [details["info"]["generation"]]
    data["summons"] += [details["summoningInfo"]["summons"]]
    data["maxSummons"] += [details["summoningInfo"]["maxSummons"]]
    data["mainClass"] += [details["info"]["statGenes"]["class"]]
    data["subClass"] += [details["info"]["statGenes"]["subClass"]]

    profession = details["info"]["statGenes"]["profession"]
    # print(profession)
    data["profession"] += [profession]

    data["statBoost1"] += [short_stat[details["info"]["statGenes"]["statBoost1"]]]
    data["statBoost2"] += [short_stat[details["info"]["statGenes"]["statBoost2"]]]

    prof_stats = ideal_professsion_stats[profession]
    profStat1_val = details["stats"][prof_stats[0]]
    profStat2_val = details["stats"][prof_stats[1]]
    data["profStat1"] += [profStat1_val]
    data["profStat2"] += [profStat2_val]
    data["totalProfStats"] += [profStat1_val + profStat2_val]

    data["level"] += [details["state"]["level"]]

    # print(details)

# print(data)
df = pd.DataFrame(data=data)
df.to_csv(f'./csv/hero_tracking.csv')

