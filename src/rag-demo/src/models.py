from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from typing import Dict

@dataclass
class Product:
    product_id: str
    name: str
    category: str
    unit_price: float
    pack_size: int
    storage_temp: str

@dataclass
class Store:
    store_id: str
    name: str
    location: str
    type: str
    capacity: int
    opening_hours: str
    region: str

@dataclass
class POSTerminal:
    terminal_id: str
    store_id: str
    type: str
    location: str
    status: str
    last_maintenance: datetime

@dataclass
class Transaction:
    transaction_id: str
    store_id: str
    terminal_id: str
    product_id: str
    quantity: int
    unit_price: float
    payment_method: str
    cashier_id: Optional[str]
    timestamp: datetime
    status: str
    total_amount: float

@dataclass
class BatchOrder:
    batch_id: str
    store_id: str
    products: Dict[str, int]
    timestamp: datetime
    status: str = 'pending'
    priority: str = 'normal'
