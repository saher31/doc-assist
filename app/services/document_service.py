from fastapi import UploadFile
from services.pdf_service import PDFService
from services.pdf_text_extractor import PDFTextExtractor
from services.chunk_service import ChunkService

class DocumentService:
    def __init__(self):
        self.pdf_service = PDFService()
        self.pdf_text_extractor = PDFTextExtractor()
        self.chunk_service = ChunkService()

    async def process_document(self, file: UploadFile):
        file_path = await self.pdf_service.save_pdf(file)
        text =  self.pdf_text_extractor.extract_text(file_path)
        chunks = self.chunk_service.split_text(text)

        return {
            "file_path": file_path,
            "text": text,
            "chunks": chunks,
            "num_chunks": len(chunks)
        }

