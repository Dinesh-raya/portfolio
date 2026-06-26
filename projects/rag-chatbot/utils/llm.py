import google.generativeai as genai

GENERATION_MODEL = "models/gemini-2.0-flash-exp"

def build_prompt(question: str, context: list[str]) -> str:
    ctx = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(context))
    return (
        "You are a precise AI assistant. Answer based ONLY on the provided context.\n"
        "If the context doesn't contain the answer, say 'I couldn't find that in the documents.'\n\n"
        f"Context:\n{ctx}\n\n"
        f"Question: {question}\nAnswer:"
    )

def generate_answer(question: str, context: list[str], api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GENERATION_MODEL)
    prompt = build_prompt(question, context)
    response = model.generate_content(prompt)
    return response.text
