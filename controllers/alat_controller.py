from sqlalchemy.orm import Session
from models.alat_model import Alat
from schemas import AlatCreate, AlatUpdate
from typing import List, Optional


class AlatController:
    @staticmethod
    def create_alat(db: Session, alat_in: AlatCreate) -> Alat:
        # Check duplicate kode
        existing = db.query(Alat).filter(Alat.kode == alat_in.kode).first()
        if existing:
            raise ValueError(f"Alat dengan kode '{alat_in.kode}' sudah ada.")


        alat = Alat(
            kode=alat_in.kode,
            nama=alat_in.nama,
            kategori=alat_in.kategori,
            stok=alat_in.stok,
            harga=alat_in.harga,
        )
        
        db.add(alat)
        db.commit()
        db.refresh(alat)
        return alat

        @staticmethod
        def list_alat(db: Session) -> List[Alat]:
            return db.query(Alat).all()

        @staticmethod
        def get_alat(db: Session, id: int) -> Optional[Alat]:
            return db.query(Alat).filter(Alat.id == id).first()


        @staticmethod
        def get_by_kode(db: Session, kode: str) -> Optional[Alat]:
            return db.query(Alat).filter(Alat.kode == kode).first()

        @staticmethod
        def update_alat(db: Session, id: int, alat_in: AlatUpdate) -> Optional[Alat]:
            alat = db.query(Alat).filter(Alat.id == id).first()
        if not alat:
            return None
        
        data = alat_in.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(alat, key, value)
        db.commit()
        db.refresh(alat)
        return alat

        @staticmethod
        def delete_alat(db: Session, id: int) -> bool:
            alat = db.query(Alat).filter(Alat.id == id).first()
            if not alat:
                return False
            db.delete(alat)
            db.commit()
            return True