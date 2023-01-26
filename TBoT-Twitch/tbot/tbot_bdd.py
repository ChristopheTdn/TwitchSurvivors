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
        with open ('./TBOT-Twitch/tbot/config/config_raid.json', 'r',encoding="utf-8" ) as fichier:
            self.config_raid_json = json.load(fichier)
    
    def initTableSql(self):
        """
                Initialise la base de donnée si elle n'existe pas
        """
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        curseur = self.connexionSQL.cursor()
        curseur.execute('''CREATE TABLE IF NOT EXISTS survivant(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            profession TEXT,
            reputation INTEGER,
            level_arme INTEGER,
            level_outil INTEGER,
            level_medical INTEGER,
            level_nourriture INTEGER,
            level_automobile INTEGER,
            level_alcool INTEGER,
            level_agriculture INTEGER,            
            level_meuble INTEGER)''')
        
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
                            profession,
                            reputation,
                            level_arme,
                            level_outil,
                            level_medical,
                            level_nourriture,
                            level_automobile,
                            level_alcool,
                            level_agriculture,            
                            level_meuble)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (pseudo ,"",0,1,1,1,1,1,1,1,1)) 
        await db.commit()
        await db.close()
    
    async def get_stats_survivant(self,name: str)->dict:
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                            profession,
                            reputation,
                            level_arme,
                            level_outil,
                            level_medical,
                            level_nourriture,
                            level_automobile,
                            level_alcool,
                            level_agriculture,            
                            level_meuble FROM 'survivant' WHERE name='{name}' ''') as cur:
            listeStat = await cur.fetchone()
        await db.close()
        reponse ={"name": listeStat[0],
                "profession" : listeStat[1],
                "reputation": listeStat[2],
                "level_arme":listeStat[3],
                "level_outil":listeStat[4],
                "level_medical":listeStat[5],
                "level_nourriture":listeStat[6],
                "level_automobile":listeStat[7],
                "level_alcool":listeStat[8],
                "level_agriculture":listeStat[9],            
                "level_meuble":listeStat[10]
                }
        return reponse
    
    async def survivant_exist(self,name):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                            profession,
                            reputation,
                            level_arme,
                            level_outil,
                            level_medical,
                            level_nourriture,
                            level_automobile,
                            level_alcool,
                            level_agriculture,            
                            level_meuble FROM 'survivant' WHERE name='{name}' ''') as cur:
            reponse = await cur.fetchone()
        await db.close()
        return reponse
    
    async def raid_exist(self,name: str):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f"SELECT name FROM 'raid' WHERE name='{name}'") as cur :
            reponse = await cur.fetchone()
        await db.close()
        return reponse
    
    async def create_raid(self,name: str,type_raid: str,level: int):
        # determine si le RAID sera un succes
        
        distance_raid = self.config_raid_json["raid_"+type_raid]["distance_raid"]
        BUTIN = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-{level}"]["BUTIN"]
        BREDOUILLE = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-{level}"]["BREDOUILLE"]
        BLESSE = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-{level}"]["BLESSE"]
        MORT = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-{level}"]["MORT"]

        michemin = distance_raid//2
        
        #determine le resultat du raid
        resultRAID = random.randrange(100) # un nombre entre 0 et 99

        if resultRAID < MORT : # Mort sans appel
            resultat = "MORT"
            blesse = random.randrange(distance_raid-50,distance_raid-10)
            if blesse == michemin :
                blesse +=2
            fin = random.randrange(4,blesse-2)
            
        elif resultRAID < MORT+BLESSE :
            resultat = 'BLESSE' 
            blesse = random.randrange(distance_raid-50,distance_raid-10)
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
            type_raid = raid[1]
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
            data[f"SURVIVANT_{name}"]={"NAME":f"{name}","STATS":f"{stat_survivant}","TYPE":f"{type_raid}","DISTANCE":distancepourcent,"RENFORT":f"{renfort}"}
            await db.execute(f'''UPDATE raid SET distance = {distance} WHERE name = "{name}"''') 
            
            if distance == michemin :
                await tbot_com.message(channel,overlay=f"<span class='pseudo'>{name}</span> commence à faire demi-tour.",
                                       mod=f"'<radio {name}> allo... ..ai atteint mon object... je ...revie... a la base..",
                                       chat=f"{name} retourne à la base",son="radio5.mp3")

            elif distance == blesse : 
                await tbot_com.message(channel,overlay=f"<span class='pseudo'>{name}</span> a été attaqué durant son raid. Il est bléssé ! ", mod=f"'<radio {name}> Aidez moi! victim...zzz.. ne attaque... je suis ...gèrement bléssé... zzz..z...",chat=f"{name} a été bléssé sur une attaque !",son="radio5.mp3")

            elif distance == fin :
                print (f"Le raid se termine avec pour resultat : {resultat}")
                if fin>1 : #le joueur est mort
                    await tbot_com.message(channel,overlay=f"<span class='pseudo'>{name}</span> a succombé durant son raid ! Il a tout perdu !",
                                           mod=f"'<radio {name}> Arggg...partout. arghh... u secours... zzz..z...",
                                           chat=f"{name} a succombé durant son raid ! Il est mort !",
                                           son="radio2.mp3")
                    await db.execute(f'''DELETE from raid WHERE name = "{name}"''')
                    await db.execute(f'''DELETE from survivant WHERE name = "{name}"''')

                if distance <= 0 : #le joueur est revenu a la base

                    await self.gere_fin_raid(db,name,type_raid,channel)
                    await db.execute(f'''DELETE from raid WHERE name = "{name}"''')
                    

        await db.commit()
        await db.close()
            
        async with aiofiles.open("raid.json", "w",encoding="utf-8") as fichier:
            await fichier.write(json.dumps(data,indent=4,ensure_ascii=False))
        
    async def gere_fin_raid(self,db,name,type_raid,channel):
        
        gain_reputation = self.config_raid_json["raid_"+type_raid]["gain_reputation"]
        
        await tbot_com.message(channel,overlay=f"<span class='pseudo'>{name}</span> est revenu à la base. gain de reputation : +{gain_reputation} !!!",
                        mod=f"'<radio {name}> je suis ...nfin reven... à la base...",
                        chat=f"{name} est revenu à la base. gain de reputation : +{gain_reputation} !!!!!!!",
                        son="radio3.mp3")
        await db.execute(f'''UPDATE survivant SET reputation = reputation +{gain_reputation} WHERE name = "{name}"''')


        
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
