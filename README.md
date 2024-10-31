# HandTrack3D: Interactive Hand Tracking System

A sophisticated real-time hand tracking system that combines depth estimation, gesture recognition, and interactive zone detection for creating engaging human-computer interaction experiences.

## 🌟 Features

- **Real-time Hand Tracking**: Utilizes MediaPipe for accurate hand landmark detection
- **Depth Estimation**: Implements DepthAnything model for precise depth perception
- **Interactive Zones**: Create custom interaction areas with visual feedback
- **MQTT Integration**: Real-time communication for distributed systems
- **Visual Feedback**: Dynamic UI with progress tracking and status indicators
- **Sound Effects**: Audio feedback for enhanced user experience
- **Performance Monitoring**: Real-time FPS counter and system statistics

## 🏗️ System Architecture

The system is built with a modular architecture that ensures high performance and maintainability:

[System Architecture Diagram will be here]

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/armanruet/HandTrack3D.git
cd HandTrack3D
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

## 📦 Dependencies

- Python 3.8+
- OpenCV
- MediaPipe
- PyTorch
- Paho-MQTT
- Pygame
- NumPy
- PIL

## 🎮 Usage

1. **Launch the application**
   - The system will automatically access your camera
   - A fullscreen window will open showing the camera feed

2. **Create interaction zones**
   - Click and drag to draw up to 3 interaction zones
   - Each zone will be automatically labeled (A, B, C)

3. **Interact with zones**
   - Move your hand within the zones
   - Watch for visual and audio feedback
   - Monitor progress through the status bar

4. **Controls**
   - Press 'q' to quit
   - Press 'f' to toggle fullscreen

## 🛠️ Configuration

Key parameters can be adjusted in `config.py`:

```python
# UI Parameters
BOX_LINE_THICKNESS = 3
TARGET_BOX_COLOR = (0, 255, 0)
NON_TARGET_BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Depth Thresholds
DEPTH_THRESHOLD_NEAR = 0.20
DEPTH_THRESHOLD_FAR = 0.63
```

## 🔧 Advanced Features

### Depth Estimation
The system uses the DepthAnything model for accurate depth perception:
```python
depth_anything = DepthAnything.from_pretrained(f"LiheYoung/depth_anything_{encoder}14")
```

### MQTT Communication
Integrated MQTT broker for distributed system communication:
```python
client.connect("your-broker-address", 1883, 60)
```

## 📊 Performance

The system includes built-in performance monitoring:
- Real-time FPS counter
- Hand detection status
- Interaction timer
- Progress tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MediaPipe team for their excellent hand tracking solution
- DepthAnything team for their depth estimation model
- All contributors and supporters of this project

## 📞 Contact

For questions and support, please open an issue or contact the maintainers:
- Email: armanruet@gmail.com
- LinkedIn: @armanruet

---
Made with ❤️ by Arman
