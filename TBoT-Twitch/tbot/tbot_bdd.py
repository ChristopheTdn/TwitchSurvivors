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
            alerteResultat INTEGER 
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
    
    async def create_raid(self,name: str,type: str,distance: int):
        # determine si le RAID sera un succes
        resultRAID = random.randrange(100) # un nombre entre 0 et 99
        if resultRAID < 5 : # Mort sans appel
            resultat = "ECHOUE AVEC PERTE"
            alerteResultat = random.randrange(distance-60,distance-5) 
        elif resultRAID < 15 :
            resultat = 'ECHOUE SANS PERTE' 
            alerteResultat = 1
        elif resultRAID < 80 :
            resultat = 'SUCCES SANS BUTIN' 
            alerteResultat = 1
        else :
            resultat = 'SUCCES AVEC BUTIN' 
            alerteResultat = 1    
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute ('''INSERT OR IGNORE INTO raid
                        (name,
                        type,
                        distance,
                        michemin,
                        renfort,
                        resultat,
                        alerteResultat)
                        VALUES (?,?,?,?,?,?,?)''', (name,type,distance,distance//2,'{}',resultat,alerteResultat))
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
                        alerteResultat FROM 'raid' ''') as cur:
            listeRaid = await cur.fetchall()
        await db.close()        
        NumSurvivant = 1
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        data={}
        for raid in listeRaid:
            distance = (raid[2]*100)//(raid[3]*2)
            if raid[2] == raid[6] :
                print (f"Le raid se termine avec pour resultat : {raid[5]}")
                await db.execute(f'''UPDATE raid SET distance = {str(raid[2]-1)} WHERE name = "{raid[0]}"''') #Enleve 1 point de distance de RAID
                if raid[6]>1 : #le joueur est mort
                    await tbot_com.message(channel,overlay=f"{raid[0]} a succombé durant son raid ! Il a tout perdu !", mod=f"'<radio {raid[0]}> Arggg...partout. arghh... u secours... zzz..z...",chat=f"{raid[0]} a succombé durant son raid ! Il est mort !",son="radio4.mp3")
                    await db.execute(f'''DELETE from raid WHERE name = "{raid[0]}"''')
                    await db.execute(f'''DELETE from survivant WHERE name = "{raid[0]}"''')
            elif raid[2] <= 0 :
                await tbot_com.message(channel,overlay=f"{raid[0]} est revenu à la base, le RAID est terminé !!!!",mod=f"'<radio {raid[0]}> je suis ...nfin reven... à la base...",chat=f"{raid[0]} est revenu à la base, le RAID est terminé !!!!",son="radio4.mp3")
                await db.execute(f'''DELETE from raid WHERE name = "{raid[0]}"''')
            else:
                if raid[2] == raid[3] :
                    await tbot_com.message(channel,overlay=f"{raid[0]} commence à faire demi-tour.", mod=f"'<radio {raid[0]}> allo... ..ai atteint mon object... je ...revie... a la base..",chat=f"{raid[0]} retourne à la base",son="radio5.mp3")
                stat_survivant= await self.get_stats_survivant(raid[0])
                data[f"SURVIVANT_{raid[0]}"]={"NAME":f"{raid[0]}","STATS":stat_survivant,"TYPE":f"{raid[1]}","DISTANCE":((raid[2]*100)//(raid[3]*2)),"RENFORT":f"{raid[4]}"}
                await db.execute(f'''UPDATE raid SET distance = {str(raid[2]-1)} WHERE name = "{raid[0]}"''') #Enleve 1 point de distance de RAID
            NumSurvivant+=1
        await db.commit()
        await db.close()
        
        async with aiofiles.open("raid.json", "w",encoding="utf-8") as fichier:
            await fichier.write(json.dumps(data))
        
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')