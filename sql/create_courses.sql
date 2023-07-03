CREATE TABLE IF NOT EXISTS courses (
    course_code VARCHAR(20) NOT NULL,
    title TEXT NOT NULL,
    course_description TEXT,
    prerequisites TEXT,
    subject_id INT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    id INT AUTO_INCREMENT PRIMARY KEY
);
