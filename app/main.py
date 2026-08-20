from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import os

from app.crud_storage import upload_file, list_files, download_file, delete_file, update_file
from app.crud_database import list_file_metadata, update_file_metadata, delete_file_metadata

app = FastAPI(title="Supabase CRUD API")

@app.post("/api/files")
async def api_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    res = upload_file(file.filename, contents, file.content_type)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/api/files")
def api_list_files():
    db_res = list_file_metadata()
    if not db_res["success"]:
        raise HTTPException(status_code=400, detail=db_res["error"])
    return {"success": True, "data": db_res["data"]}

@app.delete("/api/files/{filename}")
def api_delete_file(filename: str):
    # Delete from storage
    storage_res = delete_file(filename)
    if not storage_res["success"]:
        raise HTTPException(status_code=400, detail=storage_res["error"])
    
    # Delete from database
    db_res = delete_file_metadata(filename)
    if not db_res["success"]:
        raise HTTPException(status_code=400, detail=db_res["error"])
        
    return {"success": True, "message": "File deleted successfully"}

@app.get("/api/files/{filename}/download")
def api_download_file(filename: str):
    res = download_file(filename)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])
    # Return as raw bytes
    return Response(content=res["data"], media_type="application/octet-stream")

@app.put("/api/files/{record_id}")
async def api_update_filename(record_id: str, new_filename: str):
    res = update_file_metadata(record_id, new_filename)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

# Mount static files to serve the frontend UI
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
