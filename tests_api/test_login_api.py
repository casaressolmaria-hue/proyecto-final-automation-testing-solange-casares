import pytest

from utils.api_utils import post
from utils.datos import leer_csv

_CASOS_LOGIN = leer_csv('datos/reqres_in_login.csv')

@pytest.mark.api
@pytest.mark.parametrize("correo,contrasena,estado_esperado,token_esperado", _CASOS_LOGIN)
def test_login(logger, correo, contrasena, estado_esperado, token_esperado):
    """
    Test parametrizado del endpoint POST /login de Reqres.

    Valida:
    - Códigos de estado esperados según combinación de email/contraseña.
    - Presencia de token si el login debe funcionar.
    - Presencia de error si el login debe fallar.
    """
        
    logger.info(f"Iniciando test de login. Parámetros recibidos -> correo='{correo}', contraseña='{contrasena}', estado_esperado={estado_esperado}, token_esperado={token_esperado}")

    datos = {}
    datos["email"] = correo or None
    datos["password"] = contrasena or None

    logger.info(f"Payload enviado: {datos}")

    respuesta = post("login", datos)
    logger.info(f"Status recibido: {respuesta.status_code}")

    contenido = respuesta.json()
    logger.info(f"Contenido recibido: {contenido}")

    error_recibido = contenido.get("error", "Sin mensaje de error")

    assert respuesta.status_code == int(estado_esperado), (
        f"Se esperaba status {estado_esperado} para correo='{correo}', "
        f"contraseña='{contrasena}', pero se obtuvo {respuesta.status_code}. "
        f"Error recibido: {error_recibido}"
    )

    if token_esperado == "True":
        assert "token" in contenido and contenido["token"], (
            f"Se esperaba token para correo='{correo}', contraseña='{contrasena}', "
            f"pero no se recibió"
        )
        logger.info("Token recibido correctamente.")
    else:
        assert "error" in contenido, (
            f"Se esperaba error para correo='{correo}', contraseña='{contrasena}', "
            f"pero no se recibió"
        )
        logger.info(f"Error recibido correctamente: {error_recibido}")
