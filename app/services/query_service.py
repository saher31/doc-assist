from services.embedding_service import EmbeddingService
from providers.vector_db.qdrant_provider import QdrantProvider    
from core.config import settings

class QueryService:
    def __init__(self):
        self.embedding_services = EmbeddingService()
        self.qdrant_provider = QdrantProvider()


    def search(self,query: str):
        query_embedding = self.embedding_services.embed_query(query)
        
        results = self.qdrant_provider.search(
            query_embedding=query_embedding,
            limit=settings.TOP_K
        )

        return results

        