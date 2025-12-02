# Proyecto de Automatización de Pruebas

**Autor**: Solange Casares

## Propósito del proyecto

El objetivo de este proyecto es automatizar pruebas funcionales para la plataforma **SauceDemo**, y de APIs **reqres** y **jsonplaceholder**, garantizando que sus funcionalidades
críticas operen correctamente.\
Incluye pruebas de interfaz web con Selenium y pruebas de API,
permitiendo validar comportamientos clave del sistema mediante scripts
reproducibles.

## Tecnologías utilizadas

-   **Python 3**
-   **Selenium WebDriver**
-   **pytest**
-   **pytest-html** (para generar reportes en HTML)
-   **Requests**
-   **Faker**

## Estructura del proyecto

    conftest.py            # Archivo de configuración de Pytest
    pytest.ini             # Configuración de Pytest
    requirements.txt       # Lista de dependencias Python necesarias para el proyecto
    pages/                 # Carpeta que contiene Page Objects para tests UI
    tests/                 # Carpeta con tests de UI
    tests_api/             # Carpeta con tests de API
    ├── jsonplaceholder    # Subcarpeta para tests relacionados con la API de JSONPlaceholder
    └── reqres             # Subcarpeta para tests relacionados con la API de Reqres
    utils/                 # Funciones auxiliares y helpers
    datos/                 # Archivos de datos de prueba - CSV, JSON
    logs/                  # Carpeta donde se guardan logs generados
    reports/               # Carpeta donde se guardan reportes de ejecución (HTML, screenshots)
    README.md              # Documentación del proyecto

## ¿Cómo instalar las dependencias?

    pip install -r requirements.txt

## ¿Cómo ejecutar las pruebas?

### UI

    pytest -v tests/

### API

    pytest -v tests_api/

### Con markers
definidos en pytest.ini

    pytest -m <marker>

### Completo

    pytest -v

### Reporte HTML
en un único archivo

    pytest --html=reports/reporte.html --self-contained-html -v -s

## ¿Cómo interpretar los reportes generados?

Los reportes se guardan en `reports/` e incluyen:

 - Estado de cada prueba y tiempos
 - Subcarpeta `screens/` - contiene las capturas de pantalla tomadas para los tests que fallaron
 - Información del entorno
