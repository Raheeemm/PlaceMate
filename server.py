from typing import Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import (
    ToolError,
    ResourceNotFoundError
)

from database import get_db

from models import (
    search_jobs_db,
    add_application_db,
    list_applications_db,
    update_application_db
)

mcp = MCPServer(
    "placemate-jobs",
    instructions=(
        "PlaceMate is a campus placement assistant. "
        "It helps students search jobs and track applications."
    )
)

@mcp.tool()
def search_jobs(
    keyword: str = "",
    location: str = ""
) -> list[dict]:

    """Search available jobs using keyword and location."""

    return search_jobs_db(keyword, location)

@mcp.tool()
def add_application(
    student_name: str,
    job_id: int
) -> dict:

    """Save a student's application for a job."""

    if not student_name.strip():
        raise ToolError("Student name cannot be empty.")

    application = add_application_db(student_name, job_id)

    if application is None:
        raise ToolError(
            f"Job ID {job_id} does not exist. Search for available jobs first."
        )

    return application

@mcp.tool()
def list_applications(student_name: str) -> list[dict]:

    """Show all applications belonging to a student."""

    return list_applications_db(student_name)

@mcp.tool()
def update_status(
    application_id: int,
    status: Literal[
        "applied",
        "shortlisted",
        "interview",
        "offer",
        "rejected"
    ]
) -> dict:

    """Update the status of a student's application."""

    result = update_application_db(application_id, status)

    if result is None:
        raise ToolError(
            f"Application ID {application_id} does not exist."
        )

    return result

if __name__ == "__main__":
    mcp.run()