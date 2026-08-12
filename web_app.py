"""Hafta 4 (Secenek B): Streamlit tabanli web arayuzu.

Calistirmak icin:
    venv\\Scripts\\streamlit run web_app.py

Chat gecmisini session_state icinde tutar, her soru icin
qa.answer_query() cagirir ve cevabi + kullanilan kaynaklari gosterir.
"""

import pathlib

import streamlit as st

import qa
import retrieval

DB_PATH = pathlib.Path(__file__).parent / "documents.db"

st.set_page_config(page_title="Local RAG Assistant", page_icon="🤖")

st.title("Local RAG Assistant")
st.caption(
    "Foundry Local ile tamamen cevrimdisi calisan, RAG mimarisine dayali "
    "dokuman soru-cevap asistani."
)

if not DB_PATH.exists():
    st.error("`documents.db` bulunamadi. Once terminalde `python ingest.py` calistirin.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

for entry in st.session_state.history:
    with st.chat_message("user"):
        st.write(entry["question"])
    with st.chat_message("assistant"):
        st.write(entry["answer"])
        if entry["sources"]:
            st.caption("Kaynaklar: " + ", ".join(entry["sources"]))

question = st.chat_input("Bir soru sor...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Dokumanlar araniyor ve cevap uretiliyor..."):
            chunks = retrieval.get_top_chunks(question, k=3)
            answer = qa.answer_query(question)
            sources = sorted({chunk.source for chunk in chunks if chunk.similarity >= qa.MIN_SIMILARITY_THRESHOLD})
        st.write(answer)
        if sources:
            st.caption("Kaynaklar: " + ", ".join(sources))

    st.session_state.history.append({"question": question, "answer": answer, "sources": sources})

with st.sidebar:
    st.header("Hakkinda")
    st.write(
        "- Embedding modeli: `qwen3-embedding-0.6b`\n"
        "- Sohbet modeli: `phi-3.5-mini`\n"
        "- Tum cikarim yerel cihazda calisir, internet baglantisi gerekmez."
    )
    if st.button("Sohbet gecmisini temizle"):
        st.session_state.history = []
        st.rerun()
