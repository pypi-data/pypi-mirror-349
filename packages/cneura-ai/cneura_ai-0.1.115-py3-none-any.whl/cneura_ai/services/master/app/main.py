from fastapi import FastAPI
from app.routes import sample
from app.dependencies import db_hub  # <-- Moved here

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db_hub.connect()

@app.on_event("shutdown")
async def shutdown():
    await db_hub.disconnect()

app.include_router(sample.router)
