"""Pydantic models for chat functionality."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    user_type: str = "visitor"  # can be 'recruiter', 'developer', or 'visitor'
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Tell me about your experience with FastAPI",
                "user_type": "recruiter",
                "conversation_id": "conv_123"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    reply: str
    context_used: List[str]
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None
    user_type: str
    response_time_ms: Optional[float] = None
    timestamp: datetime = None

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

    class Config:
        json_schema_extra = {
            "example": {
                "reply": "I have extensive experience with FastAPI...",
                "context_used": ["FastAPI experience", "Backend development"],
                "user_type": "recruiter",
                "response_time_ms": 1250.5,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }