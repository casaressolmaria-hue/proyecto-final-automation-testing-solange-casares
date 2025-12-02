import pytest

@pytest.mark.smoke
@pytest.mark.login
def test_login(logger, driver, request, usuario_logueado):
    """
    Prueba el proceso de inicio de sesión en la aplicación.

    Pasos:
    - Abre la página de login.
    - Ingresa credenciales válidas.
    - Verifica que se acceda correctamente al inventario.
    - Valida que los títulos esperados estén presentes.

    """
    
    request.node.page_url = driver.current_url
    
    logger.info("Iniciando verificación de login y página de inventario")
    inventory_page = usuario_logueado

    # Verifica que exista el elemento del título y que su texto sea 'Swag Labs'
    logger.info("Verificando el título del logo de la página")
    titulo = inventory_page.titulo()
    assert titulo, "No se encontró el titulo"
    logger.info("Título encontrado: '%s'", titulo.text)
    assert titulo.text == "Swag Labs", f"Texto inesperado en logo: se esperaba 'Swag Labs' pero se obtuvo '{titulo.text}'"

    # Verifica título de sección
    logger.info("Verificando título de la sección de productos")
    seccion = inventory_page.titulo_de_seccion()
    assert seccion, "No se encontró el elemento de título de sección"
    logger.info("Título de sección encontrado: '%s'", seccion.text)
    assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

    logger.info("Login completado correctamente y se ingresó a la página de inventario.")
