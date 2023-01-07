import json
import twitchio
from twitchio.ext import commands, sounds
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

    async def event_message(self,message: str):
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
      
    def creation_HTML(self, message: str):
        """
        Genere un fichier HTML utilisable comme OVERLAY dans OBS

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
                setTimeout(function(){location.reload()},2000);
            </script>
        </head>'''
        ligne_overlay.insert(0,message)
        with open('tbot.html',"w") as fichier:
            fichier.write(template)
            for ligne in ligne_overlay:
                fichier.write ("<p>"+ligne+"</p>\n")
            fichier.write('''
            </body>
            </html>
            ''')

    def createPlayer(self,pseudo: str)->bool:
        """
        Genere un nouveau survivant et l ajoute a la base de données

        Args:
            pseudo (str): le pseudo du survivant.
        """   
        if TBOTBDD.player_exist(pseudo)!=None : #le pseudo existe deja dans la base de donnée
            return False
        else :
            TBOTBDD.create_survivant(pseudo)
        return True

    @commands.command()
    async def new_survivant(self, ctx: commands.Context):
        """
        Commande !new_survivant
        -----------
        Traite la commande twitch !new_survivant
        """

        if self.createPlayer(ctx.author.name) :
            message = f"Le joueur {ctx.author.name} vient d'apparaitre sur le serveur!"
            messagehtml = f"Le joueur <strong>{ctx.author.display_name}</strong> vient d'apparaitre sur le serveur PZOMBOID !"
            await ctx.send(message)
            self.creation_HTML(messagehtml)
            sound = sounds.Sound(source=os.path.join(TBOTPATH, "sound/radio1.mp3"))
            self.event_player.play(sound)
            message=f"<RADIO> : ...allo ! je m'appelle {ctx.author.display_name}... Je suis un surviva....pret a aider....d'autres messages suivront..."
            with open(URLMOD+"texte.txt","w") as fichier:
                fichier.write(f"RADIO ({ctx.author.display_name}) : {message}")
        else :
            message = f"Echec de tentative de création du joueur {ctx.author.name} sur le serveur ! Le survivant existe déjà. Tapes !info_survivant"
            messagehtml = f"Echec de tentative de création du joueur {ctx.author.name} sur le serveur !"
            await ctx.send(message)   
             
    @commands.command()
    async def parle(self, ctx: commands.Context):
        messagehtml = f"Le joueur <strong>{ctx.author.display_name}</strong> envois un message radio"
        self.creation_HTML(messagehtml)
        sound = sounds.Sound(source=(os.path.join(TBOTPATH, "sound\\radio2.mp3")))
        self.event_player.play(sound)
        message = ctx.message.content
        message=message.replace('!parle',"")
        with open(URLMOD+"texte.txt","w") as fichier:
            fichier.write(f"RADIO ({ctx.author.display_name}) : {message}")

if __name__ == '__main__': 
    print('Ne peut etre lancé directement')
    