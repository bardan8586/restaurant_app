#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # exit on error

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"
echo "🍽️ Restaurant Reservation System ready for deployment!"
