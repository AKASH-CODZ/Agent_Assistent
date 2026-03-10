from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import logging

# Fix relative imports
from app.services.groq_client import groq_client
from app.services.pinecone_db import pinecone_db

# Import utilities
from app.utils.monitoring import health_checker, system_monitor

# Configure logging
logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter(prefix="/api/v1", tags=["chat"])

# Store service references for health checking
SERVICES = {
    "groq": groq_client,
    "pinecone": pinecone_db
}

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    user_type: str = "visitor"  # can be 'recruiter', 'developer', or 'visitor'
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    context_used: List[str]
    conversation_id: Optional[str] = None
    user_type: str
    session_id: Optional[str] = None
    response_time_ms: float

class ServiceStatus(BaseModel):
    status: str
    response_time_ms: float
    timestamp: str
    details: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    system: str
    uptime_seconds: float
    services: Dict[str, ServiceStatus]
    system_resources: Dict[str, Any]

# Routes
@router.get("/", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    logger.info("Health check requested")
    
    # Check individual services
    services_status = {}
    for service_name, service in SERVICES.items():
        services_status[service_name] = await health_checker.check_service_health(
            service_name, service.health_check
        )
    
    # Get system resources
    system_resources = system_monitor.get_system_resources()
    
    # Determine overall status
    overall_status = health_checker.get_overall_status(services_status)
    
    return HealthResponse(
        status=overall_status,
        system="Akash AI Engine",
        uptime_seconds=health_checker.get_uptime(),
        services=services_status,
        system_resources=system_resources
    )

@router.get("/services/{service_name}/health")
async def service_health_check(service_name: str):
    """Check health of a specific service."""
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    service = SERVICES[service_name]
    health_status = await health_checker.check_service_health(service_name, service.health_check)
    
    return ServiceStatus(**health_status)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user queries using real LLM capabilities.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Chat request received: {request.message} from {request.user_type}")
        
        # Step 1: The user asks a question
        user_query = request.message
        
        # Step 2: Query Pinecone for relevant data
        relevant_docs_data = await pinecone_db.query(
            query_text=user_query,
            top_k=3,
            user_type=request.user_type
        )
        
        # Extract text content from documents
        relevant_docs = [doc.get('text', '') for doc in relevant_docs_data]
        
        # Step 3: Send context and question to Groq LLM
        final_answer = await groq_client.generate_response(
            query=user_query,
            context=relevant_docs,
            user_type=request.user_type
        )
        
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Generated response in {response_time:.2f}ms")
        
        return ChatResponse(
            reply=final_answer,
            context_used=relevant_docs,
            user_type=request.user_type,
            conversation_id=request.conversation_id,
            session_id=request.session_id,
            response_time_ms=round(response_time, 2)
        )

    except Exception as e:
        response_time = (time.time() - start_time) * 1000
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Internal server error",
                "message": str(e),
                "response_time_ms": round(response_time, 2)
            }
        )

@router.get("/stats")
async def get_statistics():
    """Get system statistics and performance metrics."""
    stats = {
        "system": system_monitor.get_system_resources(),
        "process": system_monitor.get_process_info(),
        "uptime_seconds": health_checker.get_uptime()
    }
    return stats

# Note: Middleware should be added in main.py, not on the router
# The add_process_time_header function has been removed from here
