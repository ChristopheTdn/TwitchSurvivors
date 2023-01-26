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
    
    
    
TBOTPATH, filename = os.path.split(__file__)    
ligne_overlay=[]
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
        name_survivant = await TBOTBDD.get_stats_survivant(name)
        if name_survivant != None : #le pseudo existe deja dans la base de donnée
            await tbot_com.message(channel,overlay=f"❌ Echec de tentative de création du joueur <span class='pseudo'>{name}</span> sur le serveur !",
                chat=f"❌- Echec de tentative de creation du joueur {name} sur le serveur ! Le survivant existe déjà. Tapes !info_survivant")
        
        else :
            await TBOTBDD.create_survivant(name)
            await tbot_com.message(channel,mod=f" : ...allo ! je m'appelle {name}... Je suis un surviva....pret a aider....d'autres messages suivront...",
                            overlay=f"⛹Le joueur <span class='pseudo'>{name}</span> vient d'apparaitre sur le serveur.",
                            chat=f"⛹ Le joueur {name} vient d'apparaitre sur le serveur!",
                            son="radio1.mp3")
            
    async def creer_raid(self,ctx: commands.Context,type_raid: str):
        
        name = ctx.author.display_name
        channel = ctx.channel
        test_survivant_exist = await TBOTBDD.get_stats_survivant(name)
        test_raid_exist = await TBOTBDD.raid_exist(name)
        
        if test_survivant_exist == None :
            await tbot_com.message(channel,chat=f"❌-le survivant {name} n'existe pas sur le serveur ! Creer un nouveau survivant avec tes points de chaine.")

        elif test_raid_exist != None :

            await tbot_com.message(channel,chat=f"❌-un Raid est dejà en cours pour {name} ! tapez !mon_survivant pour plus d'info.")

        else :
            """Création du Raid
            """
            # recupere le level du joueur en fonction du type de raid
               
                           
            raid_name = self.config_raid_json["raid_"+type_raid]["nom_raid"]
            msg_start_chat = self.config_raid_json["raid_"+type_raid]["msg_start_chat"]
            msg_start_overlay = self.config_raid_json["raid_"+type_raid]["msg_start_overlay"]
            msg_start_mod = self.config_raid_json["raid_"+type_raid]["msg_start_mod"]
            raid_icon = self.config_raid_json["raid_"+type_raid]["icon"]
            
            heure =  datetime.now().hour
            minute = datetime.now().minute
            
            await TBOTBDD.create_raid(name,raid_name)

            await tbot_com.message(channel,mod=f"<radio {name}> : ...allo ! ici {name}... {msg_start_mod}",
                                     overlay=f"{raid_icon}- radio : ...allo ! ici <span class='pseudo'>{name}</span>... {msg_start_overlay}",
                                     chat=f"{raid_icon}- il est {heure}:{minute}, {name} part en Raid {msg_start_chat}",
                                     son="radio3.mp3")           
    async def upgrade_aptitude(self,ctx: commands.Context ,aptitude: str):
        
        name = ctx.author.display_name
        channel = ctx.channel
        survivant = await TBOTBDD.get_stats_survivant(name)
        raid = await TBOTBDD.raid_exist(name)
        level=1
        
        
        if survivant == None :
            await tbot_com.message(channel,chat=f"❌-le survivant {name} n'existe pas sur le serveur ! Creer un nouveau survivant avec tes points de chaine.")
        elif raid != None :
            await tbot_com.message(channel,chat=f"❌-un Raid est en cours pour {name} ! tu ne peux pas modifier ses aptitudes.")
        else :
            level = survivant[f"level_{aptitude}"]                
            reputation = survivant["reputation"]
            tarif=[0,1000,2500,6000,13000]
            
            if  tarif[level]<=reputation:
                await TBOTBDD.upgrade_aptitude(name,aptitude,tarif[level])
                await tbot_com.message(channel,overlay=f"<span class='pseudo'>{name}</span> > upgrade son aptitude {aptitude} pour {tarif[level]}.",
                                       chat=f"{name} upgrade son aptitude {aptitude} pour {tarif[level]}.")
            else :
                await tbot_com.message(channel,chat=f"❌- {name} ne possède pas assez de points de réputation pour upgrade son aptitude {aptitude} (cout : {tarif[level]} pts).")  
                        
    @commands.command()
    async def parle(self, ctx: commands.Context):
        """
        Commande !parle <message>
        -----------
        Traite la commande twitch !parle. Envois in game le message passé en parametre avec un son radio
        """
        name = ctx.author.display_name
        message = ctx.message.content
        channel = ctx.channel
        message=message.replace('!parle',"")
        await tbot_com.message(channel,mod=f"<radio {name}> : {message}",
                        overlay=f"⚡&ltradio <span class='pseudo'>{name}</span> > : {message}",
                        son="radio4.mp3")
        
    @commands.command()
    async def mon_survivant(self, ctx: commands.Context):
        """
        Commande !mon_survivant 
        -----------
        Traite la commande twitch !mon_survivant. retourne les stats du joueurs dans le chat Twitch
        """
        name = ctx.author.display_name
        channel = ctx.channel
        test_survivant_exist = await TBOTBDD.get_stats_survivant(name)
        if test_survivant_exist !=None :
            dictStat= await TBOTBDD.get_stats_survivant(name)
            message = f"stat {dictStat['name']} : reputation = {dictStat['reputation']},\
                level_arme = {dictStat['level_arme']} ;\
                level_outil= {dictStat['level_outil']} ;\
                level_medical= {dictStat['level_medical']} ;\
                level_nourriture= {dictStat['level_nourriture']} ;\
                level_automobile= {dictStat['level_automobile']} ;\
                level_alcool= {dictStat['level_alcool']} ;\
                level_agriculture= {dictStat['level_agriculture']} ;\
                level_meuble = {dictStat['level_meuble']}"
            await tbot_com.message(channel,chat=message)
        else :
            await tbot_com.message(channel,overlay=f"❌- le survivant <span class='pseudo'>{name}</span> n'existe pas sur le serveur ! utilise les points de Chaine pour en creer un.",
                                     chat=f"❌- le survivant {name} n'existe pas sur le serveur ! utilise les points de Chaine pour en creer un.")
    
    @commands.command()
    async def raid_arme(self, ctx: commands.Context):
        """
        Commande !raid_arme
        -----------
        Traite la commande twitch !raid_arme. 
        """
        await self.creer_raid(ctx,"arme")

    @commands.command()
    async def raid_outil(self, ctx: commands.Context):
        """
        Commande !raid_outil
        -----------
        Traite la commande twitch !raid_outil. 
        """
        await self.creer_raid(ctx,"outil")

    @commands.command()
    async def raid_medical(self, ctx: commands.Context):
        """
        Commande !raid_medical
        -----------
        Traite la commande twitch !raid_medical. 
        """
        await self.creer_raid(ctx,"medical")
        
    @commands.command()
    async def raid_nourriture(self, ctx: commands.Context):
        """
        Commande !raid_nourriture
        -----------
        Traite la commande twitch !raid_nourriture. 
        """
        await self.creer_raid(ctx,"nourriture")
        
    @commands.command()
    async def raid_automobile(self, ctx: commands.Context):
        """
        Commande !raid_automobile
        -----------
        Traite la commande twitch !raid_automobile. 
        """
        await self.creer_raid(ctx,"automobile")
        
    @commands.command()
    async def raid_alcool(self, ctx: commands.Context):
        """
        Commande !raid_alcool
        -----------
        Traite la commande twitch !raid_alcool. 
        """
        await self.creer_raid(ctx,"alcool")

    @commands.command()
    async def raid_agriculture(self, ctx: commands.Context):
        """
        Commande !raid_agriculture
        -----------
        Traite la commande twitch !raid_agriculture. 
        """
        await self.creer_raid(ctx,"agriculture")
        
    @commands.command()
    async def raid_meuble(self, ctx: commands.Context):
        """
        Commande !raid_meuble
        -----------
        Traite la commande twitch !raid_meuble. 
        """
        await self.creer_raid(ctx,"meuble") 
        
    @commands.command()
    async def upgrade_armement(self, ctx: commands.Context):
        """
        Commande !upgrade_armement
        -----------
        Traite la commande twitch !upgrade_arme. 
        """
        await self.upgrade_aptitude(ctx,"armement")
                 
    @commands.command()
    async def upgrade_armure(self, ctx: commands.Context):
        """
        Commande !upgrade_armure
        -----------
        Traite la commande twitch !upgrade_armure. 
        """
        await self.upgrade_aptitude(ctx,"armure") 
        
    @commands.command()
    async def upgrade_transport(self, ctx: commands.Context):
        """
        Commande !upgrade_transport
        -----------
        Traite la commande twitch !upgrade_transport. 
        """
        await self.upgrade_aptitude(ctx,"transport") 

    @commands.command()
    async def upgrade_equipement(self, ctx: commands.Context):
        """
        Commande !upgrade_equipement
        -----------
        Traite la commande twitch !upgrade_equipement. 
        """
        await self.upgrade_aptitude(ctx,"equipement")                
        
if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
    
