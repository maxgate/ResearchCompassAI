
"""Service for searching scholarly works through OpenAlex."""

import requests


class OpenAlexService:
    """Search academic literature using the OpenAlex API."""

    BASE_URL = "https://api.openalex.org/works"

    def search_works(self, search_term, per_page=10):
        """Search OpenAlex and return scholarly works."""

        params = {
            "search": search_term,
            "per-page": per_page,
            "select": (
                "id,doi,title,display_name,publication_year,"
                "publication_date,authorships,primary_location,"
                "best_oa_location,open_access,cited_by_count,"
                "type,abstract_inverted_index,keywords,topics"
            ),
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("results", [])

    @staticmethod
    def extract_authors(work):
        """Extract author names from an OpenAlex work."""

        authors = []

        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            name = author.get("display_name")

            if name:
                authors.append(name)

        return ", ".join(authors)

    @staticmethod
    def extract_doi(work):
        """Extract the DOI without its URL prefix."""

        doi = work.get("doi")

        if not doi:
            return ""

        return doi.replace("https://doi.org/", "").strip()

    @staticmethod
    def extract_url(work):
        """Return the best available publication URL."""

        primary_location = work.get("primary_location") or {}
        best_oa_location = work.get("best_oa_location") or {}

        return (
            best_oa_location.get("landing_page_url")
            or primary_location.get("landing_page_url")
            or work.get("id", "")
        )

    @staticmethod
    def extract_publication(work):
        """Extract the journal, conference, or other source name."""

        primary_location = work.get("primary_location") or {}
        source = primary_location.get("source") or {}

        return source.get("display_name", "")

    @staticmethod
    def extract_citation_count(work):
        """Return the number of citations recorded by OpenAlex."""

        return work.get("cited_by_count", 0)

    @staticmethod
    def extract_abstract(work):
        """Reconstruct an abstract from OpenAlex's inverted index."""

        inverted_index = work.get("abstract_inverted_index")

        if not inverted_index:
            return ""

        word_positions = []

        for word, positions in inverted_index.items():
            for position in positions:
                word_positions.append((position, word))

        word_positions.sort(key=lambda item: item[0])

        return " ".join(
            word for _, word in word_positions
        )

    @staticmethod
    def extract_topics(work):
        """Extract topic labels assigned to a scholarly work."""

        topics = []

        for topic in work.get("topics", []):
            name = topic.get("display_name")

            if name:
                topics.append(name)

        return topics

    @staticmethod
    def extract_open_access_url(work):
        """Return an available open-access landing page or PDF URL."""

        best_oa_location = work.get("best_oa_location") or {}

        return (
            best_oa_location.get("pdf_url")
            or best_oa_location.get("landing_page_url")
            or ""
        )

    @staticmethod
    def is_open_access(work):
        """Check OpenAlex's open-access indicator."""

        open_access = work.get("open_access") or {}

        return bool(open_access.get("is_oa", False))
