# Restaurant Reservation System

**MIT400 Assessment 2 - Principles of Programming & Database Management Systems**

A comprehensive web-based restaurant reservation system built with Python Flask and MySQL, featuring customer booking capabilities and administrative management tools.

## 🏗️ Project Overview

This system allows customers to make table reservations online and provides restaurant staff with tools to manage reservations, tables, and overall restaurant operations.

### Key Features

- **Customer Portal**: Online reservation booking with real-time table availability
- **Admin Dashboard**: Comprehensive management interface for staff
- **Database Integration**: MySQL backend with proper relationships and constraints
- **User Authentication**: Role-based access control (Admin/Staff/Customer)
- **Responsive Design**: Modern web interface that works on all devices
- **Real-time Updates**: Dynamic table availability checking
- **Data Validation**: Comprehensive input validation and error handling

## 🛠️ Technology Stack

- **Backend**: Python 3.8+ with Flask framework
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **Authentication**: Flask-Login with bcrypt password hashing
- **ORM**: SQLAlchemy for database operations
- **Database Connector**: PyMySQL

## 📋 System Requirements

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package installer)
- Modern web browser

## 🚀 Installation Guide

### Step 1: Clone/Download Project Files

Ensure you have all the following files in your project directory:
```
restaurant-reservation-system/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── models.py               # Database models
├── setup_database.py       # Database setup script
├── database_schema.sql     # SQL schema file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── templates/             # HTML templates
    ├── base.html
    ├── index.html
    ├── admin.html
    ├── admin_tables.html
    ├── login.html
    ├── 404.html
    └── 500.html
```

### Step 2: Install MySQL Server

**On macOS (using Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**On Windows:**
1. Download MySQL installer from https://dev.mysql.com/downloads/installer/
2. Follow the installation wizard
3. Remember your root password

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

### Step 3: Configure MySQL

1. Connect to MySQL as root:
```bash
mysql -u root -p
```

2. Create a database user (optional but recommended):
```sql
CREATE USER 'restaurant_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON restaurant_reservation_db.* TO 'restaurant_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 4: Install Python Dependencies

1. Navigate to your project directory:
```bash
cd /path/to/restaurant-reservation-system
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

4. Install required packages:
```bash
pip install -r requirements.txt
```

### Step 5: Configure Database Connection

Edit `config.py` and update the database connection settings:

```python
# Update these values in config.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'restaurant_user'  # or 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'restaurant_reservation_db'
MYSQL_PORT = 3306
```

### Step 6: Set Up the Database

Run the database setup script:
```bash
python setup_database.py
```

This script will:
- Create the database
- Create all tables with proper constraints
- Insert sample data
- Create views and stored procedures
- Verify the setup

### Step 7: Run the Application

Start the Flask development server:
```bash
python app.py
```

The application will be available at: http://localhost:5000

## 🔐 Default Login Credentials

- **Username**: admin
- **Password**: admin123

**⚠️ Important**: Change these credentials immediately in a production environment!

## 📊 Database Schema

### Entity Relationship Diagram

The system uses four main entities:

1. **CUSTOMERS**: Customer information
2. **TABLES**: Restaurant table details
3. **RESERVATIONS**: Booking information
4. **USERS**: System authentication

### Key Relationships

- One Customer can have many Reservations (1:M)
- One Table can have many Reservations (1:M)
- Each Reservation belongs to one Customer and one Table

### Sample Data

The system comes pre-loaded with:
- 8 sample tables (various capacities and locations)
- 3 system users (admin and staff accounts)
- 5 sample customers
- 5 sample reservations

## 🎯 Core Features

### Customer Portal

- **Make Reservations**: Select date, time, and party size
- **Real-time Availability**: See available tables instantly
- **Customer Information**: Manage customer details
- **Special Requests**: Add notes for special occasions

### Admin Dashboard

- **Statistics Overview**: Daily reservation counts and occupancy rates
- **Reservation Management**: Confirm, modify, or cancel bookings
- **Table Management**: Add, edit, or remove tables
- **User Management**: Control system access

### API Endpoints

- `GET /api/tables/available` - Check table availability
- `POST /api/reservations` - Create new reservation
- `POST /api/reservations/{id}/confirm` - Confirm reservation
- `POST /api/reservations/{id}/cancel` - Cancel reservation
- `POST /api/tables` - Add new table

## 🧪 Testing Guide

### Manual Testing

1. **Customer Booking Flow**:
   - Navigate to http://localhost:5000
   - Fill out reservation form
   - Verify table availability updates
   - Submit reservation
   - Check confirmation message

2. **Admin Functions**:
   - Login with admin credentials
   - View dashboard statistics
   - Confirm/cancel reservations
   - Add new tables

### Database Testing

Run the verification script to check database integrity:
```bash
python setup_database.py
```

## 🔧 Configuration Options

### Environment Variables

You can use environment variables instead of hardcoding values in `config.py`:

```bash
export MYSQL_HOST=localhost
export MYSQL_USER=restaurant_user
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=restaurant_reservation_db
export SECRET_KEY=your-secret-key
```

### Application Settings

Key configuration options in `config.py`:
- `RESTAURANT_NAME`: Restaurant name displayed in UI
- `OPENING_TIME` / `CLOSING_TIME`: Business hours
- `MAX_ADVANCE_BOOKING_DAYS`: How far ahead bookings are allowed
- `RESERVATIONS_PER_PAGE`: Pagination for admin views

## 📝 Development Notes

### Code Structure

- **app.py**: Main Flask application with routes and API endpoints
- **models.py**: SQLAlchemy database models and utility functions
- **config.py**: Configuration classes for different environments
- **setup_database.py**: Database initialization and verification script

### Design Patterns Used

- **Application Factory Pattern**: For creating Flask app instances
- **MVC Architecture**: Clear separation of models, views, and controllers
- **Repository Pattern**: Database operations encapsulated in model methods

### Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **CSRF Protection**: Flask-WTF for form security
- **Role-based Access**: Different permission levels for users

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Verify MySQL server is running
   - Check credentials in `config.py`
   - Ensure database user has proper permissions

2. **Module Import Errors**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Template Not Found**:
   - Verify all template files are in the `templates/` directory
   - Check file permissions

4. **Port Already in Use**:
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill the process using port 5000

### Debug Mode

Enable debug mode by setting in `config.py`:
```python
DEBUG = True
SQLALCHEMY_ECHO = True  # Shows SQL queries
```

## 📚 Further Development

### Potential Enhancements

1. **Email Notifications**: Send confirmation emails to customers
2. **SMS Integration**: Text message reminders
3. **Payment Processing**: Online payment for reservations
4. **Reporting**: Advanced analytics and reporting features
5. **Mobile App**: Native mobile application
6. **Multi-restaurant**: Support for restaurant chains

### API Extensions

- RESTful API with proper HTTP status codes
- API documentation with Swagger/OpenAPI
- Rate limiting and authentication tokens
- Webhook support for third-party integrations

## 📞 Support

For questions or issues with this assessment project:

1. Review this README thoroughly
2. Check the database setup logs
3. Verify all dependencies are installed
4. Ensure MySQL server is running and accessible

## 📄 License

This project is created for educational purposes as part of MIT400 Assessment 2.

---

**Author**: [Your Name]  
**Student ID**: [Your Student ID]  
**Date**: [Current Date]  
**Unit**: MIT400 - Principles of Programming & Database Management Systems
