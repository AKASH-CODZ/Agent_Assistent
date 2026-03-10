# Makefile for Akash AI Portfolio Backend
# Streamlined development and deployment operations

# Variables
PROJECT_NAME = akash-ai-backend
DOCKER_IMAGE = akashk/ai-backend
DOCKER_TAG = latest
BACKEND_DIR = backend
PYTHON = python3
PIP = pip3

# Help target
.PHONY: help
help: ## Show this help message
	@echo "🚀 Akash AI Portfolio - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

# Development targets
.PHONY: install
install: ## Install Python dependencies
	@echo "📦 Installing dependencies..."
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt

.PHONY: dev
dev: ## Start development server
	@echo "🚀 Starting development server..."
	cd $(BACKEND_DIR) && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: check-status
check-status: ## Check API status and credentials
	@echo "🔍 Checking API status..."
	cd $(BACKEND_DIR) && $(PYTHON) check_status.py

.PHONY: check-deps
check-deps: ## Check Python dependencies
	@echo "📦 Checking dependencies..."
	cd $(BACKEND_DIR) && $(PYTHON) check_dependencies.py

.PHONY: test
test: ## Run comprehensive test suite
	@echo "🧪 Running comprehensive test suite..."
	cd $(BACKEND_DIR) && $(PYTHON) app/test_api.py

.PHONY: test-api
test-api: ## Run API integration tests
	@echo "🧪 Running API integration tests..."
	cd $(BACKEND_DIR) && pytest tests/ -v --tb=short

.PHONY: test-cov
test-cov: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	cd $(BACKEND_DIR) && pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

.PHONY: lint
lint: ## Run code linting
	@echo "🧹 Running linting..."
	cd $(BACKEND_DIR) && flake8 app/ && black --check app/

.PHONY: format
format: ## Format code
	@echo "✏️  Formatting code..."
	cd $(BACKEND_DIR) && black app/

# Docker targets
.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	cd $(BACKEND_DIR) && docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

.PHONY: docker-run
docker-run: ## Run Docker container
	@echo "🐳 Running Docker container..."
	cd $(BACKEND_DIR) && docker run -d \
		--name $(PROJECT_NAME) \
		--env-file .env \
		-p 8000:8000 \
		$(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: docker-dev
docker-dev: ## Run Docker in development mode
	@echo "🐳 Running Docker in development mode..."
	cd $(BACKEND_DIR) && docker-compose up --build

.PHONY: docker-stop
docker-stop: ## Stop Docker container
	@echo "⏹️  Stopping Docker container..."
	docker stop $(PROJECT_NAME) 2>/dev/null || true
	docker rm $(PROJECT_NAME) 2>/dev/null || true

.PHONY: docker-clean
docker-clean: ## Clean Docker images and containers
	@echo "🧹 Cleaning Docker resources..."
	docker system prune -f
	docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG) 2>/dev/null || true

# Infrastructure targets
.PHONY: infra-init
infra-init: ## Initialize Terraform infrastructure
	@echo "🏗️  Initializing Terraform..."
	cd infrastructure/terraform && terraform init

.PHONY: infra-plan
infra-plan: ## Plan Terraform changes
	@echo "📋 Planning infrastructure changes..."
	cd infrastructure/terraform && terraform plan

.PHONY: infra-apply
infra-apply: ## Apply Terraform configuration
	@echo "⚡ Applying infrastructure changes..."
	cd infrastructure/terraform && terraform apply -auto-approve

.PHONY: infra-destroy
infra-destroy: ## Destroy Terraform infrastructure
	@echo "💣 Destroying infrastructure..."
	cd infrastructure/terraform && terraform destroy -auto-approve

# Utility targets
.PHONY: clean
clean: ## Clean temporary files
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	rm -rf backend/htmlcov/ backend/.coverage

.PHONY: setup
setup: ## Initial project setup
	@echo "⚙️  Setting up project..."
	make install
	make check-status
	@echo "✅ Setup complete!"

.PHONY: deploy
deploy: ## Deploy to production
	@echo "🚀 Deploying to production..."
	make docker-build
	make docker-stop
	make docker-run
	@echo "✅ Deployment complete!"

.PHONY: health
health: ## Check application health
	@echo "🏥 Checking application health..."
	curl -s http://localhost:8000/api/v1/ | jq '.' || echo "Application not responding"

.PHONY: logs
logs: ## View application logs
	@echo "📋 Viewing application logs..."
	docker logs -f $(PROJECT_NAME) 2>/dev/null || tail -f backend/app/logs/*.log 2>/dev/null || echo "No logs found"

# Default target
.DEFAULT_GOAL := help