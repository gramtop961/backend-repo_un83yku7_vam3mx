"""
Database Helper Functions (OPTIONAL)

These functions are provided for your own application logic if you need
to perform database operations in your backend code. However, they are 
NOT required for the Flames database viewer.

For the database viewer, you only need:
1. Define schemas in schemas.py
2. Expose GET /schema endpoint (already done in main.py)
3. That's it! Flames handles all database operations.

If you want to use these helper functions in your own API endpoints,
uncomment the code below and add 'pymongo==4.6.0' back to requirements.txt
"""

# Uncomment below if you want to use database operations in your own code:

# from pymongo import MongoClient
# from datetime import datetime, timezone
# import os
# from dotenv import load_dotenv
# from typing import Union
# from pydantic import BaseModel
# 
# # Load environment variables from .env file
# load_dotenv()
# 
# _client = None
# db = None
# 
# database_url = os.getenv("DATABASE_URL")
# database_name = os.getenv("DATABASE_NAME")
# 
# if database_url and database_name:
#     _client = MongoClient(database_url)
#     db = _client[database_name]
# 
# # Helper functions for common database operations
# def create_document(collection_name: str, data: Union[BaseModel, dict]):
#     """Insert a single document with timestamp"""
#     if db is None:
#         raise Exception("Database not available. Check DATABASE_URL and DATABASE_NAME environment variables.")
# 
#     # Convert Pydantic model to dict if needed
#     if isinstance(data, BaseModel):
#         data_dict = data.model_dump()
#     else:
#         data_dict = data.copy()
# 
#     data_dict['created_at'] = datetime.now(timezone.utc)
#     data_dict['updated_at'] = datetime.now(timezone.utc)
# 
#     result = db[collection_name].insert_one(data_dict)
#     return str(result.inserted_id)
# 
# def get_documents(collection_name: str, filter_dict: dict = None, limit: int = None):
#     """Get documents from collection"""
#     if db is None:
#         raise Exception("Database not available. Check DATABASE_URL and DATABASE_NAME environment variables.")
#     
#     cursor = db[collection_name].find(filter_dict or {})
#     if limit:
#         cursor = cursor.limit(limit)
#     
#     return list(cursor)
# 
# # ... other functions
