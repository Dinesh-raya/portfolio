import requests

ENDPOINTS = [
    ("gemini-2.5-flash", "v1beta"),
    ("gemini-2.0-flash", "v1beta"),
    ("gemini-2.5-flash", "v1"),
    ("gemini-2.0-flash", "v1"),
]

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
    errors = []
    for model, version in ENDPOINTS:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        errors.append(f"{version}/{model}: {resp.status_code}")
    raise RuntimeError(f"All generation endpoints failed:\n" + "\n".join(errors))

def list_gen_models(api_key: str) -> list[str]:
    for version in ["v1beta", "v1"]:
        url = f"https://generativelanguage.googleapis.com/{version}/models?key={api_key}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            all_models = [m["name"] for m in data.get("models", [])]
            gen = [m for m in all_models if "gemini-" in m and "embed" not in m and "tts" not in m]
            return gen
    return []
