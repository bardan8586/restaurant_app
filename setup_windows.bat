@echo off
echo.
echo ===============================================
echo   Restaurant Reservation System - Windows Setup
echo ===============================================
echo.

echo Installing Python packages...
python -m pip install -r requirements.txt

echo.
echo ===============================================
echo              SETUP COMPLETE!
echo ===============================================
echo.
echo To start the app:
echo   python app.py
echo.
echo Then open: http://localhost:5001
echo Admin login: admin / admin123
echo.
echo Make sure XAMPP MySQL is running!
echo ===============================================
pause
