#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Create a PCA9685 object
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Servo configuration
#define SERVO_MIN 150  // Pulse length for 0 degrees
#define SERVO_MAX 600  // Pulse length for 180 degrees
#define NUM_SERVOS 5   // Number of servos (Thumb, Index, Middle, Ring, Pinky)

int servoPins[NUM_SERVOS] = {0, 1, 2, 3, 4}; // Channels on the PCA9685
int servoStates[NUM_SERVOS] = {0, 0, 0, 0, 0}; // Finger bending states

void setup() {
    Serial.begin(9600);
    pwm.begin();
    pwm.setPWMFreq(60);  // Set frequency to 60Hz for servos
}

void loop() {
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n'); // Read incoming data
        int newStates[NUM_SERVOS];

        // Parse comma-separated values
        int index = 0;
        char *token = strtok((char *)data.c_str(), ",");
        while (token != NULL && index < NUM_SERVOS) {
            newStates[index] = atoi(token);
            token = strtok(NULL, ",");
            index++;
        }

        // Update servo positions based on finger states
        for (int i = 0; i < NUM_SERVOS; i++) {
            if (newStates[i] != servoStates[i]) {
                servoStates[i] = newStates[i];

                // Map states (0-3) to servo angles
                int angle = map(servoStates[i], 0, 3, 0, 90);
                int pulseWidth = map(angle, 0, 90, SERVO_MIN, SERVO_MAX);
                pwm.setPWM(servoPins[i], 0, pulseWidth);
            }
        }
    }
}








