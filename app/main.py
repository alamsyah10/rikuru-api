from fastapi import FastAPI
from app.api import file_processor
from app.services import chatgpt_service

app = FastAPI()
app.include_router(file_processor.router)

# Register routes
# app.include_router(items.router, prefix="/items", tags=["items"])
# app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/chat-gpt")
def call_gpt(text:str, prompt:str):
    return chatgpt_service.call_gpt(text, prompt)