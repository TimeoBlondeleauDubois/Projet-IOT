import serial
import json

ser = serial.Serial('COM8', 9600)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        data = {}
        pairs = line.split(', ')
        for pair in pairs:
            key, value = pair.split(':')
            data[key.strip()] = float(value)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)
