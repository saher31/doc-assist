from fastapi import APIRouter 
from schemas.chat import ChatRequest
from services import RAGService

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)   

rag_service = RAGService()

@chat_router.post("/ask")
def chat(request: ChatRequest):

    return rag_service.ask(
        request.question
    )