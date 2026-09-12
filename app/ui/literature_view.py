"""Literature management interface."""

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.models.literature import Literature


class LiteratureView(QWidget):
    """Display and manage literature for a research project."""

    def __init__(self, project, literature_repository, parent=None):
        super().__init__(parent)

        self.project = project
        self.literature_repository = literature_repository

        # Stores the literature currently being edited.
        # None means we are adding a new source.
        self.editing_literature_id = None

        self.setup_ui()
        self.load_literature()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        title = QLabel("Literature Review")
        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
            """
        )
        main_layout.addWidget(title)

        description = QLabel(
            "Add, edit, and manage the academic sources "
            "used for this research project."
        )
        description.setWordWrap(True)
        main_layout.addWidget(description)

        form = QFormLayout()

        self.title_input = QLineEdit()
        self.authors_input = QLineEdit()
        self.year_input = QLineEdit()
        self.publication_input = QLineEdit()
        self.doi_input = QLineEdit()
        self.url_input = QLineEdit()

        form.addRow("Title:", self.title_input)
        form.addRow("Authors:", self.authors_input)
        form.addRow("Year:", self.year_input)
        form.addRow("Publication:", self.publication_input)
        form.addRow("DOI:", self.doi_input)
        form.addRow("URL:", self.url_input)

        self.problem_input = QTextEdit()
        self.problem_input.setPlaceholderText(
            "What problem does the study address?"
        )

        self.methodology_input = QTextEdit()
        self.methodology_input.setPlaceholderText(
            "What methodology did the researchers use?"
        )

        self.findings_input = QTextEdit()
        self.findings_input.setPlaceholderText(
            "What were the major findings?"
        )

        self.gap_input = QTextEdit()
        self.gap_input.setPlaceholderText(
            "What research gap does this study reveal?"
        )

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Additional notes..."
        )

        form.addRow("Problem:", self.problem_input)
        form.addRow("Methodology:", self.methodology_input)
        form.addRow("Findings:", self.findings_input)
        form.addRow("Research Gap:", self.gap_input)
        form.addRow("Notes:", self.notes_input)

        main_layout.addLayout(form)

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Add Literature")
        self.save_button.clicked.connect(self.save_literature)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_form)

        buttons.addWidget(self.save_button)
        buttons.addWidget(clear_button)

        main_layout.addLayout(buttons)

        main_layout.addWidget(QLabel("Saved Literature"))

        self.literature_list = QVBoxLayout()
        main_layout.addLayout(self.literature_list)

        main_layout.addStretch()

    def save_literature(self):
        """Create a new source or update an existing source."""

        title = self.title_input.text().strip()
        authors = self.authors_input.text().strip()

        if not title or not authors:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Title and authors are required.",
            )
            return

        year_text = self.year_input.text().strip()
        year = None

        if year_text:
            try:
                year = int(year_text)
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Invalid Year",
                    "Year must be a number.",
                )
                return

        literature = Literature(
            project_id=self.project.id,
            title=title,
            authors=authors,
            year=year,
            publication=self.publication_input.text().strip(),
            doi=self.doi_input.text().strip(),
            url=self.url_input.text().strip(),
            problem=self.problem_input.toPlainText().strip(),
            methodology=self.methodology_input.toPlainText().strip(),
            findings=self.findings_input.toPlainText().strip(),
            research_gap=self.gap_input.toPlainText().strip(),
            notes=self.notes_input.toPlainText().strip(),
            id=self.editing_literature_id,
        )

        # Update existing literature.
        if self.editing_literature_id is not None:
            updated = self.literature_repository.update_literature(
                literature
            )

            if updated:
                QMessageBox.information(
                    self,
                    "Literature Updated",
                    "The literature source was updated successfully.",
                )

        # Otherwise create a new literature source.
        else:
            literature_id = (
                self.literature_repository.create_literature(
                    literature
                )
            )

            print("Literature saved. ID:", literature_id)

        self.clear_form()
        self.load_literature()

    def load_literature(self):
        """Load all literature belonging to the current project."""

        while self.literature_list.count():
            item = self.literature_list.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        literature_items = (
            self.literature_repository
            .get_project_literature(self.project.id)
        )

        if not literature_items:
            self.literature_list.addWidget(
                QLabel("No literature added yet.")
            )
            return

        for literature in literature_items:
            self.add_literature_card(literature)

    def add_literature_card(self, literature):
        """Create a display card for one literature source."""

        card = QWidget()
        layout = QVBoxLayout(card)

        information = QLabel(
            f"""
            <b>{literature.title}</b><br>
            Authors: {literature.authors}<br>
            Year: {literature.year or "Not provided"}<br>
            Publication: {literature.publication or "Not provided"}
            """
        )
        information.setWordWrap(True)

        layout.addWidget(information)

        buttons = QHBoxLayout()

        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(
            lambda checked=False, item=literature:
            self.edit_literature(item)
        )

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(
            lambda checked=False, item_id=literature.id:
            self.delete_literature(item_id)
        )

        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)
        buttons.addStretch()

        layout.addLayout(buttons)

        self.literature_list.addWidget(card)

    def edit_literature(self, literature):
        """Load a literature source into the form for editing."""

        self.editing_literature_id = literature.id

        self.title_input.setText(literature.title)
        self.authors_input.setText(literature.authors)

        if literature.year is not None:
            self.year_input.setText(str(literature.year))
        else:
            self.year_input.clear()

        self.publication_input.setText(
            literature.publication
        )
        self.doi_input.setText(literature.doi)
        self.url_input.setText(literature.url)

        self.problem_input.setPlainText(
            literature.problem
        )
        self.methodology_input.setPlainText(
            literature.methodology
        )
        self.findings_input.setPlainText(
            literature.findings
        )
        self.gap_input.setPlainText(
            literature.research_gap
        )
        self.notes_input.setPlainText(
            literature.notes
        )

        self.save_button.setText("Update Literature")

    def delete_literature(self, literature_id):
        """Delete a literature source after confirmation."""

        answer = QMessageBox.question(
            self,
            "Delete Literature",
            "Are you sure you want to delete this literature source?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        deleted = self.literature_repository.delete_literature(
            literature_id
        )

        if deleted:
            self.load_literature()

    def clear_form(self):
        """Clear the form and return to add mode."""

        self.editing_literature_id = None

        self.title_input.clear()
        self.authors_input.clear()
        self.year_input.clear()
        self.publication_input.clear()
        self.doi_input.clear()
        self.url_input.clear()

        self.problem_input.clear()
        self.methodology_input.clear()
        self.findings_input.clear()
        self.gap_input.clear()
        self.notes_input.clear()

        self.save_button.setText("Add Literature")
