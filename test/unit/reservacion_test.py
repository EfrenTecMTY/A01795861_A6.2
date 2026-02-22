# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 21:26:08 2026

@author: Efrén Alejandro
"""
# flake8: noqa: E402
# test/unit/reservacion_test.py
import os
import sys

sys.path.insert(  # pylint: disable=wrong-import-position
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "source")
    )
)

import json
import unittest
from unittest.mock import patch

import persistencia
from hotel import Hotel
from cliente import Cliente
from tipo_cuarto import TipoCuarto
from reservacion import Reservacion


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_TEST = os.path.join(TEST_DATA_DIR, "reservaciones.json")
ARCHIVO_HOTELES = os.path.join(TEST_DATA_DIR, "hoteles.json")
ARCHIVO_CLIENTES = os.path.join(TEST_DATA_DIR, "clientes.json")
ARCHIVO_TIPOS = os.path.join(TEST_DATA_DIR, "tipos_cuarto.json")

ARCHIVOS = [ARCHIVO_TEST, ARCHIVO_HOTELES, ARCHIVO_CLIENTES, ARCHIVO_TIPOS]


def crear_entidades_prueba():
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


def datos_reservacion_valido():
    """Retorna un diccionario con datos validos de reservacion."""
    return {
        "rfc_hotel": "CAM123456ABC",
        "rfc_cliente": "PEJJ800101ABC",
        "fecha": "2026-03-01",
        "noches": 3,
        "detalle": [
            {"tipo": "DOBLE", "cantidad": 2, "costo": 0}
        ]
    }


class TestReservacionInit(unittest.TestCase):
    """Pruebas para el constructor de Reservacion."""

    def _datos_completos(self):
        """Crea datos completos con referencias para instanciar Reservacion."""
        return {
            "referencias": {
                "rfc_hotel": "CAM123456ABC",
                "rfc_cliente": "PEJJ800101ABC",
                "fecha": "2026-03-01",
                "nemotecnica": "CAM123456ABC_PEJJ800101ABC_2026-03-01"
            },
            "noches": 3,
            "detalle": [{"tipo": "DOBLE", "cantidad": 2, "costo": 1500.00}],
            "importe": 9000.00,
            "es_pagado": False
        }

    def test_init_exitoso(self):
        """Verifica que la reservacion se crea con datos validos."""
        res = Reservacion(self._datos_completos())
        self.assertIsNotNone(res.uuid)
        self.assertIsNotNone(res.referencias)
        self.assertEqual(res.noches, 3)

    def test_init_genera_uuid(self):
        """Verifica que se genera un UUID automaticamente."""
        res = Reservacion(self._datos_completos())
        self.assertEqual(len(res.uuid), 36)

    def test_init_uuid_existente_se_respeta(self):
        """Verifica que un UUID existente no se sobreescribe."""
        datos = self._datos_completos()
        datos["uuid"] = "uuid-fijo-1234"
        res = Reservacion(datos)
        self.assertEqual(res.uuid, "uuid-fijo-1234")

    def test_init_referencias_contiene_rfc_hotel(self):
        """Verifica que referencias contiene rfc_hotel."""
        res = Reservacion(self._datos_completos())
        self.assertEqual(res.referencias["rfc_hotel"], "CAM123456ABC")

    def test_init_referencias_contiene_nemotecnica(self):
        """Verifica que referencias contiene la clave nemotecnica."""
        res = Reservacion(self._datos_completos())
        self.assertIn("CAM123456ABC", res.referencias["nemotecnica"])

    def test_init_campo_faltante(self):
        """Verifica que se lanza KeyError si falta un campo requerido."""
        datos = self._datos_completos()
        del datos["noches"]
        with self.assertRaises(KeyError):
            Reservacion(datos)

    def test_init_campo_faltante_muestra_error(self):
        """Verifica que se muestra error en consola si falta un campo."""
        datos = self._datos_completos()
        del datos["noches"]
        with patch("builtins.print") as mock_print:
            with self.assertRaises(KeyError):
                Reservacion(datos)
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_init_noches_cero_lanza_error(self):
        """Verifica que se lanza ValueError con noches cero."""
        datos = self._datos_completos()
        datos["noches"] = 0
        with self.assertRaises(ValueError):
            Reservacion(datos)

    def test_init_noches_negativas_lanza_error(self):
        """Verifica que se lanza ValueError con noches negativas."""
        datos = self._datos_completos()
        datos["noches"] = -1
        with self.assertRaises(ValueError):
            Reservacion(datos)

    def test_init_detalle_vacio_lanza_error(self):
        """Verifica que se lanza ValueError con detalle vacio."""
        datos = self._datos_completos()
        datos["detalle"] = []
        with self.assertRaises(ValueError):
            Reservacion(datos)

    def test_init_cantidad_cero_lanza_error(self):
        """Verifica que se lanza ValueError con cantidad cero en detalle."""
        datos = self._datos_completos()
        datos["detalle"] = [
            {"tipo": "DOBLE", "cantidad": 0, "costo": 1500.00}
        ]
        with self.assertRaises(ValueError):
            Reservacion(datos)

    def test_init_valor_invalido_muestra_error(self):
        """Verifica que se muestra error en consola con valor invalido."""
        datos = self._datos_completos()
        datos["noches"] = 0
        with patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError):
                Reservacion(datos)
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)


class TestReservacionCrear(unittest.TestCase):
    """Pruebas para Reservacion.crear."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)
        crear_entidades_prueba()

    def tearDown(self):
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_crear_reservacion_exitoso(self):
        """Verifica que se crea y persiste una reservacion correctamente."""
        res = Reservacion.crear(datos_reservacion_valido())
        self.assertIsNotNone(res)
        self.assertTrue(os.path.exists(ARCHIVO_TEST))
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertIn(res.uuid, datos)

    def test_crear_aplica_costo_catalogo(self):
        """Verifica que el costo se toma del catalogo ignorando el enviado."""
        res = Reservacion.crear(datos_reservacion_valido())
        self.assertEqual(res.detalle[0]["costo"], 1500.00)

    def test_crear_calcula_importe(self):
        """Verifica que el importe se calcula automaticamente."""
        res = Reservacion.crear(datos_reservacion_valido())
        # 2 cuartos * 1500 costo * 3 noches = 9000
        self.assertEqual(res.importe, 9000.00)

    def test_crear_es_pagado_default_false(self):
        """Verifica que es_pagado es False por defecto."""
        res = Reservacion.crear(datos_reservacion_valido())
        self.assertFalse(res.es_pagado)

    def test_crear_guarda_referencias(self):
        """Verifica que se persiste el dict referencias en archivo."""
        res = Reservacion.crear(datos_reservacion_valido())
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertIn("referencias", datos[res.uuid])
        self.assertEqual(
            datos[res.uuid]["referencias"]["rfc_hotel"], "CAM123456ABC"
        )

    def test_crear_dos_reservaciones_distintas(self):
        """Verifica que se pueden crear dos reservaciones distintas."""
        Reservacion.crear(datos_reservacion_valido())
        Reservacion.crear(datos_reservacion_valido())
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 2)

    def test_crear_retorna_instancia_reservacion(self):
        """Verifica que crear retorna una instancia de Reservacion."""
        res = Reservacion.crear(datos_reservacion_valido())
        self.assertIsInstance(res, Reservacion)

    def test_crear_hotel_inexistente_retorna_none(self):
        """Verifica que retorna None si el hotel no existe."""
        datos = datos_reservacion_valido()
        datos["rfc_hotel"] = "RFC_INEXISTENTE"
        resultado = Reservacion.crear(datos)
        self.assertIsNone(resultado)

    def test_crear_hotel_inexistente_muestra_error(self):
        """Verifica que muestra error si el hotel no existe."""
        datos = datos_reservacion_valido()
        datos["rfc_hotel"] = "RFC_INEXISTENTE"
        with patch("builtins.print") as mock_print:
            Reservacion.crear(datos)
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_crear_cliente_inexistente_retorna_none(self):
        """Verifica que retorna None si el cliente no existe."""
        datos = datos_reservacion_valido()
        datos["rfc_cliente"] = "RFC_INEXISTENTE"
        resultado = Reservacion.crear(datos)
        self.assertIsNone(resultado)

    def test_crear_tipo_cuarto_inexistente_retorna_none(self):
        """Verifica que retorna None si el tipo de cuarto no existe."""
        datos = datos_reservacion_valido()
        datos["detalle"] = [
            {"tipo": "SUITE", "cantidad": 1, "costo": 0}
        ]
        resultado = Reservacion.crear(datos)
        self.assertIsNone(resultado)

    def test_crear_noches_cero_lanza_error(self):
        """Verifica que no se crea reservacion con noches cero."""
        datos = datos_reservacion_valido()
        datos["noches"] = 0
        with self.assertRaises(ValueError):
            Reservacion.crear(datos)

    def test_crear_multiples_tipos_cuarto(self):
        """Verifica que se puede crear reservacion con varios tipos."""
        TipoCuarto.crear({
            "rfc_hotel": "CAM123456ABC",
            "tipo": "SUITE",
            "costo": 3000.00
        })
        datos = datos_reservacion_valido()
        datos["detalle"] = [
            {"tipo": "DOBLE", "cantidad": 1, "costo": 0},
            {"tipo": "SUITE", "cantidad": 1, "costo": 0}
        ]
        res = Reservacion.crear(datos)
        # (1*1500 + 1*3000) * 3 noches = 13500
        self.assertEqual(res.importe, 13500.00)


class TestReservacionCancelar(unittest.TestCase):
    """Pruebas para Reservacion.cancelar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)
        crear_entidades_prueba()
        self.res = Reservacion.crear(datos_reservacion_valido())

    def tearDown(self):
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_cancelar_exitoso(self):
        """Verifica que se cancela una reservacion existente."""
        resultado = self.res.cancelar()
        self.assertTrue(resultado)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertNotIn(self.res.uuid, datos)

    def test_cancelar_inexistente_retorna_false(self):
        """Verifica que retorna False al cancelar reservacion inexistente."""
        self.res.cancelar()
        resultado = self.res.cancelar()
        self.assertFalse(resultado)

    def test_cancelar_inexistente_muestra_error(self):
        """Verifica que se muestra error al cancelar reservacion inexistente."""
        self.res.cancelar()
        with patch("builtins.print") as mock_print:
            self.res.cancelar()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)


class TestReservacionBuscar(unittest.TestCase):
    """Pruebas para Reservacion.buscar y buscar_por_referencia."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)
        crear_entidades_prueba()
        self.res = Reservacion.crear(datos_reservacion_valido())

    def tearDown(self):
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_buscar_por_uuid_existente(self):
        """Verifica que buscar retorna dict de reservacion existente."""
        resultado = Reservacion.buscar(self.res.uuid)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["uuid"], self.res.uuid)

    def test_buscar_por_uuid_inexistente(self):
        """Verifica que buscar retorna None si no existe."""
        resultado = Reservacion.buscar("uuid-inexistente")
        self.assertIsNone(resultado)

    def test_buscar_por_referencia_existente(self):
        """Verifica que buscar_por_referencia retorna la reservacion."""
        nemotecnica = self.res.referencias["nemotecnica"]
        resultado = Reservacion.buscar_por_referencia(nemotecnica)
        self.assertIsNotNone(resultado)

    def test_buscar_por_referencia_inexistente(self):
        """Verifica que buscar_por_referencia retorna None si no existe."""
        resultado = Reservacion.buscar_por_referencia("REF_INEXISTENTE")
        self.assertIsNone(resultado)


class TestReservacionMostrarInfo(unittest.TestCase):
    """Pruebas para Reservacion.mostrar_info."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)
        crear_entidades_prueba()

    def tearDown(self):
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_mostrar_info_imprime_uuid(self):
        """Verifica que mostrar_info imprime el UUID."""
        res = Reservacion.crear(datos_reservacion_valido())
        with patch("builtins.print") as mock_print:
            res.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn(res.uuid, salida)

    def test_mostrar_info_imprime_referencia(self):
        """Verifica que mostrar_info imprime la referencia nemotecnica."""
        res = Reservacion.crear(datos_reservacion_valido())
        with patch("builtins.print") as mock_print:
            res.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn(res.referencias["nemotecnica"], salida)

    def test_mostrar_info_imprime_importe(self):
        """Verifica que mostrar_info imprime el importe."""
        res = Reservacion.crear(datos_reservacion_valido())
        with patch("builtins.print") as mock_print:
            res.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("9000", salida)

    def test_mostrar_info_imprime_detalle(self):
        """Verifica que mostrar_info imprime el detalle de cuartos."""
        res = Reservacion.crear(datos_reservacion_valido())
        with patch("builtins.print") as mock_print:
            res.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("DOBLE", salida)


class TestReservacionArchivoCorrupto(unittest.TestCase):
    """Pruebas para comportamiento con archivo corrupto y sin archivo."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)
        crear_entidades_prueba()

    def tearDown(self):
        for archivo in ARCHIVOS:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_cancelar_sin_archivo_retorna_false(self):
        """Verifica que cancelar funciona correctamente sin archivo."""
        res = Reservacion.crear(datos_reservacion_valido())
        os.remove(ARCHIVO_TEST)
        resultado = res.cancelar()
        self.assertFalse(resultado)

    def test_crear_con_archivo_corrupto_retorna_reservacion(self):
        """Verifica que crear maneja JSON invalido y crea la reservacion."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        resultado = Reservacion.crear(datos_reservacion_valido())
        self.assertIsNotNone(resultado)

    def test_crear_con_archivo_corrupto_muestra_error(self):
        """Verifica que se muestra error en consola con JSON invalido."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        with patch("builtins.print") as mock_print:
            Reservacion.crear(datos_reservacion_valido())
            llamadas = [str(c) for c in mock_print.call_args_list]
            self.assertTrue(any("ERROR" in c for c in llamadas))


if __name__ == "__main__":
    unittest.main()
