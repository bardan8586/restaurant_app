# Restaurant Reservation System Configuration
# MIT400 Assessment 2 - Database Configuration

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration - supports multiple databases
    DATABASE_URL = os.environ.get('DATABASE_URL')
    MYSQL_URL = os.environ.get('MYSQL_URL')
    
    if DATABASE_URL and 'mysql' in DATABASE_URL:
        # Railway MySQL database
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif MYSQL_URL:
        # Alternative MySQL URL from Railway
        SQLALCHEMY_DATABASE_URI = MYSQL_URL
    elif DATABASE_URL:
        # PostgreSQL or other databases
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif os.environ.get('REPLIT_DB_URL'):
        # Replit environment - use SQLite for simplicity
        SQLALCHEMY_DATABASE_URI = 'sqlite:///restaurant.db'
    else:
        # Check if MySQL is available locally
        try:
            MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
            MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
            MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
            MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'restaurant_reservation_db'
            MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3307))
            
            # SQLAlchemy Configuration for MySQL
            SQLALCHEMY_DATABASE_URI = (
                f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
                f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
            )
        except:
            # Fallback to SQLite for easy deployment
            SQLALCHEMY_DATABASE_URI = 'sqlite:///restaurant.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL query logging
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Application Settings
    RESTAURANT_NAME = "Bella Vista Restaurant"
    OPENING_TIME = "17:00"  # 5:00 PM
    CLOSING_TIME = "22:00"  # 10:00 PM
    TIME_SLOT_DURATION = 30  # minutes
    MAX_ADVANCE_BOOKING_DAYS = 30
    
    # Pagination
    RESERVATIONS_PER_PAGE = 10
    
    # Email Configuration (for future implementation)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
