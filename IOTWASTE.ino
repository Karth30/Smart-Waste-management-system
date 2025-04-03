#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFiClientSecureBearSSL.h>

// WiFi Credentials
const char* ssid = "Karthi";  
const char* password = "karthi11";  

// Google Apps Script Webhook URL
const char* serverName = "https://script.google.com/macros/s/AKfycbzucsh7nbFMkp6guf4NK15Bjx2h3iiTcw378rtCxppfC3vAr_pgoKsvkrNRqNKMvaFu/exec";
// Sensor Pins
const int trigPin = D5;
const int echoPin = D6;
const int gasSensorPin = A0;

int baselineGas = 0;  // Stores gas sensor baseline value
String lastAlertStatus = "No"; // Stores last alert status to avoid spam emails

void connectToWiFi() {
    Serial.print("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    
    int attempt = 0;
    while (WiFi.status() != WL_CONNECTED && attempt < 20) {
        delay(500);
        Serial.print(".");
        attempt++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nConnected to WiFi");
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\nWiFi connection failed!");
    }
}

//  **Calibrate Gas Sensor** (sets baseline air value)
void calibrateGasSensor() {
    Serial.println("Calibrating gas sensor...");
    int sum = 0;
    
    for (int i = 0; i < 50; i++) {
        sum += analogRead(gasSensorPin);
        delay(100);
    }
    
    baselineGas = sum / 50;  // Set baseline
    Serial.print("Baseline Gas Value: ");
    Serial.println(baselineGas);
}

//  **Measure Distance Using Ultrasonic Sensor**
float getDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);
    float distance = duration * 0.034 / 2;  

    if (distance <= 0 || distance > 400) { // Sanity check
        Serial.println("Invalid distance detected, ignoring...");
        return -1;
    }

    return distance;
}

// **Detect Smoke (Dynamic Threshold)**
String getSmokeStatus() {
    int gasValue = analogRead(gasSensorPin);
    
    Serial.print("Gas Sensor Value: ");
    Serial.println(gasValue);

    return (gasValue > baselineGas * 1.3) ? "Yes" : "No";  // Adjust sensitivity (1.3 = 30% higher)
}

// **Send Data to Google Sheets**
bool sendDataToServer(float distance, String smokeStatus, String alertStatus) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi disconnected! Reconnecting...");
        connectToWiFi();
        return false;
    }

    std::unique_ptr<BearSSL::WiFiClientSecure> client(new BearSSL::WiFiClientSecure);
    client->setInsecure();  // Disable SSL verification

    HTTPClient http;
    http.begin(*client, serverName);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> jsonDoc;
    jsonDoc["distance"] = distance;
    jsonDoc["smoke"] = smokeStatus;
    jsonDoc["alert"] = alertStatus;

    String jsonData;
    serializeJson(jsonDoc, jsonData);

    Serial.print("Sending Data: ");
    Serial.println(jsonData);

    int httpResponseCode = http.POST(jsonData);
    http.end();

    return httpResponseCode > 0;
}

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(gasSensorPin, INPUT);

    calibrateGasSensor(); // **Auto-calibrate gas sensor**
}

void loop() {
    float distance = getDistance();
    String smokeStatus = getSmokeStatus();
    
    String alertStatus = (distance > 0 && distance < 5) ? "Yes" : "No";  // **Alert when distance < 5 cm**
    
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" cm, Gas Sensor Value: ");
    Serial.print(analogRead(gasSensorPin));
    Serial.print(", Smoke Detected: ");
    Serial.print(smokeStatus);
    Serial.print(", Alert: ");
    Serial.println(alertStatus);

    // **Prevent spam: Only send data if alert status changes**
    if (distance > 0 && alertStatus != lastAlertStatus) {
        sendDataToServer(distance, smokeStatus, alertStatus);
        lastAlertStatus = alertStatus;  // Update last alert status
    }

    delay(5000);  // Wait 5 seconds before next reading
}
