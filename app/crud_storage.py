import os
import httpx
from app.db import supabase
from app.config import STORAGE_BUCKET, SUPABASE_URL
from app.crud_database import create_file_metadata

def upload_file(file_name: str, file_bytes: bytes, content_type: str):
    """
    Create/Upload: Uploads a file to Supabase Storage, calls Edge Function, and saves metadata in DB.
    """
    file_size = len(file_bytes)
    
    try:
        # Upload to Storage
        res = supabase.storage.from_(STORAGE_BUCKET).upload(
            file_name, 
            file_bytes, 
            {"content-type": content_type}
        )
        
        # Call Edge Function
        try:
            function_url = f"{SUPABASE_URL}/functions/v1/process-file"
            payload = {"filename": file_name, "size": file_size}
            httpx.post(function_url, json=payload, timeout=5.0)
        except Exception:
            pass # Ignore edge function failure for this demo

        # Insert metadata to Database
        db_res = create_file_metadata(file_name, file_size, content_type)
        if not db_res["success"]:
            return {"success": False, "error": "Storage upload succeeded, but DB insert failed: " + db_res["error"]}
            
        return {"success": True, "data": db_res["data"]}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_files():
    """Read: List all files in the storage bucket."""
    try:
        files = supabase.storage.from_(STORAGE_BUCKET).list()
        return {"success": True, "data": files}
    except Exception as e:
        return {"success": False, "error": str(e)}

def download_file(file_name: str):
    """Read: Download a file from the storage bucket."""
    try:
        res = supabase.storage.from_(STORAGE_BUCKET).download(file_name)
        return {"success": True, "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_file(file_name: str, file_bytes: bytes, content_type: str):
    """Update: Replace an existing file in the storage bucket."""
    try:
        res = supabase.storage.from_(STORAGE_BUCKET).update(
            file_name, 
            file_bytes, 
            {"content-type": content_type}
        )
        return {"success": True, "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_file(file_name: str):
    """Delete: Removes a file from storage."""
    try:
        res = supabase.storage.from_(STORAGE_BUCKET).remove([file_name])
        return {"success": True, "data": res}
    except Exception as e:
        return {"success": False, "error": str(e)}
