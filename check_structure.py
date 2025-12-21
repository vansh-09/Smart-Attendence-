#!/usr/bin/env python3
"""
Directory structure validator for Smart Attendance System.
Checks if the required folders and CSV file are properly set up.
"""

import os
import csv
from pathlib import Path


def check_structure(base_dir=None):
    """Check if project structure is properly set up."""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("\n🔍 Checking Smart Attendance Project Structure...\n")
    
    checks_passed = 0
    checks_total = 0
    
    # Check data/students directory
    checks_total += 1
    data_students_dir = os.path.join(base_dir, "data", "students")
    if os.path.isdir(data_students_dir):
        print(f"✅ data/students directory exists")
        checks_passed += 1
    else:
        print(f"❌ data/students directory missing - creating...")
        os.makedirs(data_students_dir, exist_ok=True)
        print(f"✅ Created data/students directory")
        checks_passed += 1
    
    # Check students.csv
    checks_total += 1
    csv_path = os.path.join(data_students_dir, "students.csv")
    if os.path.isfile(csv_path):
        print(f"✅ students.csv exists")
        checks_passed += 1
        
        # Check CSV content
        checks_total += 1
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    print(f"   ✅ CSV contains {len(rows)} students")
                    for row in rows[:3]:  # Show first 3
                        print(f"      - {row.get('roll_number', 'N/A')}: {row.get('name', 'N/A')}")
                    if len(rows) > 3:
                        print(f"      ... and {len(rows) - 3} more")
                    checks_passed += 1
                else:
                    print(f"   ⚠️  CSV is empty (template only)")
        except Exception as e:
            print(f"   ❌ Error reading CSV: {e}")
    else:
        print(f"❌ students.csv missing")
    
    # Check reference directory
    checks_total += 1
    ref_dir = os.path.join(base_dir, "reference")
    if os.path.isdir(ref_dir):
        print(f"✅ reference/ directory exists")
        checks_passed += 1
    else:
        print(f"❌ reference/ directory missing")
    
    # Check for embeddings
    checks_total += 1
    embed_path = os.path.join(ref_dir, "students_embeddings.json")
    if os.path.isfile(embed_path):
        print(f"✅ students_embeddings.json exists")
        checks_passed += 1
    else:
        print(f"⚠️  students_embeddings.json not found (run --train-batch first)")
    
    # Check for logs directory
    checks_total += 1
    logs_dir = os.path.join(base_dir, "logs")
    if os.path.isdir(logs_dir):
        print(f"✅ logs/ directory exists")
        checks_passed += 1
    else:
        print(f"❌ logs/ directory missing - creating...")
        os.makedirs(logs_dir, exist_ok=True)
        print(f"✅ Created logs/ directory")
        checks_passed += 1
    
    # Check student folders
    checks_total += 1
    student_folders = [d for d in os.listdir(data_students_dir) 
                      if os.path.isdir(os.path.join(data_students_dir, d)) and d != '__pycache__']
    
    if student_folders:
        print(f"✅ Found {len(student_folders)} student folders")
        for folder in sorted(student_folders)[:5]:
            folder_path = os.path.join(data_students_dir, folder)
            photos = [f for f in os.listdir(folder_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            status = "✅" if len(photos) >= 2 else "⚠️"
            print(f"   {status} {folder}: {len(photos)} photos")
        if len(student_folders) > 5:
            print(f"   ... and {len(student_folders) - 5} more")
        checks_passed += 1
    else:
        print(f"⚠️  No student folders found (add students in data/students/)")
    
    # Summary
    print(f"\n📊 Structure Check: {checks_passed}/{checks_total} passed\n")
    
    if checks_passed == checks_total:
        print("✨ Project structure is ready!\n")
        return True
    else:
        print(f"⚠️  Please fix {checks_total - checks_passed} issues\n")
        return False


if __name__ == "__main__":
    import sys
    success = check_structure()
    sys.exit(0 if success else 1)
