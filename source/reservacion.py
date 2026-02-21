# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:52:32 2026

@author: Efrén Alejandro
"""


class Reservacion:
    """Representa una reservacion de hotel."""

    def __init__(
        self,
        hotel,
        cliente,
        fecha,
        noches,
        detalle,
        importe,
        es_pagado
    ):
        self.hotel = hotel
        self.cliente = cliente
        self.fecha = fecha
        self.noches = noches
        self.detalle = detalle
        self.importe = importe
        self.es_pagado = es_pagado

    @classmethod
    def crear(cls, hotel, cliente, fecha, noches, detalle):
        """Crea una reservacion y la persiste en archivo."""

    def cancelar(self):
        """Cancela la reservacion y actualiza el archivo."""
