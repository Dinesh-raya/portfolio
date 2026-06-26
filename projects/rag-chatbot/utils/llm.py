import requests

GENERATION_MODEL = "gemini-1.5-flash"

def build_prompt(question: str, context: list[str]) -> str:
    ctx = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(context))
    return (
        "You are a precise AI assistant. Answer based ONLY on the provided context.\n"
        "If the context doesn't contain the answer, say 'I couldn't find that in the documents.'\n\n"
        f"Context:\n{ctx}\n\n"
        f"Question: {question}\nAnswer:"
    )

def generate_answer(question: str, context: list[str], api_key: str) -> str:
    prompt = build_prompt(question, context)
    url = f"https://generativelanguage.googleapis.com/v1/models/{GENERATION_MODEL}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
