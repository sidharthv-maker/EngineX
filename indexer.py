import spacy
from collections import Counter
from db import connect
nlp = spacy.load("en_core_web_sm")

def prop_token(text):
    #preprocess properly
    voc = nlp(text)
    lst = []
    for txt in voc:
        if txt.is_alpha and not txt.is_stop:
            lst.append(txt.lemma_.lower())
    return lst

def index_document(text):
    terms = prop_token(text)
    return Counter(terms), len(terms)

def index_page(conn, page_row):
    #index each page separately
    doc_id = page_row["id"]
    text = (page_row["title"] or "") + " " + (page_row["content"] or "")
    term_freqs, doc_length = index_document(text)
    conn.execute(
        "INSERT OR REPLACE INTO doc_stats(doc_id, length) VALUES (?, ?)",
        (doc_id, doc_length),
    )
    for term, tf in term_freqs.items():
        conn.execute("INSERT OR IGNORE INTO terms(term) VALUES (?)", (term,))
        term_id = conn.execute(
            "SELECT id FROM terms WHERE term = ?", (term,)
        ).fetchone()[0]
        conn.execute(
            "INSERT OR REPLACE INTO postings(term_id, doc_id, tf) VALUES (?, ?, ?)",
            (term_id, doc_id, tf),
        )

def index_all_pages(conn):
    # Wipe and rebuild — simplest correct behavior for re-runs.
    conn.execute("DELETE FROM postings")
    conn.execute("DELETE FROM doc_stats")
    conn.execute("DELETE FROM terms")

    rows = conn.execute("SELECT id, title, content FROM pages").fetchall()
    for i, page in enumerate(rows):
        index_page(conn, page)
        #progress bar
        if i % 100 == 0:
            print(f"  {i}/{len(rows)}")
    #count of number of distinct docs it appears in.
    conn.execute("""
        UPDATE terms SET df = (
            SELECT COUNT(*) FROM postings WHERE term_id = terms.id
        )
    """)
    
#guard
if __name__ == "__main__":
    with connect() as conn:
        n = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        if n == 0:
            print("No pages in DB - insert test rows first.")
        else:
            index_all_pages(conn)
            print(f"Indexed {n} page(s).")

