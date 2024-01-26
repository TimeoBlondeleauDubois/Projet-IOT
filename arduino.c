#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C

const char *ssid = "legra";
const char *password = "123";
const char *serverIP = "192.168.170.187";
const int serverPort = 5000;

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);
  Wire.pins(0, 2);
  Wire.begin();

  bool status;
  status = bme.begin(0x76);
  if (!status) {
    Serial.println("Impossible de détecter un capteur BME280, vérifiez les connexions!");
    while (1);
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion au WiFi en cours...");
  }
  Serial.println("Connecté au WiFi!");

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Échec de l'allocation SSD1306"));
    for (;;);
  }
  delay(2000);
}

void loop() {
  float temperature = bme.readTemperature();
  float pressure = bme.readPressure() / 100.0F;
  float humidity = bme.readHumidity();

  displayDataOnScreen(temperature, humidity, pressure);
  sendDataToServer(temperature, humidity, pressure);

  delay(5000);
}

void sendDataToServer(float temperature, float humidity, float pressure) {
  HTTPClient http;

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/insert_data";
  String postData = "temperature=" + String(temperature) +
                    "&humidity=" + String(humidity) +
                    "&pressure=" + String(pressure);

  http.begin(url);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpResponseCode = http.POST(postData);

  if (httpResponseCode > 0) {
    Serial.println("Données envoyées avec succès au serveur");
  } else {
    Serial.print("Erreur lors de l'envoi des données au serveur. Code d'erreur : ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void displayDataOnScreen(float temperature, float humidity, float pressure) {
  Serial.print("Temperature = ");
  Serial.print(temperature);
  Serial.println(" *C");

  Serial.print("Pression = ");
  Serial.print(pressure);
  Serial.println(" hPa");

  Serial.print("Humidite = ");
  Serial.print(humidity);
  Serial.println(" %");

  display.clearDisplay();
  display.setCursor(0, 10);
  display.setTextSize(1);
  display.setTextColor(WHITE);

  display.println("METEO");
  display.println();

  display.print("Temp. = ");
  display.print(temperature);
  display.println(" C");

  display.print("Press. = ");
  display.print(pressure);
  display.println(" hPa");

  display.print("Hum. = ");
  display.print(humidity);
  display.println(" %");

  display.display();
}
