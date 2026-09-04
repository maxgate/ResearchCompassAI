"""Projects dashboard for Research Compass AI."""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ProjectsView(QWidget):
    """Display and manage saved research projects."""

    def __init__(self, project_repository, parent=None):
        super().__init__(parent)

        self.project_repository = project_repository

        self.setup_ui()
        self.load_projects()

    def setup_ui(self):
        """Build the projects dashboard interface."""

        self.main_layout = QVBoxLayout(self)

        title = QLabel("My Research Projects")
        title.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
            """
        )

        self.main_layout.addWidget(title)

        self.projects_container = QVBoxLayout()
        self.main_layout.addLayout(self.projects_container)

        self.main_layout.addStretch()

        create_button = QPushButton("+ Create Project")
        create_button.setFixedHeight(40)

        self.main_layout.addWidget(create_button)

    def load_projects(self):
        """Load all saved projects from the database."""

        # Remove existing project cards before reloading.
        while self.projects_container.count():
            item = self.projects_container.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        projects = self.project_repository.get_all_projects()

        if not projects:
            empty_label = QLabel(
                "No research projects yet.\n"
                "Click '+ Create Project' to create your first project."
            )

            empty_label.setStyleSheet(
                """
                QLabel {
                    font-size: 16px;
                    padding: 30px;
                }
                """
            )

            self.projects_container.addWidget(empty_label)
            return

        for project in projects:
            self.add_project_card(project)

    def add_project_card(self, project):
        """Create a visual card for a research project."""

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(card)

        title = QLabel(project.title)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            """
        )

        details = QLabel(
            f"{project.discipline} • {project.research_type}"
        )

        methodology = QLabel(
            f"Methodology: {project.methodology}"
        )

        buttons_layout = QHBoxLayout()

        open_button = QPushButton("Open")
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        delete_button.clicked.connect(
            lambda checked=False, project_id=project.id:
            self.delete_project(project_id)
        )

        buttons_layout.addWidget(open_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)

        layout.addWidget(title)
        layout.addWidget(details)
        layout.addWidget(methodology)
        layout.addLayout(buttons_layout)

        self.projects_container.addWidget(card)

    def delete_project(self, project_id):
        """Delete a project after asking the user for confirmation."""

        answer = QMessageBox.question(
            self,
            "Delete Project",
            "Are you sure you want to delete this project?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        deleted = self.project_repository.delete_project(project_id)

        if deleted:
            self.load_projects()