#!/bin/bash
# Smart Attendance System - Example Usage Script
# This script demonstrates the typical workflow

set -e  # Exit on error

echo "🎓 Smart Attendance System - Example Workflow"
echo "=============================================="
echo ""

# Note: This is a documentation script showing the workflow
# Copy and modify these commands for your actual setup

# ============================================
# PHASE 1: SETUP
# ============================================
echo "📋 PHASE 1: SETUP"
echo "────────────────"
echo ""

echo "1. Check project structure:"
echo "   python3 check_structure.py"
echo ""

echo "2. View the current students CSV:"
echo "   cat data/students/students.csv"
echo ""

# ============================================
# PHASE 2: ENROLLMENT
# ============================================
echo ""
echo "📷 PHASE 2: ENROLLMENT"
echo "────────────────────"
echo ""

echo "3. Update students CSV (edit with your students):"
echo "   nano data/students/students.csv"
echo ""
echo "   Example content:"
echo "   roll_number,name"
echo "   101,John Doe"
echo "   102,Jane Smith"
echo "   103,Alice Johnson"
echo ""

echo "4. Create student folders (one per roll number):"
echo "   mkdir -p data/students/101"
echo "   mkdir -p data/students/102"
echo "   mkdir -p data/students/103"
echo ""

echo "5. Add photos to each student folder:"
echo "   cp john_photo1.jpg data/students/101/"
echo "   cp john_photo2.jpg data/students/101/"
echo "   cp jane_photo1.jpg data/students/102/"
echo "   cp jane_photo2.jpg data/students/102/"
echo "   # ... repeat for all students"
echo ""

# ============================================
# PHASE 3: TRAINING
# ============================================
echo ""
echo "🚀 PHASE 3: TRAINING"
echo "──────────────────"
echo ""

echo "6. Train embeddings for all students:"
echo "   python3 main.py --train-batch"
echo ""
echo "   Expected output:"
echo "   🎯 Starting batch training..."
echo "   ✅ 101: John Doe (2 valid faces from 2 photos)"
echo "   ✅ 102: Jane Smith (2 valid faces from 2 photos)"
echo "   ✅ 103: Alice Johnson (2 valid faces from 2 photos)"
echo "   💾 Saved 3 student embeddings..."
echo "   ✨ Training complete! Enrolled 3 students."
echo ""

# ============================================
# PHASE 4: RECOGNITION
# ============================================
echo ""
echo "📹 PHASE 4: RECOGNITION"
echo "──────────────────────"
echo ""

echo "7. Run attendance recognition:"
echo "   python3 main.py --recognize"
echo ""
echo "   or simply:"
echo "   python3 main.py"
echo ""
echo "   Expected output:"
echo "   ✅ Loaded 3 students"
echo "   🎥 Running batch recognition with 3 students"
echo "   Press 'q' to quit."
echo ""
echo "   The system will:"
echo "   - Open your webcam"
echo "   - Detect faces in real-time"
echo "   - Match against all enrolled students"
echo "   - Mark attendance automatically"
echo "   - Save to logs/attendance.csv"
echo ""

# ============================================
# PHASE 5: CLEANUP (OPTIONAL)
# ============================================
echo ""
echo "🗑️  PHASE 5: CLEANUP (Optional)"
echo "──────────────────────────────"
echo ""

echo "8. Preview what will be deleted:"
echo "   python3 main.py --cleanup-dry-run"
echo ""

echo "9. Delete photos to save space (embeddings are safe):"
echo "   python3 main.py --cleanup-photos"
echo ""

# ============================================
# ADVANCED: MANAGEMENT
# ============================================
echo ""
echo "🔧 ADVANCED: Management Commands"
echo "────────────────────────────────"
echo ""

echo "Add more students later:"
echo "  1. Edit CSV: nano data/students/students.csv"
echo "  2. Create folder: mkdir data/students/104"
echo "  3. Add photos: cp photos... data/students/104/"
echo "  4. Retrain: python3 main.py --train-batch"
echo "  5. Run: python3 main.py"
echo ""

echo "Adjust recognition sensitivity:"
echo "  More lenient (0.5):  python3 main.py --threshold 0.5"
echo "  Default (0.6):       python3 main.py"
echo "  Stricter (0.7):      python3 main.py --threshold 0.7"
echo ""

echo "View attendance log:"
echo "  cat logs/attendance.csv"
echo ""

echo "Reset everything:"
echo "  rm -rf data/students/*"
echo "  rm reference/students_embeddings.json"
echo "  # Now start from PHASE 2"
echo ""

# ============================================
# SAMPLE CSV CONTENT
# ============================================
echo ""
echo "📋 SAMPLE: students.csv"
echo "──────────────────────"
echo ""
echo "roll_number,name"
echo "101,John Doe"
echo "102,Jane Smith"
echo "103,Alice Johnson"
echo "104,Bob Wilson"
echo "105,Carol White"
echo "106,David Miller"
echo "107,Emma Brown"
echo "108,Frank Davis"
echo "109,Grace Lee"
echo "110,Henry Wilson"
echo ""

# ============================================
# SAMPLE FOLDER STRUCTURE
# ============================================
echo ""
echo "📂 SAMPLE: Folder Structure After Setup"
echo "──────────────────────────────────────"
echo ""
echo "data/students/"
echo "├── students.csv"
echo "├── 101/"
echo "│   ├── photo1.jpg"
echo "│   ├── photo2.jpg"
echo "│   └── photo3.jpg"
echo "├── 102/"
echo "│   ├── photo1.jpg"
echo "│   └── photo2.jpg"
echo "├── 103/"
echo "│   ├── photo1.jpg"
echo "│   └── photo2.jpg"
echo "└── ..."
echo ""

# ============================================
# SAMPLE ATTENDANCE LOG
# ============================================
echo ""
echo "📊 SAMPLE: logs/attendance.csv (after running)"
echo "─────────────────────────────────────────────"
echo ""
echo "name,roll_no,timestamp"
echo "John Doe,101,2025-12-22T10:30:45"
echo "Jane Smith,102,2025-12-22T10:31:12"
echo "Alice Johnson,103,2025-12-22T10:32:00"
echo "John Doe,101,2025-12-22T14:15:30"
echo ""

# ============================================
# PERFORMANCE NOTES
# ============================================
echo ""
echo "⚡ PERFORMANCE NOTES"
echo "──────────────────"
echo ""
echo "Setup time (10 students):    ~45 minutes"
echo "  - CSV setup:               5 min"
echo "  - Add photos:              30 min (3 min per student)"
echo "  - Training:                10 min"
echo ""
echo "Recognition speed:"
echo "  - Per frame:               ~100ms"
echo "  - Webcam FPS:              ~10-15 FPS"
echo "  - Face detection:          ~50ms"
echo "  - Embedding generation:    ~40ms"
echo "  - Comparison (10 students):~10ms"
echo ""
echo "Storage:"
echo "  - Per student embedding:   ~4KB"
echo "  - Per photo:               ~1-5MB"
echo "  - After cleanup (10 students): ~40KB"
echo ""

# ============================================
# TROUBLESHOOTING
# ============================================
echo ""
echo "🐛 TROUBLESHOOTING"
echo "─────────────────"
echo ""
echo "Problem: No batch embeddings found"
echo "Solution: Make sure CSV has data, create student folders, run --train-batch"
echo ""
echo "Problem: 'No faces detected' error"
echo "Solution: Check photo quality, ensure faces are visible, add more photos"
echo ""
echo "Problem: Low accuracy"
echo "Solution: Add more photos (3-5), use better lighting, retrain"
echo ""
echo "Problem: Recognition too strict/lenient"
echo "Solution: Adjust threshold (--threshold 0.5 to 0.8)"
echo ""

echo ""
echo "✅ Setup Complete! Start with QUICK_START.md for guided steps."
echo ""
