#!/bin/bash
# Publish to Homebrew (requires homebrew-smart-attendance tap)

set -e

echo "🍺 Publishing to Homebrew..."
echo ""

# Get version from setup.py
VERSION=$(grep "version=" setup.py | head -n1 | grep -oP '\d+\.\d+\.\d+')
echo "Version: $VERSION"

# Create release archive
echo "📦 Creating release archive..."
git archive --format=tar.gz --prefix=smart-attendance-$VERSION/ -o smart-attendance-$VERSION.tar.gz HEAD

# Calculate SHA256
SHA256=$(shasum -a 256 smart-attendance-$VERSION.tar.gz | cut -d' ' -f1)
echo "SHA256: $SHA256"

# Update formula
echo ""
echo "📝 Update smart-attendance.rb with:"
echo "  url: https://github.com/yourusername/smart-attendance/archive/v$VERSION.tar.gz"
echo "  sha256: $SHA256"
echo ""

# Push to tap (if using homebrew-smart-attendance tap)
echo "🚀 To publish to Homebrew:"
echo "  1. Fork homebrew-core or create homebrew-smart-attendance tap"
echo "  2. Update the formula with values above"
echo "  3. Submit pull request or push to tap"
echo ""

# Cleanup
rm -f smart-attendance-$VERSION.tar.gz

echo "✅ Done! Users can now install with:"
echo "   brew tap yourusername/smart-attendance"
echo "   brew install smart-attendance"
