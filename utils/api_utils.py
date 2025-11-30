import requests

_URL_BASE = "https://reqres.in/api"
_API_KEY = "reqres-free-v1"

def get(ruta):
    headers = { "x-api-key": _API_KEY,
               "Content-Type": "application/json" }
    return requests.get(f"{_URL_BASE}/{ruta}", headers=headers)

def post(ruta, payload):
    headers = { "x-api-key": _API_KEY,
               "Content-Type": "application/json" }
    return requests.post(f"{_URL_BASE}/{ruta}", json=payload, headers=headers)

def validar_respuesta_api(respuesta, estado_esperado, campos_esperados=None, max_tiempo=1.0):
    """Valida estado, headers, estructura y performance de la respuesta"""

    # Nivel 1: Estado esperado
    assert respuesta.status_code == estado_esperado, f"Se esperaba status {estado_esperado}, pero se obtuvo {respuesta.status_code}"

    # Nivel 2: Headers
    if estado_esperado != 204:  # 204 puede no tener Content-Type
        assert "application/json" in respuesta.headers.get("Content-Type", ""), f"Se esperaba 'Content-Type: application/json', pero se obtuvo '{respuesta.headers.get('Content-Type', '')}'"

    # Nivel 3-4: Estructura y contenido
    if campos_esperados and respuesta.text:
        body = respuesta.json()
        assert campos_esperados <= set(body.keys()), f"Faltan campos esperados en la respuesta. Esperados: {campos_esperados}, recibidos: {set(body.keys())}"

    # Nivel 5: Performance
    tiempo_transcurrido = respuesta.elapsed.total_seconds()
    assert tiempo_transcurrido < max_tiempo, f"La respuesta tardó {tiempo_transcurrido:.2f}s, se esperaba menos de {max_tiempo}s"

