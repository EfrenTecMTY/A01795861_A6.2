# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:44:54 2026

@author: Efrén Alejandro
"""

from enum import Enum


class ClasificacionHotel(Enum):
    """Clasificacion oficial de hoteles segun Sectur Mexico."""

    SIN_CATEGORIA = "SC"
    UNA_ESTRELLA = "1E"
    DOS_ESTRELLAS = "2E"
    TRES_ESTRELLAS = "3E"
    CUATRO_ESTRELLAS = "4E"
    CINCO_ESTRELLAS = "5E"
    GRAN_TURISMO = "GT"


class TipoHabitacion(Enum):
    """Catalogo de tipos de habitacion."""

    SENCILLA = "SENCILLA"
    DOBLE = "DOBLE"
    MATRIMONIAL = "MATRIMONIAL"
    TRIPLE = "TRIPLE"
    CUADRUPLE = "CUADRUPLE"
    ESTANDAR = "ESTANDAR"
    SUPERIOR = "SUPERIOR"
    DELUXE = "DELUXE"
    EJECUTIVA = "EJECUTIVA"
    JUNIOR_SUITE = "JUNIOR_SUITE"
    SUITE = "SUITE"
    SUITE_PRESIDENCIAL = "SUITE_PRESIDENCIAL"
