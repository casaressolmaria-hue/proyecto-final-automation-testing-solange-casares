import pytest
import requests
from faker import Faker

from utils.api_utils import validar_respuesta_api

faker = Faker()
_BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="module")
def posts_url():
    """Devuelve la URL base para /posts"""
    return f"{_BASE_URL}/posts"

@pytest.fixture(scope="module")
def post_por_id_url():
    """Devuelve la URL para un post específico"""
    def _get_url(post_id):
        return f"{_BASE_URL}/posts/{post_id}"
    return _get_url

@pytest.fixture(scope="module")
def post_creado(posts_url, module_logger):
    """ Crea un post y devuelve su JSON para usar en tests encadenados """

    datos = {
        "title": faker.sentence(),
        "body": faker.text(),
        "userId": 1
    }
    module_logger.info(f"Creando post con datos: {datos}")
    respuesta = requests.post(posts_url, json=datos)

    module_logger.info(f"Status recibido al crear post: {respuesta.status_code}")
    assert respuesta.status_code == 201, f"Se esperaba status 201, pero se obtuvo {respuesta.status_code}"
    
    contenido = respuesta.json()
    module_logger.info(f"Post creado: {contenido}")
    
    return contenido

@pytest.mark.e2e
def test_actualizar_post(post_creado, post_por_id_url, module_logger):
    """Actualiza el título del post creado y valida respuesta"""

    post_id = post_creado["id"]
    datos = {"title": "Título actualizado por QA"}
    module_logger.info(f"Actualizando post ID {post_id} con datos: {datos}")

    respuesta = requests.patch(post_por_id_url(post_id), json=datos)
    module_logger.info(f"Status recibido al actualizar post: {respuesta.status_code}")

    contenido = validar_respuesta_api(respuesta, 200, campos_esperados={"title"}, max_tiempo=2.0)
    module_logger.info(f"Contenido después del patch: {contenido}")

    assert contenido["title"] == "Título actualizado por QA", "El título no se actualizó correctamente"
    module_logger.info("Título actualizado correctamente.")

@pytest.mark.e2e
def test_eliminar_post(post_creado, post_por_id_url, module_logger):
    """Elimina el post creado y valida respuesta"""

    post_id = post_creado["id"]
    module_logger.info(f"Eliminando post ID {post_id}")

    respuesta = requests.delete(post_por_id_url(post_id))
    module_logger.info(f"Status recibido al eliminar post: {respuesta.status_code}")
    
    validar_respuesta_api(respuesta, 200, {}, max_tiempo=2.0)
    module_logger.info(f"Post ID {post_id} eliminado correctamente.")
