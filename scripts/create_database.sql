-- Create the gymnasium_scheduler database
CREATE DATABASE IF NOT EXISTS gymnasium_scheduler;
USE gymnasium_scheduler;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    user_type ENUM('student', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create schedules table
CREATE TABLE IF NOT EXISTS schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    activity VARCHAR(255) NOT NULL,
    period ENUM('AM', 'PM') NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create blocked_times table
CREATE TABLE IF NOT EXISTS blocked_times (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create announcements table
CREATE TABLE IF NOT EXISTS announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('available', 'maintenance', 'closed') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample admin user (password: admin123)
INSERT INTO users (name, email, password, user_type) VALUES 
('Admin User', 'admin@admin.apc.edu.ph', 'scrypt:32768:8:1$8vQZGxJHFKqOQxJH$46d4c9e7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5', 'admin');

-- Insert sample student user (password: student123)
INSERT INTO users (name, email, password, user_type) VALUES 
('John Doe', 'john.doe@student.apc.edu.ph', 'scrypt:32768:8:1$9wRaHyKIGLrPRyKI$57e5d0f8f9g0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6', 'student');

-- Insert sample announcement
INSERT INTO announcements (title, message, status) VALUES 
('Welcome to APC Gymnasium Scheduler', 'The gymnasium is now available for booking. Please follow the guidelines and book your slots in advance.', 'available');
