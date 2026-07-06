from fastapi import FastAPI
from api import pdf_router

app = FastAPI()

app.include_router(pdf_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to DocAssist API"
    }