# 🚀 Restaurant Reservation System - MySQL Deployment

## 🗄️ **MySQL Database Options for Production**

### **Option 1: PlanetScale (Recommended - MySQL Serverless)**
- **Free Tier**: 5GB storage, 1 billion reads/month
- **MySQL Compatible**: Drop-in replacement
- **Highly Scalable**: Auto-scaling, branching
- **Setup**: Sign up at [planetscale.com](https://planetscale.com)

### **Option 2: Railway MySQL**
- **Free Tier**: 1GB storage, $0.000463/GB-hour
- **Easy Setup**: One-click MySQL deployment
- **Great Integration**: Works perfectly with your Flask app

### **Option 3: Aiven MySQL**
- **Free Trial**: $300 credits, fully managed
- **Production Ready**: High availability, backups

## 🚀 **Deployment Steps**

### **Step 1: Set up MySQL Database**

**PlanetScale Setup:**
```bash
# Install PlanetScale CLI (optional)
# Or use web interface at app.planetscale.com

1. Create account at planetscale.com
2. Create database: "restaurant-reservation"
3. Get connection string from "Connect" tab
4. Copy the MySQL URL
```

**Railway Setup:**
```bash
1. Go to railway.app
2. Create new project
3. Add MySQL database
4. Copy connection string
```

### **Step 2: Prepare Your MySQL Connection String**

Your connection string will look like:
```
mysql://username:password@host:port/database_name
```

Example:
```
mysql://user:pass123@aws.connect.psdb.cloud:3306/restaurant-reservation
```

### **Step 3: Update Environment Variables**

When deploying to Render, set these environment variables:
- `MYSQL_URL`: Your MySQL connection string
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Random secret key

## 📁 **Updated Deployment Files**

I've already updated your deployment files for MySQL:

✅ **render.yaml**: Configured for external MySQL  
✅ **requirements.txt**: Includes MySQL connectors  
✅ **config.py**: Already supports MySQL URLs  
✅ **Procfile**: Production-ready gunicorn setup  

## 🔗 **Quick MySQL Connection Test**

Before deploying, test your MySQL connection:
```python
# Test script
import mysql.connector
from config import Config

try:
    # Test connection
    conn = mysql.connector.connect(Config.SQLALCHEMY_DATABASE_URI)
    print("✅ MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```
