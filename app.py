from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from bcrypt import hashpw, gensalt
import random

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


if __name__ == "__main__":
    app.run(port=2000)
