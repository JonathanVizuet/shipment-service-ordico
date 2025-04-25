from sqlalchemy.orm import Session
from app.models import Shipment, ShipmentSummary
from app.schemas import ShipmentSchema
import pika
import json


def publish_return_event(product_id: int, quantity: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="ordico_exchange", exchange_type="topic")

    event = {
        "product_id": product_id,
        "quantity": quantity
    }

    channel.basic_publish(
        exchange="ordico_exchange",
        routing_key="event.ShipmentReturned",
        body=json.dumps(event)
    )

    print(f"[ShipmentService] Evento ShipmentReturned: {event}")
    connection.close()


class ShipmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_shipment(self, shipment_data: ShipmentSchema) -> Shipment:
        nuevo_envio = Shipment(
            product_id=shipment_data.product_id,
            name=shipment_data.name,
            quantity=shipment_data.quantity,
            destination=shipment_data.destination,
            status="pending"
        )
        self.db.add(nuevo_envio)
        self.db.commit()
        self.db.refresh(nuevo_envio)

        self._update_summary(shipment_data.product_id, shipment_data.quantity)
        return nuevo_envio


    def _update_summary(self, product_id: int, quantity: int) -> None:
        summary = self.db.query(ShipmentSummary).filter(ShipmentSummary.product_id == product_id).first()
        if summary:
            summary.total_quantity += quantity
            self.db.add(summary)
        else:
            summary = ShipmentSummary(
                product_id=product_id,
                total_quantity=quantity
            )
            self.db.add(summary)

        self.db.commit()
