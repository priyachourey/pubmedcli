import sys
import click
import logging
import pandas as pd
from typing import Optional
from .core import PubMedFetcher

# Configure logging
logger = logging.getLogger(__name__)

def setup_logging(debug: bool) -> None:
    """Configure logging based on debug flag."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def papers_to_dataframe(papers):
    """Convert paper objects to a pandas DataFrame."""
    data = []
    for paper in papers:
        non_academic_authors = paper.non_academic_authors
        data.append({
            'PubmedID': paper.pubmed_id,
            'Title': paper.title,
            'Publication Date': paper.publication_date,
            'Non-academic Author(s)': '; '.join(a.name for a in non_academic_authors),
            'Company Affiliation(s)': '; '.join(paper.company_affiliations),
            'Corresponding Author Email': paper.corresponding_author_email or ''
        })
    return pd.DataFrame(data)

@click.command()
@click.argument('query')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-f', '--file', type=str, help='Output file path (CSV)')
def main(query: str, debug: bool, file: Optional[str]) -> None:
    """
    Fetch PubMed papers based on query and identify company-affiliated authors.
    
    QUERY: The search query for PubMed (e.g., "cancer immunotherapy")
    """
    try:
        # Setup logging
        setup_logging(debug)
        
        # Initialize fetcher with a default email
        fetcher = PubMedFetcher(email="your.email@example.com")
        
        # Search for papers
        logger.info(f"Searching for: {query}")
        papers = fetcher.search_papers(query)
        
        if not papers:
            logger.warning("No papers found with company affiliations")
            sys.exit(0)
            
        # Convert to DataFrame
        df = papers_to_dataframe(papers)
        
        # Output results
        if file:
            df.to_csv(file, index=False)
            logger.info(f"Results saved to {file}")
        else:
            # Print to console
            click.echo(df.to_string(index=False))
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 