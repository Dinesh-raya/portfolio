<div align="center">

# Dinesh Raya — AI Engineer Portfolio

A clean, fast portfolio site. Static HTML/CSS served via GitHub Pages — no frameworks, no server, no build step.

**Live:** [https://dinesh-raya.github.io/portfolio/](https://dinesh-raya.github.io/portfolio/)

</div>

## Projects

| Project | Stack | Demo |
|---------|-------|------|
| [RAG Chatbot](projects/rag-chatbot/) | Python, Streamlit, Gemini API, RAG | [Live](https://drrragai.streamlit.app/) |
| [Data Pipeline](projects/data-pipeline/) | Python, pandas, SQLite, GitHub API, CI/CD | [Live](https://drrdatapipeline.streamlit.app/) |
| [AI Code Review API](projects/code-review-api/) | FastAPI, Gemini AI, Docker, CI/CD | [Live](https://drrcodereviewapi.streamlit.app/) |
| [Network Port Scanner](https://github.com/Dinesh-raya/python-network-port-scanner) | Python, Streamlit, Socket Programming | [Live](https://drrnps.streamlit.app/) |

## Structure

```
├── index.html              → Portfolio homepage (GitHub Pages)
├── styles/                 → CSS
├── components/             → Streamlit components (legacy)
├── data/                   → Portfolio data (legacy)
├── projects/               → Project source code
│   ├── rag-chatbot/        → RAG chatbot (Gemini API)
│   ├── data-pipeline/      → Trending repos ETL pipeline
│   └── code-review-api/    → AI code review (FastAPI + Gemini)
├── .github/workflows/      → CI/CD pipelines
└── app.py                  → Legacy Streamlit app
```
