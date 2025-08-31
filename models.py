"""
Database Models for Restaurant Reservation System
MIT400 Assessment 2

This module defines SQLAlchemy models for the restaurant reservation system.
Models include Customer, Table, Reservation, and User entities with proper
relationships and constraints.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

class Customer(db.Model):
    """
    Customer model for storing customer information
    
    Attributes:
        customer_id (int): Primary key
        first_name (str): Customer's first name
        last_name (str): Customer's last name  
        phone (str): Customer's phone number (unique)
        email (str): Customer's email address (unique, optional)
        created_at (datetime): Record creation timestamp
        updated_at (datetime): Record last update timestamp
    """
    __tablename__ = 'customers'
    
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(30), nullable=False, unique=True, index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with reservations
    reservations = db.relationship('Reservation', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        """Returns the customer's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        """Convert customer object to dictionary"""
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Table(db.Model):
    """
    Table model for storing restaurant table information
    
    Attributes:
        table_id (int): Primary key
        table_number (int): Table number (unique)
        capacity (int): Number of people the table can seat
        status (str): Table status (available, reserved, maintenance)
        location (str): Table location description
        created_at (datetime): Record creation timestamp
        updated_at (datetime): Record last update timestamp
    """
    __tablename__ = 'tables'
    
    table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_number = db.Column(db.Integer, nullable=False, unique=True, index=True)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('available', 'reserved', 'maintenance'), default='available', index=True)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with reservations
    reservations = db.relationship('Reservation', backref='table', lazy=True, cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )
    
    def __repr__(self):
        return f'<Table {self.table_number} (capacity: {self.capacity})>'
    
    def is_available_at(self, reservation_date, reservation_time):
        """
        Check if table is available at specific date and time
        
        Args:
            reservation_date (date): Date to check
            reservation_time (time): Time to check
            
        Returns:
            bool: True if available, False otherwise
        """
        if self.status != 'available':
            return False
            
        # Check for existing reservations at this time
        existing_reservation = Reservation.query.filter_by(
            table_id=self.table_id,
            reservation_date=reservation_date,
            reservation_time=reservation_time
        ).filter(Reservation.status.in_(['pending', 'confirmed'])).first()
        
        return existing_reservation is None
    
    def to_dict(self):
        """Convert table object to dictionary"""
        return {
            'table_id': self.table_id,
            'table_number': self.table_number,
            'capacity': self.capacity,
            'status': self.status,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(UserMixin, db.Model):
    """
    User model for system authentication and authorization
    
    Attributes:
        user_id (int): Primary key
        username (str): Username (unique)
        password_hash (str): Hashed password
        role (str): User role (admin, staff, customer)
        email (str): User email (unique)
        created_at (datetime): Record creation timestamp
        last_login (datetime): Last login timestamp
    """
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'staff', 'customer'), default='customer', index=True)
    email = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    
    def get_id(self):
        """Required for Flask-Login"""
        return str(self.user_id)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_staff(self):
        """Check if user is staff or admin"""
        return self.role in ['admin', 'staff']
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Reservation(db.Model):
    """
    Reservation model for storing reservation information
    
    Attributes:
        reservation_id (int): Primary key
        customer_id (int): Foreign key to Customer
        table_id (int): Foreign key to Table
        reservation_date (date): Date of reservation
        reservation_time (time): Time of reservation
        party_size (int): Number of people in party
        status (str): Reservation status (pending, confirmed, cancelled, completed)
        special_requests (str): Special requests or notes
        created_at (datetime): Record creation timestamp
        updated_at (datetime): Record last update timestamp
    """
    __tablename__ = 'reservations'
    
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False, index=True)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.table_id'), nullable=False, index=True)
    reservation_date = db.Column(db.Date, nullable=False, index=True)
    reservation_time = db.Column(db.Time, nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled', 'completed'), default='pending', index=True)
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('party_size > 0', name='check_party_size_positive'),
        db.UniqueConstraint('table_id', 'reservation_date', 'reservation_time', name='unique_table_datetime'),
    )
    
    def __repr__(self):
        return f'<Reservation {self.reservation_id} for {self.party_size} people>'
    
    @property
    def datetime_str(self):
        """Returns formatted date and time string"""
        return f"{self.reservation_date} at {self.reservation_time.strftime('%I:%M %p')}"
    
    def can_be_modified(self):
        """Check if reservation can be modified"""
        return self.status in ['pending', 'confirmed']
    
    def can_be_cancelled(self):
        """Check if reservation can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def confirm(self):
        """Confirm the reservation"""
        if self.status == 'pending':
            self.status = 'confirmed'
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def cancel(self):
        """Cancel the reservation"""
        if self.can_be_cancelled():
            self.status = 'cancelled'
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def complete(self):
        """Mark reservation as completed"""
        if self.status == 'confirmed':
            self.status = 'completed'
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def to_dict(self):
        """Convert reservation object to dictionary"""
        return {
            'reservation_id': self.reservation_id,
            'customer_id': self.customer_id,
            'table_id': self.table_id,
            'reservation_date': self.reservation_date.isoformat() if self.reservation_date else None,
            'reservation_time': self.reservation_time.strftime('%H:%M:%S') if self.reservation_time else None,
            'party_size': self.party_size,
            'status': self.status,
            'special_requests': self.special_requests,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'table': self.table.to_dict() if self.table else None
        }

# Utility functions for database operations

def find_available_tables(reservation_date, reservation_time, party_size):
    """
    Find available tables for a specific date, time, and party size
    
    Args:
        reservation_date (date): Date for reservation
        reservation_time (time): Time for reservation
        party_size (int): Number of people in party
        
    Returns:
        list: List of available Table objects
    """
    # Get all tables with sufficient capacity
    suitable_tables = Table.query.filter(
        Table.capacity >= party_size,
        Table.status == 'available'
    ).all()
    
    # Filter out tables that are already reserved at this time
    available_tables = []
    for table in suitable_tables:
        if table.is_available_at(reservation_date, reservation_time):
            available_tables.append(table)
    
    # Sort by capacity (smallest suitable table first)
    available_tables.sort(key=lambda t: t.capacity)
    
    return available_tables

def create_customer(first_name, last_name, phone, email=None):
    """
    Create a new customer
    
    Args:
        first_name (str): Customer's first name
        last_name (str): Customer's last name
        phone (str): Customer's phone number
        email (str, optional): Customer's email
        
    Returns:
        Customer: Created customer object or None if error
    """
    try:
        # Check if customer with this phone already exists
        existing_customer = Customer.query.filter_by(phone=phone).first()
        if existing_customer:
            return existing_customer
        
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email
        )
        db.session.add(customer)
        db.session.commit()
        return customer
    except Exception as e:
        db.session.rollback()
        print(f"Error creating customer: {e}")
        return None

def create_reservation(customer_id, table_id, reservation_date, reservation_time, party_size, special_requests=None):
    """
    Create a new reservation
    
    Args:
        customer_id (int): Customer ID
        table_id (int): Table ID
        reservation_date (date): Date of reservation
        reservation_time (time): Time of reservation
        party_size (int): Number of people
        special_requests (str, optional): Special requests
        
    Returns:
        Reservation: Created reservation object or None if error
    """
    try:
        # Check if table is available
        table = Table.query.get(table_id)
        if not table or not table.is_available_at(reservation_date, reservation_time):
            return None
        
        reservation = Reservation(
            customer_id=customer_id,
            table_id=table_id,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            party_size=party_size,
            special_requests=special_requests
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation
    except Exception as e:
        db.session.rollback()
        print(f"Error creating reservation: {e}")
        return None
