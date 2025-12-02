import pytest
from pages.login_page import LoginPage
from utils.datos import leer_csv

_CASOS_LOGIN = leer_csv('datos/login.csv')

@pytest.mark.regresion
@pytest.mark.login
@pytest.mark.parametrize("usuario, clave, debe_funcionar", _CASOS_LOGIN)
def test_login(driver, logger, request, usuario, clave, debe_funcionar):
    """
    Test de login parametrizado usando datos provenientes de un archivo CSV.

    Este test realiza las siguientes validaciones:

    1. Abre la página de login correctamente.
    2. Intenta iniciar sesión con el usuario y clave proporcionados.
    3. Si el caso indica que el login debe funcionar:
        - Verifica que el resultado del login no sea None.
        - Confirma que la URL actual contiene 'inventory.html' (indicando éxito).
    4. Si el caso indica que el login NO debe funcionar:
        - Verifica que el resultado sea None.
        - Comprueba que se muestre un mensaje de error en la página.

    Parámetros:
        driver (WebDriver): Instancia del navegador usada en la prueba.
        usuario (str): Nombre de usuario leído desde el CSV.
        clave (str): Contraseña asociada al usuario.
        debe_funcionar (bool): Indica si el caso de prueba debe resultar en un login exitoso.
    """
    
    request.node.page_url = driver.current_url
    
    logger.info("Iniciando test de login con usuario: '%s'", usuario)
    login_page = LoginPage(driver)

    logger.info("Abriendo la página de login")
    login_page.abrir()
    
    logger.info("Intentando login con usuario='%s' y clave='%s'", usuario, clave)
    resultado = login_page.login(usuario, clave)

    if debe_funcionar == "True":
        logger.info("Se espera que el login funcione")
        assert resultado is not None, "El login debía funcionar pero falló."
        logger.info("Login exitoso")
        assert "inventory.html" in driver.current_url, f"URL inesperada: {driver.current_url}"
        logger.info("Redirigido correctamente a la página de inventario")
    else:
        logger.info("Se espera que el login falle")
        assert resultado is None, "El login no debía funcionar, pero sí funcionó."
        assert login_page.hay_error(), "Se esperaba un mensaje de error y no apareció."
        logger.info("Mensaje de error mostrado correctamente")
