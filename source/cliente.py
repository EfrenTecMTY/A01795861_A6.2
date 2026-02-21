# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:51:12 2026

@author: Efrén Alejandro
"""


class Cliente:
    """Representa un cliente."""

    def __init__(
        self,
        nombre,
        sexo,
        compania,
        forma_pago,
        estatus
    ):
        self.nombre = nombre
        self.sexo = sexo
        self.compania = compania
        self.forma_pago = forma_pago
        self.estatus = estatus

    @classmethod
    def crear(cls, nombre, sexo, compania, forma_pago, estatus):
        """Crea un cliente y lo persiste en archivo."""

    @classmethod
    def eliminar(cls, nombre):
        """Elimina un cliente del archivo por nombre."""

    def mostrar_info(self):
        """Muestra la informacion del cliente en consola."""

    def modificar(self, **kwargs):
        """Modifica los atributos del cliente y actualiza el archivo."""
