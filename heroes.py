import time

# database
import sqlite3
from pypika import Query, Table, Field

# custom imports
from core import hero_core, utils

HERO_DATABASE_TABLE_NAME = "heroes"
DATABASE_FILE = "hero_database.db"
RPC_ADDRESS = "https://api.harmony.one"

def connect_db(db_file):
    db = None
    try:
        db = sqlite3.connect(db_file)
    except sqlite3.Error as e:        
        print(e)
    return db

def execute_query(connection, query, print_error=False):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return True
    except sqlite3.Error as e:
        if print_error:
            print(f"The error '{e}' occurred")
        return False

def create_heroes_table():
    db = connect_db(DATABASE_FILE)
    execute_query(db, 
        f"""
        CREATE TABLE IF NOT EXISTS {HERO_DATABASE_TABLE_NAME} (
            heroId          INTEGER PRIMARY KEY,
            summonerId      INTEGER,
            assistantId     INTEGER,
            Generation      INTEGER,
            Rarity          TEXT,
            Class_D0        TEXT,
            Class_R1        TEXT,
            Class_R2        TEXT,
            Class_R3        TEXT,
            SubClass_D0     TEXT,
            SubClass_R1     TEXT,
            SubClass_R2     TEXT,
            SubClass_R3     TEXT,
            Profession_D0   TEXT,
            Profession_R1   TEXT,
            Profession_R2   TEXT,
            Profession_R3   TEXT,
            GreenStat_D0    TEXT,
            GreenStat_R1    TEXT,
            GreenStat_R2    TEXT,
            GreenStat_R3    TEXT,
            BlueStat_D0     TEXT,
            BlueStat_R1     TEXT,
            BlueStat_R2     TEXT,
            BlueStat_R3     TEXT
        );
        """
    )
    db.close()

def insert_hero_details(db, heroId):

    # query_successful = False
    # while query_successful == False:
    try:
        raw_details = hero_core.get_hero(heroId, RPC_ADDRESS)
        query_successful = True
    except: 
        return "NoHero"

    details = hero_core.human_readable_hero(raw_details, hero_male_first_names=None, hero_female_first_names=None, hero_last_names=None)

    q = Query.into(HERO_DATABASE_TABLE_NAME).insert(
            details["id"],
            details["summoningInfo"]["summonerId"],
            details["summoningInfo"]["assistantId"],
            details["info"]["generation"],
            details["info"]["rarity"],
            details["info"]["statGenes"]["class"],
            details["info"]["statGenes"]['r1']["class"],
            details["info"]["statGenes"]['r2']["class"],
            details["info"]["statGenes"]['r3']["class"],
            details["info"]["statGenes"]["subClass"],
            details["info"]["statGenes"]['r1']["subClass"],
            details["info"]["statGenes"]['r2']["subClass"],
            details["info"]["statGenes"]['r3']["subClass"],
            details["info"]["statGenes"]["profession"],
            details["info"]["statGenes"]['r1']["profession"],
            details["info"]["statGenes"]['r2']["profession"],
            details["info"]["statGenes"]['r3']["profession"],
            details["info"]["statGenes"]["statBoost1"],
            details["info"]["statGenes"]['r1']["statBoost1"],
            details["info"]["statGenes"]['r2']["statBoost1"],
            details["info"]["statGenes"]['r3']["statBoost1"],
            details["info"]["statGenes"]["statBoost2"],
            details["info"]["statGenes"]['r1']["statBoost2"],
            details["info"]["statGenes"]['r2']["statBoost2"],
            details["info"]["statGenes"]['r3']["statBoost2"],
        )
    
    result = execute_query(db, q.get_sql())
    return result

def get_hero_details(heroId):

    db = connect_db(DATABASE_FILE)
    cur = db.cursor()
    sql = f"""select * from {HERO_DATABASE_TABLE_NAME} 
                where heroId={heroId}"""
    cur.execute(sql)
    result = cur.fetchall()
    
    if result == []: 
        update_static_database()
        sql = f"""select * from {HERO_DATABASE_TABLE_NAME} 
                where heroId={heroId}"""
        cur.execute(sql)
        result = cur.fetchall()
    
    return tuple_to_hero_details_dict(result)

def update_static_database():
    # this is the database that doesnt care about level, stats etc that can change over time
    print("updating database..")
    db = connect_db(DATABASE_FILE)
    cur = db.cursor()
    sql = f"""select MAX(heroId) from {HERO_DATABASE_TABLE_NAME} """
    result = cur.execute(sql)
    lastUpdatedID = cur.fetchall()[0][0]
    if lastUpdatedID == None: lastUpdatedID = 0

    while result != "NoHero":
        lastUpdatedID += 1
        result = insert_hero_details(db, lastUpdatedID)
        if result != "NoHero": print("hero " + str(lastUpdatedID) + " added")


    print("database updated!")

def tuple_to_hero_details_dict(obj):
    result = {}
    result['heroId'] = obj[0][0]
    result['summonerId'] = obj[0][1]
    result['assistantId'] = obj[0][2]
    result['Generation'] = obj[0][3]
    result['Level'] = obj[0][4]
    result['SumLeft'] = obj[0][5]
    result['SumMax'] = obj[0][6]
    result['Rarity'] = obj[0][7]
    result['Class_D0'] = obj[0][8]
    result['Class_R1'] = obj[0][9]
    result['Class_R2'] = obj[0][10]
    result['Class_R3'] = obj[0][11]
    result['SubClass_D0'] = obj[0][12]
    result['SubClass_R1'] = obj[0][13]
    result['SubClass_R2'] = obj[0][14]
    result['SubClass_R3'] = obj[0][15]
    result['Profession_D0'] = obj[0][16]
    result['Profession_R1'] = obj[0][17]
    result['Profession_R2'] = obj[0][18]
    result['Profession_R3'] = obj[0][19]
    result['GreenStat_D0'] = obj[0][20]
    result['GreenStat_R1'] = obj[0][21]
    result['GreenStat_R2']  = obj[0][22]
    result['GreenStat_R3'] = obj[0][23]
    result['BlueStat_D0'] = obj[0][24]
    result['BlueStat_R1'] = obj[0][25]
    result['BlueStat_R2'] = obj[0][26]
    result['BlueStat_R3'] = obj[0][27]
    return result

if __name__ == '__main__':
    
    create_heroes_table()
    update_static_database()

    # try:
    #     details = hero_core.get_hero(128788, RPC_ADDRESS)
    #     print(details)
    # except:
    #     print("Error")

    









