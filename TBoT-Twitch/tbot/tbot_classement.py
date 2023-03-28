'''
Module de gestion du classement des survivants
'''
import sqlite3
import os
import aiosqlite
import json
import aiofiles
import random
from . import tbot_com  


with open('./Configuration/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)


with open('./Configuration/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)

async def Add_Classement(TBOTBDD,id_twitch: int):
    survivant = TBOTBDD.get_stats_survivant(id_twitch)
    score =  survivant["prestige"]
    cout_prestige = CONFIG["TARIF_UPGRADE"] 
    score += cout_prestige[survivant['level_weapon']-1]
    score += cout_prestige[survivant['level_armor']-1]
    score += cout_prestige[survivant['level_transport']-1]
    score += cout_prestige[survivant['level_gear']-1]
    db = await aiosqlite.connect(os.path.join("./Sqlite", TBOTBDD.NAMEBDD))
    async with db.execute (f'''SELECT * FROM 'survivant' ''') as cur:
        listeRaid = await cur.fetchall()
        await db.close() 
    
    for i in listeRaid:
        print (i)