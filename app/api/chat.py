from fastapi import APIRouter 
from schemas import ChatRequest, ChatResponse
from services import RAGService

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)   

rag_service = RAGService()

@chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return rag_service.ask(request.question)