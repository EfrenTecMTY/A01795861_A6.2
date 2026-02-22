# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 21:51:12 2026

@author: Efrén Alejandro
"""


from persistencia import Persistencia


ARCHIVO_CLIENTES = "clientes.json"


class Cliente(Persistencia):
    """Representa un cliente."""

    def __init__(self, datos: dict):
        try:
            self.nombre = datos["nombre"]
            self.rfc = datos["rfc"]
            self.sexo = datos["sexo"]
            self.compania = datos["compania"]
            self.forma_pago = datos["forma_pago"]
            self.estatus = datos["estatus"]
        except KeyError as e:
            print(f"ERROR: Campo requerido faltante: {e}")
            raise

    # ------------------------------------------------------------------
    # Implementacion de propiedades abstractas
    # ------------------------------------------------------------------

    @property
    def archivo(self):
        """Archivo JSON donde se persisten los clientes."""
        return ARCHIVO_CLIENTES

    @property
    def id(self):
        """Identificador unico del cliente."""
        return self.rfc

    def _a_dict(self):
        """Convierte la instancia a diccionario serializable."""
        return {
            "nombre": self.nombre,
            "rfc": self.rfc,
            "sexo": self.sexo,
            "compania": self.compania,
            "forma_pago": self.forma_pago,
            "estatus": self.estatus
        }

    # ------------------------------------------------------------------
    # Metodos de clase
    # ------------------------------------------------------------------
    @classmethod
    def buscar(cls, rfc):
        """Busca un cliente por RFC, retorna dict o None si no existe."""
        cliente_temp = cls.__new__(cls)
        cliente_temp.rfc = rfc
        archivo = cliente_temp._cargar()
        return archivo.get(rfc)

    @classmethod
    def crear(cls, datos: dict):
        """Crea un cliente y lo persiste en archivo.

        Si ya existe un cliente con el mismo RFC muestra error
        en consola y continua la ejecucion sin crear duplicado.
        """
        cliente = cls(datos)
        archivo = cliente._cargar()
        if cliente.rfc in archivo:
            print(f"ERROR: Ya existe un cliente con RFC {cliente.rfc}.")
            return None
        archivo[cliente.rfc] = cliente._a_dict()
        cliente._guardar(archivo)
        return cliente

    @classmethod
    def eliminar(cls, rfc):
        """Elimina un cliente del archivo por RFC.

        Si no existe el cliente muestra error en consola
        y continua la ejecucion.
        """
        cliente = cls.__new__(cls)
        cliente.rfc = rfc
        archivo = cliente._cargar()
        if rfc not in archivo:
            print(f"ERROR: No existe un cliente con RFC {rfc}.")
            return False
        del archivo[rfc]
        cliente._guardar(archivo)
        return True

    # ------------------------------------------------------------------
    # Metodos de instancia
    # ------------------------------------------------------------------

    def mostrar_info(self):
        """Muestra la informacion del cliente en consola."""
        print("-" * 40)
        print(f"Nombre:      {self.nombre}")
        print(f"RFC:         {self.rfc}")
        print(f"Sexo:        {self.sexo}")
        print(f"Compania:    {self.compania}")
        print(f"Forma Pago:  {self.forma_pago}")
        print(f"Estatus:     {self.estatus}")
        print("-" * 40)

    def modificar(self, **kwargs):
        """Modifica los atributos del cliente y actualiza el archivo.

        Atributo no modificable: rfc (es la llave unica).
        """
        campos_validos = {
            "nombre", "sexo", "compania", "forma_pago", "estatus"
        }
        archivo = self._cargar()
        if self.rfc not in archivo:
            print(f"ERROR: Cliente con RFC {self.rfc} no encontrado.")
            return False
        for campo, valor in kwargs.items():
            if campo not in campos_validos:
                print(f"ERROR: Atributo '{campo}' no es modificable.")
                continue
            setattr(self, campo, valor)
            archivo[self.rfc][campo] = valor
        self._guardar(archivo)
        return True
