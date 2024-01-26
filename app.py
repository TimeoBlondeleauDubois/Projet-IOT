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

            temperature = request.form.get('temperature')
            humidite = request.form.get('humidite')
            pression = request.form.get('pression')
            temps = datetime.now()

            if temperature is not None and humidite is not None and pression is not None:
                cursor.execute("INSERT INTO Meteo (temperature, humidite, pression, temps) VALUES (?, ?, ?, ?)",
                               (temperature, humidite, pression, temps))
                return redirect(url_for('sonde'))
            else:
                error_message = "Veuillez saisir les trois mesures (température, humidité, pression) en même temps."
                return render_template('sonde.html', error=error_message)

    
@app.route('/afficher_mesures')
def afficher_mesures():
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Meteo")
        mesures = cursor.fetchall()
    
    mesures_enum = list(enumerate(mesures, start=1))

    return render_template('afficher_mesures.html', mesures_enum=mesures_enum)


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

@app.route('/data.json')
def get_data_json():
    # Lisez le contenu du fichier data.json
    with open('data.json', 'r') as file:
        data = file.read()

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True,port=2000#, host='192.168.164.187'
    )

