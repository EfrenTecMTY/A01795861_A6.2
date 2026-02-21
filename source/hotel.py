# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:47:30 2026

@author: Efrén Alejandro
"""


class Hotel:
    """Representa un hotel."""

    def __init__(
        self,
        nombre,
        nombre_fiscal,
        rfc,
        direccion,
        estado,
        clasificacion,
        pisos,
        cuartos,
        estatus
    ):
        self.nombre = nombre
        self.nombre_fiscal = nombre_fiscal
        self.rfc = rfc
        self.direccion = direccion
        self.estado = estado
        self.clasificacion = clasificacion
        self.pisos = pisos
        self.cuartos = cuartos
        self.estatus = estatus

    @classmethod
    def crear(cls, nombre, nombre_fiscal, rfc, direccion,
              estado, clasificacion, pisos, cuartos, estatus):
        """Crea un hotel y lo persiste en archivo."""

    @classmethod
    def eliminar(cls, nombre):
        """Elimina un hotel del archivo por nombre."""

    def mostrar_info(self):
        """Muestra la informacion del hotel en consola."""

    def modificar(self, **kwargs):
        """Modifica los atributos del hotel y actualiza el archivo."""

    def reservar_cuarto(self, reservacion):
        """Registra una reservacion en el hotel."""

    def cancelar_reservacion(self, reservacion):
        """Cancela una reservacion del hotel."""
