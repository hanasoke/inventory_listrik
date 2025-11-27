from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from database.db import get_db
from controllers.alat_controller import AlatController
from schemas import AlatCreate, AlatOut, AlatUpdate

router = APIRouter(prefix="/alat", tags=["alat"])

@router.post("/", response_model=AlatOut, status_code=status.HTTP_201_CREATED)
def create_alat(alat_in: AlatCreate, db: Session = Depends(get_db)):
    try:
        alat = AlatController.create_alat(db, alat_in)
        return alat
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    @router.get("/", response_model=List[AlatOut])
    def list_alat(db: Session = Depends(get_db)):
        return AlatController.list_alat(db)

    @router.get("/{id}", response_model=AlatOut)
    def get_alat(id: int, db: Session = Depends(get_db)):
        alat = AlatController.get_alat(db, id)
        if not alat:
            raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
        return alat

    @router.put("/{id}", response_model=AlatOut)
    def update_alat(id: int, alat_in: AlatUpdate, db: Session = Depends(get_db)):
        alat = AlatController.update_alat(db, id, alat_in)
        if not alat:
            raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
        return alat

    @router.delete("/{id}")
    def delete_alat(id: int, db: Session = Depends(get_db)):
        hasil = AlatController.delete_alat(db, id)
        if not hasil:
            raise HTTPException(status_code=404, detail="Alat tidak ditemukan")
        return {"detail": "Berhasil dihapus"}