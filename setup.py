"""
Setup configuration for Smart Attendance System
Enables packaging and distribution via pip, brew, and other package managers
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="smart-attendance",
    version="1.0.0",
    description="Face Recognition Attendance Management System with Beautiful TUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Smart Attendance Team",
    author_email="dev@smartattendance.local",
    url="https://github.com/yourusername/smart-attendance",
    license="MIT",
    
    # Package discovery
    packages=find_packages(),
    include_package_data=True,
    
    # Python version requirement
    python_requires=">=3.10",
    
    # Dependencies
    install_requires=[
        "numpy==1.26.4",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "tensorflow>=2.15.0",
        "keras-facenet>=0.13",
        "mtcnn>=0.1.1",
        "scipy>=1.11.0",
        "textual>=0.46.0",
        "rich>=13.7.0",
        "click>=8.1.0",
        "typer>=0.9.0",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
    ],
    
    # Optional dependencies for development
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
    },
    
    # Entry points for CLI
    entry_points={
        "console_scripts": [
            "smart-attendance=src.tui_app:main",
            "smart-attendance-tui=src.tui_app:main",
        ],
    },
    
    # Project metadata
    project_urls={
        "Documentation": "https://github.com/yourusername/smart-attendance#readme",
        "Source Code": "https://github.com/yourusername/smart-attendance",
        "Bug Reports": "https://github.com/yourusername/smart-attendance/issues",
    },
    
    # Classifiers for PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    
    # Keywords for searching
    keywords="attendance face-recognition machine-learning tensorflow deep-learning",
    
    # Zip safety
    zip_safe=False,
)
