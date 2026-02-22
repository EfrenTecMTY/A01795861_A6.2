# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:54:43 2026

@author: Efrén Alejandro
"""
from catalogos import TipoHabitacion
from persistencia import Persistencia


ARCHIVO_TIPOS_CUARTO = "tipos_cuarto.json"


class TipoCuarto(Persistencia):
    """Catalogo de tipos de cuarto por hotel."""
    def __init__(self, datos: dict):
        try:
            self.rfc_hotel = datos["rfc_hotel"]
            self.tipo = TipoHabitacion(datos["tipo"])
            self.costo = self._validar_costo(datos["costo"])
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
    def _validar_costo(costo):
        """Valida que el costo sea mayor a cero.
        Lanza ValueError si el costo es cero o negativo.
        """
        if costo <= 0:
            raise ValueError(
                f"El costo debe ser mayor a cero, se recibio: {costo}"
            )
        return costo

    # ------------------------------------------------------------------
    # Implementacion de propiedades abstractas
    # ------------------------------------------------------------------
    @property
    def archivo(self):
        """Archivo JSON donde se persisten los tipos de cuarto."""
        return ARCHIVO_TIPOS_CUARTO

    @property
    def id(self):
        """Identificador unico del tipo de cuarto."""
        return f"{self.rfc_hotel}_{self.tipo.value}"

    def _a_dict(self):
        """Convierte la instancia a diccionario serializable."""
        return {
            "rfc_hotel": self.rfc_hotel,
            "tipo": self.tipo.value,
            "costo": self.costo
        }

    # ------------------------------------------------------------------
    # Metodos de clase
    # ------------------------------------------------------------------
    @classmethod
    def buscar(cls, rfc_hotel, tipo):
        """Busca un tipo de cuarto, retorna dict o None si no existe."""
        tc_temp = cls.__new__(cls)
        tc_temp.rfc_hotel = rfc_hotel
        archivo = tc_temp._cargar()
        return archivo.get(f"{rfc_hotel}_{tipo}")

    @classmethod
    def crear(cls, datos: dict):
        """Crea un tipo de cuarto y lo persiste en archivo.
        Si ya existe el mismo tipo para el mismo hotel muestra error
        en consola y continua la ejecucion sin crear duplicado.
        """
        tipo_cuarto = cls(datos)
        archivo = tipo_cuarto._cargar()
        if tipo_cuarto.id in archivo:
            print(
                f"ERROR: Ya existe tipo {tipo_cuarto.tipo.value} "
                f"para hotel {tipo_cuarto.rfc_hotel}."
            )
            return None
        archivo[tipo_cuarto.id] = tipo_cuarto._a_dict()
        tipo_cuarto._guardar(archivo)
        return tipo_cuarto

    @classmethod
    def eliminar(cls, rfc_hotel, tipo):
        """Elimina un tipo de cuarto del archivo.
        Si no existe muestra error en consola y continua la ejecucion.
        """
        tipo_cuarto = cls.__new__(cls)
        tipo_cuarto.rfc_hotel = rfc_hotel
        tipo_cuarto.tipo = TipoHabitacion(tipo)
        archivo = tipo_cuarto._cargar()
        llave = f"{rfc_hotel}_{tipo}"
        if llave not in archivo:
            print(
                f"ERROR: No existe tipo {tipo} "
                f"para hotel {rfc_hotel}."
            )
            return False
        del archivo[llave]
        tipo_cuarto._guardar(archivo)
        return True

    # ------------------------------------------------------------------
    # Metodos de instancia
    # ------------------------------------------------------------------
    def mostrar_info(self):
        """Muestra la informacion del tipo de cuarto en consola."""
        print("-" * 40)
        print(f"Hotel RFC:  {self.rfc_hotel}")
        print(f"Tipo:       {self.tipo.value}")
        print(f"Costo:      {self.costo}")
        print("-" * 40)

    def modificar(self, **kwargs):
        """Modifica los atributos del tipo de cuarto y actualiza archivo.
        Atributos no modificables: rfc_hotel y tipo (son la llave unica).
        """
        campos_validos = {"costo"}
        archivo = self._cargar()
        if self.id not in archivo:
            print(f"ERROR: TipoCuarto {self.id} no encontrado.")
            return False
        for campo, valor in kwargs.items():
            if campo not in campos_validos:
                print(f"ERROR: Atributo '{campo}' no es modificable.")
                continue
            if campo == "costo":
                valor = self._validar_costo(valor)
            setattr(self, campo, valor)
            archivo[self.id][campo] = valor
        self._guardar(archivo)
        return True
