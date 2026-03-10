from fastapi.middleware.cors import CORSMiddleware
from .config import settings

def setup_cors(app):
    """
    Configure CORS middleware for the FastAPI application.
    This is crucial for allowing communication between Vercel frontend and Render backend.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "Accept",
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
        ],
        expose_headers=["Access-Control-Allow-Origin"],
    )