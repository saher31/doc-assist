from fastapi import APIRouter, File ,UploadFile , HTTPException
from services import PDFService

pdf_router = APIRouter(
    prefix="/pdf",
    tags=["pdf"] 
)


pdf_service = PDFService()

@pdf_router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = await pdf_service.save_pdf(file)
    return {
        "filename": file.filename,
        "status": "success",
        "path": str(file_path)
    }
