"""Research project data model for Research Compass AI."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ResearchProject:
    """Represent a research project and its core information."""

    title: str
    discipline: str
    research_type: str = ""
    methodology: str = ""
    research_design: str = ""
    objectives: list[str] = field(default_factory=list)
    research_questions: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def summary(self) -> str:
        """Return a short summary of the research project."""

        return (
            f"Title: {self.title}\n"
            f"Discipline: {self.discipline}\n"
            f"Research Type: {self.research_type}\n"
            f"Methodology: {self.methodology}\n"
            f"Research Design: {self.research_design}"
        )

