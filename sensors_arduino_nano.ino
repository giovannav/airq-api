#include "DHT.h"
#include <ArduinoJson.h>

#define DHTPIN 7     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);

// mq modules
const int mq135 = A0;
const int ldr = A1;
int pir_pin = 9;

void setup() {
  pinMode(pir_pin, INPUT);
  Serial.begin(9600);  
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float celcius = dht.readTemperature();
  float fahrenheit = dht.readTemperature(true);
  float mq135_value = analogRead(mq135);
  float ldr_value = analogRead(ldr);
  float presence = digitalRead(pir_pin);

  StaticJsonDocument<200> doc;
  doc["degree_c"] = celcius;
  doc["degree_f"] = fahrenheit;
  doc["humidity"] = humidity;
  doc["ppm_mq135"] = mq135_value;
  doc["voltage_ldr"] = ldr_value;
  doc["presence"] = presence;
  char json[200];
  serializeJson(doc, json);

// send JSON data to ESP8266
  Serial.println(json);
  
  delay(600000); // measures again every 10 minutes
}
