import pytest

from utils.api_utils import get

@pytest.mark.api
def test_listar_usuarios(logger):
    """
    Test del endpoint GET /users?page=1 de Reqres.

    Validaciones realizadas:
    - Código de estado debe ser 200.
    - El objeto JSON debe contener una lista de usuarios en la clave 'data'.
    - Cada usuario debe incluir las claves obligatorias:
        ['id', 'email', 'first_name', 'last_name', 'avatar']
    - El campo 'avatar' debe terminar en '.jpg'.
    """

    respuesta = get("users?page=1")
    logger.info(f"Petición enviada. Status recibido: {respuesta.status_code}")

    assert respuesta.status_code == 200, f"Se esperaba status 200, pero se obtuvo {respuesta.status_code}"

    contenido = respuesta.json()
    logger.info("Respuesta JSON recibida correctamente")

    usuarios = contenido.get("data", [])
    logger.info(f"Cantidad de usuarios encontrados: {len(usuarios)}")

    assert usuarios, "No se encontraron usuarios en la respuesta"

    for index, usuario in enumerate(usuarios):
        logger.info(f"Validando usuario índice {index}: {usuario}")

        for clave in ["id", "email", "first_name", "last_name", "avatar"]:
            assert clave in usuario, f"Falta la clave '{clave}' en el usuario índice {index}"

        avatar = usuario.get("avatar", "")
        logger.info(f"Avatar usuario índice {index}: {avatar}")

        assert avatar.endswith(".jpg"), f"El avatar del usuario índice {index} no termina en .jpg: {avatar}"
