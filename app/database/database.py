"""SQLite database management for Research Compass AI."""

import sqlite3
from pathlib import Path


class DatabaseManager:
    """Manage the Research Compass AI SQLite database."""

    def __init__(self, database_path: str = "researchcompass.db"):
        self.database_path = Path(database_path)

    def connect(self):
        """Create and return a database connection."""

        return sqlite3.connect(self.database_path)

    def initialize(self):
        """Create the required database tables."""

        with self.connect() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    discipline TEXT NOT NULL,
                    research_type TEXT,
                    methodology TEXT,
                    research_design TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS research_interviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    problem_statement TEXT,
                    aim TEXT,
                    population TEXT,
                    data_source TEXT,
                    expected_outcome TEXT,
                    additional_information TEXT,
                    FOREIGN KEY (project_id)
                        REFERENCES projects(id)
                )
                """
            )

            connection.commit()

