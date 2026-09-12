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
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=15,
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
        """Extract the DOI from an OpenAlex work."""

        doi = work.get("doi")

        if not doi:
            return ""

        return doi.replace("https://doi.org/", "")

    @staticmethod
    def extract_url(work):
        """Extract the best available URL for the work."""

        primary_location = work.get("primary_location") or {}

        landing_page = primary_location.get("landing_page_url")

        if landing_page:
            return landing_page

        return work.get("id", "")