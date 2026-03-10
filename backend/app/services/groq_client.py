from typing import List, Dict, Any
import logging
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)

class GroqClient:
    """Client for interacting with Groq LLM API."""
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.client = None
        
        # Initialize client only if API key is provided
        if self.api_key and self.api_key != "your_groq_api_key_here" and not self.api_key.startswith("your_"):
            try:
                # Simple initialization without any extra parameters
                self.client = Groq(api_key=self.api_key)
                logger.info("✅ Groq client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Groq client: {str(e)}")
                logger.error(f"Error type: {type(e)}")
                self.client = None
        else:
            logger.warning("⚠️ Groq API key not configured properly - using mock mode")
    
    async def generate_response(
        self, 
        query: str, 
        context: List[Dict[str, Any]], 
        user_type: str = "visitor"
    ) -> str:
        """
        Generate a response using Groq LLM.
        
        Args:
            query: User's question
            context: Relevant context documents
            user_type: Type of user (recruiter, developer, visitor)
            
        Returns:
            Generated response string
        """
        try:
            logger.info(f"🤖 Generating response for query: {query}")
            
            # Check if we have real Groq client
            if self.client:
                # Prepare the prompt with context and user type
                prompt = self._prepare_prompt(query, context, user_type)
                
                # Call Groq API
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": self._get_system_prompt(user_type)
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama3-8b-8192",  # Use smaller model for faster responses
                    temperature=0.7,
                    max_tokens=500
                )
                
                generated_text = response.choices[0].message.content
                logger.info("✅ Response generated successfully using Groq")
                return generated_text
            
            # Fall back to mock implementation
            logger.info("⚠️ Using mock response generator")
            return self._generate_mock_response(query, context, user_type)
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {str(e)}")
            return self._generate_fallback_response(query, user_type)

    def _prepare_prompt(self, query: str, context: List[Dict], user_type: str) -> str:
        """Prepare the prompt with context and query."""
        # Extract context text
        context_texts = [doc.get('text', '') for doc in context[:3]]  # Limit to 3 docs
        context_combined = "\n\n".join(context_texts)
        
        prompt = f"""Based on the following context information, please answer the question appropriately:

Context:
{context_combined}

Question: {query}

Please provide a helpful and accurate response based on the context provided."""

        return prompt

    def _get_system_prompt(self, user_type: str) -> str:
        """Get system prompt based on user type."""
        prompts = {
            "recruiter": "You are a professional responding to a recruiter. Focus on skills, experience, and professional achievements. Be concise and highlight relevant qualifications.",
            "developer": "You are a technical professional responding to a fellow developer. Provide detailed technical explanations, code examples when relevant, and discuss implementation approaches.",
            "visitor": "You are a friendly professional providing helpful information to visitors. Be approachable, informative, and engaging while maintaining professionalism."
        }
        return prompts.get(user_type, prompts["visitor"])

    def _generate_mock_response(self, query: str, context: List[Dict], user_type: str) -> str:
        """Generate mock response when Groq is not available."""
        # Simple mock responses based on query content
        query_lower = query.lower()
        
        if "trade" in query_lower or "trading" in query_lower:
            return """Trade-Mirror is an advanced algorithmic trading platform I developed that integrates with Zerodha and Shoonya APIs for real-time market analysis. Key features include:

• Real-time market data streaming and analysis
• Automated trading strategy execution  
• SHA-256 data integrity verification
• Risk management with stop-loss mechanisms
• Performance analytics dashboard
• RESTful API for external integrations

The platform is built with Python, FastAPI, and WebSocket technology for low-latency trading operations."""
        
        elif "portfolio" in query_lower or "website" in query_lower:
            return """My portfolio website is a modern, responsive web application built with cutting-edge technologies:

• Next.js 14 with React 18 for optimal performance
• TypeScript for type safety and better developer experience
• Tailwind CSS for responsive design system
• Framer Motion for smooth animations
• Dark/light theme toggle
• Optimized for performance (Lighthouse scores >95)
• Deployed on Vercel with CI/CD pipeline

The site showcases my projects, skills, and professional experience in an engaging, interactive format."""
        
        elif "skill" in query_lower or "experience" in query_lower:
            return """I'm a full-stack developer with expertise in modern web technologies and machine learning:

**Technical Skills:**
• Programming: Python (Expert), JavaScript/TypeScript (Advanced), SQL
• Frameworks: FastAPI, Django, React, Next.js, Node.js
• Databases: PostgreSQL, MongoDB, Redis, SQLite
• Cloud & DevOps: AWS, Docker, Git, CI/CD pipelines
• ML/AI: Machine Learning implementation, LLM integration

**Professional Experience:**
• 3+ years in software development
• Full-stack application development
• API design and implementation
• Cloud deployment and infrastructure
• Technical mentoring and code reviews

I specialize in building scalable, high-performance applications with clean, maintainable code."""
        
        else:
            return f"""Thank you for your question about "{query}". I'm Akash, a skilled full-stack developer with expertise in modern web technologies and artificial intelligence.

I'd be happy to provide more specific information about my projects, skills, or experience. Feel free to ask about:
• My trading platform (Trade-Mirror)
• Portfolio website and frontend technologies  
• Technical skills and professional experience
• Any specific project or technology you're interested in

What would you like to know more about?"""

    def _generate_fallback_response(self, query: str, user_type: str) -> str:
        """Generate fallback response for error cases."""
        return f"I apologize, but I'm having trouble processing your request about '{query}' right now. Please try rephrasing your question or ask about my projects, skills, or experience."

    async def health_check(self) -> Dict[str, Any]:
        """Check if Groq service is available."""
        if self.client is not None:
            return {"status": "success", "version": "1.0"}
        else:
            return {"status": "error", "error": "Groq client not initialized"}

# Global client instance
groq_client = GroqClient()