from fastapi import FastAPI
from routes import v1, v2
from database import init_db #database import


app = FastAPI(
    title="AI and Infrastructure Project",
    version="1.0.0"
)

init_db() #sørger for tabeller i databaase findes

app.include_router(v1)
app.include_router(v2)
               
@app.get("/")
def root():
    return {"message": "API running."}
