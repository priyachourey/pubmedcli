# PubMed Papers

A Python tool to fetch research papers from PubMed and identify papers with authors affiliated with pharmaceutical or biotech companies.

## Features

- Fetch papers using PubMed API through Biopython
- Filter papers based on author affiliations
- Export results to CSV
- Command-line interface with various options

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Install Poetry (package manager) if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository:
   ```bash
   git clone <repository-url>
   cd pubmed-papers
   ```
4. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

The tool can be used via command line:

```bash
poetry run get-papers-list "your search query" [OPTIONS]
```

Options:
- `-h, --help`: Show help message
- `-d, --debug`: Enable debug mode
- `-f, --file FILENAME`: Save results to specified CSV file (default: prints to console)

Example:
```bash
poetry run get-papers-list "cancer immunotherapy" -f results.csv
```

## Project Structure

```
pubmed_papers/
├── __init__.py
├── cli.py           # Command-line interface
├── core.py          # Core functionality
├── models.py        # Data models
└── utils.py         # Utility functions
```

## Tools Used

- [Poetry](https://python-poetry.org/) - Dependency management
- [Biopython](https://biopython.org/) - PubMed API interaction
- [Pandas](https://pandas.pydata.org/) - Data processing
- [Click](https://click.palletsprojects.com/) - CLI interface
- [MyPy](https://mypy.readthedocs.io/) - Static type checking
- [Black](https://black.readthedocs.io/) - Code formatting

## Development

This project uses:
- Type hints for better code quality
- Black for code formatting
- MyPy for static type checking

To run tests:
```bash
poetry run pytest
```

To format code:
```bash
poetry run black .
```

To run type checking:
```bash
poetry run mypy .
``` 