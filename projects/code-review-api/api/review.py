import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"

PROMPT_TEMPLATE = """You are a senior software engineer reviewing code. Be precise, actionable, and honest.

Language: {language}
Focus area: {focus}

Review the following code for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code style and best practices
- Potential improvements

If the focus is "all", cover everything. Otherwise, focus only on {focus}.

Return your review as a structured markdown with these sections (if applicable):
## Summary
## Issues Found
## Suggestions
## Positive Aspects

Code to review:
```{language}
{code}
```

Review:"""

def review_code(code: str, language: str = "python", focus: str = "all") -> str:
    prompt = PROMPT_TEMPLATE.format(code=code, language=language, focus=focus)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(f"{url}?key={API_KEY}", json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
