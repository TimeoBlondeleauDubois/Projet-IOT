import serial

ser = serial.Serial('COM8', 9600)  # Remplacez 'COMx' par le port série approprié sur votre PC

# Attendre le début de la transmission
while ser.readline().decode('utf-8').strip() != '{"averageTemperature":':
    pass

# Ouvrir un fichier pour sauvegarder les données JSON
with open('data_from_arduino.json', 'w') as file:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == '}':
            break
        file.write(line + '\n')

ser.close()
