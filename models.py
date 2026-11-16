from database import get_db

def search_jobs_db(keyword="", location=""):

    with get_db() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM jobs
            WHERE (title LIKE ? OR skills LIKE ?)
              AND location LIKE ?
            """,
            (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{location}%"
            )
        ).fetchall()

        return [dict(row) for row in rows]

def add_application_db(student_name, job_id):

    with get_db() as conn:

        job = conn.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,)
        ).fetchone()

        if job is None:
            return None

        cursor = conn.execute(
            """
            INSERT INTO applications (student_name, job_id)
            VALUES (?, ?)
            """,
            (student_name, job_id)
        )

        application = conn.execute(
            "SELECT * FROM applications WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        result = dict(application)
        result["job_title"] = job["title"]

        return result

def list_applications_db(student_name):

    with get_db() as conn:

        rows = conn.execute(
            """
            SELECT
                a.id,
                a.student_name,
                a.job_id,
                a.status,
                a.created_at,
                j.title AS job_title,
                j.company
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.student_name = ? COLLATE NOCASE
            ORDER BY a.id DESC
            """,
            (student_name,)
        ).fetchall()

        return [dict(row) for row in rows]

def update_application_db(application_id, status):

    with get_db() as conn:

        cursor = conn.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id)
        )

        if cursor.rowcount == 0:
            return None

        row = conn.execute(
            "SELECT * FROM applications WHERE id = ?",
            (application_id,)
        ).fetchone()

        return dict(row)

