# 🚀 Deployment Guide

## 📋 Prerequisites

Before deploying, ensure you have:

- **AWS Account** with appropriate permissions
- **Docker** installed locally
- **Terraform** CLI installed
- **GitHub** repository set up
- **Domain name** (optional but recommended)

## 🔧 Local Development Setup

### 1. Environment Configuration

```bash
# Clone the repository
git clone <your-repo-url>
cd akash-ai-portfolio/backend

# Create environment file
cp .env.example .env
# Edit .env with your actual API keys
```

### 2. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using conda
conda env create -f environment.yml
conda activate akash-ai
```

### 3. Run Locally

```bash
# Development mode with auto-reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or using Docker
docker-compose up --build
```

### 4. Verify Installation

```bash
# Check health endpoint
curl http://localhost:8000/api/v1/

# View API documentation
open http://localhost:8000/docs
```

## ☁️ AWS Deployment

### 1. Infrastructure Setup

```bash
# Navigate to infrastructure directory
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

### 2. Manual EC2 Setup (Alternative)

If you prefer manual setup:

```bash
# Launch EC2 instance
# AMI: Amazon Linux 2
# Instance Type: t3.micro
# Security Group: Allow ports 22, 80, 443, 8000

# SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum update -y
sudo yum install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Deploy Application

```bash
# Clone repository on EC2
git clone <your-repo-url>
cd akash-ai-portfolio/backend

# Create environment file
cat > .env << EOF
GROQ_API_KEY=your_actual_key
PINECONE_API_KEY=your_actual_key
PINECONE_INDEX_NAME=your_index_name
APP_ENV=production
DEBUG=False
EOF

# Build and run with Docker
docker build -t akash-ai-backend .
docker run -d \
  --name ai-backend \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  akash-ai-backend
```

## 🐳 Docker Deployment

### Production Docker Setup

```dockerfile
# Multi-stage build for security and size optimization
FROM python:3.11-slim as builder
# ... build steps ...

FROM python:3.11-slim
# ... production setup ...
```

### Docker Compose for Production

```yaml
version: '3.8'
services:
  backend:
    image: akashk/ai-backend:latest
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 🔄 CI/CD Pipeline

### GitHub Actions Configuration

The `.github/workflows/ci-cd.yml` file includes:

1. **Testing Stage**: Runs on multiple Python versions
2. **Building Stage**: Creates Docker images
3. **Deployment Stage**: Deploys to AWS EC2

### Setting Up Secrets

In GitHub repository settings, add these secrets:

```bash
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_TOKEN=your_dockerhub_token
AWS_HOST=your_ec2_hostname
AWS_USERNAME=ec2-user
AWS_PRIVATE_KEY=your_private_key
GROQ_API_KEY=your_groq_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=your_index_name
```

## 🔒 Security Configuration

### SSL/TLS Setup

```bash
# Install Certbot
sudo yum install -y certbot

# Obtain SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure Nginx reverse proxy
sudo yum install -y nginx
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring Setup

### System Monitoring

```bash
# Install monitoring agents
sudo yum install -y amazon-cloudwatch-agent

# Configure CloudWatch
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

### Log Management

```bash
# Set up log rotation
sudo tee /etc/logrotate.d/ai-backend << EOF
/var/log/ai-backend/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Find process using port
lsof -i :8000
# Kill the process
kill -9 <PID>
```

2. **Docker Permission Denied**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

3. **API Key Issues**
```bash
# Verify environment variables
docker exec -it ai-backend env | grep API
```

4. **Database Connection**
```bash
# Test Pinecone connectivity
curl -H "Api-Key: $PINECONE_API_KEY" https://controller.pinecone.io/databases
```

### Health Checks

```bash
# Check application health
curl http://localhost:8000/api/v1/

# Check specific service
curl http://localhost:8000/api/v1/services/groq/health

# Get system stats
curl http://localhost:8000/api/v1/stats
```

## 📈 Performance Tuning

### Memory Optimization
```bash
# Monitor memory usage
docker stats ai-backend

# Adjust Docker memory limits
docker run --memory=1g --memory-swap=2g ...
```

### CPU Optimization
```bash
# Monitor CPU usage
top -p $(pgrep -f "uvicorn")

# Adjust worker count
--workers 4  # In uvicorn command
```

## 🆘 Support

For deployment issues:
1. Check logs: `docker logs ai-backend`
2. Verify environment: `docker exec -it ai-backend env`
3. Test connectivity: `curl localhost:8000/api/v1/`
4. Contact support: akash@example.com

---

*Deployment Guide Version: 2.0.0*
*Last Updated: November 2024*