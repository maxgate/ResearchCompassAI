"""Main application window for Research Compass AI."""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.wizard.project_wizard import ProjectWizard
from app.models.research_project import ResearchProject
from app.services.methodology_engine import recommend_methodology
from app.ui.methodology_dialog import MethodologyDialog
from app.ui.research_interview_dialog import ResearchInterviewDialog
from app.ui.projects_view import ProjectsView

from app.database.database import DatabaseManager
from app.database.project_repository import ProjectRepository
from app.database.research_interview_repository import (
    ResearchInterviewRepository,
)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Research Compass AI")
        self.resize(1200, 750)

        # Initialize the database before building the user interface.
        self.database = DatabaseManager()
        self.database.initialize()

        # Create repositories used by the application.
        self.project_repository = ProjectRepository(self.database)
        self.interview_repository = ResearchInterviewRepository(
            self.database
        )

        # Build the user interface.
        self.setup_ui()

    def setup_ui(self):
        """Build the main application interface."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)


        # Create the main content area.
        self.content_stack = QStackedWidget()


        # Create the sidebar.
        sidebar = self.create_sidebar()

      
        # Dashboard page.
        dashboard = self.create_content()

        # Projects page.
        self.projects_view = ProjectsView(
            self.project_repository,
            self,
        )

        # Add pages to the stack.
        self.content_stack.addWidget(dashboard)
        self.content_stack.addWidget(self.projects_view)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

    def create_sidebar(self):
        """Create the application's navigation sidebar."""

        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)

        title = QLabel(
            "🧭 Research Compass AI - Research Assistant"
        )
        title.setWordWrap(True)

        layout.addWidget(title)

        self.menu = QListWidget()

        items = [
            "🏠 Dashboard",
            "📁 Projects",
            "📚 Literature",
            "📊 Analysis",
            "📖 References",
            "✍️ Chapter Editor",
            "⚙ Settings",
        ]

        for item in items:
            self.menu.addItem(QListWidgetItem(item))

        # Switch the main content when the user selects a menu item.
        self.menu.currentRowChanged.connect(
            self.change_page
        )

        # Select Dashboard when the application starts.
        self.menu.setCurrentRow(0)

        layout.addWidget(self.menu)
        layout.addStretch()

        return sidebar

    def change_page(self, index):
        """Switch the main content page based on sidebar selection."""

        # Dashboard
        if index == 0:
            self.content_stack.setCurrentIndex(0)

        # Projects
        elif index == 1:
            self.projects_view.load_projects()
            self.content_stack.setCurrentIndex(1)

        # Other sections are not implemented yet.
        else:
            self.content_stack.setCurrentIndex(0)

    def create_content(self):
        """Create the dashboard page."""

        content = QFrame()
        layout = QVBoxLayout(content)

        title = QLabel("Welcome to Research Compass AI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        description = QLabel(
            "Your intelligent research assistant "
            "from Chapter One to Chapter Five."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Start New Research")
        button.setFixedHeight(45)

        button.clicked.connect(self.create_project)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(button)
        layout.addStretch()

        return content

    def create_project(self):
        """Open the project wizard and create a complete research project."""

        # Step 1: Collect the basic project information.
        wizard = ProjectWizard(self)

        if not wizard.exec():
            return

        project = ResearchProject(
            title=wizard.topic_input.text().strip(),
            discipline=wizard.discipline_input.currentText(),
            research_type=wizard.research_type_input.currentText(),
        )

        # Step 2: Generate an initial methodology recommendation.
        recommendation = recommend_methodology(project)

        project.methodology = recommendation["methodology"]
        project.research_design = recommendation["research_design"]

        # Step 3: Show the recommendation to the researcher.
        methodology_dialog = MethodologyDialog(
            recommendation,
            self,
        )

        if not methodology_dialog.exec():
            return

        # Step 4: Conduct the research interview.
        interview_dialog = ResearchInterviewDialog(
            project,
            self,
        )

        if not interview_dialog.exec():
            return

        project.interview = interview_dialog.interview

        # Step 5: Save the project.
        project_id = self.project_repository.create_project(project)

        # Step 6: Save the interview and link it to the project.
        interview_id = self.interview_repository.create_interview(
            project_id,
            project.interview,
        )

        # Step 7: Refresh the Projects dashboard.
        self.projects_view.load_projects()

        # Step 8: Display confirmation in the terminal.
        print()
        print("Research Project Created")
        print("------------------------")
        print("Project ID:", project_id)
        print("Interview ID:", interview_id)

        print("\nResearch Profile")
        print("----------------")
        print(f"Title: {project.title}")
        print(f"Discipline: {project.discipline}")
        print(f"Research Type: {project.research_type}")
        print(f"Methodology: {project.methodology}")
        print(f"Research Design: {project.research_design}")

        print("\nResearch Interview")
        print("-----------------")
        print(
            f"Problem: "
            f"{project.interview.problem_statement}"
        )
        print(
            f"Aim: "
            f"{project.interview.aim}"
        )
        print(
            f"Population: "
            f"{project.interview.population}"
        )
        print(
            f"Data Source: "
            f"{project.interview.data_source}"
        )
        print(
            f"Expected Outcome: "
            f"{project.interview.expected_outcome}"
        )
        print(
            f"Additional Information: "
            f"{project.interview.additional_information}"
        )