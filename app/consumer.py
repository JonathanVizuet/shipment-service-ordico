import pika
import json

from sqlalchemy.orm import Session

from app.database import engine
from app.database import Base, SessionLocal
from app.models import Shipment
from app.services.shipment_service import ShipmentService
from app.schemas import ShipmentSchema


def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        print("Evento recibido de ReabbitMQ:")
        print(data)

        db: Session = SessionLocal()

        shipment_data = ShipmentSchema(**data)
        ShipmentService(db).create_shipment(shipment_data)
        db.close()

    except Exception as e:
        print(f"Error al recibir el evento: {e}")


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="ordico_exchange", exchange_type="topic")
    channel.queue_declare(queue="shipment_queue")
    channel.queue_bind(exchange="ordico_exchange", queue="shipment_queue", routing_key="event.OrderCreated")

    print("Esperando eventos 'OrderCreated' en ShipmentServicce... ")
    channel.basic_consume(queue="shipment_queue", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    start_consumer()