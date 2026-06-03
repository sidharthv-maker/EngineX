# EngineX

A Python-based search engine project built from scratch, starting with a web-crawler.

## Current Progress

The project contains a breadth-first web-crawler that:
- Fetches a web-page using HTTP requests
- Parses HTML using BeautifulSoup
- Extracts article links from WikiPedia pages
- Filters non-article links
- Uses a queue-based BFS traversal strategy
- Avoids re-visiting previously discovered pages
- Extracts and stores page title, page URL and page content

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