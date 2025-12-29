# Smart Attendance System v6 - Incremental Learning

Real-time facial recognition attendance tracking using FaceNet and MTCNN with **incremental learning** support.

## ✨ Key Features

- **✅ Incremental Learning**: Add new students WITHOUT retraining existing ones
- **🚀 Fast Processing**: Only processes new students, preserving existing embeddings
- **📸 Face Recognition**: Real-time attendance using FaceNet embeddings
- **📊 Attendance Logging**: Automatic CSV-based attendance records
- **All logic in one file** - `src/pipeline.py`

## 🔄 What's New in v6: Incremental Learning

This system supports **continual/incremental learning** - when you add new students, it will:

- ✅ Load existing student embeddings from JSON
- ✅ Process ONLY new students not yet trained
- ✅ Merge new embeddings with existing ones
- ❌ **NEVER** retrain existing students from scratch

**Why this matters:**

- Save time when adding students (seconds instead of minutes)
- Preserve existing embeddings (no quality degradation)
- Scalable for large student databases

## Overview

A batch attendance system that:

- **Trains** embeddings for multiple students from photos
- **Recognizes** students in real-time via webcam
- **Logs** attendance automatically to CSV
- **Incremental updates** when adding new students

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Students

**Create CSV file** - `data/students/info/students.csv`:

```csv
roll_number,name
101,John Doe
102,Jane Smith
103,Alice Johnson
```

**Create photo folders**:

```bash
mkdir -p data/students/images/{101,102,103}
```

**Add 2+ photos per student**:

```bash
cp john_photo1.jpg data/students/images/101/
cp john_photo2.jpg data/students/images/101/
cp jane_photo1.jpg data/students/images/102/
cp jane_photo2.jpg data/students/images/102/
# ... repeat for all students
```

### 3. Train Embeddings (Incremental by Default)

```bash
python main.py --train
```

**Output (First Time):**

```
🔄 Adding 3 new student(s) incrementally...
   (Keeping 0 existing student(s))

✓ 101: John Doe (2 faces)
✓ 102: Jane Smith (2 faces)
✓ 103: Alice Johnson (2 faces)

✅ Added 3 new student(s)
   Total students: 3
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

| Command                                | Description                              |
| -------------------------------------- | ---------------------------------------- |
| `python main.py --train`               | Add new students incrementally (default) |
| `python main.py --add-student ROLL_NO` | Add specific student by roll number      |
| `python main.py --full-retrain`        | Retrain ALL students from scratch        |
| `python main.py --recognize`           | Run attendance recognition               |
| `python main.py`                       | Default (same as recognize)              |
| `python main.py --threshold 0.5`       | Adjust similarity threshold              |

### Command Details

#### Incremental Training (Recommended)

```bash
# Auto-detect and add all new students
python main.py --train

# Add a specific student by roll number
python main.py --add-student 104
```

#### Full Retrain (Use only when necessary)

```bash
# Retrain ALL students from scratch
# Use only when: changing embedding model, or fixing corrupted data
python main.py --full-retrain
```

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
│   └── pipeline.py                 # Complete pipeline (all logic)
├── data/
│   └── students/
│       ├── FOLDER_STRUCTURE.md     # Documentation
│       ├── info/
│       │   └── students.csv        # Student registry
│       └── images/
│           ├── 124A8036/           # Photos by roll number
│           │   ├── img1.JPG
│           │   └── img2.JPG
│           └── ...
├── reference/
│   └── embeddings.json             # Trained embeddings
├── logs/
│   └── attendance.csv              # Attendance records
├── models/                         # FaceNet cache (auto-created)
└── requirements.txt

Total Core Files: 2 Python files (main.py + pipeline.py)
```

## Data Structure

### students.csv Format

Located at: `data/students/info/students.csv`

```csv
roll_number,name
101,John Doe
102,Jane Smith
```

**Column 1**: `roll_number` - Unique identifier (used as folder name)
**Column 2**: `name` - Student full name

### Photo Requirements

- **Location**: `data/students/images/{roll_number}/`
- **Count**: Minimum 2 photos per student
- **Format**: JPG, JPEG, or PNG (case-insensitive)
- **Quality**: Clear facial features, well-lit
- **Recommended**: 3-5 photos for better accuracy
- **Storage**: Can be deleted after training (embeddings are saved)

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
103,Charlie" > data/students/info/students.csv

# 2. Create folders
mkdir -p data/students/images/{101,102,103}

# 3. Add photos
cp alice1.jpg alice2.jpg data/students/images/101/
cp bob1.jpg bob2.jpg data/students/images/102/
cp charlie1.jpg charlie2.jpg data/students/images/103/

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

## Adding More Students Later (Incremental Learning Example)

1. **Add to CSV**:

   ```bash
   echo "104,David" >> data/students/info/students.csv
   echo "105,Emily" >> data/students/info/students.csv
   ```

2. **Create folders and add photos**:

   ```bash
   mkdir -p data/students/images/{104,105}
   cp david1.jpg david2.jpg data/students/images/104/
   cp emily1.jpg emily2.jpg data/students/images/105/
   ```

3. **Incremental Train** (only processes new students):

   ```bash
   python main.py --train
   ```

   **Output:**

   ```
   🔄 Adding 2 new student(s) incrementally...
      (Keeping 3 existing student(s))

   ✓ 104: David (2 faces)
   ✓ 105: Emily (2 faces)

   ✅ Added 2 new student(s)
      Total students: 5
   ```

   **Notice**: Only David and Emily are processed. The original 3 students (101-103) are NOT retrained!

4. **Run**:
   ```bash
   python main.py
   ```

### Alternative: Add Single Student

```bash
# Add specific student without checking all CSV entries
python main.py --add-student 106
```

## Troubleshooting

### "No embeddings found"

- Run `python main.py --train` first
- Ensure `data/students/info/students.csv` has data
- Ensure student folders exist with photos in `data/students/images/`

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
rm -rf data/students/images/*/  # keeps folder structure
python main.py --train
```

## Performance

- **Initial Training** (10 students): ~5-10 minutes
- **Incremental Add** (1 student): ~30-60 seconds
- **Recognition** (per frame): ~100-150ms
- **Memory**: ~500MB (FaceNet model)
- **Storage** (embeddings only): ~4KB per student

## Benefits of Incremental Learning

| Scenario                    | Full Retrain | Incremental Learning |
| --------------------------- | ------------ | -------------------- |
| Add 1 student to 100        | ~50 minutes  | ~30 seconds          |
| Add 5 students to 100       | ~50 minutes  | ~2.5 minutes         |
| Existing data preserved     | ❌ Retrained | ✅ Preserved         |
| Risk of quality degradation | ⚠️ Possible  | ✅ None              |

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
- **Images optional after training**: Once embeddings are saved, photos can be deleted to save space
  ```bash
  # Delete all student photo folders (keeps images/ folder structure)
  rm -rf data/students/images/*/
  ```
  ⚠️ Only run this after confirming embeddings exist in `reference/embeddings.json`

---

## 📚 How Incremental Learning Works

### The Algorithm

```python
def add_students_incremental(self, specific_roll_nos=None):
    # 1. Load existing embeddings from JSON
    existing_embeddings = self.load_embeddings()

    # 2. Get all students from CSV
    all_students = self._get_all_students_from_csv()

    # 3. Identify NEW students (not in existing embeddings)
    students_to_add = {roll: name for roll, name in all_students.items()
                      if roll not in existing_embeddings}

    # 4. Process ONLY new students
    for roll_no, name in students_to_add.items():
        result = self._process_student(roll_no, name)
        if result:
            existing_embeddings[roll_no] = result  # Add to existing

    # 5. Save updated embeddings (existing + new)
    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump(existing_embeddings, f)
```

### Process Flow Diagram

```
Step 1: Load Existing Embeddings
┌─────────────────────────────────────┐
│ reference/embeddings.json            │
│ {                                    │
│   "124A8036": {"name": "Vansh Jain", │
│                "embedding": [...]},  │
│   "124A8037": {"name": "John Doe",   │
│                "embedding": [...]}   │
│ }                                    │
└─────────────────────────────────────┘
            ↓
Step 2: Read Student CSV
┌─────────────────────────────────────┐
│ data/students/info/students.csv      │
│ 124A8036,Vansh Jain   (SKIP ✓)     │
│ 124A8037,John Doe     (SKIP ✓)     │
│ 124A8038,Jane Smith   (NEW! ⚡)     │
│ 124A8039,Alice J.     (NEW! ⚡)     │
└─────────────────────────────────────┘
            ↓
Step 3: Process ONLY New Students
┌─────────────────────────────────────┐
│ For each NEW student:                │
│ 1. Load photos                       │
│ 2. Detect faces (MTCNN)              │
│ 3. Generate embeddings (FaceNet)     │
│ 4. Compute mean embedding            │
│                                      │
│ Processing: 124A8038 ✓              │
│ Processing: 124A8039 ✓              │
└─────────────────────────────────────┘
            ↓
Step 4: Merge & Save
┌─────────────────────────────────────┐
│ Existing (preserved):                │
│   "124A8036": {...}  ← KEPT         │
│   "124A8037": {...}  ← KEPT         │
│ New (added):                         │
│   "124A8038": {...}  ← ADDED        │
│   "124A8039": {...}  ← ADDED        │
│                                      │
│ Save to: embeddings.json             │
└─────────────────────────────────────┘
```

### Comparison: Full Retrain vs Incremental

**❌ Old Method (Full Retrain)**

```
100 Existing Students + 1 New Student
         ↓
Process ALL 101 Students
   (~50 minutes)
         ↓
101 Students in Database
```

**✅ New Method (Incremental)**

```
100 Existing Students (preserved) + 1 New Student
         ↓
Process ONLY 1 New Student
   (~30 seconds)
         ↓
101 Students in Database
```

### Why This Works

- **Stateless Embeddings**: FaceNet embeddings are deterministic - same photo always produces same embedding
- **No Model Updates**: The FaceNet model is frozen; we only compute new embeddings
- **JSON Persistence**: Lightweight storage preserves all existing data
- **Selective Processing**: Only new students go through face detection pipeline
- **Data Integrity**: Existing embeddings remain unchanged and unaffected

### When to Use Each Mode

**Use `--train` (Incremental - Default)**

- ✅ Adding new students to existing database
- ✅ Regular updates to student roster
- ✅ Want fast processing
- ✅ Preserving existing quality

**Use `--add-student ROLL_NO`**

- ✅ Adding a single specific student
- ✅ Quick one-off additions
- ✅ Testing with new student

**Use `--full-retrain`**

- ⚠️ Changing embedding model or algorithm
- ⚠️ Fixing corrupted embeddings file
- ⚠️ Major system upgrade
- ⚠️ Complete system reset

---

**Ready to use. Just configure students, train, and run!** 🎓
