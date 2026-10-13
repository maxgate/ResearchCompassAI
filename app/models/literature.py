
"""Data model for research literature."""

from dataclasses import dataclass, field


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

    # Additional metadata retrieved from OpenAlex.
    abstract: str = ""
    citation_count: int = 0
    topics: list[str] = field(default_factory=list)
    is_open_access: bool = False
    open_access_url: str = ""

    id: int | None = None
