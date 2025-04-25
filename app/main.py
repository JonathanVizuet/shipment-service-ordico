from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Shipment
from app.services.shipment_service import ShipmentService
from app.services.shipment_service import publish_return_event

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ShipmentServices corriendo"}


@app.post("/shipments")
def create_shipment():
    return {"message": "Envío creado"}


@app.get("/shipments/{order_id}")
def get_shipment(order_id: int):
    return {"message": f"Se encontró el envío con ID: {order_id}"}


@app.put("/shipments/{shipment_id}/status")
def update_shipment_status(shipment_id: int, new_status: str):
    db: Session = SessionLocal()
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()

    if not shipment:
        db.close()
        raise HTTPException(status_code=404, detail="Envío no encontrado")

    if shipment.status == new_status:
        db.close()
        return {"message": "El estatus no cambia"}

    shipment.status = new_status
    db.commit()

    if new_status.lower() == "return":
        publish_return_event(shipment.product_id, shipment.quantity)
        print(f"Devolución a inventario. ID de producto: {shipment.id} Cantidad: {shipment.quantity}")

    db.close()
    return {"message": f"El status del envío a cambiado a {new_status}"}