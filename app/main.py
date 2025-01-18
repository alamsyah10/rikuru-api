from fastapi import FastAPI

app = FastAPI()

# Register routes
# app.include_router(items.router, prefix="/items", tags=["items"])
# app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}