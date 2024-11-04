#include <Arduino.h>

const int trigPin = 5;   // Pin Trig del sensor HC-SR04
const int echoPin = 18;  // Pin Echo del sensor HC-SR04

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'd') {
      // Generar un pulso en el pin Trig
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);

      // Leer el tiempo del pulso en el pin Echo
      long duration = pulseIn(echoPin, HIGH);
      // Calcular la distancia en cm
      int distance = duration * 0.034 / 2;

      // Enviar la distancia al puerto serial
      Serial.println(distance);
    }
  }
}
