from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import file_processor
from app.services import chatgpt_service
from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Allow only localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(file_processor.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/chat-gpt")
def call_gpt(text: str, prompt: str):
    return chatgpt_service.call_gpt(text, prompt)
