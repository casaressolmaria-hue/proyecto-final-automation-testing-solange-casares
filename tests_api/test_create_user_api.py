import pytest
from datetime import datetime

from utils.api_utils import post
from utils.datos import leer_csv

_USUARIOS = leer_csv('datos/usuarios.csv')

@pytest.mark.api
@pytest.mark.parametrize("nombre,trabajo", _USUARIOS)
def test_crear_usuario(logger, nombre, trabajo):
    """
    Test de creación de usuario (POST /users).

    Este test envía diferentes combinaciones de nombres y trabajos a la API
    para validar el comportamiento del endpoint de creación de usuarios.

    Validaciones:
    - El endpoint debe responder con código 201.
    - El campo 'name' debe coincidir con el enviado.
    - El campo 'job' debe coincidir con el enviado.
    - El campo 'createdAt' debe existir y contener el año actual.
    """
        
    logger.info(f"Iniciando test de creación de usuario: Parámetros -> nombre='{nombre}', trabajo='{trabajo}'")

    payload = {
        "name": nombre,
        "job": trabajo
    }

    logger.info(f"Payload enviado: {payload}")

    respuesta = post("users", payload)
    logger.info(f"Status recibido: {respuesta.status_code}")

    assert respuesta.status_code == 201, (
        f"Se esperaba status 201, pero se obtuvo {respuesta.status_code}"
    )

    contenido = respuesta.json()
    logger.info(f"Contenido recibido: {contenido}")

    assert contenido.get("name") == nombre, (
        f"Se esperaba name='{nombre}', pero se obtuvo '{contenido.get('name')}'"
    )

    assert contenido.get("job") == trabajo, (
        f"Se esperaba job='{trabajo}', pero se obtuvo '{contenido.get('job')}'"
    )

    created_at = contenido.get("createdAt")
    logger.info(f"createdAt recibido: {created_at}")

    assert created_at, "No se encontró createdAt en la respuesta"
    assert str(datetime.now().year) in created_at, (
        f"El año actual no está en createdAt: {created_at}"
    )
