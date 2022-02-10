import hero_core
import pandas as pd

user_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"
rpc_address = "https://api.harmony.one"

#user_heroes = functions.get_users_heroes(user_address, rpc_address)

# print(user_heroes)
# print(len(user_heroes))

# use manual hero id input
user_heroes = [
    43124,
    52654,
    57763,
    59353,
    62625,
    63927,
    65456,
    67570,
    68109,
    70142,
    70722,
    71631,
    72734,
    73805,
    78384,
    80331,
    80335,
    81764,
    83525,
    88002,
    89219,
    92032,
    99260,
    101896,
    106105,
    108143,
    108170,
    110191,
    111235,
    111688,
    112548,
    114994,
    116164,
    116183,
    116595,
    117394,
    117454,
    117484
]

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
    "summonsLeft": [],
    "maxSummons": [],
    "rarity" : [],
    "mainClass": [],
    "subClass": [],
    "profession": [],
    "profStat1": [],
    "profStat2": [],
    "stat1val": [],
    "stat2val": [],
    "totalProfStats": [],
    "level": []
}

for hero in user_heroes:
    raw_details = hero_core.get_hero(hero, rpc_address)
    details = functions.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
    data["heroId"] += [details["id"]]
    data["generation"] += [details["info"]["generation"]]

    maxSummons = details["summoningInfo"]["maxSummons"]
    data["summonsLeft"] += [maxSummons - details["summoningInfo"]["summons"]]
    data["maxSummons"] += [maxSummons]

    data["rarity"] += [details["info"]["rarity"]]
    data["mainClass"] += [details["info"]["statGenes"]["class"]]
    data["subClass"] += [details["info"]["statGenes"]["subClass"]]

    profession = details["info"]["statGenes"]["profession"]
    # print(profession)
    data["profession"] += [profession]

    # data["statBoost1"] += [short_stat[details["info"]["statGenes"]["statBoost1"]]]
    # data["statBoost2"] += [short_stat[details["info"]["statGenes"]["statBoost2"]]]

    prof_stats = ideal_professsion_stats[profession]
    data["profStat1"] += [short_stat[prof_stats[0]]]
    data["profStat2"] += [short_stat[prof_stats[1]]]

    profStat1_val = details["stats"][prof_stats[0]]
    profStat2_val = details["stats"][prof_stats[1]]
    data["stat1val"] += [profStat1_val]
    data["stat2val"] += [profStat2_val]
    data["totalProfStats"] += [profStat1_val + profStat2_val]

    data["level"] += [details["state"]["level"]]

    # print(details)

# print(data)
df = pd.DataFrame(data=data)
df.to_csv(f'./csv/hero_tracking.csv')

print("completed!")