# Movie Explorer API

## Run with Docker

```bash
docker compose up --build
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

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

**Start the server**

```bash
uvicorn app.main:app --reload
```

---

## Lint

```bash
ruff check .
```

---

## Test

```bash
pytest
```
