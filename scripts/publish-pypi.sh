#!/bin/bash
# Publish to PyPI

set -e

echo "📦 Publishing to PyPI..."
echo ""

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "Installing twine..."
    pip install twine
fi

# Clean old builds
rm -rf build/ dist/ *.egg-info

# Build distribution
echo "Building distribution..."
python3 -m build

# Check distribution
echo "Checking distribution..."
twine check dist/*

# Upload to PyPI
echo ""
echo "⬆️  Uploading to PyPI..."
echo "You'll be prompted for your PyPI credentials"
echo ""

twine upload dist/*

echo ""
echo "✅ Published to PyPI!"
echo ""
echo "Users can now install with:"
echo "  pip install smart-attendance"
