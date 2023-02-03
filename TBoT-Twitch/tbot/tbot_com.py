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

langue = "french"

with open (f'./TBOT-Twitch/tbot/localisation/{langue}.json', 'r',encoding="utf-8" ) as fichier:
    localisation = json.load(fichier)

with open ('./TBOT-Twitch/tbot/config/config_raid.json', 'r',encoding="utf-8" ) as fichier:
    config_raid_json = json.load(fichier)
    
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

async def message(key="empty",channel=None,name="",mod="",chat="",ovl="",sound="",gain_reputation="",listebutin=""):
    """    envois un message vers les différentes interfaces (twitch, overlay obs, chat in game PZ)

    Args:
        channel (_type_, optional): Donne l'objet channel pour envoyer un message sur le chat twitch. Defaults > None.
        overlay (str, optional): message devant etre affiché sur l'overlay. Defaults > "".
        chat (str, optional): message devant afficher le message dans le chat twitch. Defaults to "".
        mod (str, optional): message devant afficher le message dans le jeu via le Mod. Defaults to "".
        son (str, optional): nom du fichier se trouvant dans /sound a jouer. Defaults to "".
    """
    heure =  str(datetime.now().hour)
    minute = str(datetime.now().minute)
    if chat == "":
        chat= localisation[f"{key}"]["chat"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_reputation}",gain_reputation)\
            .replace("{listebutin}",listebutin)
    if ovl == "":
        ovl = localisation[f"{key}"]["ovl"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_reputation}",gain_reputation)\
            .replace("{listebutin}",listebutin)
                
    if mod == "":
        mod = localisation[f"{key}"]["mod"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_reputation}",gain_reputation)\
            .replace("{listebutin}",listebutin)
    if sound == "":
        sound = localisation[f"{key}"]["sound"]
    #envoyer les messages 
    if chat != "":
        await channel.send(chat)
    if ovl != "" :
        await affichage_Overlay(ovl)
    if mod != "" :
        async with aiofiles.open(URLMOD+"texte.txt","w",encoding="utf-8") as fichier:
            await fichier.write(mod)
    if sound != "" :
        joue_son(sound)
        
async def donne_butin(butin:str) -> str:
    """Envois le butin vers le mod PZ

    Args:
        butin (str): String qui enumere le butin (nom : class pz)

    Returns:
        str: renvois une string pour detailler les differents items du butin 
    """    
    butin=butin.replace("{","")
    butin=butin.replace("}","")
    liste_Butin=butin.split(",")
    listeClassefinale = ""
    listefinale=""
    
    for nom in liste_Butin:
        item=nom.split(':')
        item[0]= item[0].strip().replace ('"',"")
        item[1]= item[1].strip().replace ('"',"")
        listefinale += "  🔸"+item[0]+"\n"
        listeClassefinale += item[1]+"\n"
        
    async with aiofiles.open(URLMOD+"butin.txt","w",encoding="utf-8") as fichier:
        await fichier.write(listeClassefinale)
    
    return listefinale
        

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
        
    async with aiofiles.open("assets/chat.json", "w",encoding="utf-8") as fichier:
        await fichier.write(json.dumps(messageJson,indent=4,ensure_ascii=False))

async def ecrit_log(msg: str):
    heure =  datetime.now().hour
    minute = datetime.now().minute
    async with aiofiles.open("journal.log", "a",encoding="utf-8") as journal:
        await journal.write(f"{heure:2}h{minute:2} | {msg}\n")