import math

# Fingertip landmark index mapping (MediaPipe)
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

FINGER_TIPS = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]

def get_landmark_coords(hand_landmarks, frame_width, frame_height):
    coords = {}
    for id, lm in enumerate(hand_landmarks.landmark):
        coords[id] = (int(lm.x * frame_width), int(lm.y * frame_height))
    return coords

def finger_states(landmarks):
    states = []
    # Thumb (simple x comparison)
    if landmarks[THUMB_TIP][0] > landmarks[THUMB_TIP - 1][0]:
        states.append(1)
    else:
        states.append(0)

    # Other fingers (simple y comparison)
    for tip in [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]:
        if landmarks[tip][1] < landmarks[tip - 2][1]:
            states.append(1)
        else:
            states.append(0)

    return states  # [thumb, index, middle, ring, pinky]

def is_fist(states):
    return states == [0, 0, 0, 0, 0]

def is_open_hand(states):
    return states == [1, 1, 1, 1, 1]

def is_one_finger(states):
    return states == [0, 1, 0, 0, 0]

def is_two_fingers(states):
    return states == [0, 1, 1, 0, 0]

def pinch_distance(landmarks):
    x1, y1 = landmarks[THUMB_TIP]
    x2, y2 = landmarks[INDEX_TIP]
    return math.hypot(x2 - x1, y2 - y1)
