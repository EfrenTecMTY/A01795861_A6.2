# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 22:25:43 2026

@author: Efrén Alejandro
"""
import json
import os
from abc import ABC, abstractmethod
from lector_json import leer_archivo_json


DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")


class Persistencia(ABC):
    """Clase base abstracta para persistencia de entidades en archivos JSON."""

    @property
    @abstractmethod
    def archivo(self):
        """Nombre del archivo JSON donde se persiste la entidad."""

    @property
    @abstractmethod
    def id(self):
        """Identificador unico de la instancia."""

    @abstractmethod
    def _a_dict(self):
        """Convierte la instancia a diccionario serializable."""

    def _ruta_archivo(self):
        """Retorna la ruta completa del archivo JSON."""
        return os.path.join(DATA_DIR, self.archivo)

    def _cargar(self):
        # """Carga el archivo JSON y retorna el diccionario."""
        # ruta = self._ruta_archivo()
        # if not os.path.exists(ruta):
        #     return {}
        # try:
        #     with open(ruta, "r", encoding="utf-8") as f:
        #         return json.load(f)
        # except json.JSONDecodeError as e:
        #     print(f"ERROR: Archivo {self.archivo} corrupto: {e}")
        #     return {}
        return leer_archivo_json(self.archivo, DATA_DIR)

    def _guardar(self, datos):
        """Guarda el diccionario en el archivo JSON."""
        ruta = self._ruta_archivo()
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except OSError as e:
            print(f"ERROR: No se pudo guardar {self.archivo}: {e}")
