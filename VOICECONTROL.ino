#include <Servo.h>
#include <SoftwareSerial.h>

// Voice recognition module setup
SoftwareSerial mySerial(2, 3); // RX, TX

// Servo setup
Servo thumbServo, indexServo, middleServo, ringServo, pinkyServo;

// Command IDs (store after training)
#define CMD_OPEN 1
#define CMD_CLOSE 2

void setup() {
    Serial.begin(9600);
    mySerial.begin(9600);

    // Attach servos
    thumbServo.attach(6);
    indexServo.attach(7);
    middleServo.attach(8);
    ringServo.attach(9);
    pinkyServo.attach(10);

    Serial.println("Voice-Controlled Hand Ready!");
}

void loop() {
    if (mySerial.available()) {
        int command = mySerial.read();

        if (command == CMD_OPEN) {
            openHand();
        } 
        else if (command == CMD_CLOSE) {
            closeHand();
        }
    }
}

// Open Hand Function
void openHand() {
    thumbServo.write(0);
    indexServo.write(0);
    middleServo.write(0);
    ringServo.write(0);
    pinkyServo.write(0);
    Serial.println("Opening Hand...");
}

// Close Hand Function
void closeHand() {
    thumbServo.write(180);
    indexServo.write(180);
    middleServo.write(180);
    ringServo.write(180);
    pinkyServo.write(180);
    Serial.println("Closing Hand...");
}

