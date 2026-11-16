from database import get_db

with get_db() as conn:
    jobs = conn.execute(
        "SELECT * FROM jobs"
    ).fetchall()

for job in jobs:
    print(dict(job))