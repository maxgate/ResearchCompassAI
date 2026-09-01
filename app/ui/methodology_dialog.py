"""Methodology recommendation dialog for Research Compass AI."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
)


class MethodologyDialog(QDialog):
    """Display a methodology recommendation to the researcher."""

    def __init__(self, recommendation, parent=None):
        super().__init__(parent)

        self.recommendation = recommendation

        self.setWindowTitle("Methodology Recommendation")
        self.resize(650, 450)

        self.setup_ui()

    def setup_ui(self):
        """Build the methodology recommendation interface."""

        layout = QVBoxLayout(self)

        title = QLabel("Research Methodology Recommendation")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        methodology = QLabel(
            f"<b>Recommended Methodology:</b><br>"
            f"{self.recommendation['methodology']}"
        )

        research_design = QLabel(
            f"<b>Research Design:</b><br>"
            f"{self.recommendation['research_design']}"
        )

        confidence = QLabel(
            f"<b>Confidence:</b><br>"
            f"{self.recommendation['confidence']:.0%}"
        )

        reason = QLabel(
            f"<b>Why this recommendation?</b><br>"
            f"{self.recommendation['reason']}"
        )

        reason.setWordWrap(True)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(self.accept)

        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(methodology)
        layout.addWidget(research_design)
        layout.addWidget(confidence)
        layout.addSpacing(15)
        layout.addWidget(reason)
        layout.addStretch()
        layout.addWidget(buttons)
