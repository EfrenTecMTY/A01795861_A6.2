# -*- coding: utf-8 -*-
"""Validaciones de integridad referencial entre entidades.
Created on Sat Feb 21 22:58:45 2026

@author: Efrén Alejandro
"""
# from hotel import Hotel
# from cliente import Cliente
# from tipo_cuarto import TipoCuarto
import persistencia
from lector_json import leer_archivo_json


def validar_hotel(rfc_hotel):
    """Valida que el hotel exista en el archivo."""
    archivo = leer_archivo_json("hoteles.json", persistencia.DATA_DIR)
    if rfc_hotel not in archivo:
        raise ValueError(f"No existe hotel con RFC {rfc_hotel}.")


def validar_cliente(rfc_cliente):
    """Valida que el cliente exista en el archivo."""
    archivo = leer_archivo_json("clientes.json", persistencia.DATA_DIR)
    if rfc_cliente not in archivo:
        raise ValueError(f"No existe cliente con RFC {rfc_cliente}.")


def validar_tipos_cuarto(rfc_hotel, detalle):
    """Valida que cada tipo de cuarto del detalle exista para el hotel."""
    archivo = leer_archivo_json("tipos_cuarto.json", persistencia.DATA_DIR)
    for item in detalle:
        llave = f"{rfc_hotel}_{item['tipo']}"
        if llave not in archivo:
            raise ValueError(
                f"No existe tipo {item['tipo']} "
                f"para hotel {rfc_hotel}."
            )


def aplicar_costos_catalogo(rfc_hotel, detalle):
    """Aplica costos del catalogo oficial al detalle de la reservacion."""
    archivo = leer_archivo_json("tipos_cuarto.json", persistencia.DATA_DIR)
    for item in detalle:
        llave = f"{rfc_hotel}_{item['tipo']}"
        tc = archivo.get(llave)
        if tc is not None:
            item["costo"] = tc["costo"]
    return detalle
