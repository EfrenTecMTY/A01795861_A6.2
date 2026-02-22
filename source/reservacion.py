# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:52:32 2026

@author: Efrén Alejandro
"""
import uuid
from persistencia import Persistencia
from validador import (
    validar_hotel,
    validar_cliente,
    validar_tipos_cuarto,
    aplicar_costos_catalogo
)
from config import ARCHIVO_RESERVACIONES, SEPARADOR


class Reservacion(Persistencia):
    """Representa una reservacion de hotel."""
    def __init__(self, datos: dict):
        try:
            self.referencias = datos["referencias"]
            self.noches = self._validar_detalle(
                datos["detalle"], datos["noches"]
            )
            self.detalle = datos["detalle"]
            self.importe = datos["importe"]
            self.es_pagado = datos["es_pagado"]
            self.uuid = datos.get("uuid", str(uuid.uuid4()))
        except KeyError as e:
            print(f"ERROR: Campo requerido faltante: {e}")
            raise
        except ValueError as e:
            print(f"ERROR: Valor invalido: {e}")
            raise

    # ------------------------------------------------------------------
    # Metodos privados
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_detalle(detalle, noches):
        """Valida detalle y noches de la reservacion.
        Lanza ValueError si noches es cero o negativo, detalle esta
        vacio, o cantidad de algun item es invalida.
        """
        if noches <= 0:
            raise ValueError(
                f"Las noches deben ser mayor a cero: {noches}"
            )
        if not detalle:
            raise ValueError("El detalle no puede estar vacio.")
        for item in detalle:
            if item["cantidad"] <= 0:
                raise ValueError(
                    f"La cantidad debe ser mayor a cero: {item['cantidad']}"
                )
        return noches

    @staticmethod
    def _calcular_importe(detalle, noches):
        """Calcula el importe total de la reservacion."""
        return sum(
            d["costo"] * d["cantidad"] * noches
            for d in detalle
        )

    # ------------------------------------------------------------------
    # Implementacion de propiedades abstractas
    # ------------------------------------------------------------------
    @property
    def archivo(self):
        """Archivo JSON donde se persisten las reservaciones."""
        return ARCHIVO_RESERVACIONES

    @property
    def id(self):
        """Identificador unico de la reservacion."""
        return self.uuid

    def _a_dict(self):
        """Convierte la instancia a diccionario serializable."""
        return {
            "uuid": self.uuid,
            "referencias": self.referencias,
            "noches": self.noches,
            "detalle": self.detalle,
            "importe": self.importe,
            "es_pagado": self.es_pagado
        }

    # ------------------------------------------------------------------
    # Metodos de clase
    # ------------------------------------------------------------------
    @classmethod
    def buscar(cls, uuid_res):
        """Busca una reservacion por UUID, retorna dict o None si no existe."""
        res_temp = cls.__new__(cls)
        res_temp.uuid = uuid_res
        archivo = res_temp._cargar()
        return archivo.get(uuid_res)

    @classmethod
    def buscar_por_referencia(cls, nemotecnica):
        """Busca una reservacion por referencia nemotecnica.
        Retorna dict o None si no existe.
        """
        res_temp = cls.__new__(cls)
        res_temp.uuid = None
        archivo = res_temp._cargar()
        for reservacion in archivo.values():
            if reservacion["referencias"]["nemotecnica"] == nemotecnica:
                return reservacion
        return None

    @classmethod
    def crear(cls, datos: dict):
        """Crea una reservacion y la persiste en archivo.
        Valida existencia de hotel, cliente y tipos de cuarto.
        Aplica costos del catalogo al momento de crear.
        Calcula el importe automaticamente.
        """
        try:
            validar_hotel(datos["rfc_hotel"])
            validar_cliente(datos["rfc_cliente"])
            validar_tipos_cuarto(datos["rfc_hotel"], datos["detalle"])
        except ValueError as e:
            print(f"ERROR: {e}")
            return None

        datos["detalle"] = aplicar_costos_catalogo(
            datos["rfc_hotel"], datos["detalle"]
        )
        datos["importe"] = cls._calcular_importe(
            datos["detalle"], datos["noches"]
        )
        datos["es_pagado"] = datos.get("es_pagado", False)
        datos["referencias"] = {
            "rfc_hotel": datos["rfc_hotel"],
            "rfc_cliente": datos["rfc_cliente"],
            "fecha": datos["fecha"],
            "nemotecnica": (
                f"{datos['rfc_hotel']}_{datos['rfc_cliente']}_{datos['fecha']}"
            )
        }
        reservacion = cls(datos)
        archivo = reservacion._cargar()
        archivo[reservacion.uuid] = reservacion._a_dict()
        reservacion._guardar(archivo)
        return reservacion

    # ------------------------------------------------------------------
    # Metodos de instancia
    # ------------------------------------------------------------------
    def cancelar(self):
        """Cancela la reservacion eliminandola del archivo.
        Muestra error en consola si no existe y continua la ejecucion.
        """
        archivo = self._cargar()
        if self.uuid not in archivo:
            print(
                f"ERROR: No existe reservacion con UUID {self.uuid}."
            )
            return False
        del archivo[self.uuid]
        self._guardar(archivo)
        return True

    def mostrar_info(self):
        """Muestra la informacion de la reservacion en consola."""
        print(SEPARADOR)
        print(f"UUID:        {self.uuid}")
        print(f"Referencia:  {self.referencias['nemotecnica']}")
        print(f"Hotel RFC:   {self.referencias['rfc_hotel']}")
        print(f"Cliente RFC: {self.referencias['rfc_cliente']}")
        print(f"Fecha:       {self.referencias['fecha']}")
        print(f"Noches:      {self.noches}")
        print(f"Importe:     {self.importe}")
        print(f"Pagado:      {self.es_pagado}")
        print(SEPARADOR)
        for item in self.detalle:
            print(
                f"  Tipo: {item['tipo']} | "
                f"Cantidad: {item['cantidad']} | "
                f"Costo: {item['costo']}"
            )
        print(SEPARADOR)
