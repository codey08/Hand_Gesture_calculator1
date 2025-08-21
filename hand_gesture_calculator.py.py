import cv2
import mediapipe as mp
import time

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Finger tip indices
FINGER_TIPS = [8, 12, 16, 20]
THUMB_TIP = 4

# Variables to track calculator logic
state = "num1"  # States: num1 → op → num2 → result
num1 = 0
num2 = 0
operator = ""
result = None
last_action_time = time.time()

# Helper: Count raised fingers
def count_fingers(lm_list):
    fingers_up = []

    # Thumb
    fingers_up.append(lm_list[THUMB_TIP][0] > lm_list[THUMB_TIP - 1][0])

    # 4 Fingers
    for tip in FINGER_TIPS:
        fingers_up.append(lm_list[tip][1] < lm_list[tip - 2][1])
    return fingers_up

# Start webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)
        h, w, c = image.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
                fingers_up = count_fingers(lm_list)
                total_up = fingers_up.count(True)

                # Use time gap to avoid multiple detections
                if time.time() - last_action_time > 2:

                    if state == "num1":
                        num1 = total_up
                        state = "op"
                        last_action_time = time.time()

                    elif state == "op":
                        # Define simple operator gestures
                        if total_up == 2: operator = "+"
                        elif total_up == 1: operator = "-"
                        elif total_up == 3: operator = "*"
                        elif total_up == 4: operator = "/"
                        else: operator = ""
                        if operator:
                            state = "num2"
                            last_action_time = time.time()

                    elif state == "num2":
                        num2 = total_up
                        state = "result"
                        last_action_time = time.time()

                    elif state == "result":
                        try:
                            if operator == "+": result = num1 + num2
                            elif operator == "-": result = num1 - num2
                            elif operator == "*": result = num1 * num2
                            elif operator == "/": result = round(num1 / num2, 2) if num2 != 0 else "Err"
                            else: result = "Invalid"
                        except:
                            result = "Error"
                        state = "done"

                # Draw hand landmarks
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display status on screen
        font = cv2.FONT_HERSHEY_SIMPLEX
        if state in ["num1", "op", "num2", "result", "done"]:
            cv2.putText(image, f"State: {state}", (10, 30), font, 1, (0, 255, 0), 2)
            cv2.putText(image, f"Num1: {num1}", (10, 70), font, 1, (255, 0, 0), 2)
            cv2.putText(image, f"Op: {operator}", (10, 110), font, 1, (0, 0, 255), 2)
            cv2.putText(image, f"Num2: {num2}", (10, 150), font, 1, (255, 0, 255), 2)
            if result is not None:
                cv2.putText(image, f"Result: {result}", (10, 190), font, 1, (0, 255, 255), 2)

        # Show frame
        cv2.imshow("Calculator by Hand Gesture", image)

        # Reset on ESC
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
