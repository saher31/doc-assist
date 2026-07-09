from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: str
    filename: str
    num_chunks: int


class ChatResponse(BaseModel):
    status: str
    answer: str
    sources: list[str]