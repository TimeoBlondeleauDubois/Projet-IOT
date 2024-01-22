import sqlite3

connection = sqlite3.connect('base_de_donnee.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        US_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_Utilisateur VARCHAR UNIQUE, 
        Mot_De_Passe VARCHAR
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Meteo (
        US_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature VARCHAR TINYINT,
        humidite VARCHAR TINYINT,
        presssion VARCHAR TINYINT
);
""")

connection.commit()
connection.close()