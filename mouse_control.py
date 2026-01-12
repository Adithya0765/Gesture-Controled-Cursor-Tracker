import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from gesture_utils import get_landmark_coords, finger_states

# ==========================
# Hybrid Filter (smooth)
# ==========================
class HybridFilter:
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.prev = None
        self.p = 1.0
        self.q = 0.02
        self.r = 0.01

    def update(self, m):
        self.p += self.q
        k = self.p / (self.p + self.r)
        est = m if self.prev is None else self.prev + k * (m - self.prev)
        self.p *= (1 - k)
        if self.prev is None:
            self.prev = est
        else:
            self.prev = self.alpha * est + (1 - self.alpha) * self.prev
        return self.prev

# ==========================
# Setup
# ==========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.8
)

screen_w, screen_h = pyautogui.size()

hf_x = HybridFilter()
hf_y = HybridFilter()

prev_x, prev_y = None, None
prev_scroll_y = None

# Calibration variables
top_calib = None
bottom_calib = None
calibration_stage = 0 

# Click variables
left_pinch_frames = 0
right_pinch_frames = 0
pinch_required = 4
click_threshold = 40

# Drag/Drop Variables
drag_active = False
drag_threshold = 8  # frames for drag hold

# Swipe Variables
prev_palm = None
last_swipe_time = time.time()
swipe_cooldown = 0.6
swipe_speed_x = 0.08
swipe_speed_y = 0.08
min_travel = 0.12
min_velocity = 0.08

print("\nCalibration Mode Active")
print("1) Raise finger to TOP → press SPACE")
print("2) Lower finger to BOTTOM → press SPACE")
print("Then control begins...\n")

# ==========================
# Distance Helper
# ==========================
def dist(a, b):
    return np.hypot(a[0]-b[0], a[1]-b[1])

# ==========================
# Main Loop
# ==========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    key = cv2.waitKey(1)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            lm = get_landmark_coords(hand, w, h)
            states = finger_states(lm)
            ix, iy = lm[8]

            index_up = states[1] == 1
            middle_up = states[2] == 1

            thumb_tip = lm[4]
            index_tip = lm[8]
            middle_tip = lm[12]

            dist_thumb_index = dist(thumb_tip, index_tip)
            dist_thumb_middle = dist(thumb_tip, middle_tip)

            # ==========================
            # SWIPE DETECTION (Improved)
            # ==========================
            palm_x = (hand.landmark[0].x + hand.landmark[5].x + hand.landmark[17].x) / 3
            palm_y = (hand.landmark[0].y + hand.landmark[5].y + hand.landmark[17].y) / 3

            dx = dy = 0
            now = time.time()

            # Only detect swipes if palm mode (index+middle DOWN)
            if not index_up and not middle_up:
                if prev_palm is not None:
                    dx = palm_x - prev_palm[0]
                    dy = palm_y - prev_palm[1]

                    if now - last_swipe_time > swipe_cooldown:
                        # Swipe Right
                        if dx > min_travel and dx > min_velocity:
                            pyautogui.keyDown('alt'); pyautogui.press('tab'); pyautogui.keyUp('alt')
                            last_swipe_time = now

                        # Swipe Left
                        elif dx < -min_travel and dx < -min_velocity:
                            pyautogui.keyDown('alt'); pyautogui.keyDown('shift'); pyautogui.press('tab')
                            pyautogui.keyUp('shift'); pyautogui.keyUp('alt')
                            last_swipe_time = now

                        # Swipe Up
                        elif dy < -min_travel and dy < -min_velocity:
                            pyautogui.hotkey('win','tab')
                            last_swipe_time = now

                        # Swipe Down
                        elif dy > min_travel and dy > min_velocity:
                            pyautogui.hotkey('win','m')
                            last_swipe_time = now

            prev_palm = (palm_x, palm_y)

            # ==========================
            # Calibration Stage
            # ==========================
            if calibration_stage < 2:
                if calibration_stage == 0:
                    cv2.putText(frame, "Calibrate TOP → Press SPACE", (10,40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
                else:
                    cv2.putText(frame, "Calibrate BOTTOM → Press SPACE", (10,40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

                if key == 32:
                    if calibration_stage == 0:
                        top_calib = iy
                        calibration_stage = 1
                        print("TOP calibrated at y =", iy)
                    elif calibration_stage == 1:
                        bottom_calib = iy
                        calibration_stage = 2
                        print("BOTTOM calibrated at y =", iy)
                        print("\nCalibration complete! Finger controls mouse.\n")
                continue

            # ==========================
            # MOUSE ACTIVE
            # ==========================
            cv2.putText(frame, "Mouse Active", (10,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            # ==========================
            # Mouse Move (Index Up)
            # ==========================
            if index_up and not middle_up:
                screen_x = np.interp(ix, [0, w], [0, screen_w])
                screen_y = np.interp(iy, [top_calib, bottom_calib], [0, screen_h])

                filtered_x = hf_x.update(screen_x)
                filtered_y = hf_y.update(screen_y)

                if prev_x is not None:
                    filtered_x = prev_x + 0.15 * (filtered_x - prev_x)
                    filtered_y = prev_y + 0.15 * (filtered_y - prev_y)

                if not drag_active:
                    pyautogui.moveTo(filtered_x, filtered_y, duration=0)
                else:
                    pyautogui.dragTo(filtered_x, filtered_y, duration=0)

                prev_x, prev_y = filtered_x, filtered_y
            else:
                prev_x = prev_y = None

            # ==========================
            # LEFT CLICK + DRAG (Pinch)
            # ==========================
            if dist_thumb_index < click_threshold and not middle_up:
                left_pinch_frames += 1

                # START DRAG
                if left_pinch_frames == drag_threshold and not drag_active:
                    pyautogui.mouseDown()
                    drag_active = True

            else:
                # RELEASE DRAG
                if drag_active:
                    pyautogui.mouseUp()
                    drag_active = False

                # SINGLE CLICK
                if left_pinch_frames >= pinch_required:
                    pyautogui.click()

                left_pinch_frames = 0

            # ==========================
            # RIGHT CLICK (Pinch Thumb + Index + Middle)
            # ==========================
            if dist_thumb_index < click_threshold and dist_thumb_middle < click_threshold and middle_up:
                right_pinch_frames += 1
            else:
                right_pinch_frames = 0

            if right_pinch_frames == pinch_required:
                pyautogui.rightClick()
                right_pinch_frames = 0

            # ==========================
            # SCROLL (Index + Middle Up)
            # ==========================
            if index_up and middle_up:
                if prev_scroll_y is not None:
                    dy = iy - prev_scroll_y
                    if abs(dy) > 5:
                        pyautogui.scroll(int(-dy * 3))
                prev_scroll_y = iy
            else:
                prev_scroll_y = None

    cv2.imshow("Gesture Mouse | Drag | Scroll | Swipe", frame)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
