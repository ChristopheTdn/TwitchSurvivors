import twitchio
import asyncio
from twitchio.ext import pubsub
import json

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

import twitchio
from twitchio.ext import pubsub

users_oauth_token = CLIENT_TOKEN
users_channel_id = CLIENT_USER_ID
client = twitchio.Client("7avqdwvhfq48n3511t21px7e7rjmjy",  initial_channels=["GToF_"])
client.pubsub = pubsub.PubSubPool(client)

async def event_pubsub_channel_points2(event: pubsub.PubSubChannelPointsMessage):
    message = f"{event.user.name} a utilisé '{event.reward.title}' pour un cout de {str(event.reward.cost)} point de chaine."
    print(message)
    channel = client.get_channel("GToF_")
    await channel.send(message)
     
@client.event()
async def event_ready():
    print(f"Ready | {client.nick}")
    topics = [
    pubsub.channel_points(users_oauth_token)[users_channel_id],
    pubsub.bits(users_oauth_token)[users_channel_id],]
    await client.pubsub.subscribe_topics(topics)

@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    await event_pubsub_channel_points2(event)

client.run()