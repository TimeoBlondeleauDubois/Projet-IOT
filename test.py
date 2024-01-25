from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("Received POST request")  # Ajout de ce message
        data = request.json  # Récupérer les données JSON du corps de la requête
        temperature = data['temperature']
        humidity = data['humidity']
        pressure = data['pressure']
        message = data['message']  # Récupérer le message "hello world"

        # Faire quelque chose avec les données
        print(f'Temperature: {temperature}, Humidity: {humidity}, Pressure: {pressure}')
        print(f'Message: {message}')

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
