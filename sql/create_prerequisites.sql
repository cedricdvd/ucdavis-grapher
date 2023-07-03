CREATE TABLE IF NOT EXISTS prerequisites (
    course_id INT NOT NULL,
    prerequisite_id INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (prerequisite_id) REFERENCES courses(id)
)