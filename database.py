import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent / "placemate.db"

@contextmanager
def get_db():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
        
def init_db():

    with get_db() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                skills TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                job_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'applied',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)
        count = conn.execute(
            "SELECT COUNT(*) FROM jobs"
        ).fetchone()[0]

        if count == 0:

            jobs = [
                (
                    "Junior Python Developer",
                    "TechNova",
                    "Chennai",
                    "python, sql"
                ),
                (
                    "Data Analyst Trainee",
                    "InsightWorks",
                    "Hyderabad",
                    "excel, sql, power bi"
                ),
                (
                    "ML Engineer Intern",
                    "VisionAI",
                    "Bengaluru",
                    "python, pytorch"
                )
            ]

            conn.executemany("""
                INSERT INTO jobs (title, company, location, skills)
                VALUES (?, ?, ?, ?)
            """, jobs)

init_db()