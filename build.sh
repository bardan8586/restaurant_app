#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️ Setting up database..."
python setup_database.py || echo "⚠️ Database setup failed, continuing with app startup..."

echo "✅ Build completed successfully!"