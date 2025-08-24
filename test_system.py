#!/usr/bin/env python3
"""
Test Script for Restaurant Reservation System
MIT400 Assessment 2

This script performs basic testing of the database models and core functionality.
Run this after setting up the database to verify everything works correctly.

Usage:
    python test_system.py
"""

import sys
import os
from datetime import datetime, date, time, timedelta
from config import Config
from models import db, Customer, Table, Reservation, User, find_available_tables, create_customer, create_reservation

def test_database_connection():
    """Test database connection"""
    print("🔗 Testing database connection...")
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.app_context():
            # Test basic database query
            table_count = Table.query.count()
            customer_count = Customer.query.count()
            reservation_count = Reservation.query.count()
            user_count = User.query.count()
            
            print(f"✓ Database connection successful")
            print(f"  - Tables: {table_count}")
            print(f"  - Customers: {customer_count}")
            print(f"  - Reservations: {reservation_count}")
            print(f"  - Users: {user_count}")
            
            return True
            
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_table_availability():
    """Test table availability checking"""
    print("\n🪑 Testing table availability...")
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.app_context():
            # Test date and time
            test_date = date.today() + timedelta(days=1)
            test_time = time(19, 0)  # 7:00 PM
            
            # Find available tables for 4 people
            available_tables = find_available_tables(test_date, test_time, 4)
            
            print(f"✓ Found {len(available_tables)} available tables for 4 people")
            for table in available_tables[:3]:  # Show first 3
                print(f"  - Table {table.table_number} (capacity: {table.capacity})")
            
            return True
            
    except Exception as e:
        print(f"✗ Table availability test failed: {e}")
        return False

def test_customer_creation():
    """Test customer creation"""
    print("\n👤 Testing customer creation...")
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.app_context():
            # Create test customer
            test_phone = f"555-TEST-{datetime.now().strftime('%H%M%S')}"
            customer = create_customer(
                first_name="Test",
                last_name="Customer",
                phone=test_phone,
                email="test@example.com"
            )
            
            if customer:
                print(f"✓ Customer created successfully: {customer.full_name}")
                print(f"  - ID: {customer.customer_id}")
                print(f"  - Phone: {customer.phone}")
                return True
            else:
                print("✗ Customer creation failed")
                return False
                
    except Exception as e:
        print(f"✗ Customer creation test failed: {e}")
        return False

def test_reservation_creation():
    """Test reservation creation"""
    print("\n📅 Testing reservation creation...")
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.app_context():
            # Get first available customer and table
            customer = Customer.query.first()
            if not customer:
                print("✗ No customers found for testing")
                return False
            
            # Find available table
            test_date = date.today() + timedelta(days=2)
            test_time = time(18, 30)  # 6:30 PM
            available_tables = find_available_tables(test_date, test_time, 2)
            
            if not available_tables:
                print("✗ No available tables found for testing")
                return False
            
            table = available_tables[0]
            
            # Create reservation
            reservation = create_reservation(
                customer_id=customer.customer_id,
                table_id=table.table_id,
                reservation_date=test_date,
                reservation_time=test_time,
                party_size=2,
                special_requests="Test reservation"
            )
            
            if reservation:
                print(f"✓ Reservation created successfully")
                print(f"  - ID: {reservation.reservation_id}")
                print(f"  - Customer: {reservation.customer.full_name}")
                print(f"  - Table: {reservation.table.table_number}")
                print(f"  - Date/Time: {reservation.datetime_str}")
                print(f"  - Status: {reservation.status}")
                return True
            else:
                print("✗ Reservation creation failed")
                return False
                
    except Exception as e:
        print(f"✗ Reservation creation test failed: {e}")
        return False

def test_user_authentication():
    """Test user authentication"""
    print("\n🔐 Testing user authentication...")
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.app_context():
            # Test admin user
            admin_user = User.query.filter_by(username='admin').first()
            
            if admin_user:
                print(f"✓ Admin user found: {admin_user.username}")
                print(f"  - Role: {admin_user.role}")
                print(f"  - Is Admin: {admin_user.is_admin()}")
                print(f"  - Is Staff: {admin_user.is_staff()}")
                
                # Test password verification
                if admin_user.check_password('admin123'):
                    print("✓ Password verification successful")
                else:
                    print("✗ Password verification failed")
                    return False
                
                return True
            else:
                print("✗ Admin user not found")
                return False
                
    except Exception as e:
        print(f"✗ User authentication test failed: {e}")
        return False

def test_business_logic():
    """Test business logic constraints"""
    print("\n🧠 Testing business logic...")
    
    try:
        from app import create_app
        app = create_app('testing')
        
        with app.app_context():
            # Test 1: Cannot double-book a table
            print("  Testing double-booking prevention...")
            
            customer = Customer.query.first()
            table = Table.query.first()
            test_date = date.today() + timedelta(days=3)
            test_time = time(19, 0)
            
            # Create first reservation
            reservation1 = create_reservation(
                customer_id=customer.customer_id,
                table_id=table.table_id,
                reservation_date=test_date,
                reservation_time=test_time,
                party_size=2
            )
            
            if reservation1:
                # Try to create conflicting reservation
                reservation2 = create_reservation(
                    customer_id=customer.customer_id,
                    table_id=table.table_id,
                    reservation_date=test_date,
                    reservation_time=test_time,
                    party_size=2
                )
                
                if reservation2 is None:
                    print("  ✓ Double-booking prevention works")
                else:
                    print("  ✗ Double-booking prevention failed")
                    return False
            
            # Test 2: Reservation status changes
            print("  Testing reservation status changes...")
            if reservation1.confirm():
                print("  ✓ Reservation confirmation works")
            else:
                print("  ✗ Reservation confirmation failed")
                return False
            
            return True
            
    except Exception as e:
        print(f"✗ Business logic test failed: {e}")
        return False

def generate_test_report():
    """Generate a summary test report"""
    print("\n" + "="*60)
    print("🧪 RESTAURANT RESERVATION SYSTEM - TEST REPORT")
    print("="*60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Table Availability", test_table_availability),
        ("Customer Creation", test_customer_creation),
        ("Reservation Creation", test_reservation_creation),
        ("User Authentication", test_user_authentication),
        ("Business Logic", test_business_logic)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n⚠️  {test_name} test encountered an error: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready for use.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
    
    return failed == 0

def main():
    """Main test function"""
    print("🍽️  Restaurant Reservation System - Test Suite")
    print("MIT400 Assessment 2\n")
    
    # Check if database files exist
    required_files = ['app.py', 'models.py', 'config.py', 'database_schema.sql']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all project files are in the current directory.")
        sys.exit(1)
    
    try:
        # Run comprehensive tests
        success = generate_test_report()
        
        if success:
            print("\n✅ System is ready for demonstration!")
            print("\nNext steps:")
            print("1. Start the application: python app.py")
            print("2. Open browser to: http://localhost:5000")
            print("3. Test customer portal and admin dashboard")
            
        else:
            print("\n❌ System has issues that need to be resolved.")
            print("Please check the error messages above and fix any problems.")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease ensure:")
        print("1. All dependencies are installed: pip install -r requirements.txt")
        print("2. Virtual environment is activated (if using one)")
        print("3. Python path is set correctly")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
