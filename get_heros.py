import hero_core
import auction_core
import pandas as pd
from dfk_contracts import serendale_contracts

user_address = "0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F"
rpc_address = "https://api.harmony.one"

user_heroes = hero_core.get_users_heroes(user_address, rpc_address)
print(user_heroes)
print(len(user_heroes))

sorted_user_heroes = sorted(user_heroes)
print(sorted_user_heroes)

auction_address = "0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892"

user_auctions = auction_core.get_user_auctions(auction_address, user_address, rpc_address)
print(user_auctions)

# raw_details = functions.get_hero(user_heroes[0], rpc_address)
# details = functions.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)
# print(details)