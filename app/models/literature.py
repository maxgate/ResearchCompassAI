"""Data model for research literature."""

from dataclasses import dataclass


@dataclass
class Literature:
    """Represent a literature source used in a research project."""

    project_id: int
    title: str
    authors: str
    year: int | None = None
    publication: str = ""
    doi: str = ""
    url: str = ""
    problem: str = ""
    methodology: str = ""
    findings: str = ""
    research_gap: str = ""
    notes: str = ""
    id: int | None = None