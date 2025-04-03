#include <Servo.h>

Servo handServo;  // Create Servo object
const int emgPin = A0; // EMG Sensor signal connected to A0
int emgValue = 0;  // Store muscle sensor reading

void setup() {
    Serial.begin(9600);  // Start serial monitor
    handServo.attach(9);  // Attach servo to pin 9
    handServo.write(0);   // Start with hand in open position
}

void loop() {
    emgValue = analogRead(emgPin); // Read muscle sensor data
    Serial.println(emgValue); // Print value to Serial Monitor

    // Adjust movement based on muscle intensity
    if (emgValue > 300) {  // Adjust threshold based on testing
        handServo.write(90);  // Move servo to gripping position
    } else {
        handServo.write(0);  // Open hand
    }

    delay(100);  // Small delay for stability
}
