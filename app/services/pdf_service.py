from pathlib import Path
from fastapi import HTTPException,UploadFile
from core import paths

class PDFService:
    async def save_pdf(self, file:UploadFile):
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        upload_dir = paths.UPLOAD_DIR
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir/file.filename
        content = await file.read()

        with open(file_path,"wb") as f:
            f.write(content)
        return file_path.resolve()   
                
        
        