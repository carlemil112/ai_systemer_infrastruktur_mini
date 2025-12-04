from fastapi import FastAPI
from routes import v1, v2
from database import init_db 

# Initialize the FastAPi app 
app = FastAPI(
    title="AI and Infrastructure Project",
    version="1.0.0"
)
# Creates all required database tables before the API i started. 
init_db() 

# Register API v1 and v2 routes 
app.include_router(v1)
app.include_router(v2)
               
@app.get("/")
def root():
    return {"message": "API is running."}
