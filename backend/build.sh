#!/usr/bin/env bash
# Render build script for Fake Identity Screening backend
set -e

echo "==> Updating apt..."
apt-get update -qq

echo "==> Installing Tesseract OCR and OpenCV system dependencies..."
apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Build complete!"
