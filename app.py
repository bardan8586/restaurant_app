"""
Restaurant Reservation System - Main Application
MIT400 Assessment 2

This is the main Flask application for the restaurant reservation system.
It provides a web interface for customers to make reservations and for
administrators to manage the system.

Author: 
Date: [Current Date]
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, date, time, timedelta
import os
from config import config
from models import db, Customer, Table, Reservation, User, find_available_tables, create_customer, create_reservation

def create_app(config_name=None):
    """
    Application factory pattern
    
    Args:
        config_name (str): Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints and routes
    register_routes(app)
    
    return app

def register_routes(app):
    """Register all application routes"""
    
    @app.route('/')
    def index():
        """Main page - Customer portal"""
        return render_template('index.html')
    
    @app.route('/favicon.ico')
    def favicon():
        """Serve favicon"""
        from flask import send_from_directory, current_app
        import os
        try:
            return send_from_directory(
                os.path.join(current_app.root_path, 'static'),
                'favicon.svg', 
                mimetype='image/svg+xml'
            )
        except Exception as e:
            # Fallback: return a simple text response
            return "🍽️", 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    @app.route('/static/favicon.svg')
    def favicon_svg():
        """Serve SVG favicon directly"""
        from flask import send_from_directory, current_app
        import os
        return send_from_directory(
            os.path.join(current_app.root_path, 'static'),
            'favicon.svg', 
            mimetype='image/svg+xml'
        )
    
    @app.route('/api/tables/available')
    def get_available_tables():
        """
        API endpoint to get available tables
        
        Query Parameters:
            date (str): Reservation date (YYYY-MM-DD)
            time (str): Reservation time (HH:MM)
            party_size (int): Number of people
            
        Returns:
            JSON: List of available tables
        """
        try:
            reservation_date = request.args.get('date')
            reservation_time = request.args.get('time')
            party_size = request.args.get('party_size', type=int)
            
            if not all([reservation_date, reservation_time, party_size]):
                return jsonify({'error': 'Missing required parameters'}), 400
            
            # Parse date and time
            res_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()
            res_time = datetime.strptime(reservation_time, '%H:%M').time()
            
            # Find available tables
            available_tables = find_available_tables(res_date, res_time, party_size)
            
            return jsonify({
                'available_tables': [table.to_dict() for table in available_tables],
                'count': len(available_tables)
            })
            
        except ValueError as e:
            return jsonify({'error': 'Invalid date or time format'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/reservations', methods=['POST'])
    def create_reservation_api():
        """
        API endpoint to create a new reservation
        
        Expected JSON payload:
        {
            "first_name": "string",
            "last_name": "string", 
            "phone": "string",
            "email": "string" (optional),
            "date": "YYYY-MM-DD",
            "time": "HH:MM",
            "party_size": int,
            "special_requests": "string" (optional)
        }
        
        Returns:
            JSON: Reservation details or error message
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'phone', 'date', 'time', 'party_size']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Parse date and time
            res_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            res_time = datetime.strptime(data['time'], '%H:%M').time()
            
            # Validate future date
            if res_date < date.today():
                return jsonify({'error': 'Reservation date must be in the future'}), 400
            
            # Create or get customer
            customer = create_customer(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                email=data.get('email')
            )
            
            if not customer:
                return jsonify({'error': 'Failed to create customer'}), 500
            
            # Find available table
            available_tables = find_available_tables(res_date, res_time, data['party_size'])
            
            if not available_tables:
                return jsonify({
                    'error': f'No tables available for {data["party_size"]} people on {data["date"]} at {data["time"]}'
                }), 409
            
            # Use the smallest suitable table
            selected_table = available_tables[0]
            
            # Create reservation
            reservation = create_reservation(
                customer_id=customer.customer_id,
                table_id=selected_table.table_id,
                reservation_date=res_date,
                reservation_time=res_time,
                party_size=data['party_size'],
                special_requests=data.get('special_requests')
            )
            
            if not reservation:
                return jsonify({'error': 'Failed to create reservation'}), 500
            
            return jsonify({
                'message': 'Reservation created successfully',
                'reservation': reservation.to_dict()
            }), 201
            
        except ValueError as e:
            return jsonify({'error': 'Invalid date or time format'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login page"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Simple login - no password hashing
            if username == 'admin' and password == 'admin123':
                # Get or create admin user
                user = User.query.filter_by(username='admin').first()
                if not user:
                    user = User(
                        username='admin',
                        role='admin',
                        email='admin@restaurant.com'
                    )
                    user.password_hash = 'simple'  # Simple placeholder
                    db.session.add(user)
                    db.session.commit()
                
                login_user(user)
                flash('Welcome to Admin Dashboard!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password. Use: admin / admin123', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        logout_user()
        flash('You have been logged out successfully', 'success')
        return redirect(url_for('index'))
    
    @app.route('/admin', methods=['GET', 'POST'])
    @login_required
    def admin_dashboard():
        """Admin dashboard - requires staff/admin privileges"""
        if not current_user.is_staff():
            flash('Access denied. Staff privileges required.', 'error')
            return redirect(url_for('index'))
        
        # Get today's reservations
        today = date.today()
        today_reservations = Reservation.query.filter_by(reservation_date=today).all()
        
        # Get statistics
        total_reservations = len(today_reservations)
        confirmed_count = len([r for r in today_reservations if r.status == 'confirmed'])
        pending_count = len([r for r in today_reservations if r.status == 'pending'])
        
        # Get all tables
        all_tables = Table.query.all()
        available_tables = len([t for t in all_tables if t.status == 'available'])
        
        # Calculate occupancy rate (simplified)
        total_capacity = sum(t.capacity for t in all_tables if t.status == 'available')
        reserved_capacity = sum(r.party_size for r in today_reservations if r.status in ['confirmed', 'pending'])
        occupancy_rate = (reserved_capacity / total_capacity * 100) if total_capacity > 0 else 0
        
        return render_template('admin.html',
                             reservations=today_reservations,
                             stats={
                                 'total_reservations': total_reservations,
                                 'available_tables': available_tables,
                                 'occupancy_rate': round(occupancy_rate),
                                 'pending_count': pending_count
                             })
    
    @app.route('/admin/reservations')
    @login_required
    def admin_reservations():
        """Admin reservations management"""
        if not current_user.is_staff():
            flash('Access denied. Staff privileges required.', 'error')
            return redirect(url_for('index'))
        
        # Get all reservations with pagination
        page = request.args.get('page', 1, type=int)
        reservations = Reservation.query.order_by(Reservation.reservation_date.desc(), Reservation.reservation_time.desc()).paginate(
            page=page, per_page=app.config['RESERVATIONS_PER_PAGE'], error_out=False)
        
        return render_template('admin_reservations.html', reservations=reservations)
    
    @app.route('/admin/tables')
    @login_required
    def admin_tables():
        """Admin table management"""
        if not current_user.is_staff():
            flash('Access denied. Staff privileges required.', 'error')
            return redirect(url_for('index'))
        
        tables = Table.query.order_by(Table.table_number).all()
        return render_template('admin_tables.html', tables=tables)
    
    @app.route('/api/reservations/<int:reservation_id>/confirm', methods=['POST'])
    @login_required
    def confirm_reservation(reservation_id):
        """API endpoint to confirm a reservation"""
        if not current_user.is_staff():
            return jsonify({'error': 'Access denied'}), 403
        
        reservation = Reservation.query.get_or_404(reservation_id)
        
        if reservation.confirm():
            db.session.commit()
            return jsonify({'message': 'Reservation confirmed successfully'})
        else:
            return jsonify({'error': 'Cannot confirm this reservation'}), 400
    
    @app.route('/api/reservations/<int:reservation_id>/cancel', methods=['POST'])
    @login_required
    def cancel_reservation(reservation_id):
        """API endpoint to cancel a reservation"""
        if not current_user.is_staff():
            return jsonify({'error': 'Access denied'}), 403
        
        reservation = Reservation.query.get_or_404(reservation_id)
        
        if reservation.cancel():
            db.session.commit()
            return jsonify({'message': 'Reservation cancelled successfully'})
        else:
            return jsonify({'error': 'Cannot cancel this reservation'}), 400
    
    @app.route('/api/reservations/search')
    @login_required
    def search_reservations():
        """API endpoint to search reservations"""
        if not current_user.is_staff():
            return jsonify({'error': 'Access denied'}), 403
        
        search_term = request.args.get('q', '').lower()
        date_filter = request.args.get('date')
        
        query = Reservation.query
        
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter_by(reservation_date=filter_date)
            except ValueError:
                pass
        
        reservations = query.order_by(Reservation.reservation_date.desc(), 
                                    Reservation.reservation_time.desc()).all()
        
        if search_term:
            filtered_reservations = []
            for reservation in reservations:
                searchable_text = f"{reservation.customer.full_name} {reservation.customer.phone} {reservation.table.table_number}".lower()
                if search_term in searchable_text:
                    filtered_reservations.append(reservation)
            reservations = filtered_reservations
        
        return jsonify({
            'reservations': [reservation.to_dict() for reservation in reservations[:50]],
            'count': len(reservations)
        })
    
    @app.route('/api/stats')
    def get_stats():
        """Public API endpoint for basic restaurant stats"""
        try:
            total_tables = Table.query.filter_by(status='available').count()
            today = date.today()
            today_reservations = Reservation.query.filter_by(reservation_date=today).count()
            
            return jsonify({
                'total_tables': total_tables,
                'today_reservations': today_reservations,
                'restaurant_name': app.config.get('RESTAURANT_NAME', 'Bella Vista Restaurant'),
                'status': 'online'
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/database/view')
    @login_required
    def view_database():
        """API endpoint to view all database data - like phpMyAdmin"""
        if not current_user.is_admin():
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        try:
            # Get all data in JSON format
            customers = [customer.to_dict() for customer in Customer.query.all()]
            tables = [table.to_dict() for table in Table.query.all()]
            reservations = [reservation.to_dict() for reservation in Reservation.query.all()]
            users = [user.to_dict() for user in User.query.all()]
            
            return jsonify({
                'database_info': {
                    'type': 'SQLite',
                    'uri': app.config['SQLALCHEMY_DATABASE_URI']
                },
                'tables': {
                    'customers': {'count': len(customers), 'data': customers},
                    'tables': {'count': len(tables), 'data': tables},
                    'reservations': {'count': len(reservations), 'data': reservations},
                    'users': {'count': len(users), 'data': users}
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/tables', methods=['POST'])
    @login_required
    def create_table():
        """API endpoint to create a new table"""
        if not current_user.is_admin():
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['table_number', 'capacity']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            
            # Check if table number already exists
            existing_table = Table.query.filter_by(table_number=data['table_number']).first()
            if existing_table:
                return jsonify({'error': 'Table number already exists'}), 409
            
            table = Table(
                table_number=data['table_number'],
                capacity=data['capacity'],
                status=data.get('status', 'available'),
                location=data.get('location')
            )
            
            db.session.add(table)
            db.session.commit()
            
            return jsonify({
                'message': 'Table created successfully',
                'table': table.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/tables/<int:table_id>', methods=['GET'])
    @login_required
    def get_table(table_id):
        """API endpoint to get a specific table"""
        if not current_user.is_staff():
            return jsonify({'error': 'Access denied. Staff privileges required.'}), 403
        
        table = Table.query.get_or_404(table_id)
        return jsonify({'table': table.to_dict()})
    
    @app.route('/api/tables/<int:table_id>', methods=['PUT'])
    @login_required
    def update_table(table_id):
        """API endpoint to update a table"""
        if not current_user.is_admin():
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        try:
            table = Table.query.get_or_404(table_id)
            data = request.get_json()
            
            # Check if table number is being changed and if it already exists
            if 'table_number' in data and data['table_number'] != table.table_number:
                existing_table = Table.query.filter_by(table_number=data['table_number']).first()
                if existing_table:
                    return jsonify({'error': 'Table number already exists'}), 409
            
            # Update fields
            if 'table_number' in data:
                table.table_number = data['table_number']
            if 'capacity' in data:
                table.capacity = data['capacity']
            if 'status' in data:
                table.status = data['status']
            if 'location' in data:
                table.location = data['location']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Table updated successfully',
                'table': table.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/tables/<int:table_id>', methods=['DELETE'])
    @login_required
    def delete_table(table_id):
        """API endpoint to delete a table"""
        if not current_user.is_admin():
            return jsonify({'error': 'Access denied. Admin privileges required.'}), 403
        
        try:
            table = Table.query.get_or_404(table_id)
            
            # Check if table has active reservations
            active_reservations = Reservation.query.filter_by(
                table_id=table_id
            ).filter(Reservation.status.in_(['pending', 'confirmed'])).first()
            
            if active_reservations:
                return jsonify({'error': 'Cannot delete table with active reservations'}), 400
            
            db.session.delete(table)
            db.session.commit()
            
            return jsonify({'message': 'Table deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Template filters
    @app.template_filter('datetime')
    def datetime_filter(value):
        """Format datetime for templates"""
        if value is None:
            return ""
        return value.strftime('%Y-%m-%d %H:%M')
    
    @app.template_filter('date')
    def date_filter(value):
        """Format date for templates"""
        if value is None:
            return ""
        return value.strftime('%Y-%m-%d')
    
    @app.template_filter('time')
    def time_filter(value):
        """Format time for templates"""
        if value is None:
            return ""
        return value.strftime('%I:%M %p')

# Application factory
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Simple admin user setup - no password hashing needed
        print("Admin Login: username=admin, password=admin123")
    
    # Run the application
    print("🍽️ Restaurant Reservation System Starting...")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Use PORT environment variable for production (Railway, Heroku, Render)
    port = int(os.environ.get('PORT', 5001))
    is_production = (os.environ.get('RAILWAY_ENVIRONMENT') or 
                    os.environ.get('HEROKU_APP_NAME') or 
                    os.environ.get('RENDER_EXTERNAL_URL'))
    
    if is_production:
        print(f"🚀 Running in production mode on port {port}")
        print(f"🌐 Access URL: {os.environ.get('RENDER_EXTERNAL_URL', 'Production environment')}")
        print("👨‍💼 Admin login: username=admin, password=admin123")
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        print("🏠 Development mode")
        print("Access the application at: http://localhost:5001")
        print("Admin login: username=admin, password=admin123")
        app.run(debug=True, host='0.0.0.0', port=port)
