from flask import Flask, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    pressure = request.form['pressure']
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connection = sqlite3.connect('base_de_donnee.db')
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Meteo (temperature, humidite, pression, temps) 
        VALUES (?, ?, ?, ?)
    """, (temperature, humidity, pressure, current_time))

    connection.commit()
    connection.close()

    return 'Données insérées avec succès !'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
