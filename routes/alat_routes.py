from fastapi import APIRouter 
from controllers.alat_controller import AlatController 

router = APIRoutes()
controller = AlatController()

@router.post("/alat")
def tambah_alat(data: dict):
    return controller.tambah(data)

@router.get("/alat")
def semua_alat(): 
    return controller.semua()

@router.get("/alat/{id}")
def detail_alat(id: int): 
    return controller.get(id)

@router.put("/alat/{id}")
def update_alat(id: int, data: dict):
    return controller.update(id, data)

@router.delete("alat/{id}")
def hapus_alat(id: int):
    return controller.delete(id)
