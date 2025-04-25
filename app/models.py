from sqlalchemy import Column, Integer, String
from app.database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    destination = Column(String, nullable=False)

class ShipmentSummary(Base):
    __tablename__ = "shipment_summary"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    total_quantity = Column(Integer, nullable=False)
