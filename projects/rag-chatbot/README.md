# RAG Chatbot

Ask questions about your documents. Powered by Google Gemini (free tier — no credit card needed).

## How it works

1. Upload a PDF, DOCX, or TXT file
2. Document is chunked and embedded using Gemini Embedding API
3. Ask questions — relevant chunks are retrieved via cosine similarity
4. Gemini generates an answer grounded in those chunks

## Run locally

```bash
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env
streamlit run app.py
```

## Deploy on Streamlit Cloud (free)

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → New app → select repo
3. Add `GEMINI_API_KEY` in **Settings → Secrets**
4. Deploy

## Get a free API key

1. Visit https://aistudio.google.com/apikey
2. Click **Get API Key** → Create API Key
3. Copy the key — no credit card required (60 req/min free)

## Architecture

```
app.py              → Streamlit UI (chat + upload)
utils/
├── ingestion.py    → PDF/DOCX/TXT parsing + text chunking
├── embeddings.py   → Gemini embeddings + cosine similarity search
└── llm.py          → Gemini prompt builder + answer generation
```

No database, no Docker, no backend server. Everything runs in-process on Streamlit Cloud.
