# 🖐️ Simple Hand Wave Chrome Tab Switcher

A lightweight Python application that uses MediaPipe to detect simple hand wave gestures and switch between Chrome tabs. Just wave your hand left or right to navigate through your browser tabs!

## ✨ Features

- **Simple wave detection** - Only left/right hand movements
- **Balanced sensitivity** - One deliberate wave = one tab change  
- **Chrome tab switching** via keyboard shortcuts
- **Real-time hand tracking** using MediaPipe
- **Docker support** for easy deployment
- **Clean modular code** structure

## 🎯 Gestures (Simple & Effective)

| Gesture | Action | Keyboard Shortcut |
|---------|--------|------------------|
| 👈 Wave Left | Previous Tab | `Ctrl + Shift + Tab` |
| 👉 Wave Right | Next Tab | `Ctrl + Tab` |

*That's it! No complex hand poses or finger counting - just simple left/right waves.*

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone and build**:
   ```bash
   git clone <repository-url>
   cd hand-gesture-tab-switcher
   docker-compose build
   ```

2. **Enable X11 forwarding** (Linux/macOS):
   ```bash
   xhost +local:docker
   ```

3. **Run the application**:
   ```bash
   docker-compose up
   ```

### Option 2: Local Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```

## 📋 Requirements

- **Camera**: Webcam or built-in camera
- **Chrome Browser**: Make sure Chrome is your active window when gesturing
- **Python 3.7+** (for local installation)
- **Docker & Docker Compose** (for containerized deployment)

### Python Dependencies

- `mediapipe==0.10.9` - Hand tracking and gesture detection
- `opencv-python==4.8.1.78` - Computer vision and camera handling
- `pyautogui==0.9.54` - Keyboard automation for tab switching
- `numpy==1.24.3` - Numerical operations

## 🖱️ Usage Instructions

1. **Start the application** using Docker or Python
2. **Position yourself** in front of the camera
3. **Open Chrome** and make it your active window
4. **Make deliberate left/right hand movements** to switch tabs
5. **Press 'q' or Ctrl+C** to quit the application

### 💡 Tips for Best Results

- **Make deliberate movements**: Clear, substantial left-to-right or right-to-left motions
- **Keep hand visible**: Ensure good lighting and contrast  
- **Wait between gestures**: 1.2 second cooldown ensures one wave = one change
- **One hand only**: Use one hand for cleaner detection
- **Consistent direction**: Move steadily in one direction for reliable detection

### 🛡️ Safety Features

- **Failsafe**: Move mouse to screen corner to emergency stop
- **Gesture cooldown**: Prevents rapid-fire tab switching (1.2 seconds)
- **Visual feedback**: Live camera view with hand tracking overlay

## 📁 Project Structure

```
hand-gesture-tab-switcher/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main application entry point
│   ├── gesture_detector.py   # Simple wave detection functions
│   └── tab_controller.py     # Chrome tab control functions
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── run.py                  # Simple entry point script
└── README.md               # This file
```

## 🔧 Configuration (Optimized for Sensitivity)

### Gesture Detection Settings

Balanced for reliable one-wave-one-change in `src/gesture_detector.py`:

- `MAX_POSITIONS = 8` - Enough positions for reliable detection
- `GESTURE_COOLDOWN = 1.2` - Prevents multiple triggers per wave
- `MOVEMENT_THRESHOLD = 60` - Requires deliberate movements
- `MIN_MOVEMENT = 40` - Substantial movement needed

### Camera Settings

Optimized settings in `src/main.py`:

- Frame size: `640x480` (good balance of speed/quality)
- FPS: `30` (smooth detection)
- Camera index: `0` (change if using external camera)

## 🐛 Troubleshooting

### Camera Issues
- **Linux**: Make sure your user is in the `video` group
- **Docker**: Ensure camera device is properly mapped in docker-compose.yml
- **macOS**: Grant camera permissions to Terminal/Docker

### Display Issues (Docker)
- **Linux**: Run `xhost +local:docker` before starting
- **macOS**: Install XQuartz and configure X11 forwarding
- **Windows**: Use WSL2 with X11 server (e.g., VcXsrv)

### Wave Detection Issues
- **Not detecting**: Try larger, more deliberate movements
- **Too sensitive**: Increase `MOVEMENT_THRESHOLD` in gesture_detector.py
- **Lighting**: Ensure good contrast between hand and background
- **Position**: Keep hand clearly visible, avoid rapid movements

## 🤝 Contributing

Feel free to contribute improvements! Areas for enhancement:

- Fine-tune sensitivity parameters
- Add gesture visualization improvements
- Cross-platform compatibility improvements
- Performance optimizations

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) - Google's ML framework for hand tracking
- [OpenCV](https://opencv.org/) - Computer vision library
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Cross-platform automation 