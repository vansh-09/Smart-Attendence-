#!/bin/bash
# Installation script for Smart Attendance System

set -e

echo "🚀 Smart Attendance System - Installation Script"
echo "=================================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
min_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "❌ Python 3.10+ required (found $python_version)"
    exit 1
fi

echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "🔗 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo ""
echo "🔧 Installing Smart Attendance in development mode..."
pip install -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To run the application:"
echo "   source venv/bin/activate"
echo "   smart-attendance"
echo ""
echo "   OR directly:"
echo "   python3 main.py"
echo ""
