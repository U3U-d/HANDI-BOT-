import os
import cv2
import mediapipe as mp
import serial
import time
import numpy as np

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize serial connection (update with your Arduino COM port)
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=1)
time.sleep(2)  # Wait for connection

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.8
)

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height


# Moving Average Filter for smoothing
class MovingAverage:
    def __init__(self, size=5):
        self.size = size
        self.values = []

    def update(self, new_value):
        self.values.append(new_value)
        if len(self.values) > self.size:
            self.values.pop(0)
        return sum(self.values) / len(self.values)  # Smoothed value


# Create filters for each finger and wrist
filters = [MovingAverage(5) for _ in range(6)]  # 5 fingers + wrist


# Function to calculate finger states (0 = closed, 4 = fully open) & wrist position
def get_finger_states_and_wrist(landmarks):
    finger_states = []

    # Thumb - Inverted value for correct mapping
    thumb_value = np.interp(landmarks[2].x - landmarks[4].x, [-0.1, 0.1], [0, 4])  # Inverted logic
    finger_states.append(int(round(filters[0].update(thumb_value))))

    # Other fingers - Compare y-values for up/down movement
    for i, (base, mid, tip) in enumerate([(5, 6, 8), (9, 10, 12), (13, 14, 16), (17, 18, 20)]):
        finger_value = np.interp(landmarks[tip].y - landmarks[mid].y, [-0.1, 0.1], [0, 4])
        finger_states.append(int(round(filters[i + 1].update(finger_value))))

    # Wrist Position (X-Axis)
    wrist_x = landmarks[0].x  # Get wrist x-position
    wrist_angle = np.interp(wrist_x, [0.2, 0.8], [-180, 180])  # Map wrist position to servo angle
    wrist_angle = int(round(filters[5].update(wrist_angle)))  # Apply smoothing

    return finger_states, wrist_angle


prev_states = [None] * 6  # Store previous states to avoid jittery updates (5 fingers + wrist)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            finger_states, wrist_angle = get_finger_states_and_wrist(hand_landmarks.landmark)

            # Only send updates if values change significantly
            for i in range(5):
                if prev_states[i] is None or abs(prev_states[i] - finger_states[i]) >= 1:
                    prev_states[i] = finger_states[i]

            # Check wrist movement update
            if prev_states[5] is None or abs(prev_states[5] - wrist_angle) >= 5:
                prev_states[5] = wrist_angle

            # Print to log and send to Arduino
            data_to_send = f"{','.join(map(str, finger_states))},{wrist_angle}"
            print(f"Data Sent: {data_to_send}")
            arduino.write(f"{data_to_send}\n".encode())

            # Display Hand Tracking
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
