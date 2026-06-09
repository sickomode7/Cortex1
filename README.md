# Cortex - Personalized Learning Intelligence System

Cortex is an AI-powered platform that generates and adapts personalized curricula based on a learner's knowledge, goals, preferences, and performance.

## Project Structure

This is a monorepo setup containing:

- **frontend/**: Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui.
- **backend/**: FastAPI (Python), SQLAlchemy ORM.

## Setup Instructions

### 1. Database

We are using a hosted **PostgreSQL** database (via Supabase).

- Create a Supabase project.
- Retrieve the connection string.
- You will place this connection string in your `.env` files later.

### 2. Frontend Setup (Next.js)

```bash
cd frontend
npm install
# Add your Clerk API keys to frontend/.env.local (You'll need to create a Clerk app)
npm run dev
```

### 3. Backend Setup (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Add your Supabase Database URL to backend/.env
fastapi dev main.py # or uvicorn main:app --reload
```
