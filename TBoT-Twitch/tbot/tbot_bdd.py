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
        with open ('./TBOT-Twitch/tbot/data/config_raid.json', 'r',encoding="utf-8" ) as fichier:
            self.config_raid_json = json.load(fichier)
        with open ('./TBOT-Twitch/tbot/data/config_butin.json', 'r',encoding="utf-8" ) as fichier:
            self.config_butin_json = json.load(fichier)
        with open ('./TBOT-Twitch/tbot/data/config_ratio_butin.json', 'r',encoding="utf-8" ) as fichier:
            self.config_ratio_json = json.load(fichier)   

    def initTableSql(self):
        """
                Initialise la base de donnée si elle n'existe pas
        """
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        curseur = self.connexionSQL.cursor()
        curseur.execute('''CREATE TABLE IF NOT EXISTS survivant(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            name_lower TEXT UNIQUE,
            career TEXT,
            prestige INTEGER,
            credit INTEGER,
            level_weapon INTEGER,
            level_armor INTEGER,
            level_transport INTEGER,
            level_gear INTEGER,
            alive BOOLEAN,
            support_raid BOOLEAN
            )''')
        
        curseur.execute('''CREATE TABLE IF NOT EXISTS raid(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            name_lower TEXT UNIQUE,
            type TEXT,
            distance INTEGER,
            michemin INTEGER,
            renfort TEXT,
            resultat TEXT,
            blesse INTEGER,
            mort INTEGER,
            composition_butin TEXT,
            bonus_butin INTEGER,
            gfx_car TEXT,
            visi BOOLEAN,
            time_visi INTEGER,
            time_renfort INTEGER
            )''')
        self.connexionSQL.commit()
        self.connexionSQL.close()
        
    async def create_survivant(self,name: str):
        """ajoute le survivant à la base de donnée statut alive a False
        Args:
            name (str): le nom du survivant.
        """        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute('''INSERT OR IGNORE INTO survivant
                            (name,
                            name_lower,
                            career,
                            prestige,
                            credit,
                            level_weapon,
                            level_armor,
                            level_transport,
                            level_gear,
                            alive,
                            support_raid
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (name ,name.lower(),"",0,0,1,1,1,1,False,False)) 
        await db.commit()
        await db.close()
        
    async def revive_survivant(self,name: str):
        """fait revivre le survivant à la base de donnée statut alive a True

        Args:
            name (str): le nom du survivant.
        """        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET 
                        career          = "",
                        prestige        = 0,
                        level_weapon    = 1,
                        level_armor     = 1,
                        level_transport = 1,
                        level_gear      = 1,
                        alive           = True, 
                        support_raid    = False                  
                        WHERE name_lower = "{name.lower()}"''')
        await db.commit()
        await db.close()
        
    async def get_stats_survivant(self,name: str)->dict:
        """Récupère les stats du survivant
        Args:
            name (str): nom du survivant.
        Returns:
            dict: renvois un dictionnaire contenant les statistiques du survivant.
        """        
        reponse = {}
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                            name_lower,
                            career,
                            prestige,
                            credit,
                            level_weapon,
                            level_armor,
                            level_transport,
                            level_gear,
                            alive,
                            support_raid FROM 'survivant' WHERE name='{name}' ''') as cur:
            listeStat = await cur.fetchone()
        await db.close()
        if listeStat==None:
            return None
        else:                
            reponse ={"name": listeStat[0],
                    "name_lower": listeStat[1],
                    "career" : listeStat[2],
                    "prestige": listeStat[3],
                    "credit" : listeStat[4],
                    "level_weapon":listeStat[5],
                    "level_armor":listeStat[6],
                    "level_transport":listeStat[7],
                    "level_gear":listeStat[8],
                    "alive":bool(listeStat[9]),
                    "support_raid":bool(listeStat[10])
                    }
            return reponse
    
    
    async def stat_raid(self,name: str):
        """renvois un dictionnaire du raid effectué par le survivant passé en paramètre si il existe. 
        Args:
            name (str): le nom du survivant

        Returns:
            dict : renvois un dictionnaire contenant les statistiques du raid en cours si il existe sinon none.

        """        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                        name_lower,
                        type,
                        distance,
                        michemin,
                        renfort,
                        resultat,
                        blesse,
                        mort,
                        composition_butin,
                        bonus_butin,
                        gfx_car,
                        visi,
                        time_visi,
                        time_renfort
                        FROM 'raid'  WHERE name_lower='{name.lower()}' ''') as cur :
            survivant = await cur.fetchone()
        await db.close()
        if survivant != None :
            survivant_dict = {
                "name"              : survivant[0],
                "name_lower"        : survivant[1],
                "type"              : survivant[2],
                "distance"          : survivant[3],
                "michemin"          : survivant[4],
                "renfort"           : survivant[5],
                "resultat"          : survivant[6],
                "blesse"            : survivant[7],
                "mort"              : survivant[8],
                "composition_butin" : survivant[9],
                "bonus_butin"       : survivant[10],
                "gfx_car"           : survivant[11],
                "visi"              : survivant[12],
                "time_visi"         : survivant[13],
                "time_renfort"      : survivant[14]
                }
        else :
            survivant_dict = None
        return survivant_dict

        

    async def calcul_ratio_raid(self,name: str,BUTIN: int,BREDOUILLE: int,BLESSE: int,MORT: int,DISTANCE: int) -> tuple:
        """Calcul du ratio reussite du RAID en fonction du type de raid et des attributs du survivant

        Args:
            name (str): pseudo du survivant
            BUTIN (int): pourcentage de reussite du raid en BUTIN
            BREDOUILLE (int): pourcentage de reussite du raid en BREDOUILLE
            BLESSE (int): pourcentage de reussite du raid en BLESSE
            MORT (int): pourcentage de reussite du raid en MORT
            DISTANCE (int): Distancedu Raid

        Returns:
            tuple: ensemble des valeurs definissant le RAID influencées par les stats du survivants
            -> BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE
        """        
        survivant_stat= await self.get_stats_survivant(name)
        career = survivant_stat["career"]
        credit = survivant_stat["credit"]
        level_weapon = survivant_stat["level_weapon"]
        level_armor=survivant_stat["level_armor"]
        level_transport=survivant_stat["level_transport"]
        level_gear=survivant_stat["level_gear"]
        
        if level_weapon>1:
            BUTIN=BUTIN+(5*level_weapon)-5 
            BLESSE=BLESSE-(5*level_weapon)+5 
            if BLESSE<5:
                delta = abs(BLESSE-5) 
                BLESSE = 5
                BUTIN -= delta

        if level_armor>1:
            BREDOUILLE=BREDOUILLE+(5*level_armor)-5
            MORT=MORT-(5*level_armor)+5
            if MORT<5:
                delta = abs(MORT-5) 
                MORT = 5
                BREDOUILLE-= delta 

        if level_transport>1:
            DISTANCE = DISTANCE - (15*level_transport)+15
        
        await tbot_com.ecrit_log(f"Name>{name} : Butin={BUTIN}%, Bredouille={BREDOUILLE}%, Blesse={BLESSE}%,Mort={MORT}%, Distance={DISTANCE}.")

        return (BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE) 
    
        
    async def genere_raid(self,name: str,type_raid: str,cout_raid: int,level_transport: int) -> None:

        """Genere les Stats du RAID et son resultat

        Args:
            name (str): nom du survivant
            type_raid (str): type du raid
            cout_raid (int): prix en credit du raid

        """        
        
        # determine si le RAID sera un succes
        
        DISTANCE = self.config_raid_json["raid_"+type_raid]["distance_raid"]
        BUTIN = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-1"]["BUTIN"]
        BREDOUILLE = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-1"]["BREDOUILLE"]
        BLESSE = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-1"]["BLESSE"]
        MORT = self.config_raid_json["raid_"+type_raid]["stats_raid"][f"niveau-1"]["MORT"]
        

        BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE = await self.calcul_ratio_raid(name,BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE)
        composition_butin={}
        bonus_butin=0
        gfx_car = f"{level_transport}-{(random.randrange(4)+1)}.png"

        #determine le resultat du raid
        resultRAID = random.randrange(100) # un nombre entre 0 et 99

        if resultRAID < MORT : # Mort sans appel
            resultat = "MORT"
            blesse = random.randrange(DISTANCE-50,DISTANCE-10)
            if blesse == DISTANCE//2 :
                blesse +=2
            fin = random.randrange(2,blesse-2)
            
        elif resultRAID < MORT+BLESSE :
            resultat = 'BLESSE' 
            blesse = random.randrange(DISTANCE-50,DISTANCE-10)
            if blesse == DISTANCE//2 :
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
            (composition_butin,bonus_butin) = await self.genere_butin(name,type_raid)     
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute ('''INSERT OR IGNORE INTO raid
                        (name,
                        name_lower,
                        type,
                        distance,
                        michemin,
                        renfort,
                        resultat,
                        blesse,
                        mort,
                        composition_butin,
                        bonus_butin,
                        gfx_car,
                        visi,
                        time_visi,
                        time_renfort
                        )
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (name,name.lower(),type_raid,DISTANCE,DISTANCE//2,[],resultat,blesse,fin,json.dumps(composition_butin),bonus_butin,gfx_car,False,0,0))
                        
        await db.execute(f'''UPDATE survivant SET credit = credit - {cout_raid} WHERE name_lower = "{name.lower()}"''')
        await db.commit()
        await db.close()
        
    async def add_credit(self,name,credit):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET credit = credit+{credit} WHERE name_lower = "{name.lower()}"''')

        await db.commit()
        await db.close()
        
    async def genere_butin(self,name: str,type_raid:str)->tuple:
        """Determine le Butin en fonction du level et du type de Raid

        Args:
            name (str): pseudo du survivant
            type_raid (str): type de raid

        Returns:
            tuple : (dict > dict avec nom et class du loot, int -> bonus_butin).
        """        
        survivant = await self.get_stats_survivant(name)
        level_gear = survivant["level_gear"]
        level_weapon=survivant["level_weapon"]
        butin_final={}
        bonus_butin=0
        
        for i in range(level_gear): # Autant de tour que le niveau d'equipement
            hasard=random.randrange(100)
            object_tier1=self.config_ratio_json[f"objet_{i+1}"][f"armement_{level_weapon}"]["tier_1"]
            object_tier2=self.config_ratio_json[f"objet_{i+1}"][f"armement_{level_weapon}"]["tier_2"]
            object_tier3=self.config_ratio_json[f"objet_{i+1}"][f"armement_{level_weapon}"]["tier_3"]
            if hasard<object_tier3: #Donne un objet de Tier3
                loot = self.config_butin_json[type_raid]["tier_3"]
                choix_loot = random.choice(tuple(loot.keys()))
                butin_final[choix_loot]=self.config_butin_json[type_raid][f"tier_3"][choix_loot]
                bonus_butin+=200
            elif hasard<object_tier2+object_tier3 :
                #Donne un objet de Tier2
                loot = self.config_butin_json[type_raid]["tier_2"]
                choix_loot = random.choice(tuple(loot.keys()))
                butin_final[choix_loot]=self.config_butin_json[type_raid][f"tier_2"][choix_loot]
                bonus_butin+=100
            else: #Donne un objet de Tier1
                loot = self.config_butin_json[type_raid]["tier_1"]
                choix_loot = random.choice(tuple(loot.keys()))
                butin_final[choix_loot]=self.config_butin_json[type_raid][f"tier_1"][choix_loot]
                bonus_butin+=50
                    
            if random.randrange(100)>50 : #test si on arrete le tour (50 % de chance que oui)
                break
            
        return (butin_final,bonus_butin)
    
    
        
    async def actualise_statRaid(self,channel):
        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        async with db.execute (f'''SELECT name,
                        name_lower,
                        type,
                        distance,
                        michemin,
                        renfort,
                        resultat,
                        blesse,
                        mort,
                        composition_butin,
                        bonus_butin,
                        gfx_car,
                        visi,
                        time_visi,
                        time_renfort
                        FROM 'raid' ''') as cur:
            listeRaid = await cur.fetchall()
        await db.close()  

        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        data={}
        for raid in listeRaid:
            name = raid[0]
            name_lower = raid[1]
            type_raid = raid[2]
            distance = raid[3]
            michemin = raid[4]
            distance_total = michemin*2
            renfort = raid[5]
            resultat = raid[6]
            blesse = raid[7]
            mort = raid[8]
            composition_butin = raid[9]
            bonus_butin = raid[10]
            gfx_car=raid[11]
            visi = bool(raid[12])
            time_visi = raid[13]
            time_renfort = raid[14]

                
            distance -=1
            distancepourcent = (distance*100)//(distance_total)
            stat_survivant= await self.get_stats_survivant(name)
            
            await db.execute(f'''UPDATE raid SET distance = {distance},time_renfort = time_renfort+1 WHERE name_lower = "{name_lower}"''')
            
            if time_visi > 0 :
                await db.execute(f'''UPDATE raid SET time_visi = time_visi - 1 WHERE name_lower = "{name_lower}"''')
            if time_visi == 0 and visi == True :    
                await db.execute(f'''UPDATE raid SET visi = False WHERE name_lower = "{name_lower}"''')
            
            if len(listeRaid)<5 : #affiche toujours les infos raid si moinds de 5 raids en simultané
                visi = True
                
            data[f"SURVIVANT_{name}"]={"NAME":name,
                                       "STATS": stat_survivant,
                                        "TYPE":type_raid,
                                        "DISTANCE":distancepourcent,
                                        "RENFORT":renfort,
                                        "DEAD":(distance<=mort),
                                        "HURT":(distance<=blesse),
                                        "GFX_CAR":gfx_car,
                                        "VISI":visi}
                
            if distance == 0:
                if mort >1 :
                    await tbot_com.message("raid_retour_base_mort",channel=channel,name=name)
                    await db.execute(f'''DELETE from raid WHERE name_lower = "{name_lower}"''')
                    await db.execute(f'''UPDATE survivant SET alive = 0 WHERE name_lower = "{name_lower}"''')
                else :
                    await self.gere_fin_raid(db,name,type_raid,resultat,composition_butin,bonus_butin,channel)
                    await db.execute(f'''DELETE from raid WHERE name_lower = "{name_lower}"''')
                    
            elif distance == michemin :
                await tbot_com.message("raid_mi_chemin",channel=channel,name=name)
            elif distance == blesse : 
                await tbot_com.message("raid_blesse",channel=channel,name=name)
            elif distance == mort :
                await tbot_com.message("raid_mort_enroute",channel=channel,name=name)

        await db.commit()
        await db.close()
            
        async with aiofiles.open("TBoT_Overlay/raid.json", "w",encoding="utf-8") as fichier:
            await fichier.write(json.dumps(data,indent=4,ensure_ascii=False))
        
    async def gere_fin_raid(self,db,name,type_raid,resultat,composition_butin,bonus_butin,channel):
        
        gain_prestige = self.config_raid_json["raid_"+type_raid]["gain_prestige"]
        listebutin=""
        if resultat =="BUTIN":
            gain_prestige = gain_prestige*2
            listebutin = "<br>"+await tbot_com.donne_butin(composition_butin) 
            await tbot_com.message("raid_win_butin",channel=channel,name=name,gain_prestige=str(gain_prestige),listebutin=listebutin,bonus_butin=str(bonus_butin))
            await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige+bonus_butin} WHERE name_lower = "{name.lower()}"''')
        if resultat =="BREDOUILLE":
            gain_prestige =gain_prestige*1
            
            await tbot_com.message("raid_win_bredouille",channel=channel,name=name,gain_prestige=str(gain_prestige))
            await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige} WHERE name_lower = "{name.lower()}"''')
        if resultat =="BLESSE": 
            gain_prestige = gain_prestige//2
            await tbot_com.message("raid_win_blesse",channel=channel,name=name,gain_prestige=str(gain_prestige))
            await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige} WHERE name_lower = "{name.lower()}"''')

            
    async def upgrade_aptitude(self,name,aptitude: str,cout_upgrade: int):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET prestige = prestige - {cout_upgrade} WHERE name_lower = "{name.lower()}"''')
        await db.execute(f'''UPDATE survivant SET level_{aptitude} = level_{aptitude} + 1 WHERE name_lower = "{name.lower()}"''') 
        await db.commit()
        await db.close()
        
    async def add_visi(self,name: str, duree: int=5):
        """permet d'afficher pour une certaine durée les infos du raid
        Args:
            name (str): nom du survivant
            duree (int, optional): nombre de cycle d'affichage des infos. Default à 5.
        """        
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute(f'''UPDATE raid SET visi = true , time_visi = {duree} WHERE name_lower = "{name.lower()}"''')
        await db.commit()
        await db.close()
        
    async def join_raid(self,raider,helper,equipe):
        db = await aiosqlite.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        await db.execute(f'''UPDATE raid SET renfort = '{','.join([str(elem) for elem in equipe])}' WHERE name_lower = "{raider.lower()}"''')
        await db.execute(f'''UPDATE raid SET support_raid = True WHERE name_lower = "{helper.lower()}"''') 
        await db.commit()
        await db.close()

if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
