#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

Adafruit_BME280 bme; // I2C

const char* ssid = "Alexandre's Galaxy S21 5G";
const char* password = "MMMMMMMM";
const char* serverUrl = "http://127.0.0.1:2000/fichier.json"; // Replace with your PC address and desired path

void setup() {
  Serial.begin(115200);

  bool status;
  status = bme.begin(0x76);
  if (!status) {
    Serial.println("Could not detect a BME280 sensor, Fix wiring Connections!");
    while (1);
  }

  // WiFi Connection
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.print("WiFi connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void sendJSONToServer(float temperature, float humidity, float pressure) {
  HTTPClient http;

  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  // Create JSON object
  DynamicJsonDocument jsonDoc(1024);
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;
  jsonDoc["pressure"] = pressure;

  // Convert JSON to string
  String jsonString;
  serializeJson(jsonDoc, jsonString);

  int httpResponseCode = http.POST(jsonString);

  if (httpResponseCode > 0) {
    Serial.print("Data sent successfully, Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error sending data, Response code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void loop() {
  // Read sensor data
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  // Send data to the server
  sendJSONToServer(temperature, humidity, pressure);

  // Wait before the next reading
  delay(5000);
}
