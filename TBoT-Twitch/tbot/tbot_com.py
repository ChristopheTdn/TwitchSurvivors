'''
Module de gestion des communication twitch chat, Mod, overlay Obs pour le Projet TBoT_Terror
'''
import json
import os
from pygame import mixer
import aiofiles
from datetime import datetime
import winreg
from pathlib import Path, PureWindowsPath


with open('./Configuration/config.json', 'r') as fichier:
    CONFIG = json.load(fichier)

with open (f'./Language/{CONFIG["LANGUE"].lower()}.json', 'r',encoding="utf-8" ) as fichier:
    LOCALISATION = json.load(fichier)

with open ('./Data/raid.json', 'r',encoding="utf-8" ) as fichier:
    CONFIG_RAID = json.load(fichier)
    

    
TBOTPATH, filename = os.path.split(__file__) 

ligne_overlay=[]

def get_reg(name,reg_path):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

URLMOD =  get_reg("InstallLocation",r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 108600")
if URLMOD != None :
    URLMOD = URLMOD.replace(r"common\ProjectZomboid","workshop\content"+ os.sep +"108600"+ os.sep +CONFIG["STEAM_MOD_ID"]+ os.sep +"mods"+ os.sep +CONFIG["STEAM_MOD_NAME"]+ os.sep +"media\config")

if URLMOD == None or not CONFIG["MOD_STEAM"]:
    URLMOD = CONFIG["MOD_PATH"]
    
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
        radio (str, optional): nom du fichier se trouvant dans le repertoire /sounds. Defaults > "radio1.mp3".
    """
    if CONFIG["PLAY_SOUND"] : #joue les sons du Mod en fonction de la configuration
        mixer.init()   
        mixer.music.load(f'./Sounds/{CONFIG["LANGUE"]}/'+radio)
        mixer.music.set_volume(CONFIG["VOLUME"])
        mixer.music.play()

async def message(key="empty",channel=None,name="",name2="",mod="",chat="",ovl="",sound="",gain_prestige="",listebutin="",aptitude="",tarif_level="",credit="",bonus_butin=""):
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
    
    if key !='empty':
        chat= LOCALISATION[f"{key}"]["chat"]
        ovl = LOCALISATION[f"{key}"]["ovl"]
        mod = LOCALISATION[f"{key}"]["mod"]
        
    chat= chat\
            .replace("{name}",name)\
            .replace("{name2}",name2)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)
    ovl = ovl\
            .replace("{name}",f"<span class='pseudo'>{name}</span>")\
            .replace("{name2}",name2)\
            .replace("{heure}",heure)\
            .replace("{minute}",minute)\
            .replace("{gain_prestige}",gain_prestige)\
            .replace("{listebutin}",listebutin)\
            .replace("{aptitude}",aptitude)\
            .replace("{tarif_level}",tarif_level)\
            .replace("{credit}",credit)\
            .replace("{bonus_butin}",bonus_butin)
    mod = mod\
            .replace("{name}",name)\
            .replace("{name2}",name2)\
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
        async with aiofiles.open(URLMOD+os.sep+"radio.txt","w",encoding="utf-8") as fichier:
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
        
    async with aiofiles.open(URLMOD+os.sep+"butin.txt","w",encoding="utf-8") as fichier:
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