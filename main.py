from fastapi import FastAPI
from database.db import Base, engine
from routers.alat_routes import router as alat_router

app = FastAPI(title="Inventory Toko Alat Listrik")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(alat_router)

@app.get("/")
def root():
    return {
    "message": "Inventory Toko Alat Listrik - API up. Buka /docs untuk dokumentasi."
    }