from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from bcrypt import hashpw, gensalt
from datetime import datetime
from flask import request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')

def connect_db():
    db_path = 'base_de_donnee.db'
    print(f"Connecté à la base de données : {db_path}")
    return sqlite3.connect(db_path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            return redirect(url_for('dashboard'))
        else:
            error = 'Nom d\'utilisateur ou mot de passe incorrect'
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Avant create_user: {username}, {password}")
        if create_user(username, password):
            print("Après create_user: Utilisateur créé avec succès")
            return redirect(url_for('login'))
        else:
            error = 'Nom d\'utilisateur déjà pris'
    return render_template('signup.html', error=error)



@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

def check_credentials(username, password):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT Mot_De_Passe FROM User WHERE Nom_Utilisateur = ?", (username,))
        stored_password = cursor.fetchone()

    if stored_password is not None:
        stored_password = stored_password[0]
        if hashpw(password.encode('utf-8'), stored_password) == stored_password:
            return True

    return False


def create_user(username, password):
    try:
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO User (Nom_Utilisateur, Mot_De_Passe) VALUES (?, ?)", (username, hashed_password))
        print(f"Utilisateur {username} créé avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")
        return False


@app.route('/sonde')
def sonde():
    return render_template('sonde.html')

@app.route('/sonde1', methods=['POST'])
def sonde1():
    if request.method == 'POST':
        with connect_db() as db:
            cursor = db.cursor()

            valeur = request.form['valeur']
            type_mesure = request.form['type_mesure']
            temps = datetime.now()

            if type_mesure == 'temperature':
                cursor.execute("INSERT INTO Meteo (temperature, temps) VALUES (?, ?)", (valeur, temps))
            elif type_mesure == 'humidite':
                cursor.execute("INSERT INTO Meteo (humidite, temps) VALUES (?, ?)", (valeur, temps))
            elif type_mesure == 'pression':
                cursor.execute("INSERT INTO Meteo (pression, temps) VALUES (?, ?)", (valeur, temps))

        return redirect(url_for('sonde'))
    
@app.route('/afficher_mesures')
def afficher_mesures():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Meteo")
        mesures = cursor.fetchall()
    return render_template('afficher_mesures.html', mesures=mesures)

@app.route('/supprimer_mesure/<int:mesure_id>', methods=['POST'])
def supprimer_mesure(mesure_id):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Meteo WHERE M_Id = ?", (mesure_id,))
        db.commit()

    return redirect(url_for('afficher_mesures'))


@app.route('/get_data')
def get_data():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT temps, temperature, humidite, pression FROM Meteo")
        data = cursor.fetchall()

    # Convertir les résultats en format compréhensible (dictionnaire JSON)
    result = {
        "temps": [entry[0] for entry in data],
        "temperature": [entry[1] for entry in data],
        "humidity": [entry[2] for entry in data],
        "pressure": [entry[3] for entry in data]
    }
    
    return jsonify(result)


@app.route('/fichier.json', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        data = request.get_json()  # Cette ligne récupère les données JSON

        # Faites quelque chose avec les données, par exemple imprimez-les
        print("Received data:", data)

        # Vous pouvez également enregistrer les données dans la base de données ou effectuer d'autres actions nécessaires

        return jsonify({"message": "Data received successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True,port=2000#, host='192.168.164.187')
    )

