# 🚀 Akash AI Assistant Backend

Production-grade FastAPI backend for my digital portfolio clone with RAG (Retrieval Augmented Generation) capabilities.

## 🏗️ Architecture Overview

This backend implements a modern microservice architecture designed for high performance and scalability:

```
akash-ai-backend/
├── api/              # API routes and request/response models
├── core/             # Configuration, security, and settings
├── services/         # External service integrations
├── embed_data.py     # Data pipeline for vector embeddings
├── portfolio_data.json # Portfolio content source
├── main.py           # FastAPI application entry point
└── requirements.txt  # Python dependencies
```

## 🔧 Key Features

- **Lightning-fast inference** with Groq LLM API
- **Semantic search** powered by Pinecone vector database
- **Role-based responses** for recruiters, developers, and visitors
- **Industrial-grade structure** with proper separation of concerns
- **Comprehensive logging** and error handling
- **CORS configuration** for secure cross-origin communication
- **Health check endpoints** for monitoring
- **Docker-ready** for easy deployment

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file with your API keys:

```env
# Application Settings
APP_ENV=development
DEBUG=True

# API Keys
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=akash-portfolio

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000
```

### 3. Run the Development Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 4. Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 API Endpoints

### Health Check
```
GET /
```
Returns basic system status and service health.

### Chat Endpoint
```
POST /api/v1/chat
```

**Request Body:**
```json
{
  "message": "Tell me about your trading project",
  "user_type": "recruiter",
  "conversation_id": "optional-uuid"
}
```

**Response:**
```json
{
  "reply": "Trade-Mirror is an algorithmic trading platform I built...",
  "context_used": ["Project: Trade-Mirror...", "..."],
  "conversation_id": "optional-uuid",
  "user_type": "recruiter"
}
```

## 🔄 Data Pipeline

### 1. Prepare Portfolio Data

Edit `portfolio_data.json` with your portfolio information:

```json
[
  {
    "id": "unique-project-id",
    "title": "Project Name",
    "description": "Detailed project description",
    "technologies": ["Python", "FastAPI", "..."],
    "features": ["Feature 1", "Feature 2", "..."],
    "category": "trading|web-development|ai-ml|skills|experience"
  }
]
```

### 2. Generate and Upload Embeddings

Run the data pipeline to convert your portfolio data into searchable vector embeddings:

```bash
python embed_data.py
```

This script will:
- Load portfolio data from JSON
- Generate semantic embeddings using sentence-transformers
- Create Pinecone index if it doesn't exist
- Upload vector embeddings with metadata

## 🔌 Service Integrations

### Groq LLM Client
- Uses `llama3-70b-8192` model for high-quality responses
- Implements role-based prompting for different user types
- Graceful fallback to mock responses when API unavailable
- Configurable temperature and token limits

### Pinecone Vector Database
- Semantic search using cosine similarity
- Real-time embedding generation with sentence-transformers
- Category-based filtering for relevant results
- Automatic index creation and management

## 🛡️ Security Features

### CORS Configuration
```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-frontend.vercel.app"  # Add your Vercel URL
]
```

### Input Validation
- Pydantic models for request/response validation
- Sanitized user inputs
- Proper error handling and logging

## 📈 Performance Monitoring

### Built-in Health Checks
```bash
curl http://localhost:8000/api/v1/
```

Returns service status for both Groq and Pinecone connections.

### Logging
Comprehensive logging at different levels:
- INFO: General operations and service status
- WARNING: Non-critical issues and fallbacks
- ERROR: Failed operations and exceptions

## 🐳 Deployment

### Production Environment Variables
```env
APP_ENV=production
DEBUG=False
FRONTEND_URL=https://your-portfolio.vercel.app
```

### Running in Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🧪 Testing

### Test the API
```bash
python test_api.py
```

### Test LLM Capabilities
```bash
python test_llm_capabilities.py
```

## 📁 Project Structure Details

```
core/
├── config.py         # Environment variables and settings
├── security.py       # CORS middleware configuration
└── __init__.py

api/
├── routes.py         # API endpoints and models
└── __init__.py

services/
├── groq_client.py    # Groq LLM integration
├── pinecone_db.py    # Pinecone vector database
└── __init__.py
```

## 🤝 Integration with Frontend

This backend is designed to work seamlessly with a Next.js frontend hosted on Vercel:

1. **CORS**: Pre-configured to allow requests from your Vercel frontend
2. **API Contract**: Consistent request/response formats
3. **Error Handling**: Standardized error responses
4. **Health Monitoring**: Easy integration with frontend status checks

## 🚨 Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Or run with full path
   python -m uvicorn main:app --reload
   ```

2. **API Key Issues**
   - Verify `.env` file exists and contains valid keys
   - Check that API keys are not placeholder values
   - Ensure Pinecone index exists or run `embed_data.py`

3. **Port Conflicts**
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   
   # Or use different port
   uvicorn main:app --port 8001
   ```

4. **CORS Errors**
   - Update `FRONTEND_URL` in `.env` with your actual Vercel URL
   - Restart the server after configuration changes

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Sentence Transformers](https://www.sbert.net/)

## 📄 License

This project is part of my personal portfolio and is not licensed for commercial use.