"""Research interview dialog for Research Compass AI."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QMessageBox,
)

from app.models.research_interview import ResearchInterview
from app.models.research_project import  ResearchProject


class ResearchInterviewDialog(QDialog):
    """Collect additional research information from the researcher."""

    def __init__(self, project: ResearchProject, parent=None):
        super().__init__(parent)

        self.project = project
        self.interview = ResearchInterview()

        self.setWindowTitle("Research Interview")
        self.resize(700, 650)

        self.setup_ui()

    def setup_ui(self):
        """Build the research interview interface."""

        layout = QVBoxLayout(self)

        title = QLabel("Research Interview")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        introduction = QLabel(
            "Answer the questions below. "
            "Research Compass AI will use your answers "
            "to understand your research context."
        )

        introduction.setWordWrap(True)

        context_label = QLabel(
            f"<b>Project:</b> {self.project.title}<br>"
            f"<b>Discipline:</b> {self.project.discipline}<br>"
            f"<b>Research Type:</b> {self.project.research_type}"
        )

        context_label.setWordWrap(True)

        layout.addWidget(context_label)


        problem_label = QLabel(
            "1. What problem does your research intend to solve?"
        )

        self.problem_input = QTextEdit()
        self.problem_input.setPlaceholderText(
            "Describe the research problem..."
        )

        aim_label = QLabel(
            "2. What is the main aim of your research?"
        )

        self.aim_input = QTextEdit()
        self.aim_input.setPlaceholderText(
            "State the overall aim of the research..."
        )

        population_label = QLabel(
            "3. Who or what is the population or subject of study?"
        )

        self.population_input = QLineEdit()
        self.population_input.setPlaceholderText(
            "Example: Undergraduate students in Nigerian universities"
        )

        data_source_label = QLabel(
            "4. What source of data will you use?"
        )

        self.data_source_input = QLineEdit()
        self.data_source_input.setPlaceholderText(
            "Example: Questionnaire, experiment, existing dataset..."
        )

        outcome_label = QLabel(
            "5. What do you expect the research to achieve?"
        )

        self.outcome_input = QTextEdit()
        self.outcome_input.setPlaceholderText(
            "Describe the expected outcome..."
        )

        # Context-specific question
        self.context_label = QLabel(
            self.get_context_question()
        )

        self.context_input = QTextEdit()

        self.context_input.setPlaceholderText(
            "Provide additional Information about your research..."
        )

        layout.addWidget(self.context_label)
        layout.addWidget(self.context_input)


        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(self.save_interview)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(introduction)

        layout.addWidget(problem_label)
        layout.addWidget(self.problem_input)

        layout.addWidget(aim_label)
        layout.addWidget(self.aim_input)

        layout.addWidget(population_label)
        layout.addWidget(self.population_input)

        layout.addWidget(data_source_label)
        layout.addWidget(self.data_source_input)

        layout.addWidget(outcome_label)
        layout.addWidget(self.outcome_input)

        layout.addStretch()
        layout.addWidget(buttons)

    def save_interview(self):
        """Save the interview responses."""


        self.interview.problem_statement = (
            self.problem_input.toPlainText().strip()
        )

        self.interview.aim = (
            self.aim_input.toPlainText().strip()
        )

        self.interview.population = (
            self.population_input.text().strip()
        )

        self.interview.data_source = (
            self.data_source_input.text().strip()
        )

        self.interview.expected_outcome = (
            self.outcome_input.toPlainText().strip()
        )

        self.interview.additional_information = (
        self.context_input.toPlainText().strip()
        )

        if not self.interview.is_complete():
            QMessageBox.warning(
                self,
                "Incomplete Research Profile",
                "Please provide answers to all required"
                "research questions before continuing.",
            )
            return

        self.accept()

    def get_context_question(self):
        """Return a question based on the research discipline."""

        discipline = self.project.discipline.lower()

        if discipline == "engineering":
            return (
                "5. What system, device,  process, or  prototype "
                "are you designing or investigating?"
            )
        
        if discipline == "computer science / information technology":
            return (
                "5. What software, algorithm, information system, "
                "or computing problem are you addressing?"
            )

        if discipline == "social sciences":
            return (
                "5. What social group, population, behaviour, or "
                "social phenomenon are you investigating?"
            )

        if discipline == "education":
            return (
                "5. What educational process, learner group, "
                "teacher group, or institution are you studying?"
            )

        if discipline == "law": 
            return ( 
                "5. What legal issue, statute, case, regulation, " 
                "or legal principle does your research examine?" 
            ) 

        if discipline == "natural sciences": 
            return ( 
                "5. What scientific phenomenon, material, organism, " 
                "or process are you investigating?" 
            ) 

        if discipline == "medicine / health sciences": 
            return ( 
                "5. What health condition, intervention, population, " 
                "or clinical problem are you investigating?" 
            ) 

        if discipline == "agriculture":
            return ( 
                "5. What agricultural process, crop, animal, " 
                "environment, or production problem are you studying?" 
            ) 

        if discipline == "business / management": 
            return ( 
                "5. What business process, organisation, market, " 
                "or management problem are you investigating?" 
                ) 
        
        return ( 
            "5. What specific aspect of your research requires " 
            "the most investigation?" 
        )

