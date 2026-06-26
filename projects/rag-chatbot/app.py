import os
import tempfile
import streamlit as st

from utils.ingestion import extract_text, chunk_text
from utils.embeddings import get_embedding, retrieve_chunks
from utils.llm import generate_answer

st.set_page_config(page_title="RAG Chatbot", page_icon="", layout="wide")

st.markdown("""
<style>
    .block-container { max-width: 800px; }
    .stChatMessage { border-radius: 12px; }
    .source-tag {
        font-size: 0.7rem; color: #64748b; background: rgba(79,124,255,0.08);
        padding: 2px 8px; border-radius: 4px; display: inline-block; margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.title(" RAG Chatbot")
st.markdown("Upload a document and ask questions about it. Powered by Google Gemini (free).")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found. Set it in Streamlit Cloud secrets or .env")
    st.info("Get a free key at https://aistudio.google.com/apikey — no credit card needed.")
    st.stop()

if "chunks" not in st.session_state:
    st.session_state.chunks = []
    st.session_state.embeddings = []
    st.session_state.sources = []
    st.session_state.messages = []

with st.sidebar:
    st.markdown("### Upload Document")
    uploaded = st.file_uploader("Choose PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded.name.split('.')[-1]}") as tmp:
            tmp.write(uploaded.read())
            path = tmp.name
        text = extract_text(path)
        st.session_state.chunks = chunk_text(text)
        st.session_state.sources = [uploaded.name] * len(st.session_state.chunks)
        with st.spinner("Generating embeddings..."):
            try:
                st.session_state.embeddings = [
                    get_embedding(c, api_key) for c in st.session_state.chunks
                ]
            except Exception as e:
                st.error(f"Embedding failed: {e}")
                with st.expander("Debug: available embedding models"):
                    try:
                        from utils.embeddings import list_models
                        models = list_models(api_key)
                        st.write("\n".join(models) if models else "No embedding models found.")
                    except Exception as e2:
                        st.write(f"Could not list models: {e2}")
                st.stop()
        os.unlink(path)
        st.success(f"Ingested {len(st.session_state.chunks)} chunks from {uploaded.name}")

    if st.session_state.chunks:
        st.markdown(f"**{len(st.session_state.chunks)} chunks** loaded")
        if st.button("Clear documents"):
            st.session_state.chunks = []
            st.session_state.embeddings = []
            st.session_state.sources = []
            st.session_state.messages = []
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg:
            st.markdown("".join(f'<span class="source-tag">{s}</span>' for s in msg["sources"]), unsafe_allow_html=True)

if question := st.chat_input("Ask a question about your document..."):
    if not st.session_state.chunks:
        st.warning("Upload a document first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                context = retrieve_chunks(question, st.session_state.chunks, st.session_state.embeddings, api_key)
                answer = generate_answer(question, context, api_key)
            except Exception as e:
                answer = f"Error: {e}"
                with st.expander("Debug: available generation models"):
                    try:
                        from utils.llm import list_gen_models
                        st.write("\n".join(list_gen_models(api_key)))
                    except Exception as e2:
                        st.write(f"Could not list models: {e2}")
            st.markdown(answer)
            sources = list(set(st.session_state.sources[st.session_state.chunks.index(c)] for c in context))
            st.markdown("".join(f'<span class="source-tag">{s}</span>' for s in sources), unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
