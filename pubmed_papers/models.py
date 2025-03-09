from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class Author:
    """Represents an author of a research paper."""
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None
    is_corresponding: bool = False
    is_company_affiliated: bool = False

@dataclass
class Paper:
    """Represents a research paper from PubMed."""
    pubmed_id: str
    title: str
    publication_date: date
    authors: List[Author]
    company_affiliations: List[str]

    @property
    def non_academic_authors(self) -> List[Author]:
        """Returns a list of authors affiliated with companies."""
        return [author for author in self.authors if author.is_company_affiliated]

    @property
    def corresponding_author_email(self) -> Optional[str]:
        """Returns the email of the corresponding author if available."""
        for author in self.authors:
            if author.is_corresponding and author.email:
                return author.email
        return None 