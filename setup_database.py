#!/usr/bin/env python3
"""
Database Setup Script for Restaurant Reservation System
MIT400 Assessment 2

This script creates the database and tables for the restaurant reservation system.
Run this script before starting the Flask application.

Usage:
    python setup_database.py

Requirements:
    - MySQL server running
    - mysql-connector-python installed
    - Proper database credentials in config.py
"""

import mysql.connector
from mysql.connector import Error
import sys
import os
from config import Config

def create_database():
    """Create the restaurant reservation database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
            print(f"✓ Database '{Config.MYSQL_DATABASE}' created successfully")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False

def execute_sql_file(file_path):
    """Execute SQL commands from a file"""
    try:
        # Connect to the specific database
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read and execute SQL file
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # Split by semicolon and execute each statement
            statements = sql_script.split(';')
            
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"Warning: {e}")
            
            connection.commit()
            print(f"✓ SQL file '{file_path}' executed successfully")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Error executing SQL file: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ SQL file '{file_path}' not found")
        return False

def verify_database_setup():
    """Verify that all tables were created successfully"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if all required tables exist
            required_tables = ['customers', 'tables', 'reservations', 'users']
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            print("\n📋 Database Setup Verification:")
            print(f"Database: {Config.MYSQL_DATABASE}")
            print("Tables created:")
            
            all_tables_exist = True
            for table in required_tables:
                if table in existing_tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"  ✓ {table} ({count} records)")
                else:
                    print(f"  ✗ {table} (missing)")
                    all_tables_exist = False
            
            # Check views
            cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
            views = cursor.fetchall()
            print(f"\nViews created: {len(views)}")
            for view in views:
                print(f"  ✓ {view[0]}")
            
            # Check procedures
            cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (Config.MYSQL_DATABASE,))
            procedures = cursor.fetchall()
            print(f"\nStored Procedures: {len(procedures)}")
            for proc in procedures:
                print(f"  ✓ {proc[1]}")
            
            cursor.close()
            connection.close()
            
            return all_tables_exist
            
    except Error as e:
        print(f"✗ Error verifying database setup: {e}")
        return False

def main():
    """Main setup function"""
    print("🏗️  Restaurant Reservation System - Database Setup")
    print("=" * 50)
    
    # Check if MySQL is accessible
    try:
        test_connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        test_connection.close()
        print("✓ MySQL connection successful")
    except Error as e:
        print(f"✗ Cannot connect to MySQL: {e}")
        print("\nPlease ensure:")
        print("1. MySQL server is running")
        print("2. Credentials in config.py are correct")
        print("3. MySQL port is accessible")
        sys.exit(1)
    
    # Step 1: Create database
    print("\n1. Creating database...")
    if not create_database():
        sys.exit(1)
    
    # Step 2: Execute SQL schema
    sql_file = "database_schema.sql"
    print(f"\n2. Executing SQL schema from {sql_file}...")
    if not os.path.exists(sql_file):
        print(f"✗ SQL file '{sql_file}' not found in current directory")
        print("Please ensure database_schema.sql is in the same directory as this script")
        sys.exit(1)
    
    if not execute_sql_file(sql_file):
        sys.exit(1)
    
    # Step 3: Verify setup
    print("\n3. Verifying database setup...")
    if verify_database_setup():
        print("\n🎉 Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Run the Flask application: python app.py")
    else:
        print("\n⚠️  Database setup completed with warnings")
        print("Some tables may be missing. Check the error messages above.")

if __name__ == "__main__":
    main()
