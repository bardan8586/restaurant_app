# 🍽️ Restaurant Reservation System - Easy Setup

## Quick Start for Friends!

Hey! Here's how to run this awesome restaurant reservation system on your computer:

### 📋 What You Need
- Python 3.8+ (Download from [python.org](https://python.org))
- MySQL (Download [XAMPP](https://www.apachefriends.org/) for easy setup)

### 🚀 Setup Steps (5 minutes!)

#### Step 1: Download the Files
1. Download all the project files to a folder like `restaurant-app`
2. Open Terminal/Command Prompt
3. Navigate to the folder: `cd path/to/restaurant-app`

#### Step 2: Install Python Packages
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### Step 3: Setup Database (XAMPP)
1. Start XAMPP and start MySQL service
2. Open phpMyAdmin (usually http://localhost/phpmyadmin)
3. Create a new database called `restaurant_reservation_db`
4. That's it! The app will create tables automatically.

#### Step 4: Run the App!
```bash
python app.py
```

🎉 **Done!** Open your browser and go to: http://localhost:5001

### 🎯 What You Can Do

#### For Customers:
- Visit: http://localhost:5001
- Book tables for any date/time
- See available tables in real-time
- Simple phone validation (just need 10+ digits)

#### For Admin (Restaurant Staff):
- Visit: http://localhost:5001/login
- **Username**: `admin`
- **Password**: `admin123`
- Confirm/cancel reservations
- View all bookings
- Manage restaurant tables
- Search reservations

### 🔧 Troubleshooting

**If you get port errors:**
- XAMPP MySQL might be on port 3307
- No worries! The app will still work.

**If database connection fails:**
- Make sure XAMPP MySQL is running
- Check that the database `restaurant_reservation_db` exists

**If you get "module not found" errors:**
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### 📱 Features You'll Love
- **Beautiful Interface**: Modern, responsive design
- **Real-time Updates**: See table availability instantly  
- **Smart Table Selection**: Automatically picks best available table
- **Admin Dashboard**: Complete booking management
- **Search & Filter**: Find reservations quickly
- **Status Indicators**: See system status at a glance

### 🎮 Try These Things:
1. Make a reservation for tonight
2. Login as admin and confirm it
3. Try booking multiple tables
4. Search for reservations by name
5. Add new restaurant tables

### 💡 Pro Tips:
- The app creates sample data automatically
- Admin can see real-time statistics
- Phone numbers just need to be 10+ digits
- Tables are auto-selected for best experience

**Have fun with your restaurant reservation system!** 🚀

---
*Built with Python Flask, MySQL, and lots of ❤️*
