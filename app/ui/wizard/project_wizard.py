"""Project creation wizard for Research Compass AI."""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
)


class ProjectWizard(QDialog):
    """Collect the initial information for a new research project."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Research Project")
        self.resize(700, 450)

        self.setup_ui()

    def setup_ui(self):
        """Build the user interface for the project setup."""

        layout = QVBoxLayout(self)

        title = QLabel("Create a New Research Project")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        # Research topic
        topic_label = QLabel(
            "What is the topic or title of your research project?"
        )

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText(
            "Example: Design and Implementation of an "
            "IoT-Based Smart Irrigation System"
        )

        # Research discipline
        discipline_label = QLabel(
            "Which discipline does your research belong to?"
        )

        self.discipline_input = QComboBox()

        self.discipline_input.addItems(
            [
                "Select a discipline",
                "Engineering",
                "Computer Science / Information Technology",
                "Natural Sciences",
                "Social Sciences",
                "Education",
                "Law",
                "Medicine / Health Sciences",
                "Agriculture",
                "Business / Management",
                "Arts / Humanities",
                "Environmental Sciences",
                "Other",
            ]
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)

        layout.addWidget(topic_label)
        layout.addWidget(self.topic_input)

        layout.addWidget(discipline_label)
        layout.addWidget(self.discipline_input)

      
         # Research type
        research_type_label = QLabel(
            "What type of research are you conducting?"
        )

        self.research_type_input = QComboBox()

        self.research_type_input.addItems(
            [
                "Select a research type",
                "Quantitative",
                "Qualitative",
                "Mixed Methods",
                "Experimental",
                "Descriptive",
                "Exploratory",
                "Theoretical / Conceptual",
                "Applied Research",
                "Other",
            ]
        )

        layout.addWidget(research_type_label)
        layout.addWidget(self.research_type_input)

        layout.addStretch()
        layout.addWidget(buttons)




    def validate_input(self):
        """Validate the information entered by the researcher."""

        topic = self.topic_input.text().strip()
        discipline = self.discipline_input.currentText()

        if not topic:
             QMessageBox.warning(
                self,
                "Missing Research Topic",
                "Please enter your research topic.",
             )
             return False

        if discipline == "Select a discipline": 
            QMessageBox.warning( 
                self, 
                "Missing Discipline", 
                "Please select a research discipline.", 
            ) 
            return False

        research_type = self.research_type_input.currentText()

        if research_type == "Select a research type":
           QMessageBox.warning(
                self,
                "Missing Discipline",
                "Please select a research type.",
            )
           return False
        
        return True

    
    def validate_and_accept(self):
         """Validate the form and close the wizard when valid."""

         if self.validate_input():
                self.accept()

