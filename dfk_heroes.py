import hero_core
import pandas as pd

import hero_core
import auction_core
import pandas as pd
from dfk_contracts import serendale_contracts

auction_address = "0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892"
rpc_address = "https://api.harmony.one"

user_addresses = [
    "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F",   #Pete
    "0xc4b35c78e83b598cf8e60f87e380731457eb824f"    #Pon

]

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

print(user_heroes)
print(len(user_heroes))

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
    details = hero_core.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
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