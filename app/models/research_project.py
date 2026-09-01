"""Research project data model for Research Compass AI."""

from dataclasses import dataclass, field
from datetime import datetime
from app.models.research_interview import ResearchInterview


@dataclass
class ResearchProject:
    """Represent a research project and its core information."""

    title: str
    discipline: str
    research_type: str = ""
    methodology: str = ""
    research_design: str = ""
    
    interview: ResearchInterview = field(
        default_factory=ResearchInterview
    )

    def summary(self) -> str:
        """Return a short summary of the research project."""

        return (
            f"Title: {self.title}\n"
            f"Discipline: {self.discipline}\n"
            f"Research Type: {self.research_type}\n"
            f"Methodology: {self.methodology}\n"
            f"Research Design: {self.research_design}"
        )

