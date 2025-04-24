from pydantic import BaseModel

class ShipmentSchema(BaseModel):
    product_id: int
    name: str
    quantity: int
    destination: str