"""Interface for finding relevant academic literature."""

import re

from PySide6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class LiteratureSearchView(QWidget):
    """Collect and prepare an academic literature search request."""

    def __init__(self, project, parent=None):
        super().__init__(parent)

        self.project = project
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
        """Prepare simple search terms from the user's request."""

        search_request = self.search_input.toPlainText().strip()

        if not search_request:
            QMessageBox.warning(
                self,
                "Missing Search Request",
                "Please describe the literature you want to find.",
            )
            return

        search_terms = self.generate_search_terms(search_request)

        formatted_terms = "\n".join(
            f"• {term}" for term in search_terms
        )

        self.result_label.setText(
            "Search request received.\n\n"
            f"Prepared search terms:\n{formatted_terms}\n\n"
            "The next stage will send these terms to academic "
            "literature databases."
        )

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