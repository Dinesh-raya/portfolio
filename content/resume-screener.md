---
title: "Building a Resume Screener with NLP and Streamlit"
date: "2026-05-25"
category: "Artificial Intelligence"
excerpt: "How I built a production-ready resume screening tool that extracts skills from PDFs and ranks candidates using TF-IDF and custom skill taxonomies."
---

# Building a Resume Screener with NLP and Streamlit

Resume screening is one of the most time-consuming tasks in hiring. Automating it with NLP doesn't just save hours — it ensures consistent, unbiased evaluation. Here's how I built a resume screener that extracts skills, ranks candidates, and visualizes matches.

## Architecture Overview

The system follows a pipeline architecture: ingest, parse, extract, score, and visualize.

```
PDF Upload → Text Extraction → Skill Extraction → Vectorization → Ranking → Dashboard
```

## PDF Text Extraction

The first challenge is getting clean text from PDFs. Using PyMuPDF (fitz), we extract text page by page:

```python
import fitz

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
```

Key considerations:
- Handle scanned PDFs with OCR fallback
- Preserve section structure (education, experience, skills)
- Clean up encoding artifacts and special characters

## Skill Extraction with TF-IDF

Instead of relying on external APIs, we use a curated skill taxonomy and TF-IDF vectorization for lightweight, local matching:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_TAXONOMY = {
    "python": ["python", "django", "flask", "fastapi"],
    "machine_learning": ["machine learning", "deep learning", "tensorflow", "pytorch"],
    "data_engineering": ["etl", "pipeline", "spark", "airflow"],
    "devops": ["docker", "kubernetes", "ci/cd", "jenkins"],
}
```

This approach:
- Works entirely offline — no API keys needed
- Handles synonyms and related terms
- Produces a dense skill vector for each candidate

## Candidate Scoring

Each resume is scored across multiple dimensions:

| Dimension | Weight | Method |
|-----------|--------|--------|
| Skill Match | 40% | TF-IDF cosine similarity to job description |
| Experience | 30% | Years extracted from timeline sections |
| Education | 15% | Degree level and relevance |
| Certifications | 15% | Presence of relevant certs |

The composite score feeds into a ranked leaderboard displayed in Streamlit.

## Streamlit Dashboard

The frontend provides three views:

1. **Upload & Parse**: Drag-and-drop PDF upload with real-time extraction preview
2. **Skill Matrix**: Heatmap showing which skills each candidate possesses
3. **Ranked Leaderboard**: Sorted candidate cards with scores and expandable detail panels

```python
# Streamlit column layout for candidate cards
cols = st.columns(3)
for i, candidate in enumerate(ranked):
    with cols[i % 3]:
        st.metric(candidate["name"], f"{candidate['score']}/100")
        st.progress(candidate["score"] / 100)
```

## Lessons Learned

1. **PDF quality varies wildly**: Some resumes have no extractable text (scanned images)
2. **Skill taxonomy needs regular updates**: Domain-specific terms evolve quickly
3. **Structured extraction outperforms raw parsing**: Detecting sections improves accuracy
4. **TF-IDF is surprisingly effective**: For domain-specific matching, it often matches embedding-based approaches

## Conclusion

Building a resume screener taught me that practical NLP doesn't always require large language models. With careful feature engineering and a well-designed pipeline, you can build production-quality tools using lightweight, local approaches.
