# Smart Attendance - Docker Distribution
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data/students logs models reference

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SMART_ATTENDANCE_HOME=/app

# Expose port for potential web UI in future
EXPOSE 8000

# Run the application
CMD ["smart-attendance"]
