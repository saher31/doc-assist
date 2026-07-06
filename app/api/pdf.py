from fastapi import APIRouter, File ,UploadFile , HTTPException
from services import  DocumentService

pdf_router = APIRouter(
    prefix="/pdf",
    tags=["pdf"] 
)


document_service = DocumentService()

@pdf_router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    result = await document_service.process_document(file)
    return {
        "filename": file.filename,
        "status": "success",
        "num_chunks": result["num_chunks"] ,
        "embedding_dimension": result["embedding_dimension"]
    }
