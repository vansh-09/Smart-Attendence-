# Smart Attendance System v4

Real-time facial recognition attendance tracking using FaceNet and MTCNN.

## Overview

A batch attendance system that:

- **Trains** embeddings for multiple students from photos
- **Recognizes** students in real-time via webcam
- **Logs** attendance automatically to CSV
- **All logic in one file** - `src/pipeline.py`

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Students

**Create CSV file** - `data/students/students.csv`:

```csv
roll_number,name
101,John Doe
102,Jane Smith
103,Alice Johnson
```

**Create photo folders**:

```bash
mkdir -p data/students/101 data/students/102 data/students/103
```

**Add 2+ photos per student**:

```bash
cp john_photo1.jpg data/students/101/
cp john_photo2.jpg data/students/101/
cp jane_photo1.jpg data/students/102/
cp jane_photo2.jpg data/students/102/
# ... repeat for all students
```

### 3. Train Embeddings

```bash
python main.py --train
```

**Output:**

```
Training 3 students...
✓ 101: John Doe (2 faces)
✓ 102: Jane Smith (2 faces)
✓ 103: Alice Johnson (2 faces)
✓ Trained 3 students
```

This generates `reference/embeddings.json` with face embeddings for all students.

### 4. Run Attendance Recognition

```bash
python main.py --recognize
```

or simply:

```bash
python main.py
```

**What it does:**

- Opens webcam
- Detects faces in real-time
- Compares with all enrolled students
- Shows best match and confidence score
- Marks attendance automatically (once per session)
- Logs to `logs/attendance.csv`

**Stop**: Press `q` to quit

## Commands

| Command                          | Description                       |
| -------------------------------- | --------------------------------- |
| `python main.py --train`         | Train embeddings for all students |
| `python main.py --recognize`     | Run attendance recognition        |
| `python main.py`                 | Default (same as recognize)       |
| `python main.py --threshold 0.5` | Adjust similarity threshold       |

### Threshold Explanation

- Default: `0.6` (cosine similarity)
- Lower (0.4-0.5): More lenient, easier to match
- Higher (0.7-0.8): Stricter, harder to match

```bash
# Lenient matching
python main.py --threshold 0.5

# Strict matching
python main.py --threshold 0.7
```

## Project Structure

```
Smart-Attendence-/
├── main.py                         # CLI entry point
├── src/
│   └── pipeline.py                # Complete pipeline (all logic)
├── data/
│   └── students/
│       ├── students.csv           # Student registry
│       ├── 101/                   # Photos by roll number
│       │   ├── photo1.jpg
│       │   └── photo2.jpg
│       └── ...
├── reference/
│   └── embeddings.json            # Trained embeddings
├── logs/
│   └── attendance.csv             # Attendance records
├── models/                        # FaceNet cache (auto-created)
└── requirements.txt
```

## Data Structure

### students.csv Format

```csv
roll_number,name
101,John Doe
102,Jane Smith
```

**Column 1**: `roll_number` - Unique identifier (used as folder name)
**Column 2**: `name` - Student full name

### Photo Requirements

- **Location**: `data/students/{roll_number}/`
- **Count**: Minimum 2 photos per student
- **Format**: JPG, JPEG, or PNG
- **Quality**: Clear facial features, well-lit
- **Recommended**: 3-5 photos for better accuracy

### embeddings.json (Auto-generated)

```json
{
  "101": {
    "name": "John Doe",
    "embedding": [0.123, -0.456, ..., 0.789]  // 512 floats
  },
  "102": {
    "name": "Jane Smith",
    "embedding": [...]
  }
}
```

### attendance.csv (Auto-generated)

```csv
name,roll_no,timestamp
John Doe,101,2025-12-22T10:30:45
Jane Smith,102,2025-12-22T10:31:12
```

## Complete Workflow Example

```bash
# 1. Create student registry
echo "roll_number,name
101,Alice
102,Bob
103,Charlie" > data/students/students.csv

# 2. Create folders
mkdir -p data/students/{101,102,103}

# 3. Add photos
cp alice1.jpg alice2.jpg data/students/101/
cp bob1.jpg bob2.jpg data/students/102/
cp charlie1.jpg charlie2.jpg data/students/103/

# 4. Train
python main.py --train

# 5. Run attendance
python main.py

# 6. View results
cat logs/attendance.csv
```

## Architecture

**Single pipeline file** (`src/pipeline.py`) contains:

- **FaceDetector** - MTCNN face detection
- **FaceEmbedder** - FaceNet embeddings
- **AttendancePipeline** - Complete workflow
- **UI Functions** - Draw boxes and labels
- **AttendanceLogger** - CSV logging

**Main app** (`main.py`) - 18 lines, just CLI interface

## Adding More Students Later

1. **Add to CSV**:

   ```bash
   echo "104,David" >> data/students/students.csv
   ```

2. **Create folder and add photos**:

   ```bash
   mkdir data/students/104
   cp david1.jpg david2.jpg data/students/104/
   ```

3. **Retrain**:

   ```bash
   python main.py --train
   ```

4. **Run**:
   ```bash
   python main.py
   ```

## Troubleshooting

### "No embeddings found"

- Run `python main.py --train` first
- Ensure `data/students/students.csv` has data
- Ensure student folders exist with photos

### Low recognition accuracy

- Add more photos (aim for 3-5 per student)
- Use better lighting
- Ensure clear facial features
- Retrain with `--train`

### No faces detected

- Check photo quality
- Ensure faces are clearly visible
- Avoid extreme angles or partial faces

### Reset everything

```bash
rm reference/embeddings.json
rm -rf data/students/*/  # keeps CSV
python main.py --train
```

## Performance

- **Training** (10 students): ~5-10 minutes
- **Recognition** (per frame): ~100-150ms
- **Memory**: ~500MB (FaceNet model)
- **Storage** (embeddings only): ~4KB per student

## Requirements

- Python 3.7+
- OpenCV (cv2)
- TensorFlow/Keras
- keras-facenet
- MTCNN
- Numpy
- Pillow

See `requirements.txt` for exact versions.

## Notes

- **Models cached**: FaceNet weights downloaded once to `models/` folder
- **Offline capable**: Works completely offline after first run
- **Attendance marked once**: Same student won't be marked twice in one session
- **CSV appended**: Attendance records append to CSV on each run

---

**Ready to use. Just configure students, train, and run!** 🎓
