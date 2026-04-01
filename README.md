# million-miles-testovoe

## Architecture

```
/backend   FastAPI + SQLAlchemy + Alembic
/parser    Playwright scraper + APScheduler
/frontend  Next.js (TS) + Tailwind
```

## Backend

### Dev (SQLite)

- Copy `backend/.env.example` -> `backend/.env`
- Create venv and install:

```bash
pip install -r backend/requirements.txt
```

- Run миграции:

```bash
cd backend
alembic upgrade head
```

- Start:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Production (PostgreSQL via Docker)

```bash
docker compose up --build
```

Backend будет доступен на `http://localhost:8000`.

## Parser

- Copy `parser/.env.example` -> `parser/.env`
- Install:

```bash
pip install -r parser/requirements.txt
playwright install chromium
```

- One-shot запуск:

```bash
python parser/main.py --once
```

- Scheduler (daily):

```bash
python parser/main.py
```

## Frontend

- Copy `frontend/.env.example` -> `frontend/.env`
- Install + run:

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

Frontend: `http://localhost:3000`.