from pydantic import BaseModel, Field
from typing import Optional

class AlatBase(BaseModel):
    kode: str = Field(..., example="KD-001")
    nama: str = Field(..., example="Lampu LED 9W")
    kategori: Optional[str] = Field(None, example="Penerangan")
    stok: int = Field(..., ge=0, example=50)
    harga: float = Field(..., ge=0, example=12000.0)

class AlatCreate(AlatBase):
    pass


class AlatUpdate(BaseModel):
    nama: Optional[str]
    kategori: Optional[str]
    stok: Optional[int]
    harga: Optional[float]


class AlatOut(AlatBase):
    id: int


class Config:
    orm_mode = True