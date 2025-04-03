#include <Servo.h>

// Create Servo objects for each finger
Servo thumbServo, indexServo, middleServo, ringServo, pinkyServo;

// Assign flex sensors to analog pins
const int thumbSensor = A0;
const int indexSensor = A1;
const int middleSensor = A2;
const int ringSensor = A3;
const int pinkySensor = A4;

void setup() {
    Serial.begin(9600);
    
    // Attach servos to digital pins
    thumbServo.attach(6);
    indexServo.attach(7);
    middleServo.attach(8);
    ringServo.attach(9);
    pinkyServo.attach(10);
}

void loop() {
    // Read values from flex sensors
    int thumbVal = analogRead(thumbSensor);
    int indexVal = analogRead(indexSensor);
    int middleVal = analogRead(middleSensor);
    int ringVal = analogRead(ringSensor);
    int pinkyVal = analogRead(pinkySensor);

    // Convert sensor values to servo angles (adjust min/max mapping)
    int thumbAngle = map(thumbVal, 600, 900, 0, 180);
    int indexAngle = map(indexVal, 600, 900, 0, 180);
    int middleAngle = map(middleVal, 600, 900, 0, 180);
    int ringAngle = map(ringVal, 600, 900, 0, 180);
    int pinkyAngle = map(pinkyVal, 600, 900, 0, 180);

    // Move servos based on sensor readings
    thumbServo.write(thumbAngle);
    indexServo.write(indexAngle);
    middleServo.write(middleAngle);
    ringServo.write(ringAngle);
    pinkyServo.write(pinkyAngle);

    // Print values for debugging
    Serial.print("Thumb: "); Serial.print(thumbVal);
    Serial.print(" | Index: "); Serial.print(indexVal);
    Serial.print(" | Middle: "); Serial.print(middleVal);
    Serial.print(" | Ring: "); Serial.print(ringVal);
    Serial.print(" | Pinky: "); Serial.println(pinkyVal);

    delay(100);  // Small delay for stability
}

