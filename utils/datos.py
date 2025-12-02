import csv
import pathlib
import json

def leer_csv(ruta_archivo):
    """
    Lee un archivo CSV y devuelve una lista de tuplas genéricas
    para usar en parametrización de pytest.
    """
    datos = []
    ruta = pathlib.Path(ruta_archivo)
    
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector, None)
        for fila in lector:
            datos.append(tuple(fila))
    
    return datos

def leer_json(ruta_archivo):
    """
    Lee un archivo JSON
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = json.load(archivo)
    
    return contenido
