"""Methodology recommendation engine for Research Compass AI."""

from app.models.research_project import ResearchProject


def recommend_methodology(project: ResearchProject) -> dict:
    """
    Recommend a research methodology based on project context.

    The first version uses simple rules. Later versions will
    incorporate AI-assisted reasoning.
    """

    discipline = project.discipline.lower()
    research_type = project.research_type.lower()
    title = project.title.lower()

    # Engineering and Computer Science projects that involve
    # designing, implementing, building, or testing systems
    # are commonly suited to experimental or design-based research.
    if (
        discipline in {
            "engineering",
            "computer science / information technology",
        }
        and research_type in {"experimental", "applied research"}
    ):
        return {
            "methodology": "Experimental Research",
            "research_design": "Experimental Design",
            "confidence": 0.90,
            "reason": (
                "The project involves a technical discipline and "
                "an experimental or applied research approach. "
                "This supports system development, implementation, "
                "testing, and performance evaluation."
            ),
        }

    # Quantitative research commonly uses surveys and
    # statistical analysis when studying measurable variables.
    if research_type == "quantitative":
        return {
            "methodology": "Quantitative Research",
            "research_design": "Survey or Correlational Design",
            "confidence": 0.80,
            "reason": (
                "The project is identified as quantitative, making "
                "structured data collection and statistical analysis "
                "appropriate."
            ),
        }

    # Qualitative projects generally focus on experiences,
    # opinions, meanings, and contextual understanding.
    if research_type == "qualitative":
        return {
            "methodology": "Qualitative Research",
            "research_design": "Case Study or Phenomenological Design",
            "confidence": 0.80,
            "reason": (
                "The project is identified as qualitative, which "
                "supports in-depth exploration of experiences, "
                "perceptions, meanings, or social contexts."
            ),
        }

    # Mixed-methods research combines quantitative and qualitative
    # approaches.
    if research_type == "mixed methods":
        return {
            "methodology": "Mixed Methods Research",
            "research_design": "Sequential or Concurrent Mixed Methods",
            "confidence": 0.85,
            "reason": (
                "The project combines quantitative and qualitative "
                "approaches, allowing numerical evidence and "
                "contextual explanations to be integrated."
            ),
        }

    # Descriptive research focuses on describing characteristics,
    # conditions, populations, or phenomena.
    if research_type == "descriptive":
        return {
            "methodology": "Descriptive Research",
            "research_design": "Descriptive Survey Design",
            "confidence": 0.75,
            "reason": (
                "The project is descriptive and therefore focuses "
                "on systematically describing a population, "
                "condition, or phenomenon."
            ),
        }

    # Exploratory research is useful when the research problem
    # requires initial investigation.
    if research_type == "exploratory":
        return {
            "methodology": "Exploratory Research",
            "research_design": "Exploratory Design",
            "confidence": 0.70,
            "reason": (
                "The exploratory classification suggests that the "
                "research seeks to investigate a problem or area "
                "where existing understanding may be limited."
            ),
        }

    # If the topic contains strong system-development language,
    # provide a fallback recommendation.
    development_keywords = {
        "design",
        "development",
        "implementation",
        "system",
        "prototype",
        "application",
        "software",
    }

    if any(keyword in title for keyword in development_keywords):
        return {
            "methodology": "Design and Development Research",
            "research_design": "Design-Based / Developmental Design",
            "confidence": 0.65,
            "reason": (
                "The project title contains system development "
                "language such as design, development, implementation, "
                "or prototype."
            ),
        }

    # Final fallback when the available information is insufficient.
    return {
        "methodology": "Further Analysis Required",
        "research_design": "To Be Determined",
        "confidence": 0.30,
        "reason": (
            "There is not enough project context to confidently "
            "recommend a methodology. More information about the "
            "research objectives and problem is required."
        )
    }