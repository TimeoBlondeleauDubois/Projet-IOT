from flask import Flask, request
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/insert_data', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        print("Received data:", data)

        data = request.get_json()
        temperature = data['temperature']
        humidity = data['humidity']
        pressure = data['pressure']
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        connection = sqlite3.connect('base_de_donnee.db')
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Meteo (temperature, humidite, pression, temps)
            VALUES (?, ?, ?, ?)
        """, (temperature, humidity, pressure, current_time))

        connection.commit()
        connection.close()

        return 'Données insérées avec succès dans la base de données!'
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
