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
        M_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        temperature VARCHAR TINYINT,
        humidite VARCHAR TINYINT,
        pression VARCHAR TINYINT,
        temps TIME,
        FOREIGN KEY (user_id) REFERENCES User(US_Id)
);
""")

connection.commit()
connection.close()