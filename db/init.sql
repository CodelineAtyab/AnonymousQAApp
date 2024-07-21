-- Create a table "question" to store questions posted by users
CREATE TABLE IF NOT EXISTS question (
    id VARCHAR(50) PRIMARY KEY,
    question_text TEXT
);

-- Insert some questions as dummy data
INSERT INTO question (id, question_text) VALUES ("q10", "Do you think, containerization is important to know");
INSERT INTO question (id, question_text) VALUES ("q11", "Do you work on multiple projects using different version of same dependency");
INSERT INTO question (id, question_text) VALUES ("q12", "Do you share solutions in the form of code with others");
INSERT INTO question (id, question_text) VALUES ("q13", "Do you have more than one machine (host) to run the same projects");
