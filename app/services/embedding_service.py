import torch
from sentence_transformers import SentenceTransformer
from core import settings

class EmbeddingService:
    def __init__(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        print(f"Loading BGE-M3 model on {self.device}...")
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL, device=self.device)
        print("Embedding model loaded successfully!")
    
    def embed_documents(self,chunks: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            chunks,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True
        )
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return embedding.tolist()
 