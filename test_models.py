from models import (
    search_jobs_db,
    add_application_db,
    list_applications_db,
    update_application_db
)

# 1. Search jobs
print("\n--- SEARCH JOBS ---")
print(search_jobs_db("python", "Chennai"))

# 2. Add application
print("\n--- ADD APPLICATION ---")
print(add_application_db("Raheem", 1))

# 3. List applications
print("\n--- LIST APPLICATIONS ---")
print(list_applications_db("Raheem"))

# 4. Update status
print("\n--- UPDATE STATUS ---")
print(update_application_db(1, "shortlisted"))
