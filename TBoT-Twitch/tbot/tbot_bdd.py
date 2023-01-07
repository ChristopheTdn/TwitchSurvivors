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
            pseudo TEXT UNIQUE,
            health INTEGER,
            reputation INTEGER,
            levelGun INTEGER,
            levelWear INTEGER,
            levelCar INTEGER,
            stock INTEGER)''')
        curseur.execute('''INSERT OR IGNORE INTO player
                        (pseudo,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock)
                        VALUES (?,?,?,?,?,?,?)''', ("vide", 100,0,0,0,0,0))
        self.connexionSQL.commit()
        self.connexionSQL.close()
        
    def create_survivant (self,pseudo):
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute('''INSERT OR IGNORE INTO player
                        (pseudo,
                        health,
                        reputation,
                        levelGun,
                        levelWear,
                        levelCar,
                        stock)
                        VALUES (?,?,?,?,?,?,?)''', (pseudo , 100,0,0,0,0,0))
        self.connexionSQL.commit()
        self.connexionSQL.close()
    
    def player_exist(self,pseudo):
        self.connexionSQL = sqlite3.connect(os.path.join(self.TBOTPATH, self.NAMEBDD))
        cur = self.connexionSQL.cursor()
        cur.execute(f"SELECT pseudo FROM 'player' WHERE pseudo='{pseudo}'")
        reponse = cur.fetchone()
        self.connexionSQL.close()
        return reponse

if __name__ == '__main__': 
    print('Ne peut etre lancé directement')