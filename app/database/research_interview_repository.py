"""Database operations for research interviews."""

from app.models.research_interview import ResearchInterview


class ResearchInterviewRepository:
    """Handle CRUD operations for research interviews."""

    def __init__(self, database):
        self.database = database

    def create_interview(
        self,
        project_id: int,
        interview: ResearchInterview,
    ) -> int:
        """Save a research interview and return its database ID."""

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO research_interviews (
                    project_id,
                    problem_statement,
                    aim,
                    population,
                    data_source,
                    expected_outcome,
                    additional_information
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    interview.problem_statement,
                    interview.aim,
                    interview.population,
                    interview.data_source,
                    interview.expected_outcome,
                    interview.additional_information,
                ),
            )

            return cursor.lastrowid
