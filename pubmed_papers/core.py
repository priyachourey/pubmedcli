from typing import List, Optional, Set, Union
from datetime import datetime
import re
import logging
from Bio import Entrez
from Bio import Medline
from .models import Author, Paper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PubMedFetcher:
    """Class to handle PubMed paper fetching and processing."""
    
    def __init__(self, email: str):
        """Initialize the fetcher with user's email (required by NCBI)."""
        Entrez.email = email
        self.company_keywords = {
            'pharma', 'biotech', 'therapeutics', 'biosciences',
            'laboratories', 'inc', 'corp', 'ltd', 'llc', 'gmbh'
        }
        self.academic_keywords = {
            'university', 'college', 'institute', 'school',
            'academia', 'hospital', 'medical center', 'clinic'
        }

    def is_company_affiliation(self, affiliation: Optional[str]) -> bool:
        """Determine if an affiliation is from a company."""
        if not affiliation:
            return False
        
        affiliation_lower = affiliation.lower()
        
        # Check for company keywords
        has_company_keyword = any(keyword in affiliation_lower 
                                for keyword in self.company_keywords)
        
        # Check for academic keywords
        has_academic_keyword = any(keyword in affiliation_lower 
                                 for keyword in self.academic_keywords)
        
        return has_company_keyword and not has_academic_keyword

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text using regex."""
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def process_affiliations(self, affiliations: Union[str, List[str]]) -> List[str]:
        """Process affiliations that can be either a string or a list."""
        if isinstance(affiliations, str):
            return [aff.strip() for aff in affiliations.split(';') if aff.strip()]
        elif isinstance(affiliations, list):
            return [aff.strip() for aff in affiliations if aff.strip()]
        return []

    def search_papers(self, query: str, max_results: int = 100) -> List[Paper]:
        """Search PubMed for papers matching the query."""
        logger.info(f"Searching PubMed for: {query}")
        
        # Search PubMed
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()

        # Get the list of IDs
        id_list = record["IdList"]
        if not id_list:
            logger.warning("No results found")
            return []

        # Fetch details for each paper
        handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
        records = Medline.parse(handle)
        
        papers: List[Paper] = []
        for record in records:
            try:
                # Process authors and their affiliations
                authors: List[Author] = []
                company_affiliations: Set[str] = set()
                
                # Extract author information
                if "AU" in record:
                    author_names = record.get("AU", [])
                    # Get affiliations if available
                    raw_affiliations = record.get("AD", [])
                    affiliations = self.process_affiliations(raw_affiliations)
                    
                    for i, name in enumerate(author_names):
                        affiliation = affiliations[i] if i < len(affiliations) else None
                        is_company = self.is_company_affiliation(affiliation)
                        email = self.extract_email(affiliation) if affiliation else None
                        
                        author = Author(
                            name=name,
                            affiliation=affiliation,
                            email=email,
                            is_corresponding=bool(email),  # Simple heuristic
                            is_company_affiliated=is_company
                        )
                        authors.append(author)
                        
                        if is_company and affiliation:
                            company_affiliations.add(affiliation)

                # Create paper object
                paper = Paper(
                    pubmed_id=record.get("PMID", ""),
                    title=record.get("TI", ""),
                    publication_date=datetime.strptime(
                        record.get("DP", "").split()[0], "%Y"
                    ).date(),
                    authors=authors,
                    company_affiliations=list(company_affiliations)
                )
                
                # Only add papers with company-affiliated authors
                if paper.non_academic_authors:
                    papers.append(paper)
                    
            except Exception as e:
                logger.error(f"Error processing paper {record.get('PMID', '')}: {str(e)}")
                continue

        handle.close()
        return papers 