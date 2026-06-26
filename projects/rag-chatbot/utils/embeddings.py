import numpy as np
import google.generativeai as genai

EMBEDDING_MODEL = "models/embedding-001"

def get_embedding(text: str, api_key: str) -> list[float]:
    genai.configure(api_key=api_key)
    result = genai.embed_content(model=EMBEDDING_MODEL, content=text)
    return result["embedding"]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve_chunks(question: str, chunks: list[str], embeddings: list[list[float]], api_key: str, top_k: int = 4) -> list[str]:
    q_emb = get_embedding(question, api_key)
    scored = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(embeddings)]
    scored.sort(reverse=True)
    return [chunks[i] for _, i in scored[:top_k]]
