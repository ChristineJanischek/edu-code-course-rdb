import os

API_VERSION = "v1"
MAX_REQUEST_BYTES = int(os.getenv("MAX_REQUEST_BYTES", "262144"))

ALLOWED_SUBMISSION_KINDS = {
    "answer",
    "summary",
    "translation",
    "transcript",
    "note",
    "code",
}

ALLOWED_SUBMISSION_STATUS = {"submitted", "draft", "reviewed", "published"}

SUBMISSION_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS learning_submissions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    submission_uuid CHAR(32) NOT NULL UNIQUE,
    learner_alias VARCHAR(80) NOT NULL,
    task_id VARCHAR(120) NOT NULL,
    response_kind VARCHAR(32) NOT NULL,
    response_text LONGTEXT NOT NULL,
    source_context VARCHAR(160) DEFAULT NULL,
    metadata_json LONGTEXT DEFAULT NULL,
    teacher_note LONGTEXT DEFAULT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'submitted',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_learning_submissions_learner_alias (learner_alias),
    INDEX idx_learning_submissions_task_id (task_id),
    INDEX idx_learning_submissions_created_at (created_at)
)
"""
