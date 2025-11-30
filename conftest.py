import os
import pytest
import time
import pathlib
import logging
from datetime import datetime
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
    path_dir = pathlib.Path("logs")
    path_dir.mkdir(exist_ok=True)

    log_file = path_dir / "historial.log"

    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        logger_fixture = item.funcargs.get("logger")
        if driver and logger_fixture:
            os.makedirs("reports", exist_ok=True)
            tiempo = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            archivo = f"reports/{item.name}_{tiempo}.png"
            driver.save_screenshot(archivo)
            logger_fixture.error(
                "Test '%s' falló. Captura automática guardada en: %s", item.name, archivo
            )
