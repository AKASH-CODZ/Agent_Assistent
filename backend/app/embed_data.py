"""
Data Pipeline Script for Akash AI Assistant Backend.

This script converts portfolio data into vector embeddings and uploads them to Pinecone.
It handles the transformation of structured data into searchable vector representations
that can be used for semantic search in the RAG system.
"""

import json
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import pinecone
from pinecone import Pinecone, ServerlessSpec
import uuid
from core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortfolioEmbedder:
    """Handles conversion of portfolio data to vector embeddings."""
    
    def __init__(self):
        """Initialize the embedder with sentence transformer model."""
        try:
            # Use a model that generates 1024-dimensional embeddings to match Pinecone index
            self.model = SentenceTransformer('thenlper/gte-large')  # 1024 dimensions
            logger.info("✅ SentenceTransformer model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {str(e)}")
            raise
    
    def load_portfolio_data(self, file_path: str = "portfolio_data.json") -> List[Dict[str, Any]]:
        """Load portfolio data from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"✅ Loaded {len(data)} portfolio items from {file_path}")
            return data
        except FileNotFoundError:
            logger.warning(f"⚠️ Portfolio data file {file_path} not found, using sample data")
            return self._get_sample_portfolio_data()
        except Exception as e:
            logger.error(f"❌ Error loading portfolio data: {str(e)}")
            return []
    
    def _get_sample_portfolio_data(self) -> List[Dict[str, Any]]:
        """Generate sample portfolio data when JSON file is not available."""
        return [
            {
                "id": "trade-mirror-project",
                "title": "Trade-Mirror Algorithmic Trading Platform",
                "description": "A sophisticated algorithmic trading platform that integrates with Zerodha and Shoonya APIs for real-time market analysis and automated trading execution.",
                "technologies": ["Python", "FastAPI", "WebSocket", "PostgreSQL", "Redis", "Zerodha API", "Shoonya API"],
                "features": ["Real-time market data streaming", "Automated trading strategies", "SHA-256 data integrity", "Risk management", "Performance analytics"],
                "category": "trading",
                "complexity": "high"
            },
            {
                "id": "portfolio-website",
                "title": "Personal Portfolio Website",
                "description": "Modern responsive portfolio website built with Next.js featuring smooth animations, dark/light themes, and optimized performance.",
                "technologies": ["Next.js", "React", "TypeScript", "Tailwind CSS", "Framer Motion", "Vercel"],
                "features": ["Responsive design", "Dark/light theme", "Smooth animations", "SEO optimized", "Performance focused"],
                "category": "web-development",
                "complexity": "medium"
            },
            {
                "id": "ai-assistant-backend",
                "title": "AI Assistant Backend API",
                "description": "Production-grade FastAPI backend implementing Retrieval Augmented Generation (RAG) with Pinecone vector database and Groq LLM integration.",
                "technologies": ["FastAPI", "Python", "Pinecone", "Groq API", "Docker", "Microservices"],
                "features": ["RAG implementation", "Semantic search", "Role-based responses", "Scalable architecture", "Comprehensive logging"],
                "category": "ai-ml",
                "complexity": "high"
            },
            {
                "id": "technical-skills",
                "title": "Technical Skills Overview",
                "description": "Comprehensive skill set covering full-stack development, machine learning, cloud infrastructure, and modern development practices.",
                "technologies": ["Python", "JavaScript/TypeScript", "FastAPI", "React", "AWS", "Docker", "Git"],
                "skills": ["Full-stack development", "Machine Learning", "Cloud Infrastructure", "API Design", "DevOps"],
                "certifications": ["AWS Cloud Practitioner", "Google IT Automation with Python"],
                "category": "skills",
                "complexity": "varied"
            }
        ]
    
    def create_embeddings(self, portfolio_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert portfolio data into embeddings with metadata."""
        embedded_data = []
        
        for item in portfolio_data:
            try:
                # Create comprehensive text representation
                text_parts = []
                
                if 'title' in item:
                    text_parts.append(f"Project: {item['title']}")
                
                if 'description' in item:
                    text_parts.append(f"Description: {item['description']}")
                
                if 'technologies' in item and item['technologies']:
                    tech_str = ", ".join(item['technologies'])
                    text_parts.append(f"Technologies: {tech_str}")
                
                if 'features' in item and item['features']:
                    features_str = "; ".join(item['features'])
                    text_parts.append(f"Features: {features_str}")
                
                if 'skills' in item and item['skills']:
                    skills_str = ", ".join(item['skills'])
                    text_parts.append(f"Skills: {skills_str}")
                
                # Combine all parts into a single text for embedding
                combined_text = " | ".join(text_parts)
                
                # Generate embedding
                embedding = self.model.encode(combined_text).tolist()
                
                # Create Pinecone-compatible record
                record = {
                    'id': str(uuid.uuid4()),
                    'values': embedding,
                    'metadata': {
                        'original_id': item.get('id', ''),
                        'title': item.get('title', ''),
                        'category': item.get('category', 'general'),
                        'complexity': item.get('complexity', 'medium'),
                        'technologies': item.get('technologies', []),
                        'text': combined_text,
                        'source': 'portfolio'
                    }
                }
                
                embedded_data.append(record)
                logger.info(f"✅ Created embedding for: {item.get('title', 'Unknown')}")
                
            except Exception as e:
                logger.error(f"❌ Error creating embedding for item {item.get('id', 'unknown')}: {str(e)}")
                continue
        
        logger.info(f"✅ Created embeddings for {len(embedded_data)} portfolio items")
        return embedded_data

class PineconeUploader:
    """Handles uploading embeddings to Pinecone vector database."""
    
    def __init__(self):
        """Initialize Pinecone client."""
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index_name = settings.PINECONE_INDEX_NAME
            logger.info("✅ Pinecone client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Pinecone: {str(e)}")
            raise
    
    def create_or_get_index(self, dimension: int = 1024):
        """Create Pinecone index if it doesn't exist."""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes().names()
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=dimension,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"✅ Index {self.index_name} created successfully")
            else:
                logger.info(f"✅ Using existing index: {self.index_name}")
            
            return self.pc.Index(self.index_name)
            
        except Exception as e:
            logger.error(f"❌ Error managing Pinecone index: {str(e)}")
            raise
    
    def upload_embeddings(self, embeddings: List[Dict[str, Any]], batch_size: int = 100):
        """Upload embeddings to Pinecone in batches."""
        try:
            # Get or create index
            index = self.create_or_get_index(dimension=len(embeddings[0]['values']))
            
            # Upload in batches
            total_uploaded = 0
            for i in range(0, len(embeddings), batch_size):
                batch = embeddings[i:i + batch_size]
                index.upsert(vectors=batch)
                total_uploaded += len(batch)
                logger.info(f"📤 Uploaded batch {i//batch_size + 1}: {len(batch)} records")
            
            logger.info(f"✅ Successfully uploaded {total_uploaded} embeddings to Pinecone")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error uploading to Pinecone: {str(e)}")
            return False

def main():
    """Main execution function."""
    logger.info("🚀 Starting portfolio data embedding pipeline...")
    
    try:
        # Initialize components
        embedder = PortfolioEmbedder()
        uploader = PineconeUploader()
        
        # Load portfolio data
        portfolio_data = embedder.load_portfolio_data()
        
        if not portfolio_data:
            logger.error("❌ No portfolio data available to process")
            return False
        
        # Create embeddings
        embeddings = embedder.create_embeddings(portfolio_data)
        
        if not embeddings:
            logger.error("❌ Failed to create embeddings")
            return False
        
        # Upload to Pinecone
        success = uploader.upload_embeddings(embeddings)
        
        if success:
            logger.info("🎉 Data pipeline completed successfully!")
            logger.info(f"📊 Processed {len(portfolio_data)} portfolio items")
            logger.info(f"📊 Created {len(embeddings)} vector embeddings")
            logger.info(f"📊 Uploaded to Pinecone index: {uploader.index_name}")
            return True
        else:
            logger.error("❌ Failed to upload embeddings to Pinecone")
            return False
            
    except Exception as e:
        logger.error(f"❌ Pipeline execution failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)