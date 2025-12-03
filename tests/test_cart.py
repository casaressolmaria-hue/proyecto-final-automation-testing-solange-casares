
import pytest
from utils.datos import leer_json

_PRODUCTOS = leer_json('datos/productos.json')

@pytest.mark.regresion
@pytest.mark.carrito
@pytest.mark.parametrize("producto", _PRODUCTOS)
def test_carrito(logger, driver, request, usuario_logueado, producto):
    """
    Test end-to-end del flujo de agregar un producto al carrito.

    Este test valida:

    1. Que el usuario logueado accede correctamente a la página de inventario.
    2. Que la sección de productos muestra el título esperado ("Products").
    3. Que el catálogo contiene al menos un producto.
    4. Que el precio del producto obtenido coincide con el precio definido en los datos.
    5. Que el producto puede agregarse al carrito.
    6. Que el contador del carrito incrementa tras agregar el producto.
    7. Que el carrito contiene exactamente un producto.
    8. Que el nombre y precio del producto en el carrito coinciden con los esperados.

    Parámetros:
        driver (WebDriver): Instancia del navegador para la prueba.
        usuario_logueado (InventoryPage): Página ya autenticada para comenzar el test.
        producto (dict): Datos del producto (nombre y precio) proporcionados por la parametrización.
    """
    
    request.node.page_url = driver.current_url

    inventory_page = usuario_logueado
    logger.info("Iniciando test del carrito para el producto: %s", producto["nombre"])

    logger.info("Obteniendo título de la sección del inventario")
    seccion = inventory_page.titulo_de_seccion()
    assert seccion, "No se encontró el elemento de título de sección"
    logger.info("Título de sección encontrado: '%s'", seccion.text)
    assert seccion.text == 'Products', f"Título inesperado: se esperaba 'Products' pero se obtuvo '{seccion.text}'"

    cantidad_productos = inventory_page.obtener_cantidad_productos()
    logger.info("Cantidad de productos encontrados en el catálogo: %d", cantidad_productos)
    assert cantidad_productos > 0, "No se encontraron productos en el catálogo"

    precio_del_producto = inventory_page.obtener_precio_del_producto(producto["nombre"])
    logger.info("Precio obtenido para '%s': %s", producto["nombre"], precio_del_producto)
    assert precio_del_producto, "Producto sin precio"
    assert precio_del_producto == producto["precio"], (
        f"El precio mostrado ({precio_del_producto}) no coincide con el esperado ({producto['precio']}) para el producto {producto['nombre']}"
    )

    logger.info("Agregando producto al carrito: %s", producto["nombre"])
    inventory_page.agregar_producto_por_nombre(producto["nombre"])

    logger.info("Verificando que el contador del carrito se actualizó")
    contador_carrito = inventory_page.carrito_contador()
    logger.info("Valor del contador del carrito: %d", contador_carrito)
    assert contador_carrito > 0, "No se encontró el contador del carrito después de agregar el producto"

    logger.info("Navegando a la página del carrito")
    cart_page = inventory_page.ir_al_carrito()

    logger.info("Verificando la lista de productos en el carrito")
    lista_productos = cart_page.lista_de_los_productos()
    assert lista_productos, "No se encontró la lista de productos en el carrito"

    productos_del_carrito = cart_page.productos_del_carrito()
    logger.info("Cantidad de productos en el carrito: %d", len(productos_del_carrito))
    assert len(productos_del_carrito) == 1, f"Se esperaba 1 producto en el carrito, pero se encontraron {len(productos_del_carrito)}"
