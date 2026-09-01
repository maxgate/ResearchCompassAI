from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.ui.wizard.project_wizard import ProjectWizard
from app.models.research_project import ResearchProject
from app.services.methodology_engine import recommend_methodology
from app.ui.methodology_dialog import MethodologyDialog
from app.ui.research_interview_dialog import ResearchInterviewDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Research Compass AI")
        self.resize(1200, 750)

        self.setup_ui()
        

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        sidebar = self.create_sidebar()
        content = self.create_content()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)


    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)

        title = QLabel("🧭 Research Compass AI - Research Assistant")
        title.setWordWrap(True)

        layout.addWidget(title)

        menu = QListWidget()

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
            menu.addItem(QListWidgetItem(item))

        layout.addWidget(menu)

        layout.addStretch()

        return sidebar


    def create_content(self):
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
        """Open the project wizard and create a research project."""

        wizard = ProjectWizard(self)

        if not wizard.exec():
            return
        
        project = ResearchProject(
                title=wizard.topic_input.text().strip(),
                discipline=wizard.discipline_input.currentText(),
                research_type=wizard.research_type_input.currentText(),
            )

        recommendation = recommend_methodology(project)

        project.methodology = recommendation["methodology"]
        project.research_design = recommendation["research_design"]


        methodology_dialog = MethodologyDialog(
                recommendation,
                self,
            ) 

        methodology_dialog.exec()


        interview_dialog = ResearchInterviewDialog(
                project,
                self,
            )

        if not interview_dialog.exec():
                return

        project.interview = interview_dialog.interview

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



           

    