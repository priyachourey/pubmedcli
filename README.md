# PubMed Papers

A Python tool to fetch research papers from PubMed and identify papers with authors affiliated with pharmaceutical or biotech companies.

[![Test PyPI version](https://img.shields.io/badge/test--pypi-v0.1.0-blue)](https://test.pypi.org/project/pubmed-papers/)

## Features

- Fetch papers using PubMed API through Biopython
- Filter papers based on author affiliations
- Export results to CSV
- Command-line interface with various options

## Installation

You can install the package from Test PyPI:

```bash
pip install -i https://test.pypi.org/simple/ pubmed-papers
```

Or install from source:

1. Make sure you have Python 3.12 or higher installed
2. Install Poetry (package manager) if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository:
   ```bash
   git clone git@github.com:priyachourey/pubmedcli.git
   cd pubmedcli
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
- [Cursor](https://cursor.sh/) - Modern IDE with AI capabilities


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
