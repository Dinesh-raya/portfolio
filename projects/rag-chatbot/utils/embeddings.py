import numpy as np
import requests

ENDPOINTS = [
    ("gemini-embedding-001", "v1beta"),
    ("gemini-embedding-2", "v1beta"),
    ("gemini-embedding-001", "v1"),
    ("gemini-embedding-2", "v1"),
]

def get_embedding(text: str, api_key: str) -> list[float]:
    errors = []
    for model, version in ENDPOINTS:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:embedContent"
        payload = {"model": f"models/{model}", "content": {"parts": [{"text": text}]}}
        resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=15)
        if resp.status_code == 200:
            return resp.json()["embedding"]["values"]
        errors.append(f"{version}/{model}: {resp.status_code}")
    raise RuntimeError(f"All embedding endpoints failed:\n" + "\n".join(errors))

def list_models(api_key: str) -> list[str]:
    for version in ["v1beta", "v1"]:
        url = f"https://generativelanguage.googleapis.com/{version}/models?key={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            all_models = [m["name"] for m in data.get("models", [])]
            embed = [m for m in all_models if "embed" in m.lower() or "textembedding" in m.lower()]
            return embed
    return []

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve_chunks(question: str, chunks: list[str], embeddings: list[list[float]], api_key: str, top_k: int = 4) -> list[str]:
    q_emb = get_embedding(question, api_key)
    scored = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(embeddings)]
    scored.sort(reverse=True)
    return [chunks[i] for _, i in scored[:top_k]]
