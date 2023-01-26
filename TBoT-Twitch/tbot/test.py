
import os
import aiosqlite
import sqlite3

TBOTPATH, filename = os.path.split(__file__)    
name="GToF_"
gain_reputation = 100

NAMEBDD = "tbot_bdd.sqlite"

db_survivant = sqlite3.connect(os.path.join(TBOTPATH, NAMEBDD))
db_survivant.execute(f'''UPDATE survivant SET reputation = reputation +{gain_reputation} WHERE name = "{name}"''')
db_survivant.commit()
db_survivant.close()