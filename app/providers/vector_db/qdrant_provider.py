from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct
from core.config import settings
from providers.vector_db.base_provider import BaseVectorDBProvider
from uuid import uuid4
from qdrant_client.models import Filter, FieldCondition, MatchValue

class QdrantProvider(BaseVectorDBProvider):
    
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        self.create_collection()

    def create_collection(self):
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        if settings.QDRANT_COLLECTION in collection_names:
            return

        self.client.create_collection(
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
                        "text": chunk,
                        "source": source
                    }
                )
            )
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )
                
            

    def search(self, query_embedding: list[float], limit: int = 5):
        try:
            results = self.client.query_points(
                collection_name=settings.QDRANT_COLLECTION,
                query=query_embedding,
                limit=limit,
            )
            return results.points

        except Exception as e:
            raise RuntimeError(f"Qdrant search failed: {e}")


    def delete_by_source(self, source: str):
        self.client.delete(
            collection_name=settings.QDRANT_COLLECTION,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source)
                    )
                ]
            )
        )
