
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int servoPins[5] = {0, 1, 2, 3, 4};  // PCA9685 channels for 5 servos
int minPulse = 150;  // Adjust based on your servo
int maxPulse = 600;  // Adjust based on your servo
int neutralPulse = (minPulse + maxPulse) / 2; // Pulse width for 0 degrees

void setup() {
    Serial.begin(9600);
    pwm.begin();
    pwm.setPWMFreq(50);  // Standard for servos (50Hz)
    Serial.println("Ready to move servos.");
}

void loop() {
    // Move servos from 0° to 90°
    for (int angle = 0; angle <= 90; angle += 5) {  
        for (int i = 0; i < 5; i++) {
            int pulse = map(angle, 0, 90, neutralPulse, maxPulse);  // Mapping 0-90 degrees
            pwm.setPWM(servoPins[i], 0, pulse);
        }
        delay(20);  
    }

    delay(100);  // Short pause at 90°

    // Move servos back from 90° to 0°
    for (int angle = 90; angle >= 0; angle -= 5) {  
        for (int i = 0; i < 5; i++) {
            int pulse = map(angle, 0, 90, neutralPulse, maxPulse);  // Mapping 0-90 degrees
            pwm.setPWM(servoPins[i], 0, pulse);
        }
        delay(20);  
    }

    delay(800);  // Short pause at 0°
}

