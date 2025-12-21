# Smart Attendance - Data Structure Guide

## 📁 Directory Organization

```
Smart-Attendence-/
├── data/
│   ├── students/
│   │   ├── students.csv                 # Student info (roll_number, name)
│   │   ├── 101/                         # Folder named by roll number
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
│   │   ├── 102/
│   │   │   ├── photo1.jpg
│   │   │   └── photo2.jpg
│   │   └── ...
│   └── temp_images/                     # Optional: temporary images during processing
├── reference/
│   ├── embedding.json                   # Single person's embedding (legacy)
│   └── students_embeddings.json         # All students' embeddings (batch)
├── logs/
│   └── attendance.csv                   # Attendance records
└── models/
    └── 20180402-114759/
        └── 20180402-114759-weights.h5
```

## 📋 CSV Format (students.csv)

| roll_number | name          |
| ----------- | ------------- |
| 101         | John Doe      |
| 102         | Jane Smith    |
| 103         | Alice Johnson |

## 📸 Adding Students

### Step 1: Update CSV

Edit `data/students/students.csv` and add student information:

```
104,Bob Wilson
105,Carol White
```

### Step 2: Add Photos

Create a folder for each student with their roll number and add 2+ photos:

```
data/students/104/
  ├── photo1.jpg
  ├── photo2.jpg
  └── photo3.jpg (optional, more photos improve accuracy)

data/students/105/
  ├── photo1.jpg
  └── photo2.jpg
```

### Step 3: Train Embeddings

```bash
python main.py --train-batch
```

This will:

- Read students from CSV
- Process all photos in student folders
- Generate embeddings for each student
- Save to `reference/students_embeddings.json`

### Step 4: Clean Up Photos (Optional)

After training, delete the photos to save space:

```bash
python main.py --cleanup-photos
```

Or manually delete the `data/students/` folder.

## 🎯 Running Attendance

```bash
python main.py --recognize
```

The system will:

- Load all student embeddings from `reference/students_embeddings.json`
- Compare detected faces with all enrolled students
- Mark attendance with roll number and name

## 🔄 Workflow

1. **Add Students**: Update CSV + add photo folders
2. **Train**: `python main.py --train-batch`
3. **Run**: `python main.py --recognize`
4. **Cleanup** (optional): `python main.py --cleanup-photos`

## 📝 Notes

- Each student should have at least 2 clear photos
- Photos should be well-lit with clear facial features
- Use JPG or PNG format
- After training, photos can be deleted to save space
- Embeddings are stored in JSON for quick loading
