from app.db import supabase

def create_file_metadata(filename: str, file_size: int, content_type: str):
    """Create: Insert a new record in the file_metadata table."""
    try:
        data = {
            "filename": filename,
            "file_size": file_size,
            "content_type": content_type
        }
        res = supabase.table("file_metadata").insert(data).execute()
        return {"success": True, "data": res.data[0]}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_file_metadata():
    """Read: List all records in the file_metadata table."""
    try:
        res = supabase.table("file_metadata").select("*").execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_file_metadata(record_id: str, new_filename: str):
    """Update: Update a record in the file_metadata table."""
    try:
        data = {"filename": new_filename}
        res = supabase.table("file_metadata").update(data).eq("id", record_id).execute()
        return {"success": True, "data": res.data[0] if res.data else None}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_file_metadata(filename: str):
    """Delete: Remove a record from the file_metadata table by filename."""
    try:
        res = supabase.table("file_metadata").delete().eq("filename", filename).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
