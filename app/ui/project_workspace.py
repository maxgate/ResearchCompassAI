"""Research project workspace."""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.database.database import DatabaseManager
from app.database.literature_repository import LiteratureRepository
from app.ui.literature_view import LiteratureView
from app.ui.literature_search_view import LiteratureSearchView

class ProjectWorkspace(QWidget):
    """Display the workspace for a single research project."""

    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project

         # Connect this workspace to the database.
        self.database = DatabaseManager()
        self.database.initialize()

        # Repository responsible for literature database operations.
        self.literature_repository = LiteratureRepository(
            self.database
        )

        self.setup_ui()

    def setup_ui(self):
        """Build the project workspace interface."""

        main_layout = QHBoxLayout(self)

        # -----------------------------
        # Project navigation
        # -----------------------------

        sidebar = QListWidget()

        sections = [
            "📋 Overview",
            "📚 Literature",
            "🔎 Find Literature",
            "📖 References",
            "✍️ Chapter One",
            "✍️ Chapter Two",
            "✍️ Chapter Three",
            "📊 Chapter Four",
            "✍️ Chapter Five",
            "🤖 AI Research Assistant",
            "🔍 Project Evaluation",
        ]

        for section in sections:
            sidebar.addItem(QListWidgetItem(section))

        # -----------------------------
        # Workspace content
        # -----------------------------

        self.content_stack = QStackedWidget()

        # Create pages.
        overview = self.create_overview()

        literature_view = LiteratureView(
            self.project,
            self.literature_repository,
        )

        Literature_search_view = LiteratureSearchView(
            self.project,
        )

        self.content_stack.addWidget(overview)
        self.content_stack.addWidget(literature_view)
        self.content_stack.addWidget(Literature_search_view)

        # Add temporary pages for the remaining sections.
        for _ in range(len(sections) - 3):
            self.content_stack.addWidget(
                self.create_placeholder()
            )

        # Connect sidebar navigation.
        sidebar.currentRowChanged.connect(
            self.change_section
        )

        sidebar.setCurrentRow(0)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

    def change_section(self, index):
        """Switch the workspace content based on sidebar selection."""

        self.content_stack.setCurrentIndex(index)

    def create_overview(self):
        """Create the project overview page."""

        page = QWidget()

        layout = QVBoxLayout(page)

        # -----------------------------
        # Back to dashboard
        # -----------------------------

        back_button = QPushButton("← Back to Dashboard")
        back_button.clicked.connect(self.close)

        layout.addWidget(back_button)

        # -----------------------------
        # Project title
        # -----------------------------

        title = QLabel(self.project.title)

        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(title)

        # -----------------------------
        # Research profile
        # -----------------------------

        profile_title = QLabel("Research Profile")

        profile_title.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(profile_title)

        profile = QLabel(
            f"""
            <b>Discipline:</b> {self.project.discipline}<br>
            <b>Research Type:</b> {self.project.research_type}<br>
            <b>Methodology:</b> {self.project.methodology}<br>
            <b>Research Design:</b> {self.project.research_design}
            """
        )

        profile.setWordWrap(True)

        layout.addWidget(profile)

        # -----------------------------
        # Research progress
        # -----------------------------

        progress_title = QLabel("Research Progress")

        progress_title.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(progress_title)

        progress = QLabel(
            """
            ✓ Research profile created<br>
            ✓ Methodology recommended<br>
            ✓ Research interview completed<br>
            ○ Literature review<br>
            ○ Chapter One<br>
            ○ Chapter Two<br>
            ○ Chapter Three<br>
            ○ Chapter Four<br>
            ○ Chapter Five<br>
            ○ References
            """
        )

        layout.addWidget(progress)

        layout.addStretch()

        return page

    def create_placeholder(self):
        """Create a temporary page for unfinished workspace sections."""

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel("Coming Soon")

        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
            """
        )

        message = QLabel(
            "This section will be implemented as we build "
            "ResearchCompassAI."
        )

        message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(message)

        layout.addStretch()

        return page