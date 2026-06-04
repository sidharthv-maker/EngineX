-- EngineX SQLite schema
--
-- Contract between the crawler half and the search half.
--   pages      : written by the crawler
--   terms      : written by the indexer
--   postings   : written by the indexer
--   doc_stats  : written by the indexer

-- --------------------------------------------------------------------------
-- pages: one row per crawled Wikipedia page.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT    NOT NULL UNIQUE,
    title       TEXT,
    content     TEXT,
    crawled_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------------------
-- terms: vocabulary. `df` = number of distinct docs containing the term,
-- used to compute IDF at query time without a re-scan.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS terms (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT    NOT NULL UNIQUE,
    df   INTEGER NOT NULL DEFAULT 0
);

-- --------------------------------------------------------------------------
-- postings: the inverted index.
-- `tf` = how many times the term occurs in the doc.
-- PK ordering (term_id, doc_id) makes per-term lookup fast.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS postings (
    term_id INTEGER NOT NULL,
    doc_id  INTEGER NOT NULL,
    tf      INTEGER NOT NULL,
    PRIMARY KEY (term_id, doc_id),
    FOREIGN KEY (term_id) REFERENCES terms(id),
    FOREIGN KEY (doc_id)  REFERENCES pages(id)
);

-- Secondary index so we can also scan "all terms in doc X" cheaply
-- (useful when re-indexing or deleting a doc).
CREATE INDEX IF NOT EXISTS idx_postings_doc ON postings(doc_id);

-- --------------------------------------------------------------------------
-- doc_stats: derived per-doc statistics for ranking.
-- `length` = total token count in the doc, for length normalization.
-- Kept separate from `pages` so the crawler half doesn't need to touch it.
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doc_stats (
    doc_id INTEGER PRIMARY KEY,
    length INTEGER NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES pages(id)
);
