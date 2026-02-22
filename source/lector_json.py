# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 01:00:38 2026

@author: Efrén Alejandro
"""
import json
import os


def leer_archivo_json(nombre_archivo, data_dir):
    """Lee un archivo JSON y retorna el diccionario."""
    ruta = os.path.join(data_dir, nombre_archivo)
    if not os.path.exists(ruta):
        return {}
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Archivo {nombre_archivo} corrupto: {e}")
        return {}
