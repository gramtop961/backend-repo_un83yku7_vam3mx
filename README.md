# Backend API

A simple FastAPI backend with CORS enabled.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure port (optional):
   - Port is configured in `.env` file
   - Default: `PORT=8000`

3. Run the server:
```bash
python main.py
```
   Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` - Root endpoint
- `GET /api/hello` - Hello API endpoint
- `GET /schema` - **Database viewer schema endpoint** (see below)

## Database Viewer Integration

To use the Flames database viewer, your backend only needs to expose **one endpoint**:

### `GET /schema`

Returns JSON schemas for all your collections to enable validation in the database viewer.

**Example Response:**
```json
{
  "users": {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "email": { "type": "string", "format": "email" },
      "age": { "type": "integer", "minimum": 0 }
    },
    "required": ["name", "email"]
  },
  "products": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "price": { "type": "number", "minimum": 0 },
      "category": { "type": "string" }
    },
    "required": ["title", "price"]
  }
}
```

**Setup:**
1. Define your data models in `schemas.py` using Pydantic
2. The `/schema` endpoint automatically converts them to JSON Schema
3. That's it! The Flames platform handles all database operations directly

**Important:** All database operations (create, read, update, delete) are performed directly by the Flames platform. Your backend only provides validation schemas.
