import serial
import time

# Serial Configuration
SERIAL_PORT = 'COM3'  # Replace with your port (e.g., /dev/ttyUSB0 or COM4)
BAUD_RATE = 9600

# Thresholds: Values above this are considered 'bent'
FINGER_BEND_THRESHOLDS = {
    'Thumb': 600,
    'Index': 600,
    'Middle': 600,
    'Ring': 600,
    'Pinky': 600
}

def parse_finger_data(data):
    try:
        values = list(map(int, data.strip().split(',')))
        if len(values) != 5:
            print(f"⚠️ Expected 5 values, got {len(values)}: {data}")
            return None
        return values
    except ValueError:
        print(f"⚠️ Failed to parse data: {data}")
        return None

def detect_finger_states(values):
    labels = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    states = {}

    for label, value in zip(labels, values):
        threshold = FINGER_BEND_THRESHOLDS[label]
        state = 'Bent' if value > threshold else 'Straight'
        states[label] = state

    return states

def trigger_actions(finger_states):
    if all(state == 'Bent' for state in finger_states.values()):
        print("✊ Full fist detected! Could trigger: 'Close hand'")
    elif all(state == 'Straight' for state in finger_states.values()):
        print("🖐️ Open hand detected! Could trigger: 'Open hand'")
    elif finger_states['Index'] == 'Bent' and all(finger_states[f] == 'Straight' for f in ['Thumb', 'Middle', 'Ring', 'Pinky']):
        print("👉 Pointing detected! Could trigger: 'Point gesture'")
    elif finger_states['Thumb'] == 'Bent' and all(finger_states[f] == 'Straight' for f in ['Index', 'Middle', 'Ring', 'Pinky']):
        print("👍 Thumbs up detected!")
    else:
        print("✋ Hand in neutral or mixed gesture.")

def display_finger_data(values, finger_states):
    print("\n🤖 Finger Sensor Data:")
    for (label, val) in zip(finger_states.keys(), values):
        print(f"  {label}: {val} ({finger_states[label]})")
    print("-" * 35)

def listen_to_finger_sensors():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print("📡 Listening for finger sensor data...")
            time.sleep(2)

            while True:
                if ser.in_waiting:
                    line = ser.readline().decode().strip()
                    if line:
                        values = parse_finger_data(line)
                        if values:
                            finger_states = detect_finger_states(values)
                            display_finger_data(values, finger_states)
                            trigger_actions(finger_states)

    except serial.SerialException:
        print(f"❌ Could not connect to Arduino on port {SERIAL_PORT}.")
    except KeyboardInterrupt:
        print("\n🛑 Program stopped by user.")

if __name__ == "__main__":
    listen_to_finger_sensors()
