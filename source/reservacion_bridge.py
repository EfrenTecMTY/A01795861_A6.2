# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 00:18:10 2026

@author: Efrén Alejandro
"""
from reservacion import Reservacion


def crear_reservacion(datos):
    """Crea una reservacion delegando a Reservacion.crear."""
    return Reservacion.crear(datos)


def cancelar_reservacion(reservacion):
    """Cancela una reservacion delegando a Reservacion.cancelar."""
    return reservacion.cancelar()
