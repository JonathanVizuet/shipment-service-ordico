from fastapi import FastAPI

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