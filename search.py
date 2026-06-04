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
