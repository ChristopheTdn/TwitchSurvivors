import twitchio
import asyncio
from twitchio.ext import pubsub,sounds,commands
import json
import os
import pygame

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

users_oauth_token = CLIENT_TOKEN
users_channel_id = CLIENT_USER_ID

class TBoT_Client(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.pubsub = pubsub.PubSubPool(bot)

    @commands.Cog.event()
    async def event_ready(self):
        topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id],
        pubsub.bits(users_oauth_token)[users_channel_id],]
        await self.bot.pubsub.subscribe_topics(topics)

    async def event_pubsub_channel_points2(self, event: pubsub.PubSubChannelPointsMessage):
        # You could do this direct in the event if you wanted to
        message = f"{event.user.name} a utilisé '{event.reward.title}' pour un cout de {str(event.reward.cost)} point de chaine."
        channel = self.bot.get_channel(CLIENT_CHANNEL)
        await self.bot.creation_survivant(event.user.name,channel)

    @commands.Cog.event()
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        await self.event_pubsub_channel_points2(event)

def prepare(bot):
    bot.add_cog(TBoT_Client(bot))