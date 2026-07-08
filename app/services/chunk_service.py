from langchain_text_splitters import RecursiveCharacterTextSplitter
from core import settings

class ChunkService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = settings.CHUNK_SIZE,
            chunk_overlap = settings.CHUNK_OVERLAP,
        )

    def split_text(self, text: str) :
        return self.text_splitter.split_text(text)  