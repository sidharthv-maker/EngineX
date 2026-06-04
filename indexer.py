import spacy
from collections import Counter
from db import connect
nlp = spacy.load("en_core_web_sm")

def prop_token(text):
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

#guard

if __name__ == "__main__":
    with connect() as conn:
        page = conn.execute(
            "SELECT id, title, content FROM pages LIMIT 1"
        ).fetchone()
        if page is None:
            print("No pages in DB - insert a test row first.")
        else:
            index_page(conn, page)
            print(f"Indexed page {page['id']}: {page['title']}")

