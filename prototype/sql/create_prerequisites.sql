CREATE TABLE IF NOT EXISTS prerequisites (
    course_id INT NOT NULL,
    prerequisite_code VARCHAR(20),
    prerequisite_id INT,
    group_num INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (prerequisite_id) REFERENCES courses(id)
);
