# 🍽️ Restaurant Reservation System - Quick Setup Guide

## 📋 What's Included

This zip file contains a complete **Restaurant Reservation System** built for MIT400 Assessment 2. The system includes:

- ✅ **Customer Portal**: Make reservations online
- ✅ **Admin Dashboard**: Manage reservations and tables
- ✅ **MySQL Database**: Complete data management
- ✅ **RESTful APIs**: JSON-based data exchange
- ✅ **Professional Reports**: Technical documentation

---

## 🚀 Quick Start (Choose One Method)

### **Method 1: Automatic Setup (Recommended)**

**For Windows:**
```bash
# Double-click this file:
setup_windows.bat
```

**For Mac/Linux:**
```bash
# Run this command:
chmod +x setup_mac_linux.sh && ./setup_mac_linux.sh
```

**Alternative Python Setup:**
```bash
python easy_setup.py
```

### **Method 2: Manual Setup**

1. **Install Python 3.8+** (if not already installed)
2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # OR
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database:**
   ```bash
   python setup_database.py
   ```

5. **Run Application:**
   ```bash
   python app.py
   ```

---

## 🌐 Access the Application

After setup, open your browser and go to:
- **Customer Portal**: http://localhost:5001
- **Admin Login**: http://localhost:5001/login
  - Username: `admin`
  - Password: `admin123`

---

## 📁 Project Structure

```
restaurant_reservation/
├── app.py                    # Main Flask application
├── models.py                # Database models
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── database_schema.sql      # Database structure
├── templates/               # HTML templates
│   ├── index.html          # Customer portal
│   ├── admin.html          # Admin dashboard
│   └── ...
├── MIT400_Assessment2_Report.md  # Main assessment report
├── DIAGRAMS.md             # System diagrams
└── README.md               # Detailed documentation
```

---

## 🔧 Prerequisites

- **Python 3.8+** (Download from python.org)
- **MySQL Server** (XAMPP, MySQL Workbench, or standalone)
- **Web Browser** (Chrome, Firefox, Safari, Edge)

---

## 📊 Features Included

### **Customer Features:**
- ✅ View available tables
- ✅ Make reservations
- ✅ Real-time availability checking
- ✅ Responsive web design

### **Admin Features:**
- ✅ Dashboard with statistics
- ✅ Manage all reservations
- ✅ Confirm/cancel bookings
- ✅ Search functionality
- ✅ Table management

### **Technical Features:**
- ✅ RESTful API endpoints
- ✅ MySQL database with proper relationships
- ✅ Input validation
- ✅ Error handling
- ✅ Session management

---

## 🆘 Troubleshooting

### **Common Issues:**

1. **Port 5001 already in use:**
   ```bash
   # Kill existing process
   lsof -ti:5001 | xargs kill -9
   ```

2. **MySQL connection error:**
   - Ensure MySQL is running
   - Check username/password in `config.py`
   - Default: username=`root`, password=`` (empty)

3. **Module not found:**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Database doesn't exist:**
   ```bash
   python setup_database.py
   ```

---

## 📞 Support

If you encounter any issues:

1. Check the detailed **README.md** file
2. Review **troubleshooting** section
3. Ensure all **prerequisites** are installed
4. Try the **automatic setup** scripts first

---

## 📚 Documentation

- **README.md**: Comprehensive setup and usage guide
- **MIT400_Assessment2_Report.md**: Complete assessment report
- **DIAGRAMS.md**: System architecture diagrams
- **Restaurant_App_Report.md**: Technical overview

---

## ⚡ Quick Commands

```bash
# Start the application
python app.py

# Reset database
python setup_database.py

# Run tests
python test_system.py

# Check dependencies
pip list
```

---

## 🎯 What to Expect

After successful setup, you'll have:
- A fully functional restaurant booking system
- Admin panel for managing reservations
- Sample data for testing
- All APIs working properly
- Professional documentation

**Enjoy exploring the Restaurant Reservation System!** 🍽️✨
