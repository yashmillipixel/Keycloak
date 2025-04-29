from fastapi import APIRouter
import os
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import HTTPException

router = APIRouter()

UPLOAD_DIR = "C:/Users/dudej/Documents/app/.conda/uploads"

@router.get("/documents")
async def list_documents():
    try:
        files = os.listdir(UPLOAD_DIR)
        pdfs = [f for f in files if f.endswith(".pdf")]
        return {"documents": pdfs}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@router.get("/documents/{filename}")
async def download_document(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type='application/pdf', filename=filename)
