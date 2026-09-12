"""Interface for finding relevant academic literature."""

import re
import requests

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.openalex_service import OpenAlexService
from app.models.literature import Literature


class LiteratureSearchView(QWidget):
    """Collect and prepare an academic literature search request."""

    def __init__(
            self, 
            project, 
            literature_repository, 
            parent=None,
    ):
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

        search_button = QPushButton("Academic Search Results")
        search_button.clicked.connect(self.start_search)
        layout.addWidget(search_button)

        layout.addWidget(QLabel("Academic Search Results"))

        self.result_label = QLabel(
            "Your prepared search results will appear here."
        )
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        self.results_layout = QVBoxLayout()
        layout.addLayout(self.results_layout)

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
        """Display academic works as individual result cards."""

        if not results:
            self.result_label.setText(
                "No academic works were found for this search."
            )
            return

        self.result_label.setText(
            f"Found {len(results)} academic works."
        )

        # Remove previous result cards.
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        for work in results:
            self.add_result_card(work)

    def add_result_card(self, work):
        """Create a card for one academic work."""

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

        url = self.openalex_service.extract_url(
            work
        )

        card = QWidget()
        card_layout = QVBoxLayout(card)

        title_label = QLabel(
            f"<b>{title}</b>"
        )
        title_label.setWordWrap(True)

        metadata = QLabel(
            f"Authors: {authors or 'Unavailable'}<br>"
            f"Year: {year}<br>"
            f"DOI: {doi or 'Unavailable'}"
        )
        metadata.setWordWrap(True)

        card_layout.addWidget(title_label)
        card_layout.addWidget(metadata)

        buttons = QHBoxLayout()

        save_button = QPushButton("Save to Literature")

        save_button.clicked.connect(
            lambda checked=False, work=work:
            self.save_literature(work)
        )

        buttons.addWidget(save_button)
        buttons.addStretch()

        card_layout.addLayout(buttons)

        card.setStyleSheet(
            """
            QWidget {
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 8px;
            }
            """
        )

        self.results_layout.addWidget(card)

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


    def save_literature(self, work):
        """Save an OpenAlex work to the project literature."""

        title = work.get(
            "display_name",
            "Untitled",
        )

        authors = self.openalex_service.extract_authors(
            work
        )

        year = work.get("publication_year")

        doi = self.openalex_service.extract_doi(
            work
        )

        url = self.openalex_service.extract_url(
            work
        )

        literature = Literature(
            project_id=self.project.id,
            title=title,
            authors=authors or "Unknown",
            year=year,
            publication="",
            doi=doi,
            url=url,
        )

        literature_id = (
            self.literature_repository.create_literature(
                literature
            )
        )

        QMessageBox.information(
            self,
            "Literature Saved",
            f"'{title}' has been saved to your project literature.",
        )

        print(
            "Literature saved from OpenAlex. ID:",
            literature_id,
        )