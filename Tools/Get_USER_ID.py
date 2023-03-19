import twitchio
import json
from twitchio.ext import commands


CLIENT_TOKEN = "" #saisir le token du bot généré ici : https://twitchtokengenerator.com/ >> BOT CHAT TOKEN
CHANNEL_TWITCH = "" #saisir le nom du channel twitch 


    
class TBoT(commands.Bot):
    """Bot Twitch basé sur le package TWITCH IO

    """
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=CLIENT_TOKEN, prefix="!", initial_channels=[CHANNEL_TWITCH])
        
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')


    
bot = TBoT()  
bot.run()