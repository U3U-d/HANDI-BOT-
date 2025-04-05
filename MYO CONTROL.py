import serial
import time

# Replace this with your Arduino port
SERIAL_PORT = 'COM3'  # or '/dev/ttyUSB0' or '/dev/ttyACM0' for Linux/macOS
BAUD_RATE = 9600

# EMG thresholds
ACTIVATION_THRESHOLD = 600  # You can tune this based on your signals

def process_emg_value(emg_value):
    """
    Determines muscle activity based on EMG value.
    """
    if emg_value > ACTIVATION_THRESHOLD:
        print(f"💪 Muscle activated! EMG: {emg_value}")
        # You could trigger actions here (e.g., move robot, close hand)
    else:
        print(f"😴 Muscle relaxed. EMG: {emg_value}")

def listen_to_emg_sensor():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print("📡 Listening to EMG sensor...")
            time.sleep(2)

            while True:
                if ser.in_waiting:
                    line = ser.readline().decode().strip()
                    if line:
                        try:
                            emg_value = int(line)
                            process_emg_value(emg_value)
                        except ValueError:
                            print(f"⚠️ Invalid EMG data: {line}")
    except serial.SerialException:
        print(f"❌ Could not connect to Arduino on port {SERIAL_PORT}.")
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")

if __name__ == "__main__":
    listen_to_emg_sensor()
