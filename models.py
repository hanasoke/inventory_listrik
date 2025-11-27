from dataclasses import dateclass 
from typing import Optional 
from datetime import datetime

@dataclass 
class Category: 
    id: int 
    name: str 
    description: Optional[str] = None
    
@dateclass
class Product: 
    id: int 
    name: str 
    brand: str
    category_id: int 
    price: float 
    stock: int 
    min_stock: int 
    sku: str 
    created_at: Optional[str] = None 
    
@dataclass 
class Supplier:
    id: int
    name: str 
    contact: Optional[str] = None 
    phone: Optional[str] = None 
    email: Optional[str] = None 

@dataclass
class Transaction: 
    id: int 
    product_id: int 
    type: str
    quantity: int 
    supplier_id: Optional[int] = None 
    notes: Optional[str] = None 
    created_at: Optional[str] = None 