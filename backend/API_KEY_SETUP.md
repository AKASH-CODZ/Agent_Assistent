# 🔑 API Key Setup Guide

This guide will help you configure API keys securely for the Akash AI Portfolio backend.

## 📋 Prerequisites

- Groq account (https://console.groq.com/)
- Pinecone account (https://app.pinecone.io/)
- Python 3.8+ installed
- Git cloned repository

## 🔐 Security Best Practices

### ⚠️ IMPORTANT: Never Commit API Keys!

1. **The `.env` file is in `.gitignore`** - Never commit it to version control
2. **Use environment variables** - Store sensitive data outside code
3. **Rotate keys regularly** - Update API keys periodically
4. **Use different keys** - Separate keys for development and production

## 📝 Step-by-Step Setup

### Step 1: Copy Environment Template

```bash
cd backend
cp .env.example .env
```

### Step 2: Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up or log in to your account
3. Click "Create API Key"
4. Give it a descriptive name (e.g., "Akash Portfolio Dev")
5. Copy the generated key
6. Paste it in your `.env` file:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### Step 3: Get Pinecone API Key

1. Visit [Pinecone Console](https://app.pinecone.io/)
2. Sign up or log in to your account
3. Go to "API Keys" section
4. Copy your API key (or create a new one)
5. Create an index if you haven't already:
   - Name: `portfolio-index` (or your preferred name)
   - Dimension: Match your embedding model (e.g., 1024 for gte-large)
   - Metric: cosine
6. Update `.env` file:

```env
PINECONE_API_KEY=pcsk_your_actual_api_key_here
PINECONE_INDEX_NAME=your_index_name
```

### Step 4: Configure Application Settings

Update other settings in `.env`:

```env
# Development environment
APP_ENV=development
DEBUG=True

# Local development server
HOST=0.0.0.0
PORT=8000

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

### Step 5: Verify Configuration

Run the status checker:

```bash
python check_status.py
```

Expected output:
```
✅ Groq API - Connectivity: Connected successfully
✅ Pinecone - Index Status: Index 'your_index' exists
✅ All systems operational!
```

## 🔍 Troubleshooting

### Issue: "API Key not found"

**Solution:**
1. Ensure `.env` file exists in the `backend` directory
2. Check that variable names match exactly (case-sensitive)
3. Restart your Python interpreter/server

### Issue: "Invalid API Key"

**Solution:**
1. Verify the key was copied correctly (no extra spaces)
2. Check if the key has expired in the provider's console
3. Regenerate a new key if needed

### Issue: "Index not found"

**Solution:**
1. Log into Pinecone console
2. Verify the index name matches exactly
3. Ensure the index is in the same region as your API endpoint

### Issue: "Connection timeout"

**Solution:**
1. Check your internet connection
2. Some regions may require VPN/proxy
3. Verify firewall settings allow outbound HTTPS

## 🚀 Production Deployment

### Environment Variables in Production

For production deployments, use platform-specific secret management:

#### AWS EC2 / ECS
```bash
# Use AWS Systems Manager Parameter Store or Secrets Manager
aws ssm put-parameter --name "/akash/groq-api-key" --value "gsk_..." --type "SecureString"
```

#### Docker
```bash
# Pass via docker-compose.yml or docker run
docker run -e GROQ_API_KEY=gsk_... -e PINECONE_API_KEY=pcsk_... akash-ai-portfolio
```

#### GitHub Actions
```yaml
# Add to repository secrets
env:
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
  PINECONE_API_KEY: ${{ secrets.PINECONE_API_KEY }}
```

#### Render / Railway / Heroku
```bash
# Set via platform dashboard or CLI
render env set GROQ_API_KEY=gsk_...
```

## 📊 Monitoring & Rotation

### Regular Checks

Run status checks periodically:
```bash
# Daily health check
python check_status.py

# Dependency check
python check_dependencies.py
```

### Key Rotation Schedule

- **Development**: Rotate every 90 days
- **Production**: Rotate every 30 days
- **After team member departure**: Rotate immediately

### Rotation Process

1. Generate new API key in provider console
2. Update `.env` or secret manager
3. Restart application
4. Verify functionality with `check_status.py`
5. Delete old key from provider console

## 🛡️ Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] API keys are not hardcoded in source code
- [ ] Different keys used for dev/staging/production
- [ ] Keys are rotated regularly
- [ ] Access logs are monitored
- [ ] Minimum required permissions granted
- [ ] Backup authentication method available

## 📞 Support

If you encounter issues:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review provider documentation:
   - [Groq Docs](https://console.groq.com/docs)
   - [Pinecone Docs](https://docs.pinecone.io/)
3. Check application logs for detailed error messages
4. Verify network connectivity and firewall settings

## 🔗 Additional Resources

- [FastAPI Environment Variables Guide](https://fastapi.tiangolo.com/tutorial/environmental-variables/)
- [12-Factor App Configuration](https://12factor.net/config)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Last Updated**: March 2026  
**Version**: 2.0.0
