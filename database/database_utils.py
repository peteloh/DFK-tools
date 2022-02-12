from pypika import Query, Table, Field
import sqlite3

DATABASE_FILE = './database/heroes_data.db'

HERO_DETAILS_TABLE_NAME = 'hereos_data'

TABLES_NAMES = [
    HERO_DETAILS_TABLE_NAME,
]

create_hero_auction_success_table_sql = f"""
CREATE TABLE IF NOT EXISTS {HERO_DETAILS_TABLE_NAME} (
    heroId          INTEGER PRIMARY KEY,
    summonerId      INTEGER NOT NULL,
    assistantId     INTEGER NOT NULL,
    Generation      INTEGER NOT NULL,
    Level           INTEGER NOT NULL,
    SumLeft         INTEGER NOT NULL,
    SumMax          INTEGER NOT NULL,
    Rarity          TEXT NOT NULL,
    Class_D0        TEXT NOT NULL,
    Class_R1        TEXT NOT NULL,
    Class_R2        TEXT NOT NULL,
    Class_R3        TEXT NOT NULL,
    SubClass_D0     TEXT NOT NULL,
    SubClass_R1     TEXT NOT NULL,
    SubClass_R2     TEXT NOT NULL,
    SubClass_R3     TEXT NOT NULL,
    Profession_D0   TEXT NOT NULL,
    Profession_R1   TEXT NOT NULL,
    Profession_R2   TEXT NOT NULL,
    Profession_R3   TEXT NOT NULL,
    GreenStat_D0    TEXT NOT NULL,
    GreenStat_R1    TEXT NOT NULL,
    GreenStat_R2    TEXT NOT NULL,
    GreenStat_R3    TEXT NOT NULL,
    BlueStat_D0     TEXT NOT NULL,
    BlueStat_R1     TEXT NOT NULL,
    BlueStat_R2     TEXT NOT NULL,
    BlueStat_R3     TEXT NOT NULL,
);
"""

hero_auction_success_table = Table(HERO_AUCTION_SUCCESS_TABLE_NAME)
insert_auction_success_table = \
    Query.into(hero_auction_success_table).columns(
        'heroId', 
        'summonerId',
        'assistantId',
        'Generation',
        'Level',
        'SumLeft',
        'SumMax',
        'Rarity',
        'Class_D0',
        'Class_R1',
        'Class_R2',
        'Class_R3',
        'SubClass_D0',
        'SubClass_R1',
        'SubClass_R2L',
        'SubClass_R3',
        'Profession_D0',
        'Profession_R1',
        'Profession_R2',
        'Profession_R3',
        'GreenStat_D0',
        'GreenStat_R1',
        'GreenStat_R2',
        'GreenStat_R3',
        'BlueStat_D0',
        'BlueStat_R1',
        'BlueStat_R2',
        'BlueStat_R3'
    )

#Custom Database Utils
def insert_hero_details(details, args):

    maxSummons = details["summoningInfo"]["maxSummons"]
    SumLeft = [maxSummons - details["summoningInfo"]["summons"]]

    db = args['db']
    q = insert_hereos_data_table \
        .insert(
            details["id"],
            details["summoningInfo"]["summonerId"],
            details["summoningInfo"]["summonerId"],
            details["info"]["generation"],
            details["state"]["level"],
            SumLeft,
            maxSummons,
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

# Basic db utils
def connect_db(db_file):
    db = None
    try:
        db = sqlite3.connect(DATABASE_FILE)
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

def delete_record(tb_name, where="", db=None):
    to_close = False
    if db is None:
        db = connect_db(DATABASE_FILE)
        to_close = True
    
    if where != "":
        where = " where " + where
    sql = f"delete from {tb_name}" + where
    result = execute_query(db, sql)

    if to_close:
        db.close()

    return result

def drop_table(tb_name, db=None):
    to_close = False
    if db is None:
        db = connect_db(DATABASE_FILE)
        to_close = True

    sql = f"drop table {tb_name}"
    result = execute_query(db, sql)

    if to_close:
        db.close()

    return result

def select_table(tb_name, where=None, db=None, is_print=False):
    to_close = False
    if db is None:
        db = connect_db(DATABASE_FILE)
        to_close = True

    cur = db.cursor()
    sql =   f"select * from {tb_name}" if where is None else \
            f"select * from {tb_name} where {where};"
    
    result = None
    try:
        result = cur.execute(sql)
    
        if is_print:
            for r in result:
                print(r)
        result = list(result)
    finally:
        if to_close:
            db.close()

    return result

