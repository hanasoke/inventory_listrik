from sqlalchemy import Column, Integer, String, Float 
from database.db import Base 

class Alat(Base): 
    __tablename__ = "alat_listrik"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    kategori = Column(String)
    stok = Column(Integer)
    harga = Column(Float)