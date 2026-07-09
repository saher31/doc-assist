from fastapi import FastAPI
from api import pdf_router, chat_router

app = FastAPI()

app.include_router(pdf_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to DocAssist API"
    }