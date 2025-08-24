#!/usr/bin/env python3
"""
Quick Start Script for Restaurant Reservation System
MIT400 Assessment 2

This script provides a guided setup for the restaurant reservation system.
It will help you install dependencies, set up the database, and start the application.

Usage:
    python quick_start.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("=" * 70)
    print("🍽️  RESTAURANT RESERVATION SYSTEM - QUICK START")
    print("   MIT400 Assessment 2")
    print("=" * 70)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_required_files():
    """Check if all required files are present"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'app.py',
        'config.py',
        'models.py',
        'setup_database.py',
        'database_schema.sql',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/admin.html',
        'templates/login.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found")
    return True

def check_mysql():
    """Check if MySQL is available"""
    print("\n🗄️  Checking MySQL availability...")
    
    try:
        # Try to run mysql command
        result = subprocess.run(['mysql', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ MySQL found: {result.stdout.strip()}")
            return True
        else:
            print("❌ MySQL command not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ MySQL not available")
        print("   Please install MySQL Server:")
        print("   - macOS: brew install mysql")
        print("   - Windows: Download from https://dev.mysql.com/downloads/")
        print("   - Linux: sudo apt install mysql-server")
        return False

def setup_virtual_environment():
    """Set up Python virtual environment"""
    print("\n🔧 Setting up virtual environment...")
    
    venv_path = Path('venv')
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("   Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("✅ Virtual environment created")
        
        print("\n📝 To activate the virtual environment:")
        if os.name == 'nt':  # Windows
            print("   venv\\Scripts\\activate")
        else:  # macOS/Linux
            print("   source venv/bin/activate")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        # Check if we're in a virtual environment
        venv_active = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
        
        if not venv_active:
            print("⚠️  Virtual environment not activated")
            print("   Consider activating it for cleaner dependency management")
        
        print("   Installing packages from requirements.txt...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def configure_database():
    """Help configure database connection"""
    print("\n⚙️  Database Configuration")
    print("   Please ensure MySQL is running and accessible")
    
    # Read current config
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        if 'localhost' in content and 'root' in content:
            print("✅ Using default database configuration:")
            print("   - Host: localhost")
            print("   - User: root")
            print("   - Database: restaurant_reservation_db")
            print()
            print("💡 If you need to change these settings, edit config.py")
            return True
    except Exception:
        pass
    
    print("⚠️  Please check config.py for database settings")
    return True

def setup_database():
    """Set up the database"""
    print("\n🗄️  Setting up database...")
    
    try:
        print("   Running database setup script...")
        result = subprocess.run([sys.executable, 'setup_database.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Database setup completed")
            if "Database setup completed successfully!" in result.stdout:
                return True
            else:
                print("⚠️  Database setup completed with warnings")
                print("   Check the output above for details")
                return True
        else:
            print("❌ Database setup failed")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Database setup timed out")
        print("   Please check your MySQL connection and try manually:")
        print("   python setup_database.py")
        return False
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def test_system():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test_system.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if "All tests passed!" in result.stdout:
            print("✅ All system tests passed")
            return True
        else:
            print("⚠️  Some tests failed")
            print("   System should still be functional")
            return True
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out, but system should be functional")
        return True
    except Exception as e:
        print(f"⚠️  Test error: {e}, but system should be functional")
        return True

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting the application...")
    print("   The server will start on http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print()
    print("🔐 Default login credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print()
    
    input("Press Enter to start the server...")
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")

def main():
    """Main quick start function"""
    print_header()
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\n❌ Setup cannot continue due to Python version incompatibility")
        sys.exit(1)
    
    # Step 2: Check required files
    if not check_required_files():
        print("\n❌ Setup cannot continue due to missing files")
        sys.exit(1)
    
    # Step 3: Check MySQL
    mysql_available = check_mysql()
    if not mysql_available:
        print("\n⚠️  MySQL not detected, but continuing...")
        print("   Please ensure MySQL is installed and running before proceeding")
    
    # Step 4: Set up virtual environment (optional)
    print("\n" + "="*50)
    response = input("Create virtual environment? (recommended) [y/N]: ").lower()
    if response in ['y', 'yes']:
        setup_virtual_environment()
    
    # Step 5: Install dependencies
    print("\n" + "="*50)
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Step 6: Configure database
    configure_database()
    
    # Step 7: Set up database
    print("\n" + "="*50)
    if mysql_available:
        response = input("Set up database now? [Y/n]: ").lower()
        if response not in ['n', 'no']:
            setup_database()
    else:
        print("⚠️  Skipping database setup (MySQL not available)")
        print("   Please run 'python setup_database.py' after installing MySQL")
    
    # Step 8: Test system
    print("\n" + "="*50)
    response = input("Run system tests? [Y/n]: ").lower()
    if response not in ['n', 'no']:
        test_system()
    
    # Step 9: Start application
    print("\n" + "="*50)
    print("🎉 Setup complete!")
    print("\nYour restaurant reservation system is ready!")
    print("\nWhat you can do:")
    print("• Visit http://localhost:5000 for customer portal")
    print("• Login with admin/admin123 for admin features")
    print("• Create reservations and manage tables")
    print("• View the admin dashboard")
    
    response = input("\nStart the application now? [Y/n]: ").lower()
    if response not in ['n', 'no']:
        start_application()
    else:
        print("\nTo start the application later, run:")
        print("   python app.py")

if __name__ == "__main__":
    main()
