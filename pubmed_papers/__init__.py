"""
PubMed Papers - A tool to fetch research papers with company affiliations.
"""

from .core import PubMedFetcher
from .models import Author, Paper

__version__ = "0.1.0"
__all__ = ["PubMedFetcher", "Author", "Paper"] 