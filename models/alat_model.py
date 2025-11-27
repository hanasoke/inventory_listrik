from sqlalchemy import Column, Integer, String, Float
from database.db import Base


class Alat(Base):
    __tablename__ = "alat_listrik"

    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(50), unique=True, index=True, nullable=False)
    nama = Column(String(200), nullable=False)
    kategori = Column(String(100), nullable=True)
    stok = Column(Integer, default=0)
    harga = Column(Float, default=0.0)