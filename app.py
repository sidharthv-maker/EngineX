import streamlit as st
from search import search

st.set_page_config(page_title="EngineX", layout="centered")

st.title("EngineX")
st.caption("A from-scratch search engine over Wikipedia.")

query = st.text_input("Search")

if query:
    results = search(query, k=10)
    if not results:
        st.info("No results found.")
    else:
        st.write(f"**{len(results)}** result(s)")
        for hit in results:
            st.subheader(hit["title"])
            st.markdown(f"[{hit['url']}]({hit['url']})")
            st.caption(f"score: {hit['score']:.3f}")
            st.divider()
