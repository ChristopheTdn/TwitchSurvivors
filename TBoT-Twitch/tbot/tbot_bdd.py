import sqlite3
import os
import aiosqlite
import json
import aiofiles

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
        curseur.execute('''CREATE TABLE IF NOT EXISTS player(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            health INTEGER,
            reputation INTEGER,
            levelGun INTEGER,
            levelWear INTEGER,
            levelCar INTEGER,
            stock INTEGER)''')
        
        curseur.execute('''CREATE TABLE IF NOT EXISTS raid(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            type TEXT,
            timing INTEGER,
            retour INTEGER,
            renfort TEXT 
            )''')
        self.connexionSQL.commit()
        self.connexionSQL.close()
        
    async def create_survivant(self,pseudo):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute('''INSERT OR IGNORE INTO player
                            (name,
                            health,
                            reputation,
                            levelGun,
                            levelWear,
                            levelCar,
                            stock)
                            VALUES (?,?,?,?,?,?,?)''', (pseudo , 100,0,0,0,0,0)) 
        await db.commit()
        await db.close()
    
    async def get_stats_survivant(self,name: str)->dict:
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock FROM 'player' WHERE name='{name}' ''') as cur:
            listeStat = await cur.fetchone()
        await db.close()
        reponse ={"name": listeStat[0],
                "health": listeStat[1],
                "reputation": listeStat[2],
                "levelGun": listeStat[3],
                "levelWear": listeStat[4],
                "levelCar": listeStat[5],
                "stock": listeStat[6]
                }
        return reponse
    
    async def survivant_exist(self,name):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f"SELECT name FROM 'player' WHERE name='{name}'") as cur:
            reponse = await cur.fetchone()
        await db.close()
        return reponse
    
    async def raid_exist(self,name: str):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f"SELECT name FROM 'raid' WHERE name='{name}'") as cur :
            reponse = await cur.fetchone()
        await db.close()
        return reponse
    
    async def create_raid(self,name: str,type: str,timing: int):
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute ('''INSERT OR IGNORE INTO raid
                        (name,
                        type,
                        timing,
                        retour,
                        renfort)
                        VALUES (?,?,?,?,?)''', (name,type,timing,timing/2,""))
        await db.commit()
        await db.close()
    
    async def genere_StatRaid(self):
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                        type,
                        timing,
                        retour,
                        renfort FROM 'raid' ''') as cur:
            listeRaid = await cur.fetchall()
        await db.close()
        
        NumSurvivant = 1
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        data={}
        for raid in listeRaid:
            data[f"SURVIVANT_{NumSurvivant}"]={"NAME":f"{raid[0]}","TYPE":raid[1],"DISTANCE":((raid[2]*100)//(raid[3]*2)),"RENFORT":f"{str(raid[4])}"}
            await db.execute(f'''UPDATE raid SET timing = {str(raid[2]-1)} WHERE name = "{raid[0]}"''')
            NumSurvivant+=1
        await db.commit()
        await db.close()
        
        async with aiofiles.open("raid.json", "w") as fichier:
            await fichier.write(json.dumps(data))
        
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')