-- Restaurant Reservation System Database Schema
-- MIT400 Assessment 2 - Database Design
-- Author: [Your Name]
-- Date: [Current Date]

-- Create the database
CREATE DATABASE IF NOT EXISTS restaurant_reservation_db;
USE restaurant_reservation_db;

-- Table: CUSTOMERS
-- Stores customer information for reservations
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for better performance
    INDEX idx_phone (phone),
    INDEX idx_email (email)
);

-- Table: TABLES
-- Stores restaurant table information
CREATE TABLE tables (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    capacity INT NOT NULL CHECK (capacity > 0),
    status ENUM('available', 'reserved', 'maintenance') DEFAULT 'available',
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_table_number (table_number),
    INDEX idx_capacity (capacity),
    INDEX idx_status (status)
);

-- Table: USERS
-- Stores system users (admin, staff)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff', 'customer') DEFAULT 'customer',
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    -- Indexes
    INDEX idx_username (username),
    INDEX idx_role (role)
);

-- Table: RESERVATIONS
-- Stores reservation information
CREATE TABLE reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    table_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    party_size INT NOT NULL CHECK (party_size > 0),
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_reservations_customer 
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    CONSTRAINT fk_reservations_table 
        FOREIGN KEY (table_id) REFERENCES tables(table_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    
    -- Unique constraint to prevent double booking
    CONSTRAINT unique_table_datetime 
        UNIQUE (table_id, reservation_date, reservation_time),
    
    -- Indexes for better performance
    INDEX idx_customer_id (customer_id),
    INDEX idx_table_id (table_id),
    INDEX idx_reservation_date (reservation_date),
    INDEX idx_status (status),
    INDEX idx_datetime (reservation_date, reservation_time)
);

-- Insert sample data

-- Sample Tables
INSERT INTO tables (table_number, capacity, status, location) VALUES
(1, 2, 'available', 'Window Side'),
(2, 4, 'available', 'Center'),
(3, 6, 'available', 'Private Corner'),
(4, 4, 'available', 'Garden View'),
(5, 8, 'available', 'Large Group Area'),
(6, 2, 'available', 'Bar Area'),
(7, 4, 'maintenance', 'Center'),
(8, 6, 'available', 'VIP Section');

-- Sample Users
INSERT INTO users (username, password_hash, role, email) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsRXa.KQCe', 'admin', 'admin@bellavista.com'),
('staff1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsRXa.KQCe', 'staff', 'staff1@bellavista.com'),
('staff2', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsRXa.KQCe', 'staff', 'staff2@bellavista.com');

-- Sample Customers
INSERT INTO customers (first_name, last_name, phone, email) VALUES
('John', 'Smith', '+1 (555) 123-4567', 'john.smith@email.com'),
('Sarah', 'Johnson', '+44 20 7946 0958', 'sarah.johnson@email.com'),
('Mike', 'Davis', '+1 (555) 456-7890', 'mike.davis@email.com'),
('Emily', 'Brown', '+33 1 42 86 83 26', 'emily.brown@email.com'),
('David', 'Wilson', '+977 1 4567890', 'david.wilson@email.com');

-- Sample Reservations
INSERT INTO reservations (customer_id, table_id, reservation_date, reservation_time, party_size, status, special_requests) VALUES
(1, 2, '2024-12-20', '19:00:00', 4, 'confirmed', 'Birthday celebration - need cake service'),
(2, 5, '2024-12-20', '20:30:00', 2, 'pending', NULL),
(3, 1, '2024-12-21', '18:00:00', 3, 'confirmed', 'Window seat preferred'),
(4, 3, '2024-12-21', '19:30:00', 6, 'pending', 'Business dinner'),
(5, 4, '2024-12-22', '18:30:00', 4, 'confirmed', 'Anniversary dinner');

-- Create views for common queries

-- View: Available tables for a specific date and time
CREATE VIEW available_tables_view AS
SELECT 
    t.table_id,
    t.table_number,
    t.capacity,
    t.location,
    t.status
FROM tables t
WHERE t.status = 'available';

-- View: Today's reservations
CREATE VIEW todays_reservations AS
SELECT 
    r.reservation_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.phone,
    t.table_number,
    r.reservation_time,
    r.party_size,
    r.status,
    r.special_requests
FROM reservations r
JOIN customers c ON r.customer_id = c.customer_id
JOIN tables t ON r.table_id = t.table_id
WHERE r.reservation_date = CURDATE()
ORDER BY r.reservation_time;

-- View: Reservation statistics
CREATE VIEW reservation_stats AS
SELECT 
    COUNT(*) as total_reservations,
    COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmed_count,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled_count,
    AVG(party_size) as avg_party_size
FROM reservations
WHERE reservation_date = CURDATE();

-- Note: Stored procedures and triggers removed for compatibility
-- These can be implemented in Python application logic

-- Add comments to document the schema
ALTER TABLE customers COMMENT = 'Stores customer information for the restaurant reservation system';
ALTER TABLE tables COMMENT = 'Stores restaurant table information including capacity and status';
ALTER TABLE reservations COMMENT = 'Stores all reservation data with foreign key relationships to customers and tables';
ALTER TABLE users COMMENT = 'Stores system users for authentication and role-based access';

-- Show database structure
SHOW TABLES;
DESCRIBE customers;
DESCRIBE tables;
DESCRIBE reservations;
DESCRIBE users;
