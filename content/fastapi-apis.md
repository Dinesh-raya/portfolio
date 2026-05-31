---
title: "Building REST APIs with FastAPI"
date: "2026-02-15"
category: "Python & Software Design"
excerpt: "A production-focused guide to FastAPI: Pydantic validation, dependency injection, async endpoints, and deployment patterns."
---

# Building REST APIs with FastAPI

FastAPI has become my go-to framework for building Python APIs. It combines automatic OpenAPI documentation, Pydantic validation, async support, and excellent performance — all with minimal boilerplate.

## Why FastAPI?

- **Automatic validation**: Pydantic models define request/response schemas
- **Self-documenting**: OpenAPI and ReDoc documentation generated automatically
- **Async by default**: Native support for asynchronous endpoints
- **Dependency injection**: Clean separation of concerns without heavy frameworks
- **Performance**: On par with Node.js and Go for typical API workloads

## Project Structure

A maintainable FastAPI project follows a modular structure:

```
app/
├── main.py          # Application entry point
├── config.py        # Settings and configuration
├── models/          # Pydantic schemas
├── routers/         # Endpoint definitions
├── services/        # Business logic
└── dependencies/    # Reusable dependencies
```

## Defining Models with Pydantic

Pydantic V2 provides runtime validation with near-zero overhead:

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class ContactMessage(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(default="", max_length=200)
    message: str = Field(..., min_length=10, max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ContactResponse(BaseModel):
    success: bool
    message: str
    message_id: Optional[str] = None
```

## Endpoints with Dependency Injection

Dependencies keep endpoints thin and testable:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="Portfolio API", version="1.0.0")

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact(
    message: ContactMessage,
    db: AsyncSession = Depends(get_db),
):
    try:
        message_id = await contact_service.save_message(db, message)
        await email_service.notify(message)
        return ContactResponse(success=True, message="Message sent", message_id=message_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
```

## Async Database Integration

FastAPI pairs naturally with async database drivers:

```python
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

class ContactService:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)

    async def save_message(self, db: AsyncSession, message: ContactMessage) -> str:
        stmt = contact_table.insert().values(
            name=message.name,
            email=message.email,
            subject=message.subject,
            message=message.message,
        ).returning(contact_table.c.id)
        result = await db.execute(stmt)
        await db.commit()
        return str(result.scalar_one())
```

## Error Handling

Consistent error responses improve API usability:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": str(exc)},
    )

@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "An unexpected error occurred"},
    )
```

## Deployment

Deploy FastAPI with production-ready configuration:

```python
# main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=4,
        log_level="info",
    )
```

And serve with a reverse proxy:

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Key Takeaways

1. Start with Pydantic models — they define your API contract
2. Use dependency injection for database sessions, authentication, and configuration
3. Write async endpoints for I/O-bound operations
4. Handle errors consistently with custom exception handlers
5. Always include health check and metrics endpoints in production

FastAPI's combination of modern Python features, automatic documentation, and excellent performance makes it the strongest choice for data-focused API development today.
