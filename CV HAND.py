import cv2
import mediapipe as mp
import serial
import time

# Initialize Serial Connection (Check COM port in Arduino IDE)
arduino = serial.Serial('COM8', 19200, timeout=1)  # Baud rate set to 19200
time.sleep(2)  # Allow time for connection

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Open Camera
cap = cv2.VideoCapture(0)


def get_finger_states(hand_landmarks):
    """
    Detects whether fingers are open or closed based on landmark positions.
    Returns a list of binary values (1=open, 0=closed).
    """
    finger_states = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky

    # Thumb (compare tip with MCP joint)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:  # Adjust for left/right hand
        finger_states[0] = 1

    # Other fingers (compare tip with PIP joint)
    finger_tip_ids = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    for i, tip_id in enumerate(finger_tip_ids):
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            finger_states[i + 1] = 1

    return finger_states


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally for better hand tracking
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get Finger States (1 = Open, 0 = Closed)
            finger_data = get_finger_states(hand_landmarks)

            # Reverse the logic: 1 = Closed, 0 = Open (Reverse direction)
            reversed_data = [1 - state for state in finger_data]  # Inverting the state

            command = "$" + "".join(map(str, reversed_data)) + "\n"  # e.g., "$11100\n"

            # Send Data to Arduino
            arduino.write(command.encode('utf-8'))
            print("Sent:", command)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()
