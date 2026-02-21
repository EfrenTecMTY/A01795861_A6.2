# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:54:43 2026

@author: Efrén Alejandro
"""


class TipoCuarto:
    """Catalogo de tipos de cuarto por hotel."""

    def __init__(self, hotel, tipo, costo):
        self.hotel = hotel
        self.tipo = tipo
        self.costo = costo
