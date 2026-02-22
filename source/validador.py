# -*- coding: utf-8 -*-
"""Validaciones de integridad referencial entre entidades.
Created on Sat Feb 21 22:58:45 2026

@author: Efrén Alejandro
"""
from hotel import Hotel
from cliente import Cliente
from tipo_cuarto import TipoCuarto


def validar_hotel(rfc_hotel):
    """Valida que el hotel exista en el archivo."""
    if Hotel.buscar(rfc_hotel) is None:
        raise ValueError(f"No existe hotel con RFC {rfc_hotel}.")


def validar_cliente(rfc_cliente):
    """Valida que el cliente exista en el archivo."""
    if Cliente.buscar(rfc_cliente) is None:
        raise ValueError(f"No existe cliente con RFC {rfc_cliente}.")


def validar_tipos_cuarto(rfc_hotel, detalle):
    """Valida que cada tipo de cuarto del detalle exista para el hotel."""
    for item in detalle:
        if TipoCuarto.buscar(rfc_hotel, item["tipo"]) is None:
            raise ValueError(
                f"No existe tipo {item['tipo']} "
                f"para hotel {rfc_hotel}."
            )


def aplicar_costos_catalogo(rfc_hotel, detalle):
    """Aplica costos del catalogo oficial al detalle de la reservacion."""
    for item in detalle:
        tc = TipoCuarto.buscar(rfc_hotel, item["tipo"])
        item["costo"] = tc["costo"]
    return detalle
