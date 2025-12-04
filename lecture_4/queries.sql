-- 1. CONFIGURATION AND SCHEMA DROPPING

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Drop existing tables to ensure a clean slate on rerun
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;


-- 2. CREATE TABLES

-- Create the students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Create the grades table with foreign key and grade check constraint
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
    -- If a student is deleted, their grades are automatically deleted
    FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
);


-- 3. INSERT SAMPLE DATA

-- Insert students data (IDs 1 through 9 are automatically generated)
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Insert grades data (using student IDs 1-9)
INSERT INTO grades (student_id, subject, grade) VALUES
(1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
(2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
(3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
(4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
(5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
(6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
(7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
(8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
(9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92);


-- 4. OPTIMIZATION: CREATE INDEXES

-- Index for fast JOINs and grade lookups by student_id
CREATE INDEX idx_grades_student_id ON grades(student_id);
-- Index for fast aggregation/grouping by subject
CREATE INDEX idx_grades_subject ON grades(subject);
-- Index for efficient lookup by birth year
CREATE INDEX idx_students_birth_year ON students(birth_year);


-- 5. ANALYTICAL QUERIES

-- Find all grades for Alice Johnson
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson';

-- Calculate the average grade per student, rounded to 2 decimals
SELECT s.full_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM students s
JOIN grades g ON g.student_id = s.id
GROUP BY s.id
ORDER BY avg_grade DESC;

-- List all students born after 2004
SELECT full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year DESC;

-- List all subjects and their average grades
SELECT subject, ROUND(AVG(grade), 2) AS avg_grade
FROM grades
GROUP BY subject
ORDER BY avg_grade DESC;

-- Find the top 3 students with the highest average grades
SELECT s.full_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 3;

-- Show all students who scored below 80 (show name, subject, and grade)
SELECT DISTINCT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name, g.grade ASC;