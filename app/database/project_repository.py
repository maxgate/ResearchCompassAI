"""Database repository for research projects."""

from app.database.database import DatabaseManager
from app.models.research_project import ResearchProject


class ProjectRepository:
    """Handle CRUD operations for research projects."""

    def __init__(self, database: DatabaseManager):
        self.database = database

    def create_project(self, project: ResearchProject) -> int:
        """Save a research project and return its database ID."""

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO projects (
                    title,
                    discipline,
                    research_type,
                    methodology,
                    research_design
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    project.title,
                    project.discipline,
                    project.research_type,
                    project.methodology,
                    project.research_design,
                ),
            )

            project.id = cursor.lastrowid

        return project.id


    def get_project(self, project_id: int):
         """Retrieve a research project by its ID."""

         with self.database.connect() as connection:
             cursor = connection.cursor()

             cursor.execute(
                """
                SELECT
                    id,
                    title,
                    discipline,
                    research_type,
                    methodology,
                    research_design
                FROM projects
                WHERE id = ?
                """,
                (project_id,),
             )

             row = cursor.fetchone()

         if row is None:
            return None

         return ResearchProject( 
             title=row[1], 
             discipline=row[2], 
             research_type=row[3] or "", 
             methodology=row[4] or "", 
             research_design=row[5] or "", 
             id=row[0],
        )

    def get_all_projects(self): 
        """Retrieve all research projects."""

        with self.database.connect() as connection: 
            cursor = connection.cursor()


            cursor.execute( 
                """ 
                SELECT 
                id, 
                title, 
                discipline, 
                research_type, 
                methodology, 
                research_design 
                FROM projects
                ORDER BY id DESC 
                """
            )

            rows = cursor.fetchall()

        projects = []


        for row in rows: 
            project = ResearchProject( 
            title=row[1], 
            discipline=row[2], 
            research_type=row[3] or "", 
            methodology=row[4] or "", 
            research_design=row[5] or "", 
            id=row[0], 
        ) 

        projects.append(project) 

        return projects


    
    def update_project(self, project: ResearchProject) -> bool:
     """Update an existing research project."""

     if project.id is None:
          return False
     with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
            """
            UPDATE projects
            SET
                title = ?,
                discipline = ?,
                research_type = ?,
                methodology = ?,
                research_design = ?
            WHERE id = ?
            """,
            (
                project.title,
                project.discipline,
                project.research_type,
                project.methodology,
                project.research_design,
                project.id,
            ),
        )

            return cursor.rowcount > 0



    
    def delete_project(self, project_id: int) -> bool:
         """Delete a research project by its ID."""

         with self.database.connect() as connection:

             cursor = connection.cursor()

             cursor.execute(
            """
            DELETE FROM projects
            WHERE id = ?
            """,
            (project_id,),
        )

             return cursor.rowcount > 0



