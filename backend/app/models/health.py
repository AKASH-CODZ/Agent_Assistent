"""Pydantic models for health check and monitoring."""

from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class ServiceStatus(BaseModel):
    """Status of individual services."""
    status: str  # "healthy", "degraded", "unhealthy"
    response_time_ms: Optional[float] = None
    last_checked: Optional[datetime] = None
    error_message: Optional[str] = None
    version: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "response_time_ms": 45.2,
                "last_checked": "2024-01-15T10:30:00Z",
                "version": "v1.0.0"
            }
        }


class HealthResponse(BaseModel):
    """Comprehensive health check response."""
    status: str  # "healthy", "degraded", "unhealthy"
    system: str
    version: str = "2.0.0"
    timestamp: datetime = None
    uptime_seconds: Optional[float] = None
    services: Dict[str, ServiceStatus]
    system_resources: Optional[Dict[str, float]] = None

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "system": "Akash AI Engine",
                "version": "2.0.0",
                "timestamp": "2024-01-15T10:30:00Z",
                "uptime_seconds": 3600.5,
                "services": {
                    "groq": {
                        "status": "healthy",
                        "response_time_ms": 45.2,
                        "version": "latest"
                    },
                    "pinecone": {
                        "status": "healthy",
                        "response_time_ms": 120.5,
                        "version": "v2.0"
                    }
                },
                "system_resources": {
                    "cpu_percent": 25.5,
                    "memory_percent": 65.2,
                    "disk_percent": 45.8
                }
            }
        }