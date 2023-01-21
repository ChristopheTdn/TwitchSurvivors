'''
Module de gestion des alertes sonores pour le Projet TBoT_Terror
'''

import twitchio
import asyncio
from twitchio.ext import pubsub,sounds,commands
import json
import os
from pygame import mixer
import aiofiles


TBOTPATH, filename = os.path.split(__file__) 
ligne_overlay=[]

def joue_son(radio = "radio1.mp3"):
    mixer.init()   
    mixer.music.load(os.path.join(TBOTPATH, "sound/"+radio))
    mixer.music.play()

async def message(ctx: commands.Context,overlay ="",chat="",mod="",son="",):
    '''
    envois un message vers l'overlay
    '''
    if chat != "":
        await ctx.send(chat)
    if overlay != "" :
        await affichage_Overlay(messagehtml)
    if mod != "" :
        async with aiofiles.open(URLMOD+"texte.txt","w") as fichier:
            await fichier.write(f"<radio {name}> : {message}")

async def affichage_Overlay(message: str):
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
    async with aiofiles.open('tbot.html',"w",encoding="utf-8") as fichier:
        await fichier.write(template)
        for ligne in ligne_overlay:
            await fichier.write ("<p>"+ligne+"</p>\n")
        await fichier.write('''
        </body>
        </html>
        ''')