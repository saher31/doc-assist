from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct
from core.config import settings
from providers.vector_db.base_provider import BaseVectorDBProvider
from uuid import uuid4

class QdrantProvider(BaseVectorDBProvider):
    
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

    def create_collection(self):
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        if settings.QDRANT_COLLECTION in collection_names:
            return

        self.client.recreate_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_DIMENSION,
                distance=Distance.COSINE
            )
        )
        

    def upsert(self, chunks : list[str],embeddings: list[list[float]],source: str):
        points = []
        for index , (chunk,embedding) in enumerate(zip(chunks,embeddings)):
            points.append(
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "chunk":chunk,
                        "source":source
                    }
                )
            )
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )
                
            

    def search(self,query: str):
        pass    
        
