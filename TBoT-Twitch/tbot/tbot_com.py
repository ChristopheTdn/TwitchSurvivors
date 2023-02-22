'''
Module de gestion des communication twitch chat, Mod, overlay Obs pour le Projet TBoT_Terror
'''
import json
import os
from pygame import mixer
import aiofiles
from datetime import datetime


with open('./config/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)

with open (f'./TBOT-Twitch/tbot/localisation/{CONFIG["LANGUE"]}.json', 'r',encoding="utf-8" ) as fichier:
    LOCALISATION = json.load(fichier)

with open ('./TBOT-Twitch/tbot/data/config_raid.json', 'r',encoding="utf-8" ) as fichier:
    config_raid_json = json.load(fichier)
    
TBOTPATH, filename = os.path.split(__file__) 

ligne_overlay=[]



async def msg_init_TboT():
    for i in range(30):
        ligne_overlay.append({
        "date": 0,
        "message": ""
    })     
    await message(ovl="🤖- Initialisation TBoT Done. Enjoy...")

messageJson={}


def joue_son(radio = "radio1.mp3"):
    """Joue un son passé en parametre 

    Args:
        radio (str, optional): nom du fichier se trouvant dans le repertoire /sound. Defaults > "radio1.mp3".
    """
    mixer.init()   
    mixer.music.load(os.path.join(TBOTPATH, "sound/"+radio))
    mixer.music.play()

async def message(key="empty",channel=None,name="",mod="",chat="",ovl="",sound="",gain_prestige="",listebutin="",aptitude="",tarif_level="",credit="",bonus_butin=""):
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
    if bonus_butin != "":
        bonus_butin = f" +{bonus_butin} pts de prestige pour les items ramenés."
        
    if chat == "":
        chat= LOCALISATION[f"{key}"]["chat"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)

            
    if ovl == "":
        ovl = LOCALISATION[f"{key}"]["ovl"]\
            .replace("{name}",f"<span class='pseudo'>{name}</span>")\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)\
            .replace("{bonus_butin}",bonus_butin)

                
    if mod == "":
        mod = LOCALISATION[f"{key}"]["mod"]\
            .replace("{name}",name)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)
            
    if sound == "":
        sound = LOCALISATION[f"{key}"]["sound"]
    #envoyer les messages 
    if chat != "":
        await channel.send(chat)
    if ovl != "" :
        await affichage_Overlay(ovl)
    if mod != "" :
        async with aiofiles.open(CONFIG["URLMOD"]+"texte.txt","w",encoding="utf-8") as fichier:
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
        listefinale += '<p STYLE="padding:0 0 0 20px;">  🔸'+item[0]+'</p>'
        listeClassefinale += item[1]+"\n"
        
    async with aiofiles.open(CONFIG["URLMOD"]+"butin.txt","w",encoding="utf-8") as fichier:
        await fichier.write(listeClassefinale)
    
    return listefinale
        

async def affichage_Overlay(message: str):
    """Genere un fichier JSON utilisable comme OVERLAY dans OBS via les scripts dans TBot_Overlay

    Args:
        message (str): message à ajouter au fichier JSON
    """        
    global ligne_overlay
    ligne_overlay.insert(0,{"date":int(round(datetime.now().timestamp()*1000)),"message":message})

    ligne_overlay = ligne_overlay[:30]  

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