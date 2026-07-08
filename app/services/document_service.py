from fastapi import UploadFile
from services.pdf_service import PDFService
from services.text_extraction_service import TextExtractionService
from services.chunk_service import ChunkService
from services.embedding_service import EmbeddingService
from providers.vector_db.qdrant_provider import QdrantProvider

class DocumentService:
    def __init__(self):
        self.pdf_service = PDFService()
        self.text_extraction_service = TextExtractionService()
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.qdrant_provider = QdrantProvider()

        self.qdrant_provider.create_collection()

    async def process_document(self, file: UploadFile) -> dict:
        file_path = await self.pdf_service.save_pdf(file)
        document_text =  self.text_extraction_service.extract_text(file_path)
        chunks = self.chunk_service.split_text(document_text)
        embeddings = self.embedding_service.generate_embeddings(chunks)
        self.qdrant_provider.upsert(
            chunks=chunks,
            embeddings=embeddings,
            source=file.filename
        )
        return {
            "status": "success",
            "num_chunks": len(chunks),
        }
