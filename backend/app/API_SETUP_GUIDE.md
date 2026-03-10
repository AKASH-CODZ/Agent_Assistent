# API Setup Guide - Enabling Real LLM Capabilities

## 🚀 Getting Real API Keys

### 1. Groq API Setup

1. **Sign up for Groq**:
   - Visit [console.groq.com](https://console.groq.com)
   - Create a free account
   - Navigate to API Keys section
   - Generate a new API key

2. **Update your .env file**:
   ```bash
   # Replace the placeholder with your actual Groq API key
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

### 2. Pinecone API Setup

1. **Sign up for Pinecone**:
   - Visit [pinecone.io](https://pinecone.io)
   - Create a free account
   - Create a new Index (name it something like "akash-portfolio")
   - Get your API key and index name

2. **Update your .env file**:
   ```bash
   # Replace placeholders with your actual Pinecone credentials
   PINECONE_API_KEY=your_actual_pinecone_api_key_here
   PINECONE_INDEX_NAME=your_index_name_here
   ```

## 🧪 Testing Real LLM Capabilities

Once you've added your API keys, restart the server and run the comprehensive test:

```bash
# Restart the server with new configuration
cd akash-ai-backend
uvicorn main:app --reload

# Run the LLM capabilities test
python test_llm_capabilities.py
```

## 📊 Expected Improvements with Real APIs

### With Real Groq LLM:
- **Natural Language Responses**: Instead of templated replies, you'll get fluent, conversational responses
- **Contextual Understanding**: Better comprehension of complex queries
- **Personalized Tone**: More nuanced responses based on user type
- **Dynamic Content**: Responses that adapt to the specific context provided

### With Real Pinecone:
- **Semantic Search**: Actually finding relevant content based on meaning, not just keywords
- **Better Context Matching**: More accurate document retrieval
- **Scalable Storage**: Ability to handle large amounts of portfolio data
- **Real-time Updates**: Dynamic content management

## 🔍 Sample Test Queries to Try

Once configured, test these queries:

### For Developers:
```
"Explain the RAG implementation in your AI assistant"
"How did you handle the vector database integration?"
"What challenges did you face with the FastAPI architecture?"
```

### For Recruiters:
```
"What's your experience with cloud deployment?"
"Tell me about your full-stack development background"
"How do you approach technical problem-solving?"
```

### For Visitors:
```
"Can you walk me through your portfolio projects?"
"What technologies are you most excited about?"
"How did you learn software development?"
```

## 🛠️ Troubleshooting

### Common Issues:

1. **"Groq API key not configured"**:
   - Double-check your .env file
   - Ensure no extra spaces or quotes around the key
   - Restart the server after updating

2. **"Pinecone connection failed"**:
   - Verify your index name matches exactly
   - Check that your API key has proper permissions
   - Ensure the index is active in your Pinecone dashboard

3. **Rate Limiting**:
   - Free tiers have request limits
   - Monitor your usage in the respective dashboards
   - Consider upgrading for production use

## 💡 Pro Tips

- **Start with free tiers** to test functionality
- **Monitor costs** as you scale usage
- **Keep API keys secure** - never commit them to version control
- **Test incrementally** - verify each service works before combining them

The system is designed to gracefully fall back to mock mode when APIs aren't configured, so you can develop and test even without real keys!