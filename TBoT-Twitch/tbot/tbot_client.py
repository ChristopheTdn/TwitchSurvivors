from twitchio.ext import pubsub,sounds,commands
import twitchio
import json
import os


with open('./Configuration/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)

with open('./Configuration/Secret/config_Token_Client.json', 'r') as fichier:
    CLIENT = json.load(fichier)

TBOTPATH, filename = os.path.split(__file__)    
ligne_overlay=[]


class TBoT_Client(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.pubsub = pubsub.PubSubPool(bot)

    async def event_pubsub_channel_points2(self, event: pubsub.PubSubChannelPointsMessage):
        # You could do this direct in the event if you wanted to
        if event.reward.title == "Acheter 300 crédits":
            channel = self.bot.get_channel(CLIENT["CHANNEL"])
            await self.bot.ajout_credit(event.user.id,event.user.name,channel,credit=300)
        if event.reward.title == "Acheter 2000 crédits":
            channel = self.bot.get_channel(CLIENT["CHANNEL"])
            await self.bot.ajout_credit(event.user.id,event.user.name,channel,credit=2000)
        if event.reward.title == "Acheter 5000 crédits":
            channel = self.bot.get_channel(CLIENT["CHANNEL"])
            await self.bot.ajout_credit(event.user.id,event.user.name,channel,credit=5000)   
               
    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        print(message.content)
    
            
    @commands.Cog.event()
    async def event_ready(self):
        topics = [pubsub.channel_points(CLIENT["TOKEN"])[CLIENT["USER_ID"]],
        pubsub.bits(CLIENT["TOKEN"])[CLIENT["USER_ID"]],]
        await self.bot.pubsub.subscribe_topics(topics)
        
    @commands.Cog.event()
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        await self.event_pubsub_channel_points2(event)

def prepare(bot):
    bot.add_cog(TBoT_Client(bot))
    


