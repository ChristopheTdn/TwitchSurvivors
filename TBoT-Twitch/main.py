import json
import twitchio
from twitchio.ext import commands, sounds
import sqlite3
import os

with open('./config.json', 'r') as fichier:
    data = json.load(fichier)
    BOT_TOKEN = data["BOT-TWITCH"]["TOKEN"]
    BOT_CLIENT_ID = data["BOT-TWITCH"]["CLIENT_ID"]
    BOT_PREFIX = data["BOT-TWITCH"]["BOT_PREFIX"]
    BOT_CHANNEL = data["BOT-TWITCH"]["BOT_CHANNEL"]
    URLMOD = data["URLMOD"]
TBOTPATH, filename = os.path.split(__file__)    
ligne_overlay=[]


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=BOT_TOKEN, prefix=BOT_PREFIX, initial_channels=BOT_CHANNEL)
        self.event_player = sounds.AudioPlayer(callback=self.sound_done)
        self.initTableSql()
        
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self,message: str):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

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
            message (str): message a ajouté a la page html
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
            
    def initTableSql(self):
        """
                Initialise la base de donnée si elle n'existe pas
        """
        self.connexionSQL = sqlite3.connect(os.path.join(TBOTPATH, "TBOT.BDD.sqlite"))
        curseur = self.connexionSQL.cursor()
        curseur.execute('''CREATE TABLE IF NOT EXISTS player(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            pseudo TEXT UNIQUE,
            health INTEGER,
            reputation INTEGER,
            levelGun INTEGER,
            levelWear INTEGER,
            levelCar INTEGER,
            stock INTEGER)''')
        curseur.execute('''INSERT OR IGNORE INTO player
                        (pseudo,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock)
                        VALUES (?,?,?,?,?,?,?)''', ("vide", 100,0,0,0,0,0))
        self.connexionSQL.commit()
        self.connexionSQL.close()

    def createPlayer(self,pseudo: str)->bool:
        """
        Genere un nouveau survivant et l ajoute a la base de données

        Args:
            pseudo (str): le pseudo du survivant.
        """        
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
            message = f"Echec tentative de création du joueur {ctx.author.name} sur le serveur ! Le survivant existe déjà. Tapes !info_survivant"
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
        
bot = Bot()
bot.run()