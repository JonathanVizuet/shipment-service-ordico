Feature: Gestión de envíos

  Scenario: Crear un nuevo envío con datos válidos
    Given que tengo un order_id y una dirección de entrega
    When creo un nuevo envío con esos datos
    Then el sistema debe registrar el envío y responder con un status code 201