from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import file_processor
from app.services import chatgpt_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include your file processor router
app.include_router(file_processor.router)

# Register routes
# app.include_router(items.router, prefix="/items", tags=["items"])
# app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/chat-gpt")
def call_gpt(text: str, prompt: str):
    return chatgpt_service.call_gpt(text, prompt)
