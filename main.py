from fastapi import FastAPI
from routes import router
from database import init_db #database import


app = FastAPI(
    title="AI and Infrastructure Project",
    version="1.0.0"
)

init_db() #sørger for tabeller i databaase findes
app.include_router(router)
               
@app.get("/")
def root():
    return {"message": "API running."}