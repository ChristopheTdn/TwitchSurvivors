'''
Module de gestion des alertes sonores pour le Projet TBoT_Terror
'''

import twitchio
import asyncio
from twitchio.ext import pubsub,sounds,commands
import json
import os
from pygame import mixer


TBOTPATH, filename = os.path.split(__file__) 

def joue_son(radio = "radio1.mp3"):
    mixer.init()   
    mixer.music.load(os.path.join(TBOTPATH, "sound/"+radio))
    mixer.music.play()
