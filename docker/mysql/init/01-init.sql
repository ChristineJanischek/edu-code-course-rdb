CREATE TABLE IF NOT EXISTS demo_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS submissions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(128) NOT NULL,
  task_id VARCHAR(128) NOT NULL,
  content TEXT NOT NULL,
  content_type VARCHAR(32) NOT NULL DEFAULT 'text',
  source VARCHAR(32) NOT NULL DEFAULT 'webapp',
  status VARCHAR(32) NOT NULL DEFAULT 'submitted',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_submissions_student_id (student_id),
  INDEX idx_submissions_task_id (task_id),
  INDEX idx_submissions_created_at (created_at)
);

INSERT INTO demo_items (title)
VALUES ('Erster Eintrag'), ('Zweiter Eintrag'), ('Dritter Eintrag');
