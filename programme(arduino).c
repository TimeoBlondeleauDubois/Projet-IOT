#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Adafruit_BME280 bme; // I2C

float temperatureValues[5];
float humidityValues[5];
float pressureValues[5];
int currentIndex = 0;

DynamicJsonDocument jsonDoc(1024);  // Taille du document JSON, ajustez selon vos besoins

void setup() {
  Serial.begin(9600);

  Wire.pins(0, 2);
  Wire.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  delay(2000);

  bool status;
  status = bme.begin(0x76);
  if (!status) {
    Serial.println("Could not detect a BME280 sensor, Fix wiring Connections!");
    while (1);
  }

  Serial.println("-- Print BME280 readings--");
  Serial.println();
}

void saveJson(float averageTemperature, float averageHumidity, float averagePressure) {
  Serial.print(F("averageTemperature:"));
  Serial.print(averageTemperature);
  Serial.print(F(", averageHumidity:"));
  Serial.print(averageHumidity);
  Serial.print(F(", averagePressure:"));
  Serial.println(averagePressure);
}


float calculateAverage(float values[]) {
  float sum = 0;
  for (int i = 0; i < 5; i++) {
    sum += values[i];
  }
  return sum / 5;
}

void loop() {
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F;

  temperatureValues[currentIndex] = temperature;
  humidityValues[currentIndex] = humidity;
  pressureValues[currentIndex] = pressure;

  currentIndex = (currentIndex + 1) % 5;

  if (currentIndex == 0) {
    float averageTemperature = calculateAverage(temperatureValues);
    float averageHumidity = calculateAverage(humidityValues);
    float averagePressure = calculateAverage(pressureValues);

    Serial.print("Moyenne Température = ");
    Serial.print(averageTemperature);
    Serial.println(" *C");
    Serial.print("Moyenne Humidité = ");
    Serial.print(averageHumidity);
    Serial.println(" %");
    Serial.print("Moyenne Pression = ");
    Serial.print(averagePressure);
    Serial.println(" hPa");

    display.clearDisplay();
    display.setCursor(0, 10);
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.println("METEO");
    display.println();
    display.print("Moyenne Temp. = ");
    display.print(averageTemperature);
    display.println(" C");
    display.print("Moyenne Hum. = ");
    display.print(averageHumidity);
    display.println(" %");
    display.print("Moyenne Press. = ");
    display.print(averagePressure);
    display.println(" hPa");
    display.display();

    saveJson(averageTemperature, averageHumidity, averagePressure);
  }

  delay(5000);
}
