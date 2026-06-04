# EngineX

A Python-based search-engine built from scratch over Wikipedia.

EngineX consists of three major components:
1. **Crawler** - Crawls Wikipedia pages and stores them in SQLite.
2. **Indexer** - Builds an inverted-index from crawled pages.
3. **Search Interface** - Provides a Streamlit-based UI for querying indexed pages.

## Features

### Web-Crawler
- Breadth-first search crawling strategy
- Multiple Wikipedia seed URL(s)
- Duplicate URL prevention using `discovered` and `alreadyVisited` sets
- Article-link filtering
- SQLite persistence
- Configurable crawl-limit
- Request throttling using `time.sleep()`

### Indexer
- Tokenization and lemmatization using spaCy
- Stop-word filtering
- Inverted-index construction
- Term-frequency (TF) computation
- Document-frequency (DF) computation
- Per-document statistics

### Search Engine
- TF-IDF ranking
- Top-k document retrieval
- Streamlit web-interface
- Ranked search results with scores

## Project Structure
```text
EngineX
├── crawler.py  # Wikipedia crawler
├── indexer.py  # Inverted index builder
├── search.py   # Search and ranking logic
├── app.py      # Streamlit UI
├── db.py       # Database helpers
├── schema.sql  # SQLite schema
├── enginex.db  # Generated database (ignored by git)
└── README.md
```

## Database Pipeline
```text
Wikipedia
    ↓
Crawler
    ↓
pages
    ↓
Indexer
    ↓
terms
postings
doc_stats
    ↓
Search
    ↓
Streamlit UI
```

## Technologies Used
- Python 3
- SQLite3
- Requests
- BeautifulSoup4
- spaCy
- NumPy
- Streamlit

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install requests beautifulsoup4 spacy numpy streamlit
```

3. Install the spaCy language model:
```bash
python3 -m spacy download en_core_web_sm
```

## Usage

1. Crawl pages:
```bash
python3 crawler.py
```

This populates the `pages` table in SQLite.

2. Build the index:
```bash
python3 indexer.py
```

This populates:
- `terms`
- `postings`
- `doc_stats`

3. Launch the interface:
```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

in your browser.