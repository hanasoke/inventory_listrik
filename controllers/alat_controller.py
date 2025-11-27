from models.alat_model import Alat 
from database.db import SessionLocal 

class AlatController: 
    def __init__(self): 
        self.db = SessionLocal()
        
        def tambah(self, data): 
            alat = Alat(**data)
            self.db.add(alat)
            self.db.commit()
            seld.db.refresh(alat)
            return alat 
        
        def semua(self): 
            return self.db.query(Alat).all()
        
        def get(self, id):
            return self.db.query(Alat).filter(Alat.id == id).first()
        
        def update(self, id, data): 
            alat = self.get(id)
            if not alat: 
                return None 
            
            for key, value in data.items(): 
                setattr(alat, key, value)
                
            self.db.commit()
            self.db.refresh(alat)
            return alat 
        
        def delete(self, id):
            alat = self.get(id)
            if not alat:
                return None 
            
            self.db.delete(alat)
            self.db.commit()
            return True
        