import sqlite3
import os


class Survivant():
    """gere un personnage virtuel sur le serveur Tancred_terror
    
    """  
    def __init__(self, name) -> None:
        self.create_survivant(name)
        
    def create_survivant(self,name):
        self.userTwitch  = name
        self.name        = name
        self.health      = 100
        self.reputation  = 0
        self.levelGun    = 0
        self.levelWear   = 0
        self.levelCar    = 0 
        self.stock       = 0