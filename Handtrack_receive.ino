#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Constants
#define SERVO_MIN  150  // Servo pulse min
#define SERVO_MAX  600  // Servo pulse max

// Create PCA9685 object
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// Servo channels on PCA9685
const int servo_pins[6] = {0, 1, 2, 3, 4, 5}; // Thumb, Index, Middle, Ring, Pinky, Wrist

// Function to map values (0-4 for fingers, -90 to 90 for wrist)
int mapServoPosition(int value, bool isWrist = false) {
    if (isWrist) {
        return map(value, -90, 90, SERVO_MIN, SERVO_MAX);
    }
    return map(value, 0, 4, SERVO_MIN, SERVO_MAX);
}

void setup() {
    Serial.begin(9600);
    pwm.begin();
    pwm.setPWMFreq(50); // Set frequency to 50Hz (typical for servos)
    delay(500);
}

void loop() {
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');
        data.trim();

        int values[6];
        int index = 0;

        char* token = strtok(const_cast<char*>(data.c_str()), ",");
        while (token != nullptr && index < 6) {
            values[index++] = atoi(token);
            token = strtok(nullptr, ",");
        }

        if (index == 6) {  // Ensure valid data received
            for (int i = 0; i < 5; i++) {
                int servo_pos = mapServoPosition(values[i]);
                pwm.setPWM(servo_pins[i], 0, servo_pos);
            }

            int wrist_pos = mapServoPosition(values[5], true);
            pwm.setPWM(servo_pins[5], 0, wrist_pos);

            Serial.println("Servos Updated");
        }
    }
}





