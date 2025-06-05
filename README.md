# APC Gymnasium Scheduler

A web-based gymnasium scheduling system for Asia Pacific College students and administrators.

## Features

### Student Features
- Login/Logout with APC student email (@student.apc.edu.ph)
- Check court availability
- Book time slots (7:30 AM - 5:30 PM)
- View announcements

### Admin Features
- All student features
- Remove any scheduled bookings
- Block time slots for classes/maintenance
- Post announcements about court status
- Manage court availability

## Setup Instructions

1. Install Python dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

2. Set up MySQL database:
   - Create a MySQL database named 'gymnasium_scheduler'
   - Update database credentials in app.py
   - Run the SQL scripts in the scripts folder

3. Run the application:
   \`\`\`
   python app.py
   \`\`\`

4. Access the application at http://localhost:5000

## Default Accounts

- Admin: admin@admin.apc.edu.ph (password: admin123)
- Student: john.doe@student.apc.edu.ph (password: student123)

## Database Schema

- users: Store user accounts (students and admins)
- schedules: Store court bookings
- blocked_times: Store blocked time slots
- announcements: Store court announcements

## Court Guidelines

- Available hours: 7:30 AM to 5:30 PM
- Maximum booking: 2 hours per session
- Advance booking required (minimum 1 day)
- Clean up after use
