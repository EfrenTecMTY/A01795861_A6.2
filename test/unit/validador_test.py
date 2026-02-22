# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 01:37:13 2026

@author: Efrén Alejandro
"""
# flake8: noqa: E402
import os
import sys

sys.path.insert(  # pylint: disable=wrong-import-position
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "source")
    )
)

import unittest

import persistencia
from hotel import Hotel
from cliente import Cliente
from tipo_cuarto import TipoCuarto
from validador import (
    validar_hotel,
    validar_cliente,
    validar_tipos_cuarto,
    aplicar_costos_catalogo
)


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_HOTELES = os.path.join(TEST_DATA_DIR, "hoteles.json")
ARCHIVO_CLIENTES = os.path.join(TEST_DATA_DIR, "clientes.json")
ARCHIVO_TIPOS = os.path.join(TEST_DATA_DIR, "tipos_cuarto.json")


def setup_archivos():
    """Crea hotel, cliente y tipo de cuarto de prueba."""
    Hotel.crear({
        "nombre": "Hotel Prueba",
        "nombre_fiscal": "Prueba SA",
        "rfc": "CAM123456ABC",
        "direccion": "Calle 1",
        "estado": "Jalisco",
        "clasificacion": "5E",
        "estatus": "activo"
    })
    Cliente.crear({
        "nombre": "Juan Perez",
        "rfc": "PEJJ800101ABC",
        "sexo": "M",
        "compania": "Empresa SA",
        "forma_pago": "tarjeta",
        "estatus": "activo"
    })
    TipoCuarto.crear({
        "rfc_hotel": "CAM123456ABC",
        "tipo": "DOBLE",
        "costo": 1500.00
    })


class TestValidarHotel(unittest.TestCase):
    """Pruebas para validar_hotel."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)
        setup_archivos()

    def tearDown(self):
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_validar_hotel_existente(self):
        """Verifica que no lanza excepcion con hotel existente."""
        try:
            validar_hotel("CAM123456ABC")
        except ValueError:
            self.fail("validar_hotel lanzo ValueError inesperadamente.")

    def test_validar_hotel_inexistente(self):
        """Verifica que lanza ValueError con hotel inexistente."""
        with self.assertRaises(ValueError):
            validar_hotel("RFC_INEXISTENTE")

    def test_validar_hotel_inexistente_mensaje(self):
        """Verifica el mensaje de error con hotel inexistente."""
        with self.assertRaises(ValueError) as ctx:
            validar_hotel("RFC_INEXISTENTE")
        self.assertIn("RFC_INEXISTENTE", str(ctx.exception))


class TestValidarCliente(unittest.TestCase):
    """Pruebas para validar_cliente."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)
        setup_archivos()

    def tearDown(self):
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_validar_cliente_existente(self):
        """Verifica que no lanza excepcion con cliente existente."""
        try:
            validar_cliente("PEJJ800101ABC")
        except ValueError:
            self.fail("validar_cliente lanzo ValueError inesperadamente.")

    def test_validar_cliente_inexistente(self):
        """Verifica que lanza ValueError con cliente inexistente."""
        with self.assertRaises(ValueError):
            validar_cliente("RFC_INEXISTENTE")

    def test_validar_cliente_inexistente_mensaje(self):
        """Verifica el mensaje de error con cliente inexistente."""
        with self.assertRaises(ValueError) as ctx:
            validar_cliente("RFC_INEXISTENTE")
        self.assertIn("RFC_INEXISTENTE", str(ctx.exception))


class TestValidarTiposCuarto(unittest.TestCase):
    """Pruebas para validar_tipos_cuarto."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)
        setup_archivos()

    def tearDown(self):
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_validar_tipos_cuarto_existente(self):
        """Verifica que no lanza excepcion con tipo existente."""
        detalle = [{"tipo": "DOBLE", "cantidad": 1, "costo": 1500.00}]
        try:
            validar_tipos_cuarto("CAM123456ABC", detalle)
        except ValueError:
            self.fail("validar_tipos_cuarto lanzo ValueError inesperadamente.")

    def test_validar_tipos_cuarto_inexistente(self):
        """Verifica que lanza ValueError con tipo inexistente."""
        detalle = [{"tipo": "SUITE", "cantidad": 1, "costo": 3000.00}]
        with self.assertRaises(ValueError):
            validar_tipos_cuarto("CAM123456ABC", detalle)

    def test_validar_tipos_cuarto_inexistente_mensaje(self):
        """Verifica el mensaje de error con tipo inexistente."""
        detalle = [{"tipo": "SUITE", "cantidad": 1, "costo": 3000.00}]
        with self.assertRaises(ValueError) as ctx:
            validar_tipos_cuarto("CAM123456ABC", detalle)
        self.assertIn("SUITE", str(ctx.exception))

    def test_validar_multiples_tipos_uno_inexistente(self):
        """Verifica que lanza ValueError si algún tipo no existe."""
        detalle = [
            {"tipo": "DOBLE", "cantidad": 1, "costo": 1500.00},
            {"tipo": "SUITE", "cantidad": 1, "costo": 3000.00}
        ]
        with self.assertRaises(ValueError):
            validar_tipos_cuarto("CAM123456ABC", detalle)


class TestAplicarCostosCatalogo(unittest.TestCase):
    """Pruebas para aplicar_costos_catalogo."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)
        setup_archivos()

    def tearDown(self):
        for archivo in [ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_aplicar_costos_sobreescribe_costo(self):
        """Verifica que el costo del catalogo sobreescribe el del detalle."""
        detalle = [{"tipo": "DOBLE", "cantidad": 1, "costo": 999.00}]
        resultado = aplicar_costos_catalogo("CAM123456ABC", detalle)
        self.assertEqual(resultado[0]["costo"], 1500.00)

    def test_aplicar_costos_tipo_inexistente_no_modifica(self):
        """Verifica que tipo inexistente no modifica el detalle."""
        detalle = [{"tipo": "SUITE", "cantidad": 1, "costo": 999.00}]
        resultado = aplicar_costos_catalogo("CAM123456ABC", detalle)
        self.assertEqual(resultado[0]["costo"], 999.00)

    def test_aplicar_costos_retorna_detalle(self):
        """Verifica que retorna el detalle actualizado."""
        detalle = [{"tipo": "DOBLE", "cantidad": 1, "costo": 999.00}]
        resultado = aplicar_costos_catalogo("CAM123456ABC", detalle)
        self.assertIsInstance(resultado, list)


if __name__ == "__main__":
    unittest.main()
