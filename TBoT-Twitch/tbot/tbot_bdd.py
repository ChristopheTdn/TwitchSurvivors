import sqlite3
import os

class TBOT_BDD():
        
    """Gestion de la base de donnée du TBOT
    """        
    def __init__(self,TBOTPATH) -> None:
        self.TBOTPATH=TBOTPATH
        self.NAMEBDD = "tbot_bdd.sqlite"
    
    def initTableSql(self):
        """
                Initialise la base de donnée si elle n'existe pas
        """
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        curseur = self.connexionSQL.cursor()
        curseur.execute('''CREATE TABLE IF NOT EXISTS player(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            health INTEGER,
            reputation INTEGER,
            levelGun INTEGER,
            levelWear INTEGER,
            levelCar INTEGER,
            stock INTEGER)''')

        curseur.execute('''INSERT OR IGNORE INTO player
                        (name,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock)
                        VALUES (?,?,?,?,?,?,?)''', ("vide", 100,0,0,0,0,0))
        curseur.execute('''CREATE TABLE IF NOT EXISTS raid(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            type TEXT,
            timing INTEGER,
            retour INTEGER,
            renfort TEXT 
            )''')
        curseur.execute('''INSERT OR IGNORE INTO raid
                (name,
                type,
                timing,
                retour,
                renfort)
                VALUES (?,?,?,?,?)''', ("vide", "",0,0,""))
        self.connexionSQL.commit()
        self.connexionSQL.close()
        
    def create_player(self,pseudo):
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute('''INSERT OR IGNORE INTO player
                        (name,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock)
                        VALUES (?,?,?,?,?,?,?)''', (pseudo , 100,0,0,0,0,0))
        self.connexionSQL.commit()
        self.connexionSQL.close()
    
    def get_stats_player(self,name: str)->dict:
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute(f'''SELECT name,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock FROM 'player' WHERE name='{name}' ''')
        listeStat = cur.fetchone()
        self.connexionSQL.close()
        reponse ={"name": listeStat[0],
                "health": listeStat[1],
                "reputation": listeStat[2],
                "levelGun": listeStat[3],
                "levelWear": listeStat[4],
                "levelCar": listeStat[5],
                "stock": listeStat[6]
                }
        return reponse
    
    def player_exist(self,name):
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute(f"SELECT name FROM 'player' WHERE name='{name}'")
        reponse = cur.fetchone()
        self.connexionSQL.close()
        return reponse
    
    def raid_exist(self,name: str):
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute(f"SELECT name FROM 'raid' WHERE name='{name}'")
        reponse = cur.fetchone()
        self.connexionSQL.close()
        return reponse
    
    def create_raid(self,name: str,type: str,timing: int):
        
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute('''INSERT OR IGNORE INTO raid
                        (name,
                        type,
                        timing,
                        retour,
                        renfort)
                        VALUES (?,?,?,?,?)''', (name,type,timing,timing/2,""))
        self.connexionSQL.commit()
        self.connexionSQL.close()
        

if __name__ == '__main__': 
    print('Ne peut etre lancé directement')