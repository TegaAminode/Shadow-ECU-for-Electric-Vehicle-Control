#include <Servo.h>

Servo brakeServo;

// CONFIG
const int BRAKE_PIN = 9;          // Servo (brake) actuator pin
const int LED_PIN = 13;           // LED pin (external)
const int FALLBACK_TIMEOUT = 2000; // 2 sec without commands, auto-release
//

unsigned long lastCommandTime = 0;
String incoming = "";

void setup() {
  Serial.begin(9600);
  brakeServo.attach(BRAKE_PIN);
  brakeServo.write(0);  // Brake released
  pinMode(LED_PIN, OUTPUT);  // Setup LED pin
  digitalWrite(LED_PIN, LOW); // LED off initially
  lastCommandTime = millis();

  Serial.println("Shadow ECU Ready");
}

void applyBrake() {
  brakeServo.write(90);           // Apply brake, 90 degrees on servo
  digitalWrite(LED_PIN, HIGH);    // Turn LED on
}

void releaseBrake() {
  brakeServo.write(0);            // Release brake, return to 0 degrees
  digitalWrite(LED_PIN, LOW);     // Turn LED off
}

void loop() {
  // Read new messages from logger.py
  if (Serial.available()) {
    incoming = Serial.readStringUntil('\n');
    incoming.trim();

    lastCommandTime = millis();   // Reset fallback timer

    if (incoming == "STOP") {
      applyBrake();
      Serial.println("BRAKE_APPLIED");
    }
    else if (incoming == "CLEAR") {
      releaseBrake();
      Serial.println("BRAKE_RELEASED");
    }
  }

  // Safety Fallback, If no messages received, release brake
  if (millis() - lastCommandTime > FALLBACK_TIMEOUT) {
      releaseBrake();
      Serial.println("FALLBACK_RELEASE");
      lastCommandTime = millis();
  }
}