# 🖐️ Gesture Controlled Mouse & Navigation Using Python + MediaPipe

## Control your entire computer using hand gestures in front of your webcam — no special hardware required!

This project uses:

- MediaPipe Hands (hand tracking)

- OpenCV (video input)

- PyAutoGUI (mouse + keyboard control)

- Real-time gesture recognition

- Drag & Drop, Scroll, Swipe, Right Click, etc.

# ✨ Features

✔ Mouse Cursor Control (Index Finger Tracking)

✔ Left Click (Thumb + Index Pinch)

✔ Right Click (Thumb + Index + Middle Pinch)

✔ Scroll (Index + Middle Up, Move Up/Down)

✔ Drag & Drop (Pinch & Hold to Drag, Release to Drop)

✔ Swipes Navigation

- Swipe Right → Next Window (Alt+Tab)

- Swipe Left → Previous Window (Shift+Alt+Tab)

- Swipe Up → Task View

- Swipe Down → Minimize All

✔ Calibration System (Top & Bottom alignment)
✔ Noise Filtering & Smoothing (Hybrid Kalman + EMA Filter)

No gloves, sensors, or depth cameras needed. Just a regular laptop webcam.

# 🖥️ Demo (Gestures Overview)
| Gesture                    | Action                |
| -------------------------- | --------------------- |
| ☝ Index Up                 | Move Mouse            |
| 🤏 Thumb + Index           | Left Click            |
| 🤏 Thumb + Index + Middle  | Right Click           |
| ✌ Index + Middle Up + Move | Scroll                |
| 🤏 (Hold) → Move           | Drag & Drop           |
| 🖐 Swipe Right             | Next Window (Alt+Tab) |
| 🖐 Swipe Left              | Previous Window       |
| 🖐 Swipe Up                | Task View             |
| 🖐 Swipe Down              | Minimize Windows      |

# 📦 Dependencies

- Python 3.11.x recommended

- VSCode

- pip package manager

## Python Libraries
| Library         | Purpose                  |
| --------------- | ------------------------ |
| `opencv-python` | Webcam feed              |
| `mediapipe`     | Hand landmark detection  |
| `pyautogui`     | Mouse & keyboard control |
| `numpy`         | Math & filtering         |
| `time`          | Timing / debounce        |

# 🛠️ Installation & Setup
1. Install Python 3.11

Download from:
 - https://www.python.org/downloads/

> ⚠ Make sure to check “Add to PATH” during installation.

# 🧰 VSCode Configuration Guide

### 1. Install VSCode

- https://code.visualstudio.com/

### 2. Install Extensions

Recommended extensions:

- Python (Microsoft)

- Pylance

- Code Runner (optional)

### 3. Clone this Repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```
### 4. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```
Activate it:
```bash
.\.venv\Scripts\Activate.ps1
```
### 5. Install Requirements
```bash
pip install -r requirements.txt
```

If you don’t have a requirements file, install manually:
```bash
pip install opencv-python mediapipe pyautogui numpy
```
### 6. Select Python Interpreter

Inside VSCode:
```bash
Ctrl + Shift + P → "Python: Select Interpreter"
```

Choose:
```bash
./.venv/Scripts/python.exe
```
### 7. Enable Webcam Permissions (Windows)

Go to:
```
Settings → Privacy → Camera → Allow desktop apps
```
> Make sure VSCode is allowed to use the camera.

# 🚀 Run the Program

Once dependencies are installed:
```bash
python main.py
```
Then follow calibration instructions:
```
1) Raise finger to TOP → press SPACE
2) Lower finger to BOTTOM → press SPACE
```
After calibration, mouse control starts!

# 📁 Project Structure

### Example file structure:

```
gesture-mouse/
│
├── main.py
├── gesture_utils.py
├── README.md
├── requirements.txt
└── .venv/                # optional virtual environment
```
# 📌 Tips & Best Practices

- Use good lighting

- Keep hand centered

- Avoid overexposing background

- Laptop webcam works but external webcams give better FOV

# ❗ Known Limitations

- MediaPipe doesn’t detect hands well if:

   - Background is too bright

   - Hand moves too far out of frame

   - Motion blur is high

- Gesture recognition depends on camera FOV & angle

#   🧩 Future Improvements

- Hand pose ML model

- Gesture training mode

- Voice assistant integration

- Multi-hand support

- UI visual overlays

- BLE wearable for click depth

# 🤝 Contributing

Pull requests are welcome!
If major changes are suggested, please open an issue first to discuss.

# 📜 License

MIT License — free for personal & commercial usage.
