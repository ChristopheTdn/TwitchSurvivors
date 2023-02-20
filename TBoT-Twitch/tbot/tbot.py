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

with open('./config.json', 'r') as fichier:
    data = json.load(fichier)
    URLMOD = data["URLMOD"]

    BOT_USERNAME = data["BOT-TWITCH"]["BOT_USERNAME"]
    BOT_TOKEN = data["BOT-TWITCH"]["BOT_TOKEN"]
    BOT_REFRESH = data["BOT-TWITCH"]["BOT_REFRESH"]
    BOT_VALID = data["BOT-TWITCH"]["BOT_VALID"]
    BOT_USER_ID = data["BOT-TWITCH"]["BOT_USER_ID"]
    BOT_ID = data["BOT-TWITCH"]["BOT_ID"]
    BOT_NICK = data["BOT-TWITCH"]["BOT_NICK"]
    BOT_PREFIX = data["BOT-TWITCH"]["BOT_PREFIX"]
    BOT_CHANNEL = data["BOT-TWITCH"]["BOT_CHANNEL"]

    CLIENT_USERNAME = data["BOT-TWITCH"]["CLIENT_USERNAME"]
    CLIENT_TOKEN = data["BOT-TWITCH"]["CLIENT_TOKEN"]
    CLIENT_REFRESH = data["BOT-TWITCH"]["CLIENT_REFRESH"]
    CLIENT_USER_ID = data["BOT-TWITCH"]["CLIENT_USER_ID"]
    CLIENT_VALID = data["BOT-TWITCH"]["CLIENT_VALID"]
    CLIENT_ID = data["BOT-TWITCH"]["CLIENT_ID"]
    CLIENT_NICK = data["BOT-TWITCH"]["CLIENT_NICK"]
    CLIENT_PREFIX = data["BOT-TWITCH"]["CLIENT_PREFIX"]
    CLIENT_CHANNEL = data["BOT-TWITCH"]["CLIENT_CHANNEL"]
    
    COUT_REVIVE = data["COUT_REVIVE"]
    AJOUT_CREDIT = data["AJOUT_CREDIT"]



langue = "french"    # A ajouter dans un fichier config

        

TBOTPATH, filename = os.path.split(__file__)    
TBOTBDD= TBOT_BDD(TBOTPATH)

class TBoT(commands.Bot):
    """Bot Twitch basé sur le package TWITCH IO

    """
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=BOT_TOKEN, prefix=BOT_PREFIX, initial_channels=[CLIENT_CHANNEL])
        TBOTBDD.initTableSql()
        with open ('./TBOT-Twitch/tbot/config/config_raid.json', 'r',encoding="utf-8" ) as fichier:
            self.config_raid_json = json.load(fichier)
            
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await tbot_com.msg_init_TboT()
        await self.timer_Raid()
        

    async def timer_Raid(self):
        channel = self.get_channel(CLIENT_CHANNEL)
        while True:
            await TBOTBDD.actualise_statRaid(channel)
            await asyncio.sleep(1)

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
        
    async def creation_survivant(self,name: str,channel):
        survivant = await TBOTBDD.get_stats_survivant(name)
        if survivant != None and survivant["alive"] == 1: #le pseudo existe deja dans la base de donnée
            await tbot_com.message("echec_creation_survivant",channel=channel,name=name)
        elif survivant != None and survivant["alive"] == 0: #le survivant doit etre ressucité
            if survivant["credit"]<COUT_REVIVE: #pas assez de credit
                await tbot_com.message("survivant_credit_insuffisant",channel=channel,name=name,credit=str(COUT_REVIVE))
            else : #on peut faire revivre le survivant
                await TBOTBDD.revive_survivant(name)
                await tbot_com.message("revive_survivant",channel=channel,name=name,credit=str(COUT_REVIVE))
        else :
            await tbot_com.message("survivant_no_exist",channel=channel,name=name)

            
    async def ajout_credit(self,name: str,channel): 

        CREDIT = AJOUT_CREDIT
        survivant = await TBOTBDD.get_stats_survivant(name)
        if survivant == None : #le pseudo n'existe pas dans la base de donnée
            await TBOTBDD.create_survivant(name)
            await TBOTBDD.revive_survivant(name)
            await tbot_com.message("revive_survivant",channel=channel,name=name,credit=str(COUT_REVIVE))
            CREDIT = CREDIT - COUT_REVIVE
        elif survivant["alive"]==False:
            await TBOTBDD.revive_survivant(name)
            await tbot_com.message("revive_survivant",channel=channel,name=name,credit=str(COUT_REVIVE))
            CREDIT = CREDIT - COUT_REVIVE
            
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
        test_raid_exist = await TBOTBDD.raid_exist(name)
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
                     
    async def upgrade_aptitude(self,ctx: commands.Context ,aptitude: str):
        
        name = ctx.author.display_name
        channel = ctx.channel
        survivant = await TBOTBDD.get_stats_survivant(name)
        level = survivant[f"level_{aptitude}"] 
        if level >= 5 :
            await tbot_com.message(key="survivant_max_aptitude",channel=channel,name=name,aptitude=aptitude)
            return
         
        raid = await TBOTBDD.raid_exist(name)
        
        if survivant == None or survivant["alive"] == False :
            await tbot_com.message("survivant_no_exist",channel=channel,name=name)
        elif raid != None :
            await tbot_com.message("raid_deja_en_cours",channel=channel,name=name)
        else :
                          
            prestige = survivant["prestige"]
            tarif=[0,1000,2500,6000,13000]
            
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
        
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
    
