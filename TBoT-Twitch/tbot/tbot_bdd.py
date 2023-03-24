import sqlite3
import os
import aiosqlite
import json
import aiofiles
import random
from . import tbot_com  


with open('./Configuration/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)

class TBOT_BDD():
        
    """Gestion de la base de donnée du TBOT
    """        
    def __init__(self,TBOTPATH) -> None:
        self.TBOTPATH=TBOTPATH
        self.NAMEBDD = "tbot_bdd.sqlite"
        with open ('./Data/raid.json', 'r',encoding="utf-8" ) as fichier:
            self.config_raid_json = json.load(fichier)
        with open ('./Data/butin.json', 'r',encoding="utf-8" ) as fichier:
            self.config_butin_json = json.load(fichier)
        with open ('./Data/butin_ratio.json', 'r',encoding="utf-8" ) as fichier:
            self.config_ratio_json = json.load(fichier)   

    def initTableSql(self):
        """
                Initialise la base de donnée si elle n'existe pas
        """
        self.connexionSQL = sqlite3.connect(os.path.join("./Sqlite", self.NAMEBDD))
        curseur = self.connexionSQL.cursor()
        curseur.execute('''CREATE TABLE IF NOT EXISTS survivant(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_twitch INT UNIQUE,
            name TEXT,
            name_lower TEXT,
            career TEXT,
            prestige INTEGER,
            credit INTEGER,
            level_weapon INTEGER,
            level_armor INTEGER,
            level_transport INTEGER,
            level_gear INTEGER,
            alive BOOLEAN,           
            inraid BOOLEAN,            
            support_raid TEXT 
            )''')
        
        curseur.execute('''CREATE TABLE IF NOT EXISTS raid(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            id_twitch INT UNIQUE,
            name TEXT,
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
            time_renfort INTEGER,
            levelRaid_weapon INTEGER,
            levelRaid_armor INTEGER,
            levelRaid_transport INTEGER,
            levelRaid_gear INTEGER,
            effectif_team INTEGER,
            embuscade TEXT
            )''')
        self.connexionSQL.commit()
        self.connexionSQL.close()
        
    async def create_survivant(self,id_twitch: int,name: str):
        """ajoute le survivant à la base de donnée statut alive a False
        Args:
            name (str): le nom du survivant.
        """        
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute('''INSERT OR IGNORE INTO survivant
                            (id_twitch,    
                            name,
                            name_lower,
                            career,
                            prestige,
                            credit,
                            level_weapon,
                            level_armor,
                            level_transport,
                            level_gear,
                            alive,
                            inraid,
                            support_raid) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (id_twitch,name,name.lower(),"",0,0,1,1,1,1,False,False,"")) 
        await db.commit()
        await db.close()
    
    
    async def revive_survivant(self,id_twitch: int):
        """fait revivre le survivant à la base de donnée statut alive a True
         debite les credits du cout revive

        Args:
            id_twitch (int): id du survivant.
        """

        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET 
                        career          = "",
                        credit          = credit-{CONFIG["COUT_REVIVE"]},
                        level_weapon    = 1,
                        level_armor     = 1,
                        level_transport = 1,
                        level_gear      = 1,
                        alive           = True, 
                        inraid          = False,
                        support_raid    = ""                 
                        WHERE id_twitch = {id_twitch}''')
        if CONFIG["RESET_PRESTIGE_AFTER_DEATH"] :
            await db.execute(f'''UPDATE survivant SET 
                        prestige        = 0                  
                        WHERE id_twitch = {id_twitch}''')
        await db.commit()
        await db.close()
        
    async def get_id_survivant(self, name: str):
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        async with db.execute (f'''SELECT * FROM 'survivant' WHERE name_lower='{name.lower()}' ''') as cur:
            listeStat = await cur.fetchone()
        await db.close()
        if listeStat is not None:
            return listeStat[1]
        else:
            return None
            
    async def get_stats_survivant(self,id_twitch: int)->dict:
        """Récupère les stats du survivant
        Args:
            id_twitch (int): identifiant twitch du survivant
        Returns:
            dict: renvois un dictionnaire contenant les statistiques du survivant.
        """        
        reponse = {}
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        async with db.execute (f'''SELECT 
                            id_twitch,
                            name,
                            name_lower,                            
                            career,
                            prestige,
                            credit,
                            level_weapon,
                            level_armor,
                            level_transport,
                            level_gear,
                            alive,
                            inraid,                            
                            support_raid FROM 'survivant' WHERE id_twitch='{id_twitch}' ''') as cur:
            listeStat = await cur.fetchone()
        await db.close()
        if listeStat==None:
            return None
        else:                
            reponse ={"id_twitch": listeStat[0],
                    "name": listeStat[1], 
                    "name_lower": listeStat[2],                   
                    "career" : listeStat[3],
                    "prestige": listeStat[4],
                    "credit" : listeStat[5],
                    "level_weapon":listeStat[6],
                    "level_armor":listeStat[7],
                    "level_transport":listeStat[8],
                    "level_gear":listeStat[9],
                    "alive":bool(listeStat[10]),
                    "inraid":bool(listeStat[11]),
                    "support_raid":listeStat[12],
                    }
            return reponse
    
    
    async def stat_raid(self,id_twitch: int):
        """renvois un dictionnaire du raid effectué par le survivant passé en paramètre si il existe. 
        Args:
            name (str): le nom du survivant

        Returns:
            dict : renvois un dictionnaire contenant les statistiques du raid en cours si il existe sinon none.

        """        
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        async with db.execute (f'''SELECT * FROM 'raid'  WHERE id_twitch='{id_twitch}' ''') as cur :
            survivant = await cur.fetchone()
        await db.close()
        if survivant != None :
            survivant_dict = {
                "id_twitch"           : survivant[1],
                "name"                : survivant[2],
                "type"                : survivant[3],
                "distance"            : survivant[4],
                "michemin"            : survivant[5],
                "renfort"             : survivant[6],
                "resultat"            : survivant[7],
                "blesse"              : survivant[8],
                "mort"                : survivant[9],
                "composition_butin"   : survivant[10],
                "bonus_butin"         : survivant[11],
                "gfx_car"             : survivant[12],
                "visi"                : survivant[13],
                "time_visi"           : survivant[14],
                "time_renfort"        : survivant[15],
                "levelRaid_weapon"    : survivant[16],
                "levelRaid_armor"     : survivant[17],
                "levelRaid_transport" : survivant[18],
                "levelRaid_gear"      : survivant[19],
                "effectif_team"       : survivant[20],
                "embuscade"           : survivant[21]
                }
        else :
            survivant_dict = None
        return survivant_dict

        

    async def calcul_ratio_raid(self,raid_stat: dict,BUTIN: int,BREDOUILLE: int,BLESSE: int,MORT: int,DISTANCE: int) -> tuple:
        """Calcul du ratio reussite du RAID en fonction du type de raid et des attributs du survivant

        Args:
            raid_stat (dict): les statistiques du raid
            BUTIN (int): pourcentage de reussite du raid en BUTIN
            BREDOUILLE (int): pourcentage de reussite du raid en BREDOUILLE
            BLESSE (int): pourcentage de reussite du raid en BLESSE
            MORT (int): pourcentage de reussite du raid en MORT
            DISTANCE (int): Distancedu Raid

        Returns:
            tuple: ensemble des valeurs definissant le RAID influencées par les stats du survivants
            -> BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE
        """        

        if raid_stat["levelRaid_weapon"]>1:
            BUTIN=BUTIN+(5*raid_stat["levelRaid_weapon"])-5 
            BLESSE=BLESSE-(5*raid_stat["levelRaid_weapon"])+5 
            if BLESSE<5:
                delta = abs(BLESSE-5) 
                BLESSE = 5
                BUTIN -= delta

        if raid_stat["levelRaid_armor"]>1:
            BREDOUILLE=BREDOUILLE+(5*raid_stat["levelRaid_armor"])-5
            MORT=MORT-(5*raid_stat["levelRaid_armor"])+5
            if MORT<5:
                delta = abs(MORT-5) 
                MORT = 5
                BREDOUILLE-= delta 

        if raid_stat["levelRaid_transport"]>1:
            DISTANCE = DISTANCE - (15*raid_stat["levelRaid_transport"])+15
        
        await tbot_com.ecrit_log(f"Name>{raid_stat['name']} : Butin={BUTIN}%, Bredouille={BREDOUILLE}%, Blesse={BLESSE}%,Mort={MORT}%, Distance={DISTANCE}.")

        return (BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE) 
    
    async def raid_initialise(self,survivant_stat: dict,type_raid: str,cout_raid: int) -> None:
        DISTANCE = self.config_raid_json["raid_"+type_raid]["distance_raid"]
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute ('''INSERT OR IGNORE INTO raid
                        (id_twitch,
                        name,
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
                        time_renfort,
                        levelRaid_weapon,
                        levelRaid_armor,
                        levelRaid_transport,
                        levelRaid_gear,
                        effectif_team,
                        embuscade
                        )
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (survivant_stat["id_twitch"],
                         survivant_stat["name"],
                         type_raid,
                         DISTANCE,
                         DISTANCE//2,
                         "",
                         "",
                         0,
                         0,
                         "{}",
                         0,
                         "start.png",
                         False,
                         0,
                         0,
                         survivant_stat["level_weapon"],
                         survivant_stat["level_armor"],
                         survivant_stat["level_transport"],
                         survivant_stat["level_gear"],
                         1,
                         ""                         
                         ))
                        
        await db.execute(f'''UPDATE survivant SET credit = credit - {cout_raid},
                         inraid = 1
                         WHERE id_twitch = {survivant_stat["id_twitch"]}''')
        await db.commit()
        await db.close()
                
    async def raid_generation(self,raid: dict) -> None:

        """Genere les Stats du RAID et son resultat

        Args:
            raid (dict): le dictionnaire contenant les stats du raid

        """        
        
        # determine si le RAID sera un succes
        
        DISTANCE_REF = self.config_raid_json["raid_"+raid["type"]]["distance_raid"]
        BUTIN_REF = self.config_raid_json["raid_"+raid["type"]]["stats_raid"][f"niveau-1"]["BUTIN"]
        BREDOUILLE_REF = self.config_raid_json["raid_"+raid["type"]]["stats_raid"][f"niveau-1"]["BREDOUILLE"]
        BLESSE_REF = self.config_raid_json["raid_"+raid["type"]]["stats_raid"][f"niveau-1"]["BLESSE"]
        MORT_REF = self.config_raid_json["raid_"+raid["type"]]["stats_raid"][f"niveau-1"]["MORT"]
        gfx_car = f'{raid["levelRaid_transport"]}-{(random.randrange(4)+1)}.png'
        embuscade = []
        if CONFIG["ASSISTANT_BOOST"] :
            ASSISTANT_BOOST = raid['effectif_team']
        else :
            ASSISTANT_BOOST = 1
        for tentative_survie in range(ASSISTANT_BOOST): #autant de chance de ne pas mourrir 
            BUTIN,BREDOUILLE,BLESSE,MORT,DISTANCE = await self.calcul_ratio_raid(raid,BUTIN_REF,BREDOUILLE_REF,BLESSE_REF,MORT_REF,DISTANCE_REF)
            composition_butin={}
            bonus_butin=0
            #determine le resultat du raid
            resultRAID = random.randrange(100) # un nombre entre 0 et 99

            if resultRAID < MORT : # Mort sans appel
                resultat = "MORT"
                blesse = random.randrange(DISTANCE-50,DISTANCE-10)
                if blesse == DISTANCE//2 :
                    blesse +=2
                fin = random.randrange(2,blesse-3)

                
            elif resultRAID < MORT+BLESSE :
                resultat = 'BLESSE' 
                blesse = random.randrange(DISTANCE-50,DISTANCE-10)
                if blesse == DISTANCE//2 :
                    blesse +=2
                fin = 0
                break
            elif resultRAID < MORT+BLESSE+BREDOUILLE:
                resultat = 'BREDOUILLE'
                blesse=-1
                fin = 0
                break 
            else :
                resultat = 'BUTIN' 
                blesse=-1
                fin = 0
                (composition_butin,bonus_butin) = await self.genere_butin(raid)     
                break
        if fin>0 :    
            embuscade.append(str(fin+1))
        if blesse>0 :
            embuscade.append(str(blesse+1))
        for i in range(random.randrange(1,3)):
            while "Tant que l on ne trouve pas une bonne distance":
                proposition_ambush = random.randrange(DISTANCE-50,DISTANCE-10)
                if str(proposition_ambush) not in embuscade and\
                   proposition_ambush-1 != blesse and\
                   proposition_ambush-1 != fin and\
                   proposition_ambush-1 > fin :
                    embuscade.append(str(proposition_ambush))
                    break
        
        
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute (f'''UPDATE raid SET
                        distance = {DISTANCE},
                        michemin = {DISTANCE//2},
                        resultat = '{resultat}',
                        blesse = {blesse},
                        mort = {fin},
                        composition_butin = '{json.dumps(composition_butin)}',
                        bonus_butin = {bonus_butin},
                        gfx_car = '{gfx_car}',
                        embuscade = "{",".join(embuscade)}"
                        WHERE id_twitch = {raid["id_twitch"]}''')
        await db.commit()
        await db.close()
        
    async def add_credit(self,id_twitch,credit):
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET credit = credit+{credit} WHERE id_twitch = {id_twitch}''')

        await db.commit()
        await db.close()
        
    async def withdraw_credit(self,id_twitch,credit):
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET credit = credit-{credit} WHERE id_twitch = {id_twitch}''')
        await db.commit()
        await db.close()
            
    async def genere_butin(self,raid: dict)->tuple:
        """Determine le Butin en fonction du level et du type de Raid

        Args:
            raid (dict): les données du raid en cours

        Returns:
            tuple : (dict > dict avec nom et class du loot, int -> bonus_butin).
        """        

        butin_final={}
        bonus_butin=0
        
        for i in range(raid['levelRaid_gear']): # Autant de tour que le niveau d'equipement
            hasard=random.randrange(100)
            object_tier1=self.config_ratio_json[f"objet_{i+1}"][f"armement_{raid['levelRaid_weapon']}"]["tier_1"]
            object_tier2=self.config_ratio_json[f"objet_{i+1}"][f"armement_{raid['levelRaid_weapon']}"]["tier_2"]
            object_tier3=self.config_ratio_json[f"objet_{i+1}"][f"armement_{raid['levelRaid_weapon']}"]["tier_3"]
            if hasard<object_tier3: #Donne un objet de Tier3
                loot = self.config_butin_json[raid['type']]["tier_3"]
                choix_loot = random.choice(tuple(loot.keys()))
                butin_final[choix_loot]=self.config_butin_json[raid['type']][f"tier_3"][choix_loot]
                bonus_butin+=200
            elif hasard<object_tier2+object_tier3 :
                #Donne un objet de Tier2
                loot = self.config_butin_json[raid['type']]["tier_2"]
                choix_loot = random.choice(tuple(loot.keys()))
                butin_final[choix_loot]=self.config_butin_json[raid['type']][f"tier_2"][choix_loot]
                bonus_butin+=100
            else: #Donne un objet de Tier1
                loot = self.config_butin_json[raid['type']]["tier_1"]
                choix_loot = random.choice(tuple(loot.keys()))
                butin_final[choix_loot]=self.config_butin_json[raid['type']][f"tier_1"][choix_loot]
                bonus_butin+=50
                    
            if random.randrange(100)>=CONFIG["GEAR_BOOST"] : #test si on arrete le tour (50 % de chance que oui)
                break    
        return (butin_final,bonus_butin)
    
    
        
    async def actualise_statRaid(self,channel):
        
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        async with db.execute (f'''SELECT * FROM 'raid' ''') as cur:
            listeRaid = await cur.fetchall()
        await db.close()  

        data={}

        for raid_actif in listeRaid:
            raid= await self.stat_raid(raid_actif[1])
            if raid["time_renfort"] == CONFIG["MAX_TIME_RENFORT"]:
                await self.raid_generation(raid)
                raid= await self.stat_raid(raid_actif[1])
                
            if raid["time_renfort"] > CONFIG["MAX_TIME_RENFORT"]:
                DISTANCE_POURCENT =  (raid["distance"]*100)//(raid["michemin"]*2)    
                raid["distance"] -=1
            else :
                #place la voiture au départ pour embarquement
                DISTANCE_POURCENT =  98
                raid["distance"] =  (98 * raid["michemin"]*2)//100

            stat_survivant= await self.get_stats_survivant(raid["id_twitch"])
            
            db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
            
            
            await db.execute(f'''UPDATE raid SET distance = {raid["distance"]},time_renfort = time_renfort+1 WHERE id_twitch = {raid["id_twitch"]}''')
            
            if raid["time_visi"] > 0 :
                await db.execute(f'''UPDATE raid SET time_visi = time_visi - 1 WHERE id_twitch = {raid_actif["id_twitch"]}''')
            if raid["time_visi"] == 0 and raid["visi"] == True :    
                await db.execute(f'''UPDATE raid SET visi = False WHERE id_twitch = {raid["id_twitch"]}''')
            
            if len(listeRaid) < CONFIG["MAX_VISI"]: #affiche toujours les infos raid si moinds de 5 raids en simultané
                raid["visi"] = True
                
            embuscade = list(raid["embuscade"].split(","))
            
            if str(raid["distance"]) in embuscade :
                raid["gfx_car"]="embuscade.png"
                await tbot_com.message("raid_embuscade",channel=channel,name=raid["name"])
                   
            data[f'SURVIVANT_{raid["name"]}']={"NAME":raid["name"],
                                        "STATS": stat_survivant,
                                        "TYPE":raid["type"],
                                        "DISTANCE":DISTANCE_POURCENT,
                                        "RENFORT":str(raid["renfort"]),
                                        "DEAD":(raid["distance"]<=raid["mort"]),
                                        "HURT":(raid["distance"]<=raid["blesse"]),
                                        "GFX_CAR":raid["gfx_car"],
                                        "VISI":raid["visi"]}

            if raid["distance"] == 0:
                if raid["mort"] >1 :
                    await tbot_com.message("raid_retour_base_mort",channel=channel,name=raid["name"])
                    await self.gere_fin_raid(db,raid,channel)
                    await db.execute(f'''DELETE from raid WHERE id_twitch = {raid["id_twitch"]}''')
                    await db.execute(f'''UPDATE survivant SET alive = 0,inraid = 0 WHERE id_twitch = {raid["id_twitch"]}''')
                else :
                    await self.gere_fin_raid(db,raid,channel)
                    await db.execute(f'''DELETE from raid WHERE id_twitch = {raid["id_twitch"]}''')
                    await db.execute(f'''UPDATE survivant SET inraid = 0 WHERE id_twitch = {raid["id_twitch"]}''')
                    
            elif raid["distance"] == raid["michemin"] :
                await tbot_com.message("raid_mi_chemin",channel=channel,name=raid["name"])
            elif raid["distance"] == raid["blesse"] : 
                await tbot_com.message("raid_blesse",channel=channel,name=raid["name"])
            elif raid["distance"] == raid["mort"] :
                await tbot_com.message("raid_mort_enroute",channel=channel,name=raid["name"])
                await db.execute(f'''UPDATE survivant SET 
                                     alive=0                                     
                                     WHERE id_twitch = {raid["id_twitch"]}''')
            await db.commit()
            await db.close()
            
        async with aiofiles.open("TBoT_Overlay/raid.json", "w",encoding="utf-8") as fichier:
            await fichier.write(json.dumps(data,indent=4,ensure_ascii=False))
        
    async def gere_fin_raid(self,db,raid,channel):
        
        gain_prestige = self.config_raid_json["raid_"+raid['type']]["gain_prestige"]
        listebutin=""
        if raid['resultat'] =="BUTIN":
            gain_prestige = gain_prestige*2
            listebutin = "<br>"+await tbot_com.donne_butin(raid['composition_butin']) 
            await tbot_com.message("raid_win_butin",channel=channel,name=raid['name'],gain_prestige=str(gain_prestige),listebutin=listebutin,bonus_butin=str(raid['bonus_butin']))
            await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige+raid['bonus_butin']} WHERE id_twitch = {raid['id_twitch']}''')
        if raid['resultat'] =="BREDOUILLE":
            gain_prestige =gain_prestige*1
            
            await tbot_com.message("raid_win_bredouille",channel=channel,name=raid['name'],gain_prestige=str(gain_prestige))
            await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige} WHERE id_twitch = {raid['id_twitch']}''')
        if raid['resultat'] =="BLESSE": 
            gain_prestige = gain_prestige//2
            await tbot_com.message("raid_win_blesse",channel=channel,name=raid['name'],gain_prestige=str(gain_prestige))
            await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige} WHERE id_twitch = {raid['id_twitch']}''')
        if raid['resultat'] =="MORT":
            gain_prestige = 0
        
        #Gestion renfort eventuel    
        gain_prestige = gain_prestige//4
        liste = raid['renfort'].split(",")
        listefinale = []
        for joueur in liste:
            if joueur !="":
                #todo: gerer les nom des support avec les id twitch
                await db.execute(f'''UPDATE survivant SET prestige = prestige +{gain_prestige},
                                 support_raid = "",
                                 inraid       = False
                                 WHERE name_lower = "{joueur.lower()}"''')
                await tbot_com.message("survivant_gain_support",channel=channel,name=joueur,gain_prestige=str(gain_prestige),name2=raid['name'])
                
        
            
            
    async def upgrade_aptitude(self,id_twitch: int,aptitude: str,cout_upgrade: int):
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute(f'''UPDATE survivant SET prestige = prestige - {cout_upgrade} WHERE id_twitch = {id_twitch}''')
        await db.execute(f'''UPDATE survivant SET level_{aptitude} = level_{aptitude} + 1 WHERE id_twitch = {id_twitch}''') 
        await db.commit()
        await db.close()
        
    async def add_visi(self,id_twitch: str, duree: int=5):
        """permet d'afficher pour une certaine durée les infos du raid
        Args:
            name (str): nom du survivant
            duree (int, optional): nombre de cycle d'affichage des infos. Default à 5.
        """        
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute(f'''UPDATE raid SET visi = true , time_visi = {duree} WHERE id_twitch = {id_twitch}''')
        await db.commit()
        await db.close()
        
    async def join_raid(self,raidStats,helperStats,equipe,cout_renfort):
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute(f'''UPDATE raid SET
                         renfort = '{','.join([str(elem) for elem in equipe])}',
                         effectif_team = effectif_team + 1
                         WHERE id_twitch = {raidStats["id_twitch"]}''')
        await db.execute(f'''UPDATE survivant SET
                         support_raid = "{raidStats["name"]}",
                         inraid = True,
                         credit =credit - {cout_renfort}
                         WHERE id_twitch = {helperStats["id_twitch"]}''') 
        await db.commit()
        await db.close()
        

    async def support_revision(self,type: str,raider: dict,helper_stats: dict):
        raidEnCours = await self.stat_raid(raider["id_twitch"])

        if helper_stats[f"level_{type}"] > raidEnCours[f"levelRaid_{type}"]:
                db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD)) 
                await db.execute(f'''UPDATE raid SET 
                                 levelRaid_{type} = {helper_stats[f"level_{type}"]}
                                 WHERE id_twitch = {raider["id_twitch"]}''')
                await db.commit()
                await db.close()

        
    async def kill_them_all(self,channel):
        print ("ARMAGEDDON !!!!")
        db = await aiosqlite.connect(os.path.join("./Sqlite", self.NAMEBDD))
        await db.execute("DELETE FROM raid")
        await db.execute("UPDATE survivant SET alive = false")
        await db.commit()
        await db.close()    


if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
