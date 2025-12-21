# 📸 Smart Attendance System

An intelligent, real-time facial recognition attendance tracking system built with deep learning. This offline-capable application uses state-of-the-art FaceNet embeddings and MTCNN face detection to automatically mark attendance via webcam.

## ✨ Features

- **🎯 Real-time Face Detection**: Utilizes MTCNN (Multi-task Cascaded Convolutional Networks) for accurate face detection
- **🧠 Deep Learning Recognition**: Employs pretrained FaceNet model for generating 512-dimensional face embeddings
- **📊 High Accuracy**: Cosine similarity-based matching with configurable threshold for precise identification
- **💾 Offline Operation**: Runs completely offline after initial model download
- **📝 Automated Logging**: Automatically records attendance to CSV with timestamps
- **🖥️ Live Preview**: Real-time OpenCV overlay showing recognized names and roll numbers
- **⚡ Session-based**: Smart detection ensures attendance is marked only once per session

## 🛠️ Technology Stack

- **Python 3.9+**
- **TensorFlow/Keras**: Deep learning framework
- **keras-facenet**: FaceNet model implementation
- **MTCNN**: Face detection
- **OpenCV**: Real-time video processing
- **NumPy**: Numerical computations

## 📋 Prerequisites

- Python 3.9 or higher
- Webcam
- macOS, Linux, or Windows

### For Apple Silicon (M1/M2) Users

This project is optimized for Apple Silicon and uses:
- `tensorflow-macos`
- `tensorflow-metal` (for GPU acceleration)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vansh-09/Smart-Attendence-.git
cd Smart-Attendence-
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

**Standard Installation:**
```bash
pip install -r requirements.txt
```

**Apple Silicon (M1/M2) Installation:**
```bash
pip uninstall -y tensorflow
pip install tensorflow-macos tensorflow-metal
pip install keras-facenet mtcnn opencv-python Pillow numpy
```

## 📁 Project Structure

```
smart-attendance/
├── data/
│   └── reference/          # Store reference face images here
│       ├── img1.jpg
│       ├── img2.jpg
│       └── embedding.json  # Generated embeddings
├── logs/
│   └── attendance.csv      # Attendance records
├── models/
│   └── 20180402-114759/    # Cached FaceNet model weights
├── src/
│   ├── detector.py         # Face detection logic
│   ├── embedder.py         # Embedding generation
│   ├── reference.py        # Reference image handling
│   ├── recognizer.py       # Face recognition
│   ├── ui.py               # OpenCV UI overlay
│   └── attendance.py       # Attendance logging
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── PRD.md                  # Product requirements document
└── README.md              # This file
```

## 🎓 Usage

### Step 1: Enroll Reference Images

1. Place **two clear, frontal face images** in the `data/reference/` directory
   - Images should be well-lit
   - Face should be clearly visible
   - Supported formats: JPG, JPEG, PNG

2. Generate the reference embedding:

```bash
python main.py --enroll --name "Your Name" --roll "YOUR_ROLL_NUMBER"
```

**Example:**
```bash
python main.py --enroll --name "Vansh Jain" --roll "AI23DS042"
```

This creates `data/reference/embedding.json` containing the averaged face embedding.

### Step 2: Run Attendance System

Start the real-time attendance tracking:

```bash
python main.py
```

**With custom threshold:**
```bash
python main.py --threshold 0.6
```

- **Lower threshold (0.5)**: More lenient matching (may increase false positives)
- **Higher threshold (0.7)**: Stricter matching (may increase false negatives)
- **Default: 0.6** (balanced performance)

### Step 3: Mark Attendance

- Stand in front of the webcam
- The system will detect and recognize your face
- Once recognized, attendance is automatically logged to `logs/attendance.csv`
- Press **'q'** to quit

## 📊 Attendance Log Format

The `logs/attendance.csv` file contains:

| Name | Roll Number | Timestamp |
|------|-------------|-----------|
| Vansh Jain | AI23DS042 | 2024-12-21 09:30:15 |

## 🔧 Configuration

### Adjusting Recognition Threshold

Edit `src/recognizer.py`:

```python
# Default threshold
THRESHOLD = 0.6  # Adjust between 0.4-0.8
```

Or use command-line argument:
```bash
python main.py --threshold 0.55
```

### Camera Settings

Edit `main.py` to change camera source:

```python
cap = cv2.VideoCapture(0)  # 0 for default camera, 1 for external
```

## 🐛 Troubleshooting

### SSL Certificate Error (macOS Python 3.12+)

**Solution 1: Run Certificate Installer**
```bash
open "/Applications/Python 3.12/Install Certificates.command"
```

**Solution 2: Set Certificate Path Manually**
```bash
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
```

### Model Download Issues

**Problem**: FaceNet model fails to download in offline/air-gapped environments

**Solution**: 
1. Download model on a networked machine (same Python/TensorFlow setup)
2. Copy the cached model from `models/` directory
3. Transfer to the offline machine's `models/` folder

### Low Recognition Accuracy

**Solutions**:
- Ensure good lighting conditions
- Use high-quality reference images
- Try adjusting the threshold
- Ensure face is frontal and unobstructed
- Re-enroll with better reference images

### TensorFlow Installation Issues

**For macOS (Apple Silicon)**:
```bash
pip install --upgrade pip
pip install tensorflow-macos tensorflow-metal
```

**For Linux/Windows**:
```bash
pip install tensorflow
```

## 🎯 Performance Tips

1. **Image Quality**: Use high-resolution, well-lit reference images
2. **Lighting**: Ensure consistent lighting during enrollment and recognition
3. **Distance**: Maintain 1-2 feet distance from webcam
4. **Angle**: Keep face frontal (avoid extreme angles)
5. **CPU Performance**: First run may be slow due to TensorFlow initialization

## 📝 Requirements

```txt
tensorflow>=2.10.0
keras-facenet>=0.3.2
mtcnn>=0.1.1
opencv-python>=4.7.0
Pillow>=9.0.0
numpy>=1.23.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Vansh Jain**
- GitHub: [@vansh-09](https://github.com/vansh-09)

## 🙏 Acknowledgments

- FaceNet: [Schroff et al., 2015](https://arxiv.org/abs/1503.03832)
- MTCNN: [Zhang et al., 2016](https://arxiv.org/abs/1604.02878)
- keras-facenet library

## 📧 Support

For issues and questions:
- Open an [Issue](https://github.com/vansh-09/Smart-Attendence-/issues)
- Check existing documentation
- Review troubleshooting section

---

**Note**: This system is designed for educational purposes and small-scale deployments. For production use, consider additional security measures and compliance with privacy regulations.