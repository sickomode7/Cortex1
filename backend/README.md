# Backend Setup

This backend uses:

- `FastAPI` for the API
- `SQLAlchemy` for ORM models
- `Alembic` for schema migrations
- `Supabase Postgres` as the recommended hosted database

## Environment

Copy the example environment file:

```bash
cd backend
cp .env.example .env
```

Then fill in these values from your Supabase project's `Connect` panel:

- `DATABASE_URL`
  - Recommended for backend runtime traffic
  - Use the `Session pooler` connection string on port `5432`
- `MIGRATION_DATABASE_URL`
  - Recommended for Alembic migrations
  - Use the `Direct connection` string on port `5432`

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres?sslmode=require
MIGRATION_DATABASE_URL=postgresql+psycopg2://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres?sslmode=require
```

## Why two URLs?

Supabase recommends different connection types for different jobs:

- `Direct connection` is best for migrations and admin tools
- `Session pooler` is a better fit for backend app traffic on IPv4-only networks

This project uses:

- `DATABASE_URL` for the application engine
- `MIGRATION_DATABASE_URL` for Alembic

If you only have one working URL, you can omit `MIGRATION_DATABASE_URL` and Alembic will fall back to `DATABASE_URL`.

## Install dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

## Generate the first migration

After your `.env` is configured:

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "create initial cortex schema"
```

## Apply migrations

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## Seed the Python MVP domain

Once the schema is migrated, seed the initial Python concept graph and starter assessment bank:

```bash
cd backend
source venv/bin/activate
python -m app.scripts.seed_python_domain
```

If you want to preview the configured counts without touching the database:

```bash
cd backend
source venv/bin/activate
python -m app.scripts.seed_python_domain --dry-run
```

## Run the API

```bash
cd backend
source venv/bin/activate
fastapi dev main.py
```

## Supabase project creation

Create the Supabase project in the dashboard, then copy the connection details from `Connect`.

Useful references:

- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/docs/guides/deployment/database-migrations
