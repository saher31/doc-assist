from fastapi import UploadFile
from services.pdf_service import PDFService
from services.pdf_text_extractor import PDFTextExtractor

class DocumentService:
    def __init__(self):
        self.pdf_service = PDFService()
        self.pdf_text_extractor = PDFTextExtractor()

    async def process_document(self, file: UploadFile):
        file_path = await self.pdf_service.save_pdf(file)
        text =  self.pdf_text_extractor.extract_text(file_path)

        return {
            "file_path": file_path,
            "text": text
        }
        
    