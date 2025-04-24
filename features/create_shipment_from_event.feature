Feature: Flujo asíncrono de creación de envíos

  Scenario: Crear un envío automáticamente desde el eventro de pedido
    Given se crea un pedido en el InventoryService
    When se publica el evento OrderCreated
    Then ShipmentService debe recibir el evento
    And un envío debe registrarse en la base de datos