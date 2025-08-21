import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import time

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Open YouTube once per session
youtube_opened = False

# Finger tip indices (based on MediaPipe model)
FINGER_TIPS = [8, 12, 16, 20]
THUMB_TIP = 4

# Start webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty frame.")
            continue

        # Flip and convert the image to RGB
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and find hands
        results = hands.process(rgb_image)

        # Draw hand landmarks and extract gesture
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = image.shape
                    lm_list.append((int(lm.x * w), int(lm.y * h)))

                # Count how many fingers are up
                fingers_up = []

                if lm_list:
                    # Thumb
                    fingers_up.append(lm_list[THUMB_TIP][0] > lm_list[THUMB_TIP - 1][0])
                    
                    # Fingers
                    for tip in FINGER_TIPS:
                        fingers_up.append(lm_list[tip][1] < lm_list[tip - 2][1])  # If tip is above PIP joint

                    # Interpret gestures
                    total_fingers = fingers_up.count(True)

                    if total_fingers == 1 and fingers_up[1]:  # Only index finger up
                        pyautogui.press("right")  # Next slide
                        time.sleep(1)

                    elif total_fingers == 2 and fingers_up[1] and fingers_up[2]:  # Index and middle up
                        pyautogui.press("left")  # Previous slide
                        time.sleep(1)

                    elif total_fingers == 1 and fingers_up[0] and not youtube_opened:  # Thumb up
                        webbrowser.open("https://www.youtube.com")
                        youtube_opened = True
                        time.sleep(2)

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show the output
        cv2.imshow('Hand Gesture Controller', image)

        if cv2.waitKey(5) & 0xFF == 27:  # ESC to quit
            break

cap.release()
cv2.destroyAllWindows()
