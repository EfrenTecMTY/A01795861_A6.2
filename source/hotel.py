# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:47:30 2026

@author: Efrén Alejandro
"""
from catalogos import ClasificacionHotel
from persistencia import Persistencia


ARCHIVO_HOTELES = "hoteles.json"


class Hotel(Persistencia):
    """Representa un hotel."""

    def __init__(self, datos: dict):
        try:
            self.nombre = datos["nombre"]
            self.nombre_fiscal = datos["nombre_fiscal"]
            self.rfc = datos["rfc"]
            self.direccion = datos["direccion"]
            self.estado = datos["estado"]
            self.clasificacion = ClasificacionHotel(datos["clasificacion"])
            self.estatus = datos["estatus"]
        except KeyError as e:
            print(f"ERROR: Campo requerido faltante: {e}")
            raise
        except ValueError as e:
            print(f"ERROR: Valor invalido en clasificacion: {e}")
            raise

    @property
    def archivo(self):
        """Archivo JSON donde se persisten los hoteles."""
        return ARCHIVO_HOTELES

    @property
    def id(self):
        """Identificador unico del hotel."""
        return self.rfc

    def _a_dict(self):
        """Convierte la instancia a diccionario serializable."""
        return {
            "nombre": self.nombre,
            "nombre_fiscal": self.nombre_fiscal,
            "rfc": self.rfc,
            "direccion": self.direccion,
            "estado": self.estado,
            "clasificacion": self.clasificacion.value,
            "estatus": self.estatus,
            "reservaciones": []
        }

    @classmethod
    def buscar(cls, rfc):
        """Busca un hotel por RFC, retorna dict o None si no existe."""
        hotel_temp = cls.__new__(cls)
        hotel_temp.rfc = rfc
        archivo = hotel_temp._cargar()
        return archivo.get(rfc)

    @classmethod
    def crear(cls, datos: dict):
        """Crea un hotel y lo persiste en archivo.

        Si ya existe un hotel con el mismo RFC muestra error en consola
        y continua la ejecucion sin crear duplicado.
        """
        hotel = cls(datos)
        archivo = hotel._cargar()
        if hotel.rfc in archivo:
            print(f"ERROR: Ya existe un hotel con RFC {hotel.rfc}.")
            return None
        archivo[hotel.rfc] = hotel._a_dict()
        hotel._guardar(archivo)
        return hotel

    @classmethod
    def eliminar(cls, rfc):
        """Elimina un hotel del archivo por RFC.

        Si no existe el hotel muestra error en consola
        y continua la ejecucion.
        """
        hotel = cls.__new__(cls)
        hotel.rfc = rfc
        archivo = hotel._cargar()
        if rfc not in archivo:
            print(f"ERROR: No existe un hotel con RFC {rfc}.")
            return False
        del archivo[rfc]
        hotel._guardar(archivo)
        return True

    def mostrar_info(self):
        """Muestra la informacion del hotel en consola."""
        print("-" * 40)
        print(f"Nombre:         {self.nombre}")
        print(f"Nombre Fiscal:  {self.nombre_fiscal}")
        print(f"RFC:            {self.rfc}")
        print(f"Direccion:      {self.direccion}")
        print(f"Estado:         {self.estado}")
        print(f"Clasificacion:  {self.clasificacion.value}")
        print(f"Estatus:        {self.estatus}")
        print("-" * 40)

    def modificar(self, **kwargs):
        """Modifica los atributos del hotel y actualiza el archivo.

        Atributo no modificable: rfc (es la llave unica).
        """
        campos_validos = {
            "nombre", "nombre_fiscal", "direccion",
            "estado", "clasificacion", "estatus"
        }
        archivo = self._cargar()
        if self.rfc not in archivo:
            print(f"ERROR: Hotel con RFC {self.rfc} no encontrado.")
            return False
        for campo, valor in kwargs.items():
            if campo not in campos_validos:
                print(f"ERROR: Atributo '{campo}' no es modificable.")
                continue
            setattr(self, campo, valor)
            archivo[self.rfc][campo] = (
                valor.value if hasattr(valor, "value") else valor
            )
        self._guardar(archivo)
        return True

    def reservar_cuarto(self, reservacion):
        """Registra una reservacion en el archivo del hotel.

        Si ya existe una reservacion con el mismo id muestra error
        y continua la ejecucion.
        """
        archivo = self._cargar()
        if self.rfc not in archivo:
            print(f"ERROR: Hotel con RFC {self.rfc} no encontrado.")
            return False
        reservaciones = archivo[self.rfc].get("reservaciones", [])
        if reservacion.id in [r["id"] for r in reservaciones]:
            print(
                f"ERROR: Ya existe reservacion con id {reservacion.id}."
            )
            return False
        reservaciones.append({"id": reservacion.id})
        archivo[self.rfc]["reservaciones"] = reservaciones
        self._guardar(archivo)
        return True

    def cancelar_reservacion(self, reservacion):
        """
        Cancela una reservacion del hotel en el archivo.
        """
        return reservacion.cancelar()
