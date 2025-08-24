#!/usr/bin/env python3
"""
🍽️ Restaurant Reservation System - Easy Setup Script
This script helps your friends set up the app quickly!
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("🍽️" + "="*50)
    print("   Restaurant Reservation System Setup")
    print("="*52)
    print()

def check_python():
    print("✅ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   Python {version.major}.{version.minor} - Great!")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Need Python 3.8+")
        print("   Please download from: https://python.org")
        return False

def setup_virtual_environment():
    print("\n📦 Setting up virtual environment...")
    if not os.path.exists('venv'):
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            print("   ✅ Virtual environment created!")
        except subprocess.CalledProcessError:
            print("   ❌ Failed to create virtual environment")
            return False
    else:
        print("   ✅ Virtual environment already exists!")
    return True

def install_packages():
    print("\n📚 Installing required packages...")
    
    # Determine the activation script
    system = platform.system()
    if system == "Windows":
        python_path = os.path.join('venv', 'Scripts', 'python')
        pip_path = os.path.join('venv', 'Scripts', 'pip')
    else:
        python_path = os.path.join('venv', 'bin', 'python')
        pip_path = os.path.join('venv', 'bin', 'pip')
    
    try:
        subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
        print("   ✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Failed to install packages")
        print("   Try manually: pip install -r requirements.txt")
        return False

def check_database():
    print("\n🗄️ Database Setup Instructions:")
    print("   1. Make sure XAMPP is running with MySQL started")
    print("   2. Open phpMyAdmin (http://localhost/phpmyadmin)")
    print("   3. Create database: 'restaurant_reservation_db'")
    print("   4. The app will create tables automatically!")
    print()

def show_completion():
    print("🎉" + "="*50)
    print("             SETUP COMPLETE!")
    print("="*52)
    print()
    print("🚀 To start the app:")
    
    system = platform.system()
    if system == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("   python app.py")
    print()
    print("🌐 Then open: http://localhost:5001")
    print("🔑 Admin login: admin / admin123")
    print()
    print("📖 For more help, see: SETUP_FOR_FRIENDS.md")
    print("="*52)

def main():
    print_header()
    
    if not check_python():
        sys.exit(1)
    
    if not setup_virtual_environment():
        sys.exit(1)
    
    if not install_packages():
        sys.exit(1)
    
    check_database()
    show_completion()

if __name__ == "__main__":
    main()
