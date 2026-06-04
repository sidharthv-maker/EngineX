from indexer import prop_token
import numpy as np
from db import connect
from collections import defaultdict

def query_rank(conn, query):
    qterm = prop_token(query)
    if not qterm:
        return {}
    n = conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
    scores = defaultdict(float)
    for term in qterm:
        ro = conn.execute("SELECT id, df FROM terms where term=?", (term,)).fetchone()
        if ro is None:
            continue
        term_id, df = ro["id"], ro["df"]
        idf = np.log(n/df)
        for posting in conn.execute("SELECT doc_id, tf FROM postings WHERE term_id = ?", (term_id,)):
            scores[posting["doc_id"]] += posting["tf"] * idf
    return scores

def search(query, k=10):
    with connect() as conn:
        dic = query_rank(conn, query)
        dicn = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True)[:k])
        ids = list(dicn.keys())
        if not ids:
            return []
        placeholders = ",".join("?" * len(ids))
        rows = conn.execute(
            f"SELECT id, url, title FROM pages WHERE id IN ({placeholders})",
            ids,
        ).fetchall()
        page_by_id = {r["id"]: r for r in rows}
        return [
            {
                "doc_id": d,
                "title": page_by_id[d]["title"],
                "url": page_by_id[d]["url"],
                "score": float(s),
            }
            for d, s in dicn.items()
        ]
        
#guard
if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) or "computer science"
    for hit in search(query):
        print(f"{hit['score']:.3f}  {hit['title']}  ({hit['url']})")
