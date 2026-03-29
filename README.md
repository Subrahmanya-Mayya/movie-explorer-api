# Movie Explorer API

## Run with Docker

**Using Docker Compose**

```bash
docker compose up --build
```

**Using Docker Image**

```bash
docker build -t movie-explorer-api .
```

Linux/macOS:
```bash
docker run -p 8000:8000 -v $(pwd)/app/db:/app/app/db movie-explorer-api
```

Windows:
```powershell
docker run -p 8000:8000 -v ${PWD}/app/db:/app/app/db movie-explorer-api
```

The API will be available at `http://127.0.0.1:8000`.  
Swagger/OpenAPI Spec UI: `http://127.0.0.1:8000/docs`

> The database is created and seeded with sample data automatically on first startup.

---

## Local Development

**Create and activate a virtual environment**

Linux/macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Install dependencies**

```bash
pip install -r requirements-dev.txt
```

## Lint

```bash
ruff check .
```

## Test

```bash
pytest tests/
```

**Start the server**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`
