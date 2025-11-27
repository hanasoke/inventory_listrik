from fastapi import FastAPI 
from database.db import Base, engine 
from routes.alat_routes import router as alat_router 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(alat_router)