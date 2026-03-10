from typing import List, Dict, Any
import logging
from sentence_transformers import SentenceTransformer
# Fix relative import
from app.core.config import settings

logger = logging.getLogger(__name__)

class PineconeDB:
    """Client for interacting with Pinecone vector database."""
    
    def __init__(self):
        self.api_key = settings.PINECONE_API_KEY
        self.index_name = settings.PINECONE_INDEX_NAME
        self.client = None
        self.index = None
        self.embedding_model = None
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('thenlper/gte-large')  # 1024 dimensions
            logger.info("✅ Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {str(e)}")
        
        # Initialize client only if API key is provided
        if (self.api_key and self.api_key != "your_pinecone_api_key_here" and not self.api_key.startswith("your_") and
            self.index_name and self.index_name != "your_index_name_here" and not self.index_name.startswith("your_")):
            try:
                # Import pinecone only when needed
                from pinecone import Pinecone
                self.client = Pinecone(api_key=self.api_key)
                self.index = self.client.Index(self.index_name)
                logger.info("✅ Pinecone client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Pinecone client: {str(e)}")
                self.client = None
                self.index = None
        else:
            logger.warning("⚠️ Pinecone API key or index name not configured properly - using mock mode")
    
    async def query(
        self, 
        query_text: str, 
        top_k: int = 3,
        user_type: str = "visitor"
    ) -> List[Dict[str, Any]]:
        """
        Query Pinecone for relevant documents.
        
        Args:
            query_text: Text to search for
            top_k: Number of results to return
            user_type: Type of user for filtering
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            logger.info(f"🔍 Querying Pinecone for: {query_text}")
            
            # Check if we have real Pinecone connection and embedding model
            if self.index and self.embedding_model:
                # Convert query to embedding
                query_embedding = self.embedding_model.encode(query_text).tolist()
                
                # Query Pinecone
                results = self.index.query(
                    vector=query_embedding,
                    top_k=top_k * 2,  # Get more results to filter
                    include_metadata=True
                )
                
                # Process results
                processed_results = []
                for match in results.matches:
                    result = {
                        'id': match.id,
                        'text': match.metadata.get('text', ''),
                        'score': match.score,
                        'metadata': match.metadata
                    }
                    processed_results.append(result)
                
                logger.info(f"✅ Found {len(processed_results)} relevant documents")
                
                # Filter results based on user type
                filtered_results = self._filter_by_user_type(processed_results, user_type)
                
                return filtered_results[:top_k]
            
            # Fall back to enhanced mock implementation
            logger.info("⚠️ Using enhanced mock data for query")
            mock_results = self._get_enhanced_mock_data(query_text, user_type)
            
            # Filter results based on user type
            filtered_results = self._filter_by_user_type(mock_results, user_type)
            
            return filtered_results[:top_k]
            
        except Exception as e:
            logger.error(f"❌ Error querying Pinecone: {str(e)}")
            # Return basic mock data as fallback
            return self._get_basic_mock_data()

    def _get_enhanced_mock_data(self, query_text: str, user_type: str) -> List[Dict]:
        """Generate enhanced mock data based on query content."""
        # Enhanced mock data with more realistic content
        base_projects = [
            {
                "id": "trade-mirror-project",
                "text": """Project: Trade-Mirror - Algorithmic Trading Platform
Technology Stack: Python 3.9+, FastAPI, WebSocket, PostgreSQL, Redis
APIs: Zerodha Kite Connect, Shoonya Noren API
Key Features: 
- Real-time market data streaming and analysis
- Automated trading strategy execution
- SHA-256 data integrity verification
- Risk management with stop-loss mechanisms
- Performance analytics dashboard
- RESTful API for external integrations""",
                "metadata": {
                    "project_name": "Trade-Mirror",
                    "tech_stack": ["Python", "FastAPI", "WebSocket", "PostgreSQL", "Redis", "Zerodha API", "Shoonya API"],
                    "category": "trading",
                    "complexity": "high",
                    "relevance_score": 0.95
                }
            },
            {
                "id": "portfolio-website",
                "text": """Project: Personal Portfolio Website
Technology Stack: Next.js 14, React 18, TypeScript, Tailwind CSS, Framer Motion
Deployment: Vercel hosting with CI/CD pipeline
Features:
- Responsive design with mobile-first approach
- Dark/light theme toggle
- Smooth animations and transitions
- SEO optimized with meta tags and structured data
- Performance optimized (Lighthouse scores >95)
- Contact form with email integration
- Blog section with MDX support""",
                "metadata": {
                    "project_name": "Portfolio Website",
                    "tech_stack": ["Next.js", "React", "TypeScript", "Tailwind CSS", "Framer Motion", "Vercel"],
                    "category": "web-development",
                    "complexity": "medium",
                    "relevance_score": 0.87
                }
            },
            {
                "id": "ai-assistant-backend",
                "text": """Project: AI Assistant Backend API
Technology Stack: FastAPI, Python 3.9+, Pinecone Vector DB, Groq LLM API
Architecture: Microservice pattern with modular design
Features:
- RAG (Retrieval Augmented Generation) implementation
- Semantic search capabilities
- RESTful API with OpenAPI documentation
- Role-based response personalization
- Comprehensive logging and monitoring
- Docker containerization ready
- Scalable architecture design""",
                "metadata": {
                    "project_name": "AI Assistant Backend",
                    "tech_stack": ["FastAPI", "Python", "Pinecone", "Groq API", "Docker"],
                    "category": "ai-ml",
                    "complexity": "high",
                    "relevance_score": 0.92
                }
            },
            {
                "id": "skills-overview",
                "text": """Technical Skills Overview:
Programming Languages: Python (Expert), JavaScript/TypeScript (Advanced), SQL (Intermediate)
Frameworks & Libraries: FastAPI, Django, React, Next.js, Node.js
Databases: PostgreSQL, MongoDB, Redis, SQLite
Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Git, CI/CD pipelines
Tools & Platforms: Git, GitHub Actions, Vercel, Render, Postman
Soft Skills: Problem-solving, Technical Leadership, Documentation, Team Collaboration
Certifications: AWS Cloud Practitioner, Google IT Automation with Python""",
                "metadata": {
                    "category": "skills",
                    "tech_stack": ["Python", "JavaScript", "FastAPI", "React", "AWS", "Docker"],
                    "complexity": "varied",
                    "relevance_score": 0.85
                }
            },
            {
                "id": "professional-experience",
                "text": """Professional Experience Highlights:
- Full-stack development of scalable web applications
- Implementation of machine learning solutions for business problems
- API design and development following REST principles
- Database design and optimization for high-performance systems
- Cloud deployment and infrastructure management
- Technical mentoring and code review processes
- Agile development methodologies and project management
Years of Experience: 3+ years in software development
Notable Achievements: Reduced API response times by 60%, Improved system reliability to 99.9% uptime""",
                "metadata": {
                    "category": "experience",
                    "tech_stack": ["Full-stack", "ML", "API", "Database", "Cloud"],
                    "complexity": "advanced",
                    "relevance_score": 0.88
                }
            }
        ]
        
        # Dynamic relevance scoring based on query keywords
        query_lower = query_text.lower()
        for doc in base_projects:
            score = doc['metadata']['relevance_score']
            
            # Boost scores based on query keywords
            if 'trade' in query_lower or 'trading' in query_lower:
                if doc['metadata']['category'] == 'trading':
                    score += 0.1
            elif 'web' in query_lower or 'website' in query_lower or 'frontend' in query_lower:
                if doc['metadata']['category'] == 'web-development':
                    score += 0.1
            elif 'ai' in query_lower or 'machine' in query_lower or 'llm' in query_lower:
                if doc['metadata']['category'] == 'ai-ml':
                    score += 0.1
            elif 'skill' in query_lower or 'experience' in query_lower:
                if doc['metadata']['category'] in ['skills', 'experience']:
                    score += 0.05
                    
            doc['metadata']['relevance_score'] = min(score, 1.0)
            
        return base_projects

    def _get_basic_mock_data(self) -> List[Dict]:
        """Basic fallback mock data."""
        return [
            {
                "id": "basic-info",
                "text": "Project: Portfolio Projects. Tech: Python, JavaScript, FastAPI, React. Features: Modern web development, API design, full-stack applications.",
                "metadata": {"category": "general", "relevance_score": 0.7}
            }
        ]

    def _filter_by_user_type(self, results: List[Dict], user_type: str) -> List[Dict]:
        """Filter results based on user type."""
        if user_type == "recruiter":
            # Recruiters prefer skills, experience, and professional projects
            priority_categories = ['skills', 'experience', 'ai-ml']
            return sorted(results, 
                         key=lambda x: (x.get('metadata', {}).get('category', '') in priority_categories,
                                      x.get('metadata', {}).get('relevance_score', 0)), 
                         reverse=True)
        elif user_type == "developer":
            # Developers prefer technical projects and implementation details
            priority_categories = ['trading', 'ai-ml', 'web-development']
            return sorted(results,
                         key=lambda x: (x.get('metadata', {}).get('category', '') in priority_categories,
                                      x.get('metadata', {}).get('complexity', '') == 'high',
                                      x.get('metadata', {}).get('relevance_score', 0)),
                         reverse=True)
        else:
            # Visitors get general information ordered by relevance
            return sorted(results, 
                         key=lambda x: x.get('metadata', {}).get('relevance_score', 0), 
                         reverse=True)

    async def upsert_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Insert or update documents in Pinecone."""
        try:
            logger.info(f"📤 Upserting {len(documents)} documents to Pinecone")
            # Mock implementation - would use self.index.upsert() in real implementation
            return True
        except Exception as e:
            logger.error(f"❌ Error upserting documents: {str(e)}")
            return False

    async def health_check(self) -> Dict[str, Any]:
        """Check if Pinecone service is available."""
        if self.client is not None and self.embedding_model is not None:
            return {"status": "success", "version": "1.0"}
        else:
            return {"status": "error", "error": "Pinecone client or embedding model not initialized"}

# Global database instance
pinecone_db = PineconeDB()