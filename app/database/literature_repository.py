"""Database operations for research literature."""

from app.models.literature import Literature


class LiteratureRepository:
    """Handle CRUD operations for research literature."""

    def __init__(self, database):
        self.database = database

    def create_literature(
        self,
        literature: Literature,
    ) -> int:
        """Save a literature source and return its database ID."""

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO literature (
                    project_id,
                    title,
                    authors,
                    year,
                    publication,
                    doi,
                    url,
                    problem,
                    methodology,
                    findings,
                    research_gap,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    literature.project_id,
                    literature.title,
                    literature.authors,
                    literature.year,
                    literature.publication,
                    literature.doi,
                    literature.url,
                    literature.problem,
                    literature.methodology,
                    literature.findings,
                    literature.research_gap,
                    literature.notes,
                ),
            )

            literature.id = cursor.lastrowid

            return literature.id

    def get_literature(
        self,
        literature_id: int,
    ) -> Literature | None:
        """Retrieve one literature source by ID."""

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    project_id,
                    title,
                    authors,
                    year,
                    publication,
                    doi,
                    url,
                    problem,
                    methodology,
                    findings,
                    research_gap,
                    notes
                FROM literature
                WHERE id = ?
                """,
                (literature_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return Literature(
                id=row[0],
                project_id=row[1],
                title=row[2],
                authors=row[3],
                year=row[4],
                publication=row[5],
                doi=row[6],
                url=row[7],
                problem=row[8],
                methodology=row[9],
                findings=row[10],
                research_gap=row[11],
                notes=row[12],
            )

    def get_project_literature(
        self,
        project_id: int,
    ) -> list[Literature]:
        """Retrieve all literature belonging to a project."""

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    project_id,
                    title,
                    authors,
                    year,
                    publication,
                    doi,
                    url,
                    problem,
                    methodology,
                    findings,
                    research_gap,
                    notes
                FROM literature
                WHERE project_id = ?
                ORDER BY year DESC, id DESC
                """,
                (project_id,),
            )

            rows = cursor.fetchall()

            return [
                Literature(
                    id=row[0],
                    project_id=row[1],
                    title=row[2],
                    authors=row[3],
                    year=row[4],
                    publication=row[5],
                    doi=row[6],
                    url=row[7],
                    problem=row[8],
                    methodology=row[9],
                    findings=row[10],
                    research_gap=row[11],
                    notes=row[12],
                )
                for row in rows
            ]

    def update_literature(
        self,
        literature: Literature,
    ) -> bool:
        """Update an existing literature source."""

        if literature.id is None:
            return False

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE literature
                SET
                    title = ?,
                    authors = ?,
                    year = ?,
                    publication = ?,
                    doi = ?,
                    url = ?,
                    problem = ?,
                    methodology = ?,
                    findings = ?,
                    research_gap = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    literature.title,
                    literature.authors,
                    literature.year,
                    literature.publication,
                    literature.doi,
                    literature.url,
                    literature.problem,
                    literature.methodology,
                    literature.findings,
                    literature.research_gap,
                    literature.notes,
                    literature.id,
                ),
            )

            return cursor.rowcount > 0

    def delete_literature(
        self,
        literature_id: int,
    ) -> bool:
        """Delete a literature source."""

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM literature
                WHERE id = ?
                """,
                (literature_id,),
            )

            return cursor.rowcount > 0