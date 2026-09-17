# Agent Assistant

A RAG-based portfolio assistant: a FastAPI backend that answers questions about my work
using Groq for generation and Pinecone for retrieval, with Terraform infrastructure
definitions for deployment.

## Stack

FastAPI, Groq (LLM), Pinecone (vector search), Docker, Terraform.

## Layout

| Path | What's there |
|---|---|
| `backend/app/api/` | routes |
| `backend/app/core/` | config, security middleware |
| `backend/app/models/` | request/response models (chat, health) |
| `backend/app/services/` | `groq_client.py`, `pinecone_db.py` |
| `infrastructure/terraform/` | infra as code |
| `docs/architecture.md`, `docs/deployment.md` | design notes |

## Run it

```bash
cp backend/.env.example backend/.env    # fill in API keys
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload
```

Or with Docker:

```bash
cd backend && docker-compose up
```

## License

MIT — see `LICENSE`.
