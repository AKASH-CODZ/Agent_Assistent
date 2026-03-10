# 🧪 Testing & API Integration Guide

Complete guide for testing the Akash AI Backend and integrating API keys securely.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Testing Framework](#testing-framework)
- [API Key Integration](#api-key-integration)
- [Dependency Management](#dependency-management)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Navigate to backend directory
cd backend

# Copy environment template
cp .env.example .env

# Install dependencies
make install
# or: pip install -r requirements.txt

# Check dependencies
make check-deps
```

### 2. Configure API Keys

Edit `.env` file with your actual API keys:

```env
GROQ_API_KEY=gsk_your_actual_key_here
PINECONE_API_KEY=pcsk_your_actual_key_here
PINECONE_INDEX_NAME=your_index_name
```

📖 **Detailed setup**: See [API_KEY_SETUP.md](./API_KEY_SETUP.md)

### 3. Verify Configuration

```bash
# Check system status
make check-status

# Run tests
make test
```

## 🔬 Testing Framework

### Test Suite Overview

The project includes a comprehensive test suite that validates:

- ✅ Health check endpoints
- ✅ API responsiveness
- ✅ Chat functionality with different user types
- ✅ Input validation
- ✅ Response times
- ✅ Error handling

### Running Tests

#### Full Test Suite

```bash
make test
```

This runs `app/test_api.py` which tests:
- Root health check
- API v1 health endpoint
- Chat endpoint with multiple user personas
- Validation error handling
- Response time benchmarks

#### Integration Tests

```bash
make test-api
```

Runs pytest-based integration tests in `tests/` directory.

#### Test with Coverage

```bash
make test-cov
```

Generates HTML coverage report in `htmlcov/` directory.

### Test Categories

#### 1. Health Checks
```python
# Basic connectivity tests
test_health_check()      # Root endpoint
test_api_health()        # API v1 endpoint
test_response_time()     # Performance benchmark
```

#### 2. Functionality Tests
```python
# Chat endpoint tests with different personas
test_chat_endpoint("Tell me about projects", "visitor")
test_chat_endpoint("What technologies?", "recruiter")
test_chat_endpoint("Show code examples", "developer")
```

#### 3. Validation Tests
```python
# Error handling tests
test_validation_error()  # Invalid input rejection
```

### Expected Output

```
🧪 Running Akash AI Backend Test Suite
============================================================

1️⃣  Health Checks...
✅ PASS - Root Health Check: Server running (v1.0.0)
✅ PASS - API v1 Health Check: API endpoint responsive
✅ PASS - Response Time: 150ms (acceptable)

2️⃣  Chat Functionality Tests...
✅ PASS - Chat (visitor): Reply received (245 chars), Context: 3 items
✅ PASS - Chat (recruiter): Reply received (312 chars), Context: 5 items
✅ PASS - Chat (developer): Reply received (198 chars), Context: 4 items

3️⃣  Validation Tests...
✅ PASS - Validation Error Handling: Properly rejects invalid input

============================================================
📊 Test Summary
============================================================
Total: 7 tests | ✅ Passed: 7 | ❌ Failed: 0
Success Rate: 100.0%

🎉 All tests passed!
============================================================
```

## 🔑 API Key Integration

### Supported Services

#### Groq (LLM Provider)
- **Purpose**: LLM inference for chat responses
- **Models**: Llama, Mixtral, Gemma
- **Get Key**: https://console.groq.com/keys
- **Docs**: https://console.groq.com/docs

#### Pinecone (Vector Database)
- **Purpose**: Semantic search and RAG
- **Features**: Similarity search, metadata filtering
- **Get Key**: https://app.pinecone.io/
- **Docs**: https://docs.pinecone.io/

### Secure Key Management

#### Development (.env file)

```bash
# Create .env file (already in .gitignore)
cd backend
cp .env.example .env

# Edit with your keys
nano .env
# or
code .env
```

#### Production (Environment Variables)

**Docker:**
```bash
docker run -e GROQ_API_KEY=gsk_... \
           -e PINECONE_API_KEY=pcsk_... \
           akashk/ai-backend:latest
```

**AWS EC2:**
```bash
# Export before starting server
export GROQ_API_KEY="gsk_..."
export PINECONE_API_KEY="pcsk_..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**GitHub Actions:**
```yaml
env:
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
  PINECONE_API_KEY: ${{ secrets.PINECONE_API_KEY }}
```

### Verification Steps

After configuring keys:

1. **Check Status**
   ```bash
   make check-status
   ```

2. **Expected Success Output**
   ```
   🔍 Akash AI Backend - System Status Report
   ======================================================================
   
   Groq API:
   ----------------------------------------------------------------------
     ✅ SUCCESS Connectivity: Connected successfully. Models: llama2-70b-4096, mixtral-8x7b-32768
   
   Pinecone:
   ----------------------------------------------------------------------
     ✅ EXISTS Index Status: Index 'portfolio-index' exists
     ℹ️  INFO Available Indexes: 2 indexes: portfolio-index, test-index
   
   Environment:
   ----------------------------------------------------------------------
     ℹ️  INFO APP_ENV: development
     ℹ️  INFO DEBUG: True
   
   Dependencies:
   ----------------------------------------------------------------------
     ✅ INSTALLED fastapi
     ✅ INSTALLED groq
     ✅ INSTALLED pinecone
     ✅ INSTALLED httpx
   
   ======================================================================
   Summary: ✅ 10 OK | ⚠️  0 Warnings | ❌ 0 Errors
   ======================================================================
   
   🎉 All systems operational!
   ```

## 📦 Dependency Management

### Checking Dependencies

```bash
# Check all required packages
make check-deps
```

This verifies:
- ✅ FastAPI framework
- ✅ Groq client
- ✅ Pinecone client
- ✅ HTTPX (async HTTP)
- ✅ Pydantic (validation)
- ✅ Other critical packages

### Installing Dependencies

```bash
# Install from requirements.txt
make install

# Or manually
pip install -r backend/requirements.txt
```

### Updating Dependencies

```bash
# Update specific package
pip install --upgrade groq

# Update all packages
pip install --upgrade -r backend/requirements.txt
```

### Dependency Versions

Current stable versions (as of March 2026):

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
groq==0.5.0
pinecone==3.0.0
sentence-transformers==2.2.2
torch==2.1.0
transformers==4.35.0
python-dotenv==1.0.0
pydantic==2.5.0
pytest==7.4.3
httpx==0.25.1
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'xxx'"

**Solution:**
```bash
# Reinstall dependencies
make install

# Verify installation
make check-deps
```

#### 2. "Could not connect to the API"

**Causes:**
- Server not running
- Wrong port
- Firewall blocking

**Solution:**
```bash
# Start server in another terminal
make dev

# Or run directly
cd backend
uvicorn app.main:app --reload

# Test connection
curl http://localhost:8000/
```

#### 3. "Invalid API Key"

**Solution:**
1. Check key is copied correctly (no extra spaces)
2. Verify key is active in provider dashboard
3. Regenerate if necessary
4. Restart server after updating `.env`

#### 4. "Index not found" (Pinecone)

**Solution:**
```bash
# Check index name in .env matches exactly
# Create index in Pinecone console if needed
# Verify region matches API endpoint
```

#### 5. Tests failing with connection errors

**Solution:**
```bash
# Ensure server is running on port 8000
lsof -i :8000

# If occupied, kill process or use different port
kill -9 <PID>

# Or start on different port
uvicorn app.main:app --port 8001
```

### Debug Mode

Enable detailed logging:

```env
# In .env
DEBUG=True
LOG_LEVEL=DEBUG
```

Then restart server and check logs:

```bash
make logs
```

### Getting Help

If issues persist:

1. Check logs for detailed error messages
2. Review [API_KEY_SETUP.md](./API_KEY_SETUP.md)
3. Consult provider documentation:
   - [Groq Docs](https://console.groq.com/docs)
   - [Pinecone Docs](https://docs.pinecone.io/)
4. Check network/firewall settings

## 📊 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Check dependencies
      run: |
        cd backend
        python check_dependencies.py
    
    - name: Run tests
      run: |
        cd backend
        uvicorn app.main:app &
        sleep 5
        python app/test_api.py
      env:
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        PINECONE_API_KEY: ${{ secrets.PINECONE_API_KEY }}
```

## 📈 Best Practices

### Testing Workflow

1. **Before coding**: Run existing tests
2. **After changes**: Run full test suite
3. **Before commit**: Check dependencies
4. **Before deploy**: Run integration tests

### API Key Security

- ✅ Use environment variables
- ✅ Never commit `.env` to git
- ✅ Rotate keys regularly (90 days)
- ✅ Use different keys per environment
- ✅ Monitor usage and set alerts

### Dependency Management

- ✅ Pin exact versions in requirements.txt
- ✅ Regularly update dependencies
- ✅ Test after updates
- ✅ Use virtual environments

---

**Last Updated**: March 2026  
**Version**: 2.0.0
