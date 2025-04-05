import serial
import time

# CONFIGURE THIS TO YOUR SYSTEM
SERIAL_PORT = 'COM3'  # Change this to your Arduino's port
BAUD_RATE = 9600  # Must match Arduino baud rate


def handle_command(command):
    """
    Executes logic based on recognized voice command.
    """
    command = command.strip().upper()

    if command == "OPEN":
        print("🟢 Opening robotic hand...")
        # Insert code to open robot hand
    elif command == "CLOSE":
        print("🔴 Closing robotic hand...")
        # Insert code to close robot hand
    elif command == "WAVE":
        print("👋 Waving hand...")
        # Insert code to wave
    elif command == "POINT":
        print("👉 Pointing...")
        # Insert point gesture code here
    elif command == "STOP":
        print("🛑 Stopping all movements...")
        # Insert stop command
    else:
        print(f"⚠️ Unknown command received: {command}")


def listen_to_arduino():
    """
    Listens for commands from the Arduino over serial and handles them.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to Arduino on {SERIAL_PORT} at {BAUD_RATE} baud.")
            time.sleep(2)  # Allow Arduino time to reset

            while True:
                if ser.in_waiting:
                    command = ser.readline().decode().strip()
                    if command:
                        print(f"🗣️ Voice Command: {command}")
                        handle_command(command)

    except serial.SerialException:
        print(f"❌ Could not connect to Arduino on port {SERIAL_PORT}. Check the port and try again.")
    except KeyboardInterrupt:
        print("\n🛑 Stopped listening. Exiting program.")


if __name__ == "__main__":
    listen_to_arduino()
