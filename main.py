import os
import inspect
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# ============================================================================
# SCHEMA ENDPOINT (Only endpoint needed for database viewer)
# ============================================================================

@app.get("/schema")
async def get_schemas():
    """
    Expose all Pydantic schemas as JSON Schema for validation.
    This is the ONLY endpoint your backend needs for the database viewer.
    All database operations are handled by the Flames platform.
    """
    try:
        import schemas
        schemas_dict = {}
        
        # Get all Pydantic models from schemas module
        for name, obj in inspect.getmembers(schemas):
            # Check if it's a Pydantic model
            if (inspect.isclass(obj) and 
                issubclass(obj, BaseModel) and 
                obj is not BaseModel and
                not name.startswith("_")):
                try:
                    # Convert to collection name (lowercase)
                    collection_name = name.lower()
                    # Get JSON schema for validation
                    schemas_dict[collection_name] = obj.model_json_schema()
                except Exception as e:
                    print(f"Error processing schema {name}: {e}")
        
        return schemas_dict
    except ImportError:
        raise HTTPException(status_code=400, detail="Schemas module not found. Define schemas in schemas.py")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading schemas: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
