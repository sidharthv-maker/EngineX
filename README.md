# EngineX

A Python-based search engine project built from scratch, starting with a web-crawler.

## Current Progress

The project contains an initial crawler prototype that:
- Fetches a web-page using HTTP requests
- Parses HTML using BeautifulSoup
- Extracts the page title
- Extracts paragraph tags from the page
- Displays the first five paragraphs' contents

## Technologies Used
- Python 3
- Requests
- BeautifulSoup4

## Running The Project

1. Install dependencies
```bash
pip install requests beautifulsoup4
```

2. Run
```bash
python3 crawler.py
```