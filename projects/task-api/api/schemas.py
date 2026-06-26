from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

class TokenOut(BaseModel):
    token: str

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int
    created_at: datetime
