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