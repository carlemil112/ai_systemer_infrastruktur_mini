# main.py
from fastapi import FastAPI
 
app = FastAPI(title="My AI API Server", version="1.0.0")
 
@app.get("/")
def read_root():
    return {"message": "Welcome to my AI API server!"}


