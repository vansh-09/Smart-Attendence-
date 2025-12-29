# Distribution & Publishing Guide

Complete guide for publishing Smart Attendance to various platforms.

## 📋 Pre-Release Checklist

- [ ] Update version in `setup.py` and `pyproject.toml`
- [ ] Update `CHANGELOG.md` with changes
- [ ] Test locally: `python3 main.py`
- [ ] Run tests: `pytest`
- [ ] Check lint: `flake8 src/`
- [ ] Tag release: `git tag v1.0.0`
- [ ] Commit and push: `git push origin --tags`

---

## 🚀 Distribution Methods

### Method 1: PyPI (Python Package Index)

**Easiest for pip install**

```bash
# Prerequisites
pip install build twine

# Build
python3 -m build

# Check
twine check dist/*

# Upload (will prompt for credentials)
twine upload dist/*

# Users install with
pip install smart-attendance
```

**OR use our script:**

```bash
chmod +x scripts/publish-pypi.sh
./scripts/publish-pypi.sh
```

**Account Setup:**

1. Create account at https://pypi.org/account/register/
2. Add PyPI token to `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-your-token-here
   ```

---

### Method 2: Homebrew (macOS)

**For `brew install smart-attendance`**

#### Option A: Using Homebrew Tap (Recommended)

1. **Create your tap repository:**

   ```bash
   # Create: yourusername/homebrew-smart-attendance
   # Add smart-attendance.rb formula
   ```

2. **Update formula in tap:**

   ```bash
   ./scripts/publish-homebrew.sh
   ```

3. **Users install with:**
   ```bash
   brew tap yourusername/smart-attendance
   brew install smart-attendance
   ```

#### Option B: Submit to Homebrew Core

1. Fork https://github.com/Homebrew/homebrew-core
2. Add formula to `Formula/smart-attendance.rb`
3. Test: `brew install --HEAD ./Formula/smart-attendance.rb`
4. Submit pull request

**Formula Example:**

```ruby
class SmartAttendance < Formula
  desc "Face Recognition Attendance System"
  homepage "https://github.com/yourusername/smart-attendance"
  url "https://github.com/yourusername/smart-attendance/archive/v1.0.0.tar.gz"
  sha256 "your-sha256-hash"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end
end
```

---

### Method 3: Docker Hub

**For containerized deployment**

```bash
# Build image
docker build -t yourusername/smart-attendance:latest .

# Tag version
docker tag yourusername/smart-attendance:latest yourusername/smart-attendance:1.0.0

# Login
docker login

# Push
docker push yourusername/smart-attendance:latest
docker push yourusername/smart-attendance:1.0.0

# Users run with
docker run -it yourusername/smart-attendance:latest
```

**OR use our script:**

```bash
DOCKER_REPO=yourusername/smart-attendance ./scripts/publish-docker.sh --push
```

**Create DockerHub README.md:**

- Link to GitHub repo
- Usage instructions
- Environment variables
- Volume mounts

---

### Method 4: GitHub Releases

**For direct downloads**

1. **Create release:**

   ```bash
   gh release create v1.0.0 --title "Smart Attendance v1.0.0" \
     --notes "Release notes here"
   ```

2. **Upload artifacts:**

   ```bash
   gh release upload v1.0.0 dist/smart_attendance-1.0.0-py3-none-any.whl
   ```

3. **Users download from:**
   ```
   https://github.com/yourusername/smart-attendance/releases/tag/v1.0.0
   ```

---

### Method 5: Source Distribution

**For direct Git installation**

```bash
# Users install with
pip install git+https://github.com/yourusername/smart-attendance.git

# Or from specific tag
pip install git+https://github.com/yourusername/smart-attendance.git@v1.0.0
```

---

## 🔄 Continuous Deployment with GitHub Actions

Our `.github/workflows/test-release.yml` automatically:

1. **Tests** on Python 3.10, 3.11, 3.12
2. **Lints** code with flake8
3. **Builds** distribution packages
4. **Publishes** to PyPI on release

**Setup:**

1. Create PyPI token at https://pypi.org/account/api-tokens/
2. Add to GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Create `PYPI_API_TOKEN` with your token
3. Push tag and workflow runs automatically!

---

## 📦 Create Binary with PyInstaller

**For standalone executable (no Python required)**

```bash
pip install pyinstaller

# Create executable
pyinstaller --onefile --name smart-attendance \
  --icon app.ico \
  --add-data "src:src" \
  src/tui_app.py

# Binary in dist/smart-attendance
# Share dist/smart-attendance file - no dependencies needed!
```

---

## 🎯 Distribution Checklist

### PyPI

- [x] Account created
- [x] Token generated
- [x] Version updated
- [x] Build tested locally
- [x] Uploaded to PyPI

### Homebrew

- [x] Tap created (if using tap)
- [x] Formula tested
- [x] Published to tap
- [x] Users can `brew install`

### Docker

- [x] Dockerfile created
- [x] Docker Hub account
- [x] Image built and tested
- [x] Pushed to Docker Hub
- [x] README created

### GitHub Releases

- [x] Release created
- [x] Artifacts uploaded
- [x] Release notes written

---

## 📊 Recommended Release Strategy

### For Version 1.0.0 (Initial Release)

1. **PyPI** (Primary) - Reaches most Python users
2. **GitHub Releases** - Easy download access
3. **Docker Hub** - Containerized option

### For Future Releases

1. **GitHub Actions** - Automatic testing and publishing
2. **Homebrew** - Once stable and popular
3. **Keep all updated** - Consistency across platforms

---

## 🔐 Security Best Practices

- ✅ Use PyPI tokens (not passwords)
- ✅ Store tokens in GitHub Secrets (not in code)
- ✅ Sign releases with GPG (optional)
- ✅ Use read-only tokens for CI/CD
- ✅ Rotate tokens regularly
- ✅ Don't commit .pypirc with real tokens

---

## 📝 Release Notes Template

```markdown
## v1.0.0 - December 29, 2024

### ✨ Features

- Beautiful TUI with Textual framework
- Real-time face recognition
- Student attendance logging

### 🐛 Bug Fixes

- Fixed camera issue on macOS
- Resolved TensorFlow compatibility

### 📦 Installation

- pip: `pip install smart-attendance`
- Homebrew: `brew install yourusername/smart-attendance/smart-attendance`
- Docker: `docker run -it yourusername/smart-attendance`

### 🙏 Thanks

- Thanks to all contributors!
```

---

## 🚀 Quick Launch

### One-Line Setup for Users

Homebrew:

```bash
brew tap yourusername/smart-attendance && brew install smart-attendance && smart-attendance
```

Pip:

```bash
pip install smart-attendance && smart-attendance
```

Docker:

```bash
docker run -it yourusername/smart-attendance
```

Direct:

```bash
git clone https://github.com/yourusername/smart-attendance.git && cd smart-attendance && chmod +x install.sh && ./install.sh
```

---

## 📞 Support for Users

Add to your README:

```markdown
### Installation

**Recommended: Homebrew (macOS)**
\`\`\`bash
brew install yourusername/smart-attendance/smart-attendance
smart-attendance
\`\`\`

**Alternative: Pip (All platforms)**
\`\`\`bash
pip install smart-attendance
smart-attendance
\`\`\`

**Alternative: Docker**
\`\`\`bash
docker run -it yourusername/smart-attendance
\`\`\`
```

---

**Next Steps:**

1. Create PyPI account
2. Update version numbers
3. Run `./scripts/publish-pypi.sh`
4. Create GitHub release
5. Celebrate! 🎉
