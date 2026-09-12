"""Interface for finding relevant academic literature."""

import re
import requests

from PySide6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.openalex_service import OpenAlexService


class LiteratureSearchView(QWidget):
    """Collect and prepare an academic literature search request."""

    def __init__(self, project, literature_repository, parent=None):
        super().__init__(parent)

        self.project = project
        self.literature_repository = literature_repository
        self.openalex_service = OpenAlexService()


        self.setup_ui()

    def setup_ui(self):
        """Build the literature search interface."""

        layout = QVBoxLayout(self)

        title = QLabel("Find Relevant Literature")
        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
            """
        )
        layout.addWidget(title)

        description = QLabel(
            "Describe the literature you need. ResearchCompassAI "
            "will prepare search terms and later use academic "
            "databases to find relevant sources."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        project_label = QLabel(
            f"<b>Research Project:</b> {self.project.title}"
        )
        project_label.setWordWrap(True)
        layout.addWidget(project_label)

        layout.addWidget(
            QLabel("What academic literature are you looking for?")
        )

        self.search_input = QTextEdit()
        self.search_input.setPlaceholderText(
            "Example: Find recent academic studies about "
            "IoT-based smart irrigation systems, soil moisture "
            "sensors, machine learning, and water conservation."
        )
        layout.addWidget(self.search_input)

        search_button = QPushButton("Prepare Search Terms")
        search_button.clicked.connect(self.start_search)
        layout.addWidget(search_button)

        layout.addWidget(QLabel("Prepared Search Terms"))

        self.result_label = QLabel(
            "Your prepared search terms will appear here."
        )
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        layout.addStretch()

    def start_search(self):
        """Search OpenAlex using the prepared search terms."""

        search_request = self.search_input.toPlainText().strip()

        if not search_request:
            QMessageBox.warning(
                self,
                "Missing Search Request",
                "Please describe the literature you want to find.",
            )
            return

        search_terms = self.generate_search_terms(search_request)

        if not search_terms:
            QMessageBox.warning(
                self,
                "Search Error",
                "Could not generate search terms.",
            )
            return

        search_term = search_terms[0]

        self.result_label.setText(
            "Searching academic literature..."
        )

        try:
            results = self.openalex_service.search_works(
                search_term,
                per_page=10,
            )

        except requests.RequestException as error:
            QMessageBox.critical(
                self,
                "Academic Search Error",
                f"Could not connect to OpenAlex.\n\n{error}",
            )
            return

        self.display_results(results)

    def display_results(self, results):
        """Display academic search results."""

        if not results:
            self.result_label.setText(
                "No academic works were found for this search."
            )
            return

        result_text = (
            f"<b>Found {len(results)} academic works.</b><br><br>"
        )

        for number, work in enumerate(results, start=1):
            title = work.get(
                "display_name",
                "Untitled",
            )

            year = work.get(
                "publication_year",
                "Year unavailable",
            )

            authors = self.openalex_service.extract_authors(
                work
            )

            doi = self.openalex_service.extract_doi(
                work
            )

            result_text += (
                f"<b>{number}. {title}</b><br>"
                f"Authors: {authors or 'Unavailable'}<br>"
                f"Year: {year}<br>"
                f"DOI: {doi or 'Unavailable'}<br><br>"
            )

        self.result_label.setText(result_text)
        

    def generate_search_terms(self, request):
        """Create basic keyword phrases from a search request."""

        cleaned_request = re.sub(
            r"[^a-zA-Z0-9\s-]",
            " ",
            request.lower(),
        )

        words = cleaned_request.split()

        ignored_words = {
            "find",
            "recent",
            "academic",
            "studies",
            "study",
            "about",
            "the",
            "and",
            "for",
            "with",
            "of",
            "in",
            "on",
            "to",
            "a",
            "an",
            "research",
        }

        important_words = [
            word
            for word in words
            if word not in ignored_words
            and len(word) > 2
        ]

        terms = []

        if important_words:
            terms.append(" ".join(important_words[:8]))

        if len(important_words) >= 2:
            terms.append(
                f"{important_words[0]} {important_words[1]}"
            )

        if len(important_words) >= 4:
            terms.append(
                " ".join(important_words[2:6])
            )

        # Remove duplicates while preserving order.
        unique_terms = []

        for term in terms:
            if term not in unique_terms:
                unique_terms.append(term)

        return unique_terms