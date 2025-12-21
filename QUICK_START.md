# 🎓 Smart Attendance System - Quick Setup Guide

## 📁 Directory Structure

Your project is now structured to support batch student enrollment:

```
data/students/
├── students.csv           ← Add student info here
├── 101/                   ← Roll number folder
│   ├── photo1.jpg
│   └── photo2.jpg
├── 102/
│   ├── photo1.jpg
│   └── photo2.jpg
└── ...

reference/
├── embedding.json         ← Single student (legacy)
└── students_embeddings.json  ← All students (batch)
```

## 🚀 Quick Start (Batch Mode)

### Step 1️⃣: Add Students to CSV

Edit `data/students/students.csv`:

```csv
roll_number,name
101,John Doe
102,Jane Smith
103,Alice Johnson
```

### Step 2️⃣: Add Student Photos

Create folders for each student (folder name = roll number):

```bash
# Create folders
mkdir -p data/students/101
mkdir -p data/students/102
mkdir -p data/students/103

# Add 2+ photos per student
cp john_photo1.jpg data/students/101/
cp john_photo2.jpg data/students/101/
# ... etc for other students
```

**Photo Requirements:**

- At least 2 photos per student
- Clear facial features
- Well-lit
- JPG or PNG format
- Recommended: 3-5 photos for better accuracy

### Step 3️⃣: Train Embeddings

```bash
python main.py --train-batch
```

**What it does:**

- ✅ Reads students from CSV
- ✅ Detects faces in all photos
- ✅ Generates embeddings
- ✅ Saves to `reference/students_embeddings.json`

**Output:**

```
🎯 Starting batch training...

101: John Doe (2 valid faces from 2 photos)
102: Jane Smith (2 valid faces from 2 photos)
103: Alice Johnson (3 valid faces from 3 photos)

✨ Training complete! Enrolled 3 students.
```

### Step 4️⃣: Run Attendance

```bash
python main.py --recognize
```

or simply:

```bash
python main.py
```

**What it does:**

- 📹 Opens webcam
- 🔍 Detects faces in real-time
- 🎯 Compares with all enrolled students
- ✅ Marks attendance automatically
- 📋 Saves to `logs/attendance.csv`

**Output in terminal:**

```
✅ Loaded 3 students
🎥 Running batch recognition with 3 students
Press 'q' to quit.
```

**Attendance Log:** `logs/attendance.csv`

```csv
name,roll_no,timestamp
John Doe,101,2025-12-22T10:30:45
Jane Smith,102,2025-12-22T10:31:12
```

### Step 5️⃣ (Optional): Clean Up Photos

After training, delete photos to save space:

```bash
# Preview what will be deleted
python main.py --cleanup-dry-run

# Actually delete
python main.py --cleanup-photos
```

**Photos are safe to delete because:**

- Embeddings are saved in JSON
- You can always retrain if needed
- Embeddings are reusable

---

## 📝 Adding More Students Later

1. **Add to CSV:**

   ```csv
   104,Bob Wilson
   105,Carol White
   ```

2. **Create folders and add photos:**

   ```bash
   mkdir -p data/students/104
   mkdir -p data/students/105
   cp photos... data/students/104/
   cp photos... data/students/105/
   ```

3. **Retrain:**

   ```bash
   python main.py --train-batch
   ```

4. **Run:**
   ```bash
   python main.py --recognize
   ```

---

## 🔧 Advanced Options

### Custom Similarity Threshold

Default is 0.6. Lower = more lenient, Higher = stricter:

```bash
# More lenient (might have false positives)
python main.py --recognize --threshold 0.5

# Stricter (might miss some students)
python main.py --recognize --threshold 0.7
```

### Legacy Single-Student Mode

If you only have one student (old workflow):

```bash
# Enrollment (need 2 reference images in reference/ folder)
python main.py --enroll --name "John Doe" --roll "101"

# Recognition
python main.py --recognize
```

---

## ❓ Troubleshooting

### "No faces detected" for a student

- Check photo quality and lighting
- Ensure face is clearly visible
- Add more photos
- Retrain: `python main.py --train-batch`

### Low similarity scores

- Increase photo count (aim for 4-5 photos)
- Use different angles and lighting
- Ensure good facial feature visibility

### Out of webcam frames

- Close other camera-using apps
- Restart the program

### Reset embeddings

Delete the embeddings file and retrain:

```bash
rm reference/students_embeddings.json
python main.py --train-batch
```

---

## 📚 Full Command Reference

```bash
# Batch Training
python main.py --train-batch

# Run Recognition (auto-detects batch/single)
python main.py --recognize
python main.py                    # Same as above

# Photo Management
python main.py --cleanup-dry-run  # Preview deletions
python main.py --cleanup-photos   # Delete all photos

# Legacy Single-Student Mode
python main.py --enroll --name "Name" --roll "Roll"

# Adjust threshold
python main.py --recognize --threshold 0.5
```

---

## 📊 Files Overview

| File/Folder                          | Purpose                       |
| ------------------------------------ | ----------------------------- |
| `data/students/students.csv`         | Student registry (roll, name) |
| `data/students/101/`                 | Photos for roll 101           |
| `reference/students_embeddings.json` | Trained face embeddings       |
| `logs/attendance.csv`                | Attendance records            |
| `DATA_STRUCTURE.md`                  | Full documentation            |
| `QUICK_START.md`                     | This file                     |

---

**Happy attendance tracking! 🎉**
