

# Student Data Directory Structure

Use this template as a guide for organizing student records and image assets.

### 📂 Directory Layout

Ensure your folder follows this nested structure to remain compatible with the processing script:

```text
data/students/
├── students.csv           # Contains: roll_number, name
├── 101/                   # Folder named by roll_number
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg         (Optional)
├── 102/
│   ├── photo1.jpg
│   └── photo2.jpg
└── ...

```

### 📝 Requirements

* **CSV File:** Must be located in the root `students/` directory and include `roll_number` and `name` columns.
* **Naming Convention:** Subfolders must match the `roll_number` exactly.
* **File Formats:** Use `.jpg` or `.png` for all student photos.

---

