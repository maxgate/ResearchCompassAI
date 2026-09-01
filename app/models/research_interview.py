"""Research interview data model for Research Compass AI."""

from dataclasses import dataclass, field


@dataclass
class ResearchInterview:
    """Store information collected during the research interview."""

    problem_statement: str = ""
    aim: str = ""
    objectives: list[str] = field(default_factory=list)
    research_questions: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    population: str = ""
    sample_size: str = ""
    data_source: str = ""
    variables: list[str] = field(default_factory=list)
    expected_outcome: str = ""
    additional_information: str = ""

    def is_complete(self) -> bool:
        """Check whether the minimum interview information is available."""

        required_fields = [
            self.problem_statement,
            self.aim,
            self.population,
            self.data_source,
        ]

        return all(field.strip() for field in required_fields)
