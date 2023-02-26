import json
import twitchio
from twitchio.ext import commands
import sqlite3
import asyncio
import os
from  tbot.tbot_bdd import TBOT_BDD
from datetime import datetime
import aiofiles
from . import tbot_com



with open('./CONFIGURATION/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)
    
with open('./CONFIGURATION/config_Token_TBoT.json', 'r') as fichier:
    TBOT = json.load(fichier)
    
with open('./CONFIGURATION/config_Token_Client.json', 'r') as fichier:
    CLIENT = json.load(fichier)
    

    
TBOTPATH, filename = os.path.split(__file__) 
TBOTBDD= TBOT_BDD(TBOTPATH)

class TBoT(commands.Bot):
    """Bot Twitch basé sur le package TWITCH IO

    """
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=TBOT["TOKEN"], prefix=TBOT["PREFIX"], initial_channels=[CLIENT["CHANNEL"]])
        TBOTBDD.initTableSql()
        with open ('./TBOT-Twitch/tbot/data/config_raid.json', 'r',encoding="utf-8" ) as fichier:
            self.config_raid_json = json.load(fichier)
            
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await tbot_com.msg_init_TboT()
        await self.timer_Raid()
        

    async def timer_Raid(self):
        channel = self.get_channel(CLIENT["CHANNEL"])
        while True:
            await TBOTBDD.actualise_statRaid(channel)
            await asyncio.sleep(1) #defini le cycle en seconde de progression et MaJ des raids.

    async def event_message(self,message: twitchio.Message):
        
        if message.echo:
            return
        
        #channel = self.get_channel("GToF_")
        #channel = message.channel#
        #await channel.send('coucou') #envois directement un message dans le channel a l origine du message
        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)
        
    async def creation_survivant(self,name: str,channel: str):
        """active le flag ALIVE du survivant apès avoir testé son existence e tsi les credits sont suffisants

        Args:
            name (str): _description_
            channel (str): _description_
        """        
        survivant = await TBOTBDD.get_stats_survivant(name)
        if survivant != None and survivant["alive"] == 1: #le pseudo existe deja dans la base de donnée
            await tbot_com.message("echec_creation_survivant",channel=channel,name=name)
        elif survivant != None and survivant["alive"] == 0: #le survivant doit etre ressucité
            if survivant["credit"]<CONFIG["COUT_REVIVE"]: #pas assez de credit
                await tbot_com.message("survivant_credit_insuffisant",channel=channel,name=name,credit=str(CONFIG["COUT_REVIVE"]))
            else : #on peut faire revivre le survivant
                await TBOTBDD.revive_survivant(name)
                await tbot_com.message("revive_survivant",channel=channel,name=name,credit=str(CONFIG["COUT_REVIVE"]))
        else :
            await tbot_com.message("survivant_no_exist",channel=channel,name=name)

            
    async def ajout_credit(self,name: str,channel: str,CREDIT: int= CONFIG["AJOUT_CREDIT"]): 
        """ajoute des credits au survivant

        Args:
            name (str): nom du survivant
            channel (_type_): channel twitch id
            CREDIT (_type_, optional): nombre de crédits. Default à CONFIG["AJOUT_CREDIT"].
        """   

        survivant = await TBOTBDD.get_stats_survivant(name)
        if survivant == None : #le pseudo n'existe pas dans la base de donnée
            await TBOTBDD.create_survivant(name)
            await TBOTBDD.revive_survivant(name)
            await tbot_com.message("revive_survivant",channel=channel,name=name,credit=str(CONFIG["COUT_REVIVE"]))
            CREDIT = CREDIT - CONFIG["COUT_REVIVE"]
        elif survivant["alive"]==False:
            await TBOTBDD.revive_survivant(name)
            await tbot_com.message("revive_survivant",channel=channel,name=name,credit=str(CONFIG["COUT_REVIVE"]))
            CREDIT = CREDIT - CONFIG["COUT_REVIVE"]
            
        await TBOTBDD.add_credit(name,credit=CREDIT)
        await tbot_com.message("survivant_ajout_credit",credit=str(CREDIT),channel=channel,name=name)
    
            
    async def creer_raid(self,ctx: commands.Context,type_raid: str):
        """Test la validité de la demande pour creer un raid
        Args:
            ctx (commands.Context): environnement twitchIO pour récupérer les informations
            type_raid (str): nom du raid
        """        
        name = ctx.author.display_name
        channel = ctx.channel
        survivor = await TBOTBDD.get_stats_survivant(name)
        test_raid_exist = await TBOTBDD.stat_raid(name)
        raid_name = self.config_raid_json["raid_"+type_raid]["nom_raid"]
        gain_prestige = self.config_raid_json["raid_"+type_raid]["gain_prestige"]
        
        if survivor == None or survivor["alive"] == False :
            await tbot_com.message("survivant_no_exist",channel=channel,name=name)

        elif test_raid_exist != None :
            await tbot_com.message("raid_deja_en_cours",channel=channel,name=name)

        elif survivor["credit"]<gain_prestige : 
            await tbot_com.message("raid_credit_insuffisant",channel=channel,name=name,gain_prestige=str(gain_prestige))

        else :
            """Création du Raid
            """
            # recupere le level du joueur en fonction du type de raid

            heure =  datetime.now().hour
            minute = datetime.now().minute
            
            await TBOTBDD.genere_raid(name,raid_name,gain_prestige,survivor["level_transport"])
            await tbot_com.message(f"raid_{raid_name}",channel=channel,name=name,gain_prestige=str(gain_prestige)) 
    
    async def create_support(self,helper: str,raider: str,channel: str,support: str,):

        helper_stats = await TBOTBDD.get_stats_survivant(helper)
        helper_stats_raid = await TBOTBDD.stat_raid(helper)
        
        while "tant_que_no_error" :
            if helper_stats_raid != None or helper_stats["support_raid"] != False:
                await tbot_com.message(key="survivant_no_support_when_raid",channel=channel,name=helper)
                break
            
            if helper_stats == None or helper_stats["alive"] == False :
                await tbot_com.message(key="survivant_no_exist",channel=channel,name=helper)
                break
            
            if raider == "" :
                await tbot_com.message(key="error_noName",channel=channel,name=helper)
                break
            
            raid_stats = await TBOTBDD.stat_raid(raider)
            if raid_stats == None :
                await tbot_com.message(key="error_noRaid",channel=channel,name=helper)
                break

            if raid_stats["time_renfort"] >= CONFIG["MAX_TIME_RENFORT"] :
                await tbot_com.message(key="error_raid_timeOut",channel=channel,name=helper,name2=raider)
                break
            
            equipe = raid_stats["renfort"]
            
            liste = equipe.split(",")
            if len(liste) >= 3 :
                await tbot_com.message(key="error_raid_MaxSurvivor",channel=channel,name=helper,name2=raider)
                break                

            listefinale = []
            for joueur in liste:
                if joueur !="":
                    listefinale.append(joueur)
            listefinale.append(helper)
            await TBOTBDD.join_raid(raider,helper,listefinale)
            break

    async def upgrade_aptitude(self,ctx: commands.Context ,aptitude: str):
        
        name = ctx.author.display_name
        channel = ctx.channel
        survivant = await TBOTBDD.get_stats_survivant(name)
        level = survivant[f"level_{aptitude}"] 
        if level >= 5 :
            await tbot_com.message(key="survivant_max_aptitude",channel=channel,name=name,aptitude=aptitude)
            return
         
        raid = await TBOTBDD.stat_raid(name)
        
        if survivant == None or survivant["alive"] == False :
            await tbot_com.message("survivant_no_exist",channel=channel,name=name)
        elif raid != None :
            await tbot_com.message("raid_deja_en_cours",channel=channel,name=name)
        else :
                          
            prestige = survivant["prestige"]
            tarif= CONFIG["TARIF_UPGRADE"]

            if  tarif[level]<=prestige:
                await TBOTBDD.upgrade_aptitude(name,aptitude,tarif[level])
                
                await tbot_com.message(key="survivant_upgrade_aptitude",channel=channel,name=name,aptitude=aptitude,tarif_level=str(tarif[level]))
            else :
                await tbot_com.message(key="survivant_prestige_insuffisant",channel=channel,name=name,aptitude=aptitude,tarif_level=str(tarif[level])) 
                        

    @commands.command()
    async def create_survivor(self, ctx: commands.Context):
        """
        Commande !create_survivor
        -----------
        Traite la commande twitch !create_survivor. 
        """
        channel = ctx.channel
        name = ctx.author.display_name
        await self.creation_survivant(name,channel)


    @commands.command()
    async def radio(self, ctx: commands.Context):
        """
        Commande !radio <message>
        -----------
        Traite la commande twitch !radio. Envois in game le message passé en parametre avec un son radio
        """
        name = ctx.author.display_name
        message = ctx.message.content
        channel = ctx.channel
        message=message.replace('!radio',"")
        await tbot_com.message(channel=channel,mod=f"<radio {name}> : {message}",
                        ovl=f"⚡&ltradio <span class='pseudo'>{name}</span> > : {message}",
                        sound="radio4.mp3")
        
    @commands.command()
    async def my_survivor(self, ctx: commands.Context):
        """
        Commande !my_survivor 
        -----------
        Traite la commande twitch !my_survivor. retourne les stats du joueurs dans le chat Twitch
        """
        name = ctx.author.display_name
        channel = ctx.channel
        test_survivant_exist = await TBOTBDD.get_stats_survivant(name)
        if test_survivant_exist !=None :
            dictStat= await TBOTBDD.get_stats_survivant(name)
            message = f"stat {dictStat['name']} : prestige = {dictStat['prestige']},\
                credit = {dictStat['credit']},\
                level weapon = {dictStat['level_weapon']} ;\
                level transport= {dictStat['level_transport']} ;\
                level armor= {dictStat['level_armor']} ;\
                level gear= {dictStat['level_gear']}"
            await tbot_com.message(channel=channel,chat=message)
        else :
            await tbot_com.message(key="survivant_no_exist",channel=channel,name=name)
    
    @commands.command()
    async def raid_weapon(self, ctx: commands.Context):
        """
        Commande !raid_weapon
        -----------
        Traite la commande twitch !raid_weapons
        """
        await self.creer_raid(ctx,"weapon")

    @commands.command()
    async def raid_tool(self, ctx: commands.Context):
        """
        Commande !raid_tool
        -----------
        Traite la commande twitch !raid_outil. 
        """
        await self.creer_raid(ctx,"tool")

    @commands.command()
    async def raid_medic(self, ctx: commands.Context):
        """
        Commande !raid_medic
        -----------
        Traite la commande twitch !raid_medic. 
        """
        await self.creer_raid(ctx,"medic")
        
    @commands.command()
    async def raid_food(self, ctx: commands.Context):
        """
        Commande !raid_nourriture
        -----------
        Traite la commande twitch !raid_food. 
        """
        await self.creer_raid(ctx,"food")
        
    @commands.command()
    async def raid_car(self, ctx: commands.Context):
        """
        Commande !raid_car
        -----------
        Traite la commande twitch !raid_car. 
        """
        await self.creer_raid(ctx,"car")
        
    @commands.command()
    async def raid_alcohol(self, ctx: commands.Context):
        """
        Commande !raid_alcohol
        -----------
        Traite la commande twitch !raid_alcohol. 
        """
        await self.creer_raid(ctx,"alcohol")

    @commands.command()
    async def raid_agriculture(self, ctx: commands.Context):
        """
        Commande !raid_agriculture
        -----------
        Traite la commande twitch !raid_agriculture. 
        """
        await self.creer_raid(ctx,"agriculture")
        
    @commands.command()
    async def upgrade_weapon(self, ctx: commands.Context):
        """
        Commande !upgrade_weapon
        -----------
        Traite la commande twitch !upgrade_weapon. 
        """
        await self.upgrade_aptitude(ctx,"weapon")
                 
    @commands.command()
    async def upgrade_armor(self, ctx: commands.Context):
        """
        Commande !upgrade_armor
        -----------
        Traite la commande twitch !upgrade_armor. 
        """
        await self.upgrade_aptitude(ctx,"armor") 
        
    @commands.command()
    async def upgrade_transport(self, ctx: commands.Context):
        """
        Commande !upgrade_transport
        -----------
        Traite la commande twitch !upgrade_transport. 
        """
        await self.upgrade_aptitude(ctx,"transport") 

    @commands.command()
    async def upgrade_gear(self, ctx: commands.Context):
        """
        Commande !upgrade_gear
        -----------
        Traite la commande twitch !upgrade_gear. 
        """
        await self.upgrade_aptitude(ctx,"gear")     
    
    @commands.command()
    async def add_credit(self, ctx: commands.Context):
        """
        Commande !ajout_credit
        -----------
        Traite la commande twitch !ajout_credit. 
        """
        if CONFIG["DEBUG"]:
            await self.ajout_credit(ctx.author.display_name,ctx.channel)

    @commands.command()
    async def visi_on(self, ctx: commands.Context):
        """
        Commande !ajout_credit
        -----------
        Traite la commande twitch !ajout_credit. 
        """
        name = ctx.author.display_name
        channel = ctx.channel
        survivant_stats = await TBOTBDD.get_stats_survivant(name)
        if survivant_stats == None :
            await tbot_com.message(key="survivant_no_exist",channel=channel,name=name)
        else :
            await TBOTBDD.add_visi(name)

    
                       
    @commands.command()
    async def help_transport(self, ctx: commands.Context):
        """
        Commande !help_transport
        -----------
        Traite la commande twitch !help_transport. 
        """
        
        #TODO : tester la possibilité d'utiliser la commande!help_transport


        helper = ctx.author.display_name
        helper_stats = await TBOTBDD.get_stats_survivant(helper)
        helper_stats_raid = await TBOTBDD.stat_raid(helper)
        channel = ctx.channel
        raider= ctx.message.content.replace('!help_transport',"").strip()
        await self.create_support(helper,raider,channel,"transport")



            
             

    
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
    

