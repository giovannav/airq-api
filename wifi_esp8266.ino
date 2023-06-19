#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>

SoftwareSerial mySerial(D1, D2); //RX, TX

const char* ssid = "#";
const char* password =  "#";
String url = "https://vabya630n7.execute-api.sa-east-1.amazonaws.com/prod/device/";

void setup() {
  Serial.begin(115200);  
  mySerial.begin(9600);

  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Incializa led
  pinMode(D8, OUTPUT);
}

void loop() {
    if (mySerial.available()) {
    // read JSON data from Arduino
    StaticJsonDocument<200> doc;
    char json[200];
    mySerial.readBytesUntil('\n', json, sizeof(json));
    deserializeJson(doc, json);

    // extract sensor data
    float celcius = doc["degree_c"];
    float fahrenheit = doc["degree_f"];
    float humidity = doc["humidity"];
    float ppm_mq135 = doc["ppm_mq135"];
    float voltage_ldr = doc["voltage_ldr"];
    float presence = doc["presence"];

    // print sensor data to serial monitor
    Serial.print("Temperature: ");
    Serial.print(celcius);
    Serial.print(", Fahrenheit: ");
    Serial.print(fahrenheit);
    Serial.print(", Humidity: ");
    Serial.print(humidity);
    Serial.print(", Gas: ");
    Serial.println(ppm_mq135);
    Serial.print(", Voltage LDR: ");
    Serial.println(voltage_ldr);
    Serial.print(", Presence: ");
    Serial.println(presence);

    if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure client;
    client.setInsecure();
    
    HTTPClient https;
    String fullUrl = url;
      String id = "96edb0ff-666d-4195-b169-e3925da03919";
      char tempStr[7];
      dtostrf(celcius, 5, 2, tempStr);
      
      char fahrStr[7];
      dtostrf(fahrenheit, 5, 2, fahrStr);
  
      char ppmStr[7];
      dtostrf(ppm_mq135, 5, 2, ppmStr);

      char voltageStr[7];
      dtostrf(voltage_ldr, 5, 2, voltageStr);

      char presenceStr[7];
      dtostrf(presence, 5, 2, presenceStr);

      if (https.begin(client, "https://vabya630n7.execute-api.sa-east-1.amazonaws.com/prod/station/create")) {
      https.addHeader("Content-Type", "application/json");
      String json = "{\"degree_c\":" + String(tempStr) + ", \"degree_f\":" + String(fahrStr) + ", \"humidity\":" + String(humidity) + ", \"ppm_mq135\":" + String(ppmStr) + ", \"voltage_ldr\":" + String(voltageStr) + ", \"presence\":" + String(presenceStr) + ", \"device_id\":\"" + id + "\"}";
      //String json = "{\"degree_c\":" + String(tempStr) + ", \"degree_f\":" + String(fahrStr) + ", \"humidity\":" + String(humidity) + ", \"ppm_mq135\":" + String(ppmStr) + ", \"device_id\":\"" + id + "\"}";
      int httpCode = https.POST(json);
      Serial.println("============== Response code: " + String(httpCode));
      if (httpCode > 0) {
        String response = https.getString();
        Serial.println(response);

        // turn the led on for 5 seconds
        digitalWrite(D8, HIGH);
        delay(5000);
      }
      https.end();
      } else {
        Serial.printf("[HTTPS] Unable to connect\n");
      }  
    }
    // turn the led off
    digitalWrite(D8, LOW); 
    delay(1000);
  }
}
