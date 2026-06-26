from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import ReviewRequest, ReviewResponse
from api.review import review_code

app = FastAPI(title="AI Code Review API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "AI Code Review API", "docs": "/docs", "usage": "POST /review with {code, language, focus}"}

@app.post("/review", response_model=ReviewResponse)
def review(body: ReviewRequest):
    if not body.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    if body.focus not in ["bugs", "style", "security", "performance", "all"]:
        raise HTTPException(status_code=400, detail="Focus must be: bugs, style, security, performance, or all")

    feedback = review_code(body.code, body.language, body.focus)
    lines = len(body.code.split("\n"))

    return ReviewResponse(feedback=feedback, language=body.language, focus=body.focus, line_count=lines)
