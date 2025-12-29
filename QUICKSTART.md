# Quick Start Guide

## 🎯 30-Second Setup

### On macOS

```bash
# Copy & paste this one command:
git clone https://github.com/yourusername/smart-attendance.git && \
cd smart-attendance && \
chmod +x install.sh && \
./install.sh && \
smart-attendance
```

### On Linux

```bash
git clone https://github.com/yourusername/smart-attendance.git
cd smart-attendance
sudo apt-get install python3.11 python3.11-venv
chmod +x install.sh
./install.sh
source venv/bin/activate
smart-attendance
```

### On Windows (WSL2)

```bash
wsl
git clone https://github.com/yourusername/smart-attendance.git
cd smart-attendance
chmod +x install.sh
./install.sh
smart-attendance
```

---

## 📋 First Run Walkthrough

### Step 1: Add Students

1. Open the app (should show welcome screen)
2. Click **📁 Manage Data**
3. Click **➕ Add Student**
4. Enter student name: `John Doe`
5. Enter roll number: `124A8036`
6. Click **✓ Add Student**

### Step 2: Add Photos

1. Create folder: `data/students/124A8036/`
2. Add 5-10 clear photos of the student's face
3. Supported formats: `.jpg`, `.png`, `.jpeg`
4. Good photos = good recognition!

### Step 3: Train Model

1. Click **🧠 Train Model** from main menu
2. Click **▶ Start Training**
3. Wait for completion (2-3 minutes)
4. You'll see ✓ after each student

### Step 4: Mark Attendance

1. Click **📷 Mark Attendance**
2. Adjust threshold if needed (0.6 is good)
3. Click **▶ Start Camera**
4. Look at camera when ready
5. Attendance auto-logs to CSV!

### Step 5: Check Results

1. Click **📊 Dashboard**
2. See today's attendance count
3. Click on activity log to see details
4. Check `logs/attendance.csv` for records

---

## 🖼️ Photo Tips

### Good Photos ✅

- Face clearly visible
- Good lighting (not backlit)
- Front-facing or slight angles
- Various expressions (neutral, slight smile)
- Clear eyes and nose
- Different distances from camera
- Minimum 5-10 photos per person

### Bad Photos ❌

- Face too small or blurry
- Wearing sunglasses or hat
- Heavy shadows or glare
- Extreme side angles
- Multiple people in frame
- Face partially cut off

---

## 🎮 Keyboard Shortcuts

| Key     | Action                     |
| ------- | -------------------------- |
| `q`     | Quit application           |
| `Esc`   | Go back to previous screen |
| `Tab`   | Navigate between fields    |
| `Enter` | Select/Confirm             |
| `↑/↓`   | Navigate lists             |
| `Space` | Toggle options             |

---

## 🔧 Making It Easy for Others

### Share Your Setup

```bash
# After setup, create a share package:
tar -czf smart-attendance-ready.tar.gz smart-attendance/
# Send to friends/colleagues

# They extract and run:
tar -xzf smart-attendance-ready.tar.gz
cd smart-attendance
./install.sh
smart-attendance
```

### Create a Shortcut (macOS)

```bash
# Create smart-attendance.command file with:
#!/bin/bash
cd ~/Smart-Attendance
source venv/bin/activate
smart-attendance

# Make executable:
chmod +x smart-attendance.command

# Double-click to run!
```

### Create a Shortcut (Linux/WSL)

```bash
# Create smart-attendance.sh file with:
#!/bin/bash
cd ~/smart-attendance
source venv/bin/activate
smart-attendance

# Make executable:
chmod +x smart-attendance.sh

# Create desktop shortcut or add to menu
```

---

## ⚡ Performance Tips

### Faster Training

- Use 5-8 good photos instead of 20
- Close other applications
- Ensure good lighting for photo capture

### Better Recognition

- Add photos in different lighting
- Include slight angles (45 degrees)
- Maintain consistent distance

### Better Hardware

- More RAM = faster training
- SSD = faster loading
- GPU (NVIDIA) = 5-10x faster

---

## 🆘 Common Issues

### "Camera not found"

**Solution**: Check System Preferences → Camera permissions

### "Out of memory"

**Solution**: Close other apps or reduce photos per student

### "Attendance not logging"

**Solution**: Check `data/students/` folder has photos for trained students

### "Can't find module 'textual'"

**Solution**: Run `pip install -r requirements.txt` again

### "TensorFlow error on Apple Silicon"

**Solution**: Run `pip install tensorflow-macos tensorflow-metal`

---

## 📚 Learn More

- [Installation Guide](INSTALL.md) - Detailed setup options
- [Full README](README.md) - Complete documentation
- [API Reference](API.md) - For developers

---

## 🎓 Use Cases

### 📚 Schools & Colleges

- Daily class attendance
- Exam attendance
- Event check-in
- Track student presence

### 🏢 Offices

- Employee attendance
- Meeting check-in
- Time tracking
- Access control

### 🏛️ Events

- Conference registration
- Workshop check-in
- Venue access
- Participant tracking

---

## 💡 Tips & Tricks

1. **Backup your data**: `cp -r data/ data-backup-$(date +%Y%m%d)`
2. **Merge students**: Edit `students.csv` manually
3. **Retrain individual**: Delete their embedding from `reference/embeddings.json`
4. **Adjust sensitivity**: Lower threshold (0.5) for strict, higher (0.7) for loose

---

**Need help?** [Open an issue](https://github.com/yourusername/smart-attendance/issues) or check [discussions](https://github.com/yourusername/smart-attendance/discussions)!
