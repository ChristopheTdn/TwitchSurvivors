import sqlite3
import os
import aiosqlite
import json
import aiofiles
import random
from . import tbot_com  

class TBOT_BDD():
        
    """Gestion de la base de donnée du TBOT
    """        
    def __init__(self,TBOTPATH) -> None:
        self.TBOTPATH=TBOTPATH
        self.NAMEBDD = "tbot_bdd.sqlite"
    
    def initTableSql(self):
        """
                Initialise la base de donnée si elle n'existe pas
        """
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        curseur = self.connexionSQL.cursor()
        curseur.execute('''CREATE TABLE IF NOT EXISTS survivant(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            reputation INTEGER,
            levelGun INTEGER,
            levelWear INTEGER,
            levelCar INTEGER)''')
        
        curseur.execute('''CREATE TABLE IF NOT EXISTS raid(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            type TEXT,
            distance INTEGER,
            michemin INTEGER,
            renfort TEXT,
            resultat TEXT,
            blesse INTEGER,
            fin INTEGER 
            )''')
        self.connexionSQL.commit()
        self.connexionSQL.close()
        
    async def create_survivant(self,pseudo):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute('''INSERT OR IGNORE INTO survivant
                            (name,
                            reputation,
                            levelGun,
                            levelWear,
                            levelCar)
                            VALUES (?,?,?,?,?)''', (pseudo , 0,0,0,0)) 
        await db.commit()
        await db.close()
    
    async def get_stats_survivant(self,name: str)->dict:
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar FROM 'survivant' WHERE name='{name}' ''') as cur:
            listeStat = await cur.fetchone()
        await db.close()
        reponse ={"name": listeStat[0],
                "reputation": listeStat[1],
                "levelGun": listeStat[2],
                "levelWear": listeStat[3],
                "levelCar": listeStat[4]
                }
        return reponse
    
    async def survivant_exist(self,name):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f"SELECT name FROM 'survivant' WHERE name='{name}'") as cur:
            reponse = await cur.fetchone()
        await db.close()
        return reponse
    
    async def raid_exist(self,name: str):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f"SELECT name FROM 'raid' WHERE name='{name}'") as cur :
            reponse = await cur.fetchone()
        await db.close()
        return reponse
    
    async def create_raid(self,name: str,type_raid: str):
        # determine si le RAID sera un succes
        with open('./TBOT-Twitch/tbot/config/config_raid.json', 'r',encoding="utf-8" ) as fichier:
                data = json.load(fichier)
        distance_raid = data["raid_"+type_raid]["stats_raid"]["distance_raid"]
        MORT = data["raid_"+type_raid]["stats_raid"]["MORT"]
        BLESSE = data["raid_"+type_raid]["stats_raid"]["BLESSE"]
        BREDOUILLE = data["raid_"+type_raid]["stats_raid"]["BREDOUILLE"]
        BUTIN = data["raid_"+type_raid]["stats_raid"]["BUTIN"]
        

        michemin = distance_raid//2
        
        #determine le resultat du raid
        resultRAID = random.randrange(100) # un nombre entre 0 et 99

        if resultRAID < MORT : # Mort sans appel
            resultat = "MORT"
            blesse = random.randrange(distance_raid-60,distance_raid-10)
            if blesse == michemin :
                blesse +=2
            fin = random.randrange(4,blesse-2)
            
        elif resultRAID < MORT+BLESSE :
            resultat = 'BLESSE' 
            blesse = random.randrange(distance_raid-60,distance_raid-10)
            if blesse == michemin :
                blesse +=2
            fin = 0
        elif resultRAID < MORT+BLESSE+BREDOUILLE:
            resultat = 'BREDOUILLE'
            blesse=-1
            fin = 0 
        else :
            resultat = 'BUTIN' 
            blesse=-1
            fin = 0     
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute ('''INSERT OR IGNORE INTO raid
                        (name,
                        type,
                        distance,
                        michemin,
                        renfort,
                        resultat,
                        blesse,
                        fin)
                        VALUES (?,?,?,?,?,?,?,?)''', (name,type_raid,distance_raid,distance_raid//2,'{}',resultat,blesse,fin))
        await db.commit()
        await db.close()
    
    async def actualise_statRaid(self,channel):
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                        type,
                        distance,
                        michemin,
                        renfort,
                        resultat,
                        blesse,
                        fin FROM 'raid' ''') as cur:
            listeRaid = await cur.fetchall()
        await db.close()  

        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        data={}
        for raid in listeRaid:
            name = raid[0]
            type = raid[1]
            distance = raid[2]
            michemin = raid[3]
            distance_total = michemin*2
            renfort = raid[4]
            resultat = raid[5]
            blesse = raid[6]
            fin = raid[7]
            
            distance -=1
            distancepourcent = (distance*100)//(distance_total)

            stat_survivant= await self.get_stats_survivant(name)
            data[f"SURVIVANT_{name}"]={"NAME":f"{name}","STATS":stat_survivant,"TYPE":f"{type}","DISTANCE":distancepourcent,"RENFORT":f"{renfort}"}
            await db.execute(f'''UPDATE raid SET distance = {distance} WHERE name = "{name}"''') 
            
            if distance == michemin :
                await tbot_com.message(channel,overlay=f"{name} commence à faire demi-tour.", mod=f"'<radio {name}> allo... ..ai atteint mon object... je ...revie... a la base..",chat=f"{name} retourne à la base",son="radio5.mp3")

            elif distance == blesse : 
                await tbot_com.message(channel,overlay=f"{name} a été attaqué durant son raid. Il est bléssé ! ", mod=f"'<radio {name}> Aidez moi! victim...zzz.. ne attaque... je suis ...gèrement bléssé... zzz..z...",chat=f"{name} a été bléssé sur une attaque !",son="radio5.mp3")

            elif distance == fin :
                print (f"Le raid se termine avec pour resultat : {resultat}")
                if fin>1 : #le joueur est mort
                    await tbot_com.message(channel,overlay=f"{name} a succombé durant son raid ! Il a tout perdu !",
                                           mod=f"'<radio {name}> Arggg...partout. arghh... u secours... zzz..z...",
                                           chat=f"{name} a succombé durant son raid ! Il est mort !",
                                           son="radio4.mp3")
                    await db.execute(f'''DELETE from raid WHERE name = "{name}"''')
                    await db.execute(f'''DELETE from survivant WHERE name = "{name}"''')

                if distance <= 0 : #le joueur est revenu a la base
                    await tbot_com.message(channel,overlay=f"{name} est revenu à la base, le RAID est terminé !!!!",
                                           mod=f"'<radio {name}> je suis ...nfin reven... à la base...",
                                           chat=f"{name} est revenu à la base, le RAID est terminé !!!!",
                                           son="radio4.mp3")
                    await db.execute(f'''DELETE from raid WHERE name = "{name}"''')


        await db.commit()
        await db.close()
        
        async with aiofiles.open("raid.json", "w",encoding="utf-8") as fichier:
            await fichier.write(json.dumps(data))
        
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')