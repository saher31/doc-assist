from abc import ABC,abstractmethod

class BaseVectorDBProvider(ABC):

    @abstractmethod
    def create_collection(self):
        pass

    @abstractmethod
    def upsert(self, chunks : list[str],embeddings: list[list[float]], source: str):
        pass 
    
    @abstractmethod
    def search(self,query_embedding: list[float],limit: int = 5):
        pass

    @abstractmethod
    def delete_by_source(self, source: str):
        pass