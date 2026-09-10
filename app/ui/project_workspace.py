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


class ProjectWorkspace(QWidget):
    """Display the workspace for a single research project."""

    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project

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

        overview = self.create_overview()

        self.content_stack.addWidget(overview)

        # Other sections will be implemented later.

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

    def create_overview(self):
        """Create the project overview page."""

        page = QWidget()

        layout = QVBoxLayout(page)

        # -----------------------------
        # Back to dashboard button
        # -----------------------------

        back_button = QPushButton("← Back to Dashboard")
        back_button.clicked.connect(self.close)

        layout.addWidget(back_button)

    # -----------------------------
        # Project information
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

        profile = QLabel(
            f"""
            <b>Discipline:</b> {self.project.discipline}<br>
            <b>Research Type:</b> {self.project.research_type}<br>
            <b>Methodology:</b> {self.project.methodology}<br>
            <b>Research Design:</b> {self.project.research_design}
            """
        )

        layout.addWidget(title)
        layout.addWidget(profile)

        layout.addSpacing(20)

        # -----------------------------
        # Research interview
        # -----------------------------

        interview_title = QLabel("Research Interview")
        interview_title.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(interview_title)

        interview_message = QLabel(
            "Research interview information will appear here."
        )

        layout.addWidget(interview_message)

        layout.addStretch()

        return page