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
        temperature REAL,
        humidite REAL,
        pression REAL,
        temps DATETIME,
        FOREIGN KEY (user_id) REFERENCES User(US_Id)
    );
""")

#exemples
cursor.execute("INSERT INTO Meteo (temperature, temps) VALUES (25.5, '2024-01-23 08:00:00')")
cursor.execute("INSERT INTO Meteo (temperature, temps) VALUES (26.0, '2024-01-23 09:00:00')")
cursor.execute("INSERT INTO Meteo (temperature, temps) VALUES (26.5, '2024-01-23 10:00:00')")
cursor.execute("INSERT INTO Meteo (temperature, temps) VALUES (27.0, '2024-01-23 11:00:00')")
cursor.execute("INSERT INTO Meteo (temperature, temps) VALUES (26.8, '2024-01-23 12:00:00')")

connection.commit()
connection.close()
