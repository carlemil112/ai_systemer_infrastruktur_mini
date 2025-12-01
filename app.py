# main.py
from fastapi import FastAPI
 
app = FastAPI(title="My AI API Server", version="1.0.0")
 
@app.get("/")
def read_root():
    return {"message": "Welcome to my AI API server!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

