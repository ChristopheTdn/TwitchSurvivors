'''
Module de gestion des communication twitch chat, Mod, overlay Obs pour le Projet TBoT_Terror
'''

import twitchio
import asyncio
from twitchio.ext import pubsub,sounds,commands
import json
import os
from pygame import mixer
import aiofiles
from datetime import datetime


with open('./config.json', 'r') as fichier:
    data = json.load(fichier)
    URLMOD = data["URLMOD"]
    
TBOTPATH, filename = os.path.split(__file__) 
ligne_overlay=[]
messageJson={}    

def joue_son(radio = "radio1.mp3"):
    """Joue un son passé en parametre 

    Args:
        radio (str, optional): nom du fichier se trouvant dans le repertoire /sound. Defaults > "radio1.mp3".
    """
    mixer.init()   
    mixer.music.load(os.path.join(TBOTPATH, "sound/"+radio))
    mixer.music.play()

async def message(channel=None,overlay ="",chat="",mod="",son="",):
    """    envois un message vers les differ

    Args:
        channel (_type_, optional): Donne l'objet channel pour envoer un message sur le chat twitch. Defaults > None.
        overlay (str, optional): message devant etre affiché sur l'overlay. Defaults > "".
        chat (str, optional): message devant afficher le message dans le chat twitch. Defaults to "".
        mod (str, optional): message devant afficher le message dans le jeu via le Mod. Defaults to "".
        son (str, optional): nom du fichier se trouvant dans /sound a jouer. Defaults to "".
    """
    if chat != "":
        await channel.send(chat)
    if overlay != "" :
        await affichage_Overlay(overlay)
    if mod != "" :
        async with aiofiles.open(URLMOD+"texte.txt","w",encoding="utf-8") as fichier:
            await fichier.write(mod)
    if son != "" :
        joue_son(son)

async def affichage_Overlay(message: str):
    """Genere un fichier HTML utilisable comme OVERLAY dans OBS

    Args:
        message (str): message à ajouter à la page html
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
    
    if len(ligne_overlay)>10:
        del ligne_overlay[10]  

        
    async with aiofiles.open('tbot.html',"w",encoding="utf-8") as fichier:
        await fichier.write(template)
        for ligne in ligne_overlay:
            await fichier.write ("<p>"+ligne+"</p>\n")
        await fichier.write('''
        </body>
        </html>
        ''')

    num_message = 1
    for ligne in ligne_overlay:
        messageJson[f"message_{num_message}"] = ligne
        num_message +=1
        
    async with aiofiles.open("message_overlay.json", "w",encoding="utf-8") as fichier:
        await fichier.write(json.dumps(messageJson,indent=4,ensure_ascii=False))

async def ecrit_log(self,msg: str):
    heure =  datetime.now().hour
    minute = datetime.now().minute
    async with aiofiles.open("journal.log", "w",encoding="utf-8") as journal:
        await journal.write(f"{heure}:{minute} | {msg})