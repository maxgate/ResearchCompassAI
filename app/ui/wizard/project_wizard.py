"""Project creation wizard for Research Compass AI."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)


class ProjectWizard(QDialog):
    """Collect the initial information for a new research project."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Research Project")
        self.resize(700, 450)

        self.setup_ui()

    def setup_ui(self):
        """Build the user interface for the first wizard step."""

        layout = QVBoxLayout(self)

        title = QLabel("Create a New Research Project")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        instruction = QLabel(
            "What is the topic or title of your research project?"
        )

        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText(
            "Example: Design and Implementation of an "
            "IoT-Based Smart Irrigation System"
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(instruction)
        layout.addWidget(self.topic_input)
        layout.addStretch()
        layout.addWidget(buttons)