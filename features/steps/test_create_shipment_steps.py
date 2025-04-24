from behave import given, when, then
import requests
import time
import pyodbc


@given("se crea un pedido en el InventoryService")
def step_given_crear_pedido(context):
    # Se simula una compra:
    response = requests.put("http://localhost:8000/products/2?stock=155")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    context.response = response


@when("se publica el evento OrderCreated")
def step_when_publica_evento(context):
    # Se espera al evento
    time.sleep(2)


@then("ShipmentService debe recibir el evento")
def step_then_shipmentservice_recibe(context):
    assert context.response.status_code == 200


@then("un envío debe registrarse en la base de datos")
def step_and_envio_registrado(context):
    time.sleep(2)
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;DATABASE=OrdicoShipment;"
        "UID=sa;PWD=Ordico2024!;TrustServerCertificate=yes"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM shipments WHERE product_id = 2 AND quantity = 2")
    result = cursor.fetchone()
    assert result[0] > 0
    conn.close()
