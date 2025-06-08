from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime, time
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'gymnasium_scheduler'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            user_type ENUM('student', 'admin') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            activity VARCHAR(255) NOT NULL,
            # period ENUM('AM', 'PM') NOT NULL,
            created_by VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create blocked_times table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_times (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            reason VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create announcements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            status ENUM('available', 'maintenance', 'closed') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['email'] = user[1]
            session['name'] = user[3]
            session['user_type'] = user[4]
            
            if user[4] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Determine user type based on email
        if email.endswith('@admin.apc.edu.ph'):
            user_type = 'admin'
        elif email.endswith('@student.apc.edu.ph'):
            user_type = 'student'
        else:
            flash('Please use a valid APC email address')
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('Email already registered')
            cursor.close()
            conn.close()
            return render_template('register.html')
        
        cursor.execute(
            'INSERT INTO users (name, email, password, user_type) VALUES (%s, %s, %s, %s)',
            (name, email, hashed_password, user_type)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    
    # Get announcements
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM announcements ORDER BY created_at DESC LIMIT 1')
    announcement = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('student_dashboard.html', announcement=announcement)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    return render_template('admin_dashboard.html')

@app.route('/check_availability')
def check_availability():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get existing schedules
    cursor.execute(
        'SELECT * FROM schedules WHERE date = %s ORDER BY start_time',
        (selected_date,)
    )
    schedules = cursor.fetchall()
    
    # Get blocked times
    cursor.execute(
        'SELECT * FROM blocked_times WHERE date = %s ORDER BY start_time',
        (selected_date,)
    )
    blocked_times = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('availability.html', 
                         schedules=schedules, 
                         blocked_times=blocked_times,
                         selected_date=selected_date)

from datetime import datetime
from flask import flash, redirect, render_template, request, session, url_for

@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        student_name = request.form['student_name']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        activity = request.form['activity']
        # period = request.form['period']

        # Validate time range (7:30 AM to 5:30 PM)
        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")

            if start_dt >= end_dt:
                flash("Start time must be before end time")
                return render_template('add_schedule.html', today=datetime.today().strftime('%Y-%m-%d'))

            # Court hours
            earliest = datetime.strptime("07:30", "%H:%M")
            latest = datetime.strptime("17:30", "%H:%M")

            if start_dt < earliest or end_dt > latest:
                flash("Court is only available from 7:30 AM to 5:30 PM")
                return render_template('add_schedule.html', today=datetime.today().strftime('%Y-%m-%d'))

        except ValueError:
            flash("Invalid time format")
            return render_template('add_schedule.html', today=datetime.today().strftime('%Y-%m-%d'))

        # Check for conflicts
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM schedules 
            WHERE date = %s AND (
                (start_time <= %s AND end_time > %s) OR
                (start_time < %s AND end_time >= %s) OR
                (start_time >= %s AND end_time <= %s)
            )
        ''', (date, start_time, start_time, end_time, end_time, start_time, end_time))

        if cursor.fetchone():
            flash('Time slot is already booked')
            cursor.close()
            conn.close()
            return render_template('add_schedule.html', today=datetime.today().strftime('%Y-%m-%d'))
        cursor.execute('''
            INSERT INTO schedules (student_name, date, start_time, end_time, activity, created_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (student_name, date, start_time, end_time, activity, session['email']))


        conn.commit()
        cursor.close()
        conn.close()

        flash('Schedule added successfully!')
        return redirect(url_for('check_availability'))

    # For GET request, send today's date to set min date in input
    return render_template('add_schedule.html', today=datetime.today().strftime('%Y-%m-%d'))


@app.route('/remove_schedule/<int:schedule_id>')
def remove_schedule(schedule_id):
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schedules WHERE id = %s', (schedule_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Schedule removed successfully!')
    return redirect(url_for('check_availability'))

@app.route('/block_time', methods=['GET', 'POST'])
def block_time():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        reason = request.form['reason']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO blocked_times (date, start_time, end_time, reason)
            VALUES (%s, %s, %s, %s)
        ''', (date, start_time, end_time, reason))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Time blocked successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('block_time.html')

@app.route('/manage_announcements', methods=['GET', 'POST'])
def manage_announcements():
    if 'user_id' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        status = request.form['status']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO announcements (title, message, status)
            VALUES (%s, %s, %s)
        ''', (title, message, status))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Announcement posted successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('manage_announcements.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
