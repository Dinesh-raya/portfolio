import numpy as np
import requests

EMBEDDING_MODEL = "text-embedding-004"

def get_embedding(text: str, api_key: str) -> list[float]:
    url = f"https://generativelanguage.googleapis.com/v1/models/{EMBEDDING_MODEL}:embedContent"
    payload = {"model": f"models/{EMBEDDING_MODEL}", "content": {"parts": [{"text": text}]}}
    resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["embedding"]["values"]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve_chunks(question: str, chunks: list[str], embeddings: list[list[float]], api_key: str, top_k: int = 4) -> list[str]:
    q_emb = get_embedding(question, api_key)
    scored = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(embeddings)]
    scored.sort(reverse=True)
    return [chunks[i] for _, i in scored[:top_k]]
