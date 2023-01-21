import json
import twitchio
from twitchio.ext import commands, sounds,pubsub
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
        
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await self.timer_Raid()
        

    async def timer_Raid(self):
        while True:
            await TBOTBDD.actualise_statRaid()
            await asyncio.sleep(2)

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
        
    async def creation_survivant(self,pseudo,channel):
        name_survivant = await TBOTBDD.survivant_exist(pseudo)
        if name_survivant != None : #le pseudo existe deja dans la base de donnée
            message = f"Echec de tentative de création du joueur {pseudo} sur le serveur ! Le survivant existe déjà. Tapes !info_survivant"
            messagehtml = f"❌ Echec de tentative de création du joueur {pseudo} sur le serveur !"
            await self.affichage_Overlay(messagehtml)
            await channel.send(message) 
        
        else :
            await TBOTBDD.create_survivant(pseudo)
            await tbot_com.message(channel,mod=f" : ...allo ! je m'appelle {pseudo}... Je suis un surviva....pret a aider....d'autres messages suivront...",
                            overlay=f"⛹Le joueur <strong>{pseudo}</strong> vient d'apparaitre sur le serveur.",
                            chat=f"⛹ Le joueur {pseudo} vient d'apparaitre sur le serveur!",
                            son="radio1.mp3")
            
                

                
    @commands.command()
    async def parle(self, ctx: commands.Context):
        """
        Commande !parle <message>
        -----------
        Traite la commande twitch !parle. Envois in game le message passé en parametre avec un son radio
        """
        pseudo = ctx.author.display_name
        message = ctx.message.content
        message=message.replace('!parle',"")
        tbot_com.joue_son("radio2.mp3")
        async with aiofiles.open(URLMOD+"texte.txt","w",encoding="utf-8") as fichier:
            await fichier.write(f"⚡<radio {pseudo}> : {message}")
        messagehtml = f"⚡&ltradio {pseudo}> : {message}"
        await self.affichage_Overlay(messagehtml)
        
    @commands.command()
    async def mon_survivant(self, ctx: commands.Context):
        """
        Commande !mon_survivant 
        -----------
        Traite la commande twitch !mon_survivant. retourne les stats du joueurs dans le chat Twitch
        """
        name = ctx.author.display_name
        channel = ctx.channel
        test_survivant_exist = await TBOTBDD.survivant_exist(name)
        if test_survivant_exist !=None :
            dictStat= await TBOTBDD.get_stats_survivant(name)
            message = f"stat {dictStat['name']} : reputation = {dictStat['reputation']},\
                levelgun = {dictStat['levelGun']} ; vetement = {dictStat['levelWear']}, vehicule = {dictStat['levelCar']}"
            await tbot_com.message(channel,chat=message)
     
        else :
            await tbot_com.message(channel,overlay=f"❌- le survivant <strong>{name}</strong> n'existe pas sur le serveur ! utilise les points de Chaine pour en creer un.",
                                     chat=f"❌- le survivant <strong>{name}</strong> n'existe pas sur le serveur ! utilise les points de Chaine pour en creer un.")
    
    @commands.command()
    async def raid_arme(self, ctx: commands.Context):
        """
        Commande !raid_arme
        -----------
        Traite la commande twitch !raid_arme. 
        """
        
        name = ctx.author.display_name
        channel = ctx.channel
        test_survivant_exist = await TBOTBDD.survivant_exist(name)
        test_raid_exist = await TBOTBDD.raid_exist(name)
        
        if test_survivant_exist == None :
            await tbot_com.message(channel,chat=f"❌-le survivant {name} n'existe pas sur le serveur ! Creer un nouveau survivant avec tes points de chaine.")

        elif test_raid_exist != None :

            await tbot_com.message(channel,chat=f"❌-un Raid est dejà en cours pour {name} ! tapez !mon_survivant pour plus d'info.")

        else :
            """Création du Raid_Arme
            """
            heure =  datetime.now().hour
            minute = datetime.now().minute
            jour = datetime.now().day
            await TBOTBDD.create_raid(name,"arme",90)

            await tbot_com.message(channel,mod=f"<radio {name}> : ...allo ! ici {name}... Je pars cherch... des arm. et des ..unitions.",
                                     overlay=f"🔨- radio {name} : ...allo ! ici {name}... Je pars cherch... des arm. et des ..unitions.",
                                     chat=f"🔨- il est {heure}:{minute}, {name} part en Raid pour récuperer de l'armement !",
                                     son="radio2.mp3")


if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
    