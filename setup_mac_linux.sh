#!/bin/bash

echo ""
echo "==============================================="
echo "  Restaurant Reservation System - Mac/Linux Setup"
echo "==============================================="
echo ""

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "==============================================="
echo "             SETUP COMPLETE!"
echo "==============================================="
echo ""
echo "To start the app:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5001"
echo "Admin login: admin / admin123"
echo ""
echo "Make sure MySQL is running (XAMPP or Homebrew)!"
echo "==============================================="
