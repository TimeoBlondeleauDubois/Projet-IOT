import sqlite3

connection = sqlite3.connect('base_de_donnee.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        US_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_Utilisateur VARCHAR UNIQUE,  -- Ajout d'UNIQUE pour créer un index
        Mot_De_Passe VARCHAR
);
""")

connection.commit()
connection.close()