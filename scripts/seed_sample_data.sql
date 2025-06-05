-- Insert sample schedules
INSERT INTO schedules (student_name, date, start_time, end_time, activity, period, created_by) VALUES 
('Alice Johnson', '2024-12-10', '08:00:00', '10:00:00', 'Basketball', 'AM', 'alice.johnson@student.apc.edu.ph'),
('Bob Smith', '2024-12-10', '14:00:00', '16:00:00', 'Volleyball', 'PM', 'bob.smith@student.apc.edu.ph'),
('Carol Brown', '2024-12-11', '09:00:00', '11:00:00', 'Badminton', 'AM', 'carol.brown@student.apc.edu.ph');

-- Insert sample blocked times
INSERT INTO blocked_times (date, start_time, end_time, reason) VALUES 
('2024-12-12', '10:00:00', '12:00:00', 'Physical Education Class'),
('2024-12-13', '13:00:00', '15:00:00', 'Equipment Maintenance');

-- Insert additional announcements
INSERT INTO announcements (title, message, status) VALUES 
('Maintenance Schedule', 'The gymnasium will undergo maintenance on December 15, 2024. No bookings will be accepted for that day.', 'maintenance'),
('New Equipment Available', 'We have added new basketball hoops and volleyball nets. Enjoy your games!', 'available');
