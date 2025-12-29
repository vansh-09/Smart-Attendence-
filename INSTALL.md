# 🚀 Installation & Distribution Guide

## Quick Start (Recommended)

### macOS with Homebrew (Coming Soon)

```bash
brew tap yourusername/smart-attendance
brew install smart-attendance
smart-attendance
```

### Using Pip (Recommended for all platforms)

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-attendance.git
cd smart-attendance

# Run the installer script
chmod +x install.sh
./install.sh

# Or manual installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Run the application
smart-attendance
```

### Using Docker

```bash
docker-compose up -d smart-attendance
docker-compose exec smart-attendance smart-attendance
```

### Direct Python Execution

```bash
python3 main.py
```

---

## System Requirements

- **Python**: 3.10 or higher
- **OS**: macOS, Linux, Windows (WSL2)
- **RAM**: 4GB minimum (8GB recommended)
- **GPU** (Optional): NVIDIA GPU with CUDA for faster training

### macOS Specific

On Apple Silicon (M1/M2/M3):

```bash
pip install tensorflow-macos tensorflow-metal
```

On Intel macOS:

```bash
pip install tensorflow
```

---

## Distribution Methods

### 1. PyPI Distribution

```bash
# Build the package
python3 -m build

# Upload to PyPI
twine upload dist/*

# Install from PyPI
pip install smart-attendance
```

### 2. Homebrew Distribution

1. Create a tap: `homebrew-smart-attendance`
2. Add the `smart-attendance.rb` formula
3. Users can then install with: `brew install yourusername/smart-attendance/smart-attendance`

### 3. Docker Distribution

```bash
# Build and push to Docker Hub
docker build -t yourusername/smart-attendance:latest .
docker push yourusername/smart-attendance:latest

# Users can run with:
docker run -it yourusername/smart-attendance:latest
```

### 4. Standalone Binary (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile -n smart-attendance src/tui_app.py
# Binary will be in dist/smart-attendance
```

---

## First-Time Setup

After installation, on first run:

1. **Application will guide you through**:

   - Creating data directories
   - Adding students
   - Capturing face images
   - Training the model
   - Running recognition

2. **Directory Structure Created**:

```
smart-attendance/
├── data/
│   └── students/
│       ├── students.csv
│       └── [student-roll-number]/
│           ├── image1.jpg
│           ├── image2.jpg
│           └── ...
├── models/
│   └── [tensorflow-facenet-models]/
├── logs/
│   └── attendance.csv
└── reference/
    └── embeddings.json
```

---

## TUI Features

### 📊 Dashboard

- View total students and training status
- Check today's attendance
- See recent attendance log

### 📁 Data Management

- Add new students
- Delete students
- View student details
- Count training images per student

### 🧠 Model Training

- Train embeddings for all students
- Track training progress
- View completion status

### 📷 Mark Attendance

- Start real-time face recognition
- Adjustable recognition threshold
- Automatic attendance logging

### ⚙️ Settings

- Configure recognition threshold (0.0-1.0)
- View system paths
- System information

---

## Command Line Alternatives

For users preferring CLI:

```bash
# Train model (old method, use TUI)
python3 main.py --train

# Start recognition (old method, use TUI)
python3 main.py --recognize --threshold 0.6
```

---

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Camera not working

- Check camera permissions
- On macOS: System Preferences → Security & Privacy → Camera
- Ensure no other app is using the camera

### TensorFlow/GPU issues

- Intel Mac: `pip uninstall tensorflow; pip install tensorflow==2.15.0`
- Apple Silicon: `pip install tensorflow-macos tensorflow-metal`

### Out of memory

- Reduce number of training images
- Close other applications
- Increase swap/virtual memory

---

## Development

### Setting up development environment

```bash
git clone https://github.com/yourusername/smart-attendance.git
cd smart-attendance
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

### Code quality

```bash
black src/
flake8 src/
mypy src/
```

---

## Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/smart-attendance/issues)
- 💬 [Discussions](https://github.com/yourusername/smart-attendance/discussions)

---

## License

MIT License - See LICENSE file for details
