from huggingface_hub.inference._generated.types import document_question_answering
from services.embedding_service import EmbeddingService
from providers.vector_db.qdrant_provider import QdrantProvider   
from providers.llm.gemini_provider import GeminiProvider 
from core.config import settings

class RAGService:
    def __init__(self):
        self.embedding_services = EmbeddingService()
        self.qdrant_provider = QdrantProvider()
        self.gemini_provider = GeminiProvider()

    def ask(self, question: str):
        query_embedding = self.embedding_services.embed_query(question)
        results = self.qdrant_provider.search(
            query_embedding=query_embedding,
            limit=settings.TOP_K)
        context = self._build_context(results)
        answer = self.gemini_provider.generate(
            context=context,
            question=question)
        return {
            "answer": answer,
            "sources": list(
                dict.fromkeys(
                    result.payload["source"]
                    for result in results
                )
            )
        }

    def _build_context(self,results):
        return "\n\n".join(
            result.payload["text"]
            for result in results
        )
    
