import functions
import pandas as pd

user_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"
rpc_address = "https://api.harmony.one"

heroId_1 = 117128
heroId_2 = 81764

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

raw_details1 = functions.get_hero(heroId_1, rpc_address)
details1 = functions.human_readable_hero(raw_details1, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
print(details1)
