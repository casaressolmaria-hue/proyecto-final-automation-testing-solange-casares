import pytest
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized") # Ventana grande
    options.add_argument("--guest")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5) # Espera implícita

    yield driver

    time.sleep(1)
    driver.quit()

@pytest.fixture
def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    return logging.getLogger()

@pytest.fixture
def credenciales_validas():
    return {"username": "standard_user", "password": "secret_sauce"}

@pytest.fixture
def usuario_logueado(driver, logger, credenciales_validas):
    """
    Fixture que realiza login antes de cada test de carrito
    """
    logger.info("Iniciando fixture usuario_logueado")
    login_page = LoginPage(driver)
    logger.info("Abriendo la página de login")
    login_page.abrir()
    logger.info("Realizando login con usuario estándar")
    pagina = login_page.login(credenciales_validas["username"], credenciales_validas["password"])
    logger.info("Login exitoso, devolviendo sesión de usuario")
    return pagina