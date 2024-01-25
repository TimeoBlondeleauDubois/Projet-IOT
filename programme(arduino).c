#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

Adafruit_BME280 bme; // I2C

const char* ssid = "legra";
const char* password = "123";
const char* serverUrl = "192.168.170.187"; // Remplacez par l'adresse IP de votre Raspberry Pi

void setup() {
  Serial.begin(115200);

  bool status;
  status = bme.begin(0x76);
  if (!status) {
    Serial.println("Could not detect a BME280 sensor, Fix wiring Connections!");
    while (1);
  }

  // Connexion WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.print("WiFi connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Lire les données du capteur BME280
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  // Créer un objet JSON
  DynamicJsonDocument jsonDoc(1024);
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;
  jsonDoc["pressure"] = pressure;
  jsonDoc["message"] = "hello world"; // Ajoutez cette ligne

  // Convertir l'objet JSON en chaîne
  String jsonString;
  serializeJson(jsonDoc, jsonString);

  // Créer une instance de l'objet WiFiClient
  WiFiClient client;

  // Connexion au serveur
  if (client.connect(serverUrl, 5000)) {
    // Construire l'URL pour la requête POST
    String url = "/upload";
    
    // Créer le corps de la requête avec le JSON en tant que données
    String postData = "application/json" + String(jsonString.length()) + "\r\n\r\n" + jsonString;

    // Envoyer la requête POST
    client.print("POST " + url + " HTTP/1.1\r\n");
    client.print("Host: " + String(serverUrl) + "\r\n");
    client.print("Content-Type: application/json\r\n");
    client.print("Content-Length: " + String(jsonString.length()) + "\r\n");
    client.print("\r\n");
    client.print(jsonString);

    // Attendre la réponse du serveur
    delay(1000);

    // Lire et afficher la réponse du serveur
    while (client.available()) {
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }

    // Fermer la connexion
    client.stop();
  }

  // Attente avant la prochaine lecture
  delay(5000);
}
