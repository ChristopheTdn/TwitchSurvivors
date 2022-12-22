import twitchio
from twitchio.ext import commands, sounds

ligne_overlay=[]
URLMOD = "D:\Christophe\Documents\GitHub\TBOTLua\TBoT\\"

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='2teao1hl20zyxksuws7f39x7ype9xl', prefix='!', initial_channels=['GToF_'])
        self.event_player = sounds.AudioPlayer(callback=self.sound_done)
        
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
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
      
    def creation_HTML(self, str):
        template = '''<html>
    <head>
    <link rel="stylesheet" href="style.css">
    <script>
        setTimeout(function(){location.reload()},2000);
    </script>
    </head>'''
        ligne_overlay.insert(0,str)
        with open('tbot.html',"w") as fichier:
            fichier.write(template)
            for ligne in ligne_overlay:
                fichier.write ("<p>"+ligne+"</p>\n")
            fichier.write("</body>")
        
        
          
    @commands.command()
    async def generate(self, ctx: commands.Context):
        message = f"Le joueur {ctx.author.name} vient d'apparaitre sur le serveur PZOMBOID !"
        messagehtml = f"Le joueur <strong>{ctx.author.display_name}</strong> vient d'apparaitre sur le serveur PZOMBOID !"
        await ctx.send(message)
        self.creation_HTML(messagehtml)
        sound = sounds.Sound(source='blague.mp3')
        self.event_player.play(sound)
        
    @commands.command()
    async def parle(self, ctx: commands.Context):
        messagehtml = f"Le joueur <strong>{ctx.author.display_name}</strong> vient d'apparaitre sur le serveur PZOMBOID !"
        self.creation_HTML(messagehtml)
        sound = sounds.Sound(source='blague.mp3')
        self.event_player.play(sound)
        message = ctx.message.content
        message=message.replace('!parle',"")
        with open(URLMOD+"texte.txt","w") as fichier:
            fichier.write(f"RADIO ({ctx.author.display_name}) : {message}")
        
bot = Bot()
bot.run()