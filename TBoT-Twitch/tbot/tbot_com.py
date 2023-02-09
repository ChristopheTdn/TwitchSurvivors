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



async def msg_init_TboT():
    for i in range(20):
        ligne_overlay.append("")     
    await message(ovl="Init TBoT Done.")

messageJson={}


def joue_son(radio = "radio1.mp3"):
    """Joue un son passé en parametre 

    Args:
        radio (str, optional): nom du fichier se trouvant dans le repertoire /sound. Defaults > "radio1.mp3".
    """
    mixer.init()   
    mixer.music.load(os.path.join(TBOTPATH, "sound/"+radio))
    mixer.music.play()

async def message(key="empty",channel=None,name="",mod="",chat="",ovl="",sound="",gain_prestige="",listebutin="",aptitude="",tarif_level="",credit=""):
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
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)
            
    if ovl == "":
        ovl = localisation[f"{key}"]["ovl"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)

                
    if mod == "":
        mod = localisation[f"{key}"]["mod"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)
            
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
        listefinale += '<p STYLE="padding:0 0 0 20px;"  🔸'+item[0]+'</p>\n'
        listeClassefinale += item[1]+"\n"
        
    async with aiofiles.open(URLMOD+"butin.txt","w",encoding="utf-8") as fichier:
        await fichier.write(listeClassefinale)
    
    return listefinale
        

async def affichage_Overlay(message: str):
    """Genere un fichier JSON utilisable comme OVERLAY dans OBS via les scripts dans TBot_Overlay

    Args:
        message (str): message à ajouter au fichier JSON
    """        
    global ligne_overlay
    ligne_overlay.insert(0,message)
    
    ligne_overlay = ligne_overlay[:20]  

    num_message = 1
    for ligne in ligne_overlay:
        messageJson[f"message_{num_message}"] = ligne
        num_message +=1
        
    async with aiofiles.open("TBoT_Overlay/chat.json", "w",encoding="utf-8") as fichier:
        await fichier.write(json.dumps(messageJson,indent=4,ensure_ascii=False))

async def ecrit_log(msg: str):
    heure =  datetime.now().hour
    minute = datetime.now().minute
    async with aiofiles.open("journal.log", "a",encoding="utf-8") as journal:
        await journal.write(f"{heure:2}h{minute:2} | {msg}\n")