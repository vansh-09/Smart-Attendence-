# Smart Attendance System - Makefile for common tasks

.PHONY: help install dev-install test lint format clean run build docker-build docker-run

help:
	@echo "Smart Attendance System - Available Commands"
	@echo "============================================="
	@echo ""
	@echo "  make install       - Install dependencies and package"
	@echo "  make dev-install   - Install with development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Check code quality"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make run           - Run the TUI application"
	@echo "  make build         - Build distribution packages"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo ""

install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt
	pip install -e .

dev-install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pip install build twine

test:
	pytest -v

lint:
	flake8 src/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	black src/ --line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .mypy_cache/

run:
	python3 main.py

build:
	python3 -m build
	@echo "✓ Built distribution packages in dist/"

docker-build:
	docker build -t smart-attendance:latest .

docker-run:
	docker-compose up -d smart-attendance
	docker-compose exec smart-attendance smart-attendance

.DEFAULT_GOAL := help
