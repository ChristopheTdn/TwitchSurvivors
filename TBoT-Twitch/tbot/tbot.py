import json
import twitchio
from twitchio.ext import commands, sounds,pubsub
import sqlite3
import os
from  tbot.tbot_bdd import TBOT_BDD

with open('./config.json', 'r') as fichier:
    data = json.load(fichier)
    BOT_TOKEN = data["BOT-TWITCH"]["TOKEN"]
    BOT_CLIENT_ID = data["BOT-TWITCH"]["CLIENT_ID"]
    BOT_PREFIX = data["BOT-TWITCH"]["BOT_PREFIX"]
    BOT_CHANNEL = data["BOT-TWITCH"]["BOT_CHANNEL"]
    URLMOD = data["URLMOD"]
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
        super().__init__(token=BOT_TOKEN, prefix=BOT_PREFIX, initial_channels=BOT_CHANNEL)
        self.event_player = sounds.AudioPlayer(callback=self.sound_done)
        TBOTBDD.initTableSql()
        
        
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

            

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
        
    async def sound_done(self):
        pass
    
    def affichage_Overlay(self,message: str):
        """Genere un fichier HTML utilisable comme OVERLAY dans OBS

        Args:
            message (str): message a ajouté à la page html
        """        
        template = '''
        <!doctype html>
        <html lang="fr">
        <head>
            <meta charset="utf-8">
            <title>Overlay TBOT</title>
            <link rel="stylesheet" href="style.css">
            <script>
                setTimeout(function(){location.reload()},4000);
            </script>
        </head>
        <body>
        '''
        ligne_overlay.insert(0,message)
        with open('tbot.html',"w",encoding="utf-8") as fichier:
            fichier.write(template)
            for ligne in ligne_overlay:
                fichier.write ("<p>"+ligne+"</p>\n")
            fichier.write('''
            </body>
            </html>
            ''')
                
    @commands.command()
    async def new_survivant(self, ctx: commands.Context):
        """
        Commande !new_survivant
        -----------
        Traite la commande twitch !new_survivant. Genere un nouveau survivant et l ajoute a la base de données
        """
        pseudo = ctx.author.display_name
        
        if TBOTBDD.player_exist(pseudo)!=None : #le pseudo existe deja dans la base de donnée
            message = f"Echec de tentative de création du joueur {pseudo} sur le serveur ! Le survivant existe déjà. Tapes !info_survivant"
            messagehtml = f"❌ Echec de tentative de création du joueur {pseudo} sur le serveur !"
            self.affichage_Overlay(messagehtml)
            await ctx.send(message) 
        else :
            TBOTBDD.create_player(pseudo)
            message = f"⛹ Le joueur {pseudo} vient d'apparaitre sur le serveur!"
            messagehtml = f"⛹Le joueur <strong>{pseudo}</strong> vient d'apparaitre sur le serveur."
            await ctx.send(message)
            self.affichage_Overlay(messagehtml)
            sound = sounds.Sound(source=os.path.join(TBOTPATH, "sound/radio1.mp3"))
            self.event_player.play(sound)
            message=f"<radio> : ...allo ! je m'appelle {pseudo}... Je suis un surviva....pret a aider....d'autres messages suivront..."
            with open(URLMOD+"texte.txt","w") as fichier:
                fichier.write(f"RADIO ({pseudo}) : {message}")
        

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
        sound = sounds.Sound(source=(os.path.join(TBOTPATH, "sound\\radio2.mp3")))
        self.event_player.play(sound)
        with open(URLMOD+"texte.txt","w",encoding="utf-8") as fichier:
            fichier.write(f"⚡<radio {pseudo}> : {message}")
        messagehtml = f"⚡&ltradio {pseudo}&rt : {message}"
        self.affichage_Overlay(messagehtml)
    @commands.command()
    async def mon_survivant(self, ctx: commands.Context):
        """
        Commande !mon_survivant 
        -----------
        Traite la commande twitch !mon_survivant. retourne les stats du joueurs dans le chat Twitch
        """
        pseudo = ctx.author.display_name

        if TBOTBDD.player_exist(pseudo)!=None :
            dictStat=TBOTBDD.get_stats_player(pseudo)
            message = f"stat {dictStat['pseudo']} : vie = {dictStat['health']} ; reputation = {dictStat['reputation']},\
                levelgun = {dictStat['levelGun']} ; vetement = {dictStat['levelWear']}, vehicule = {dictStat['levelCar']},\
                Stock = {dictStat['stock']}"
            await ctx.send(message)      
        else :
            message = f"❌-le survivant {pseudo} n'existe pas sur le serveur ! Tapes !new_survivant pour en creer un."
            messagehtml = f"❌-le survivant <strong>{pseudo}</strong> n'existe pas sur le serveur ! Tapes !new_survivant pour en creer un."
            self.affichage_Overlay(messagehtml)
            await ctx.send(message)
            


if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
    