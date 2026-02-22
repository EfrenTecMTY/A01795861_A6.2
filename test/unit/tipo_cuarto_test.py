# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 16:25:29 2026

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


import json
from unittest.mock import patch
import unittest


from tipo_cuarto import TipoCuarto
from catalogos import TipoHabitacion
import persistencia


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_TEST = os.path.join(TEST_DATA_DIR, "tipos_cuarto.json")


def datos_tipo_cuarto_valido():
    """Retorna un diccionario con datos validos de tipo de cuarto."""
    return {
        "rfc_hotel": "CAM123456ABC",
        "tipo": "DOBLE",
        "costo": 1500.00
    }


class TestTipoCuartoInit(unittest.TestCase):
    """Pruebas para el constructor de TipoCuarto."""

    def test_init_exitoso(self):
        """Verifica que el tipo de cuarto se crea con datos validos."""
        tc = TipoCuarto(datos_tipo_cuarto_valido())
        self.assertEqual(tc.rfc_hotel, "CAM123456ABC")
        self.assertEqual(tc.tipo, TipoHabitacion.DOBLE)
        self.assertEqual(tc.costo, 1500.00)

    def test_init_tipo_invalido(self):
        """Verifica que se lanza ValueError con tipo invalido."""
        datos = datos_tipo_cuarto_valido()
        datos["tipo"] = "HOSTEL"
        with self.assertRaises(ValueError):
            TipoCuarto(datos)

    def test_init_tipo_invalido_muestra_error(self):
        """Verifica que se muestra error en consola con tipo invalido."""
        datos = datos_tipo_cuarto_valido()
        datos["tipo"] = "HOSTEL"
        with patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError):
                TipoCuarto(datos)
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_init_campo_faltante(self):
        """Verifica que se lanza KeyError si falta un campo requerido."""
        datos = datos_tipo_cuarto_valido()
        del datos["costo"]
        with self.assertRaises(KeyError):
            TipoCuarto(datos)

    def test_init_campo_faltante_muestra_error(self):
        """Verifica que se muestra error en consola si falta un campo."""
        datos = datos_tipo_cuarto_valido()
        del datos["costo"]
        with patch("builtins.print") as mock_print:
            with self.assertRaises(KeyError):
                TipoCuarto(datos)
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_init_costo_cero_lanza_error(self):
        """Verifica que se lanza ValueError con costo cero."""
        datos = datos_tipo_cuarto_valido()
        datos["costo"] = 0
        with self.assertRaises(ValueError):
            TipoCuarto(datos)

    def test_init_costo_negativo_lanza_error(self):
        """Verifica que se lanza ValueError con costo negativo."""
        datos = datos_tipo_cuarto_valido()
        datos["costo"] = -100.00
        with self.assertRaises(ValueError):
            TipoCuarto(datos)

    def test_init_costo_invalido_muestra_error(self):
        """Verifica que se muestra error en consola con costo invalido."""
        datos = datos_tipo_cuarto_valido()
        datos["costo"] = -100.00
        with patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError):
                TipoCuarto(datos)
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_init_todos_los_tipos_habitacion(self):
        """Verifica que se pueden crear todos los tipos de habitacion."""
        for tipo in TipoHabitacion:
            datos = datos_tipo_cuarto_valido()
            datos["tipo"] = tipo.value
            tc = TipoCuarto(datos)
            self.assertEqual(tc.tipo, tipo)


class TestTipoCuartoCrear(unittest.TestCase):
    """Pruebas para TipoCuarto.crear."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_crear_tipo_cuarto_exitoso(self):
        """Verifica que se crea y persiste un tipo de cuarto correctamente."""
        tc = TipoCuarto.crear(datos_tipo_cuarto_valido())
        self.assertIsNotNone(tc)
        self.assertTrue(os.path.exists(ARCHIVO_TEST))
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertIn("CAM123456ABC_DOBLE", datos)

    def test_crear_tipo_cuarto_duplicado(self):
        """Verifica que no se crea un tipo de cuarto duplicado."""
        TipoCuarto.crear(datos_tipo_cuarto_valido())
        tc2 = TipoCuarto.crear(datos_tipo_cuarto_valido())
        self.assertIsNone(tc2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 1)

    def test_crear_tipo_cuarto_duplicado_muestra_error(self):
        """Verifica que se muestra error en consola al crear duplicado."""
        TipoCuarto.crear(datos_tipo_cuarto_valido())
        with patch("builtins.print") as mock_print:
            TipoCuarto.crear(datos_tipo_cuarto_valido())
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_crear_tipos_distintos_mismo_hotel(self):
        """Verifica que se pueden crear tipos distintos para el mismo hotel."""
        TipoCuarto.crear(datos_tipo_cuarto_valido())
        datos2 = datos_tipo_cuarto_valido()
        datos2["tipo"] = "SUITE"
        datos2["costo"] = 3000.00
        TipoCuarto.crear(datos2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 2)

    def test_crear_mismo_tipo_hoteles_distintos(self):
        """Verifica que el mismo tipo puede existir en hoteles distintos."""
        TipoCuarto.crear(datos_tipo_cuarto_valido())
        datos2 = datos_tipo_cuarto_valido()
        datos2["rfc_hotel"] = "HOT987654XYZ"
        TipoCuarto.crear(datos2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 2)

    def test_crear_retorna_instancia_tipo_cuarto(self):
        """Verifica que crear retorna una instancia de TipoCuarto."""
        tc = TipoCuarto.crear(datos_tipo_cuarto_valido())
        self.assertIsInstance(tc, TipoCuarto)

    def test_crear_costo_cero_lanza_error(self):
        """Verifica que no se crea tipo cuarto con costo cero."""
        datos = datos_tipo_cuarto_valido()
        datos["costo"] = 0
        with self.assertRaises(ValueError):
            TipoCuarto.crear(datos)

    def test_crear_costo_negativo_lanza_error(self):
        """Verifica que no se crea tipo cuarto con costo negativo."""
        datos = datos_tipo_cuarto_valido()
        datos["costo"] = -100.00
        with self.assertRaises(ValueError):
            TipoCuarto.crear(datos)


class TestTipoCuartoEliminar(unittest.TestCase):
    """Pruebas para TipoCuarto.eliminar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        TipoCuarto.crear(datos_tipo_cuarto_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_eliminar_tipo_cuarto_exitoso(self):
        """Verifica que se elimina un tipo de cuarto existente."""
        resultado = TipoCuarto.eliminar("CAM123456ABC", "DOBLE")
        self.assertTrue(resultado)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertNotIn("CAM123456ABC_DOBLE", datos)

    def test_eliminar_tipo_cuarto_inexistente(self):
        """Verifica que retorna False al eliminar tipo que no existe."""
        resultado = TipoCuarto.eliminar("CAM123456ABC", "SUITE")
        self.assertFalse(resultado)

    def test_eliminar_tipo_cuarto_inexistente_muestra_error(self):
        """Verifica que se muestra error al eliminar tipo inexistente."""
        with patch("builtins.print") as mock_print:
            TipoCuarto.eliminar("CAM123456ABC", "SUITE")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)


class TestTipoCuartoMostrarInfo(unittest.TestCase):
    """Pruebas para TipoCuarto.mostrar_info."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_mostrar_info_imprime_rfc_hotel(self):
        """Verifica que mostrar_info imprime el RFC del hotel."""
        tc = TipoCuarto(datos_tipo_cuarto_valido())
        with patch("builtins.print") as mock_print:
            tc.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("CAM123456ABC", salida)

    def test_mostrar_info_imprime_tipo(self):
        """Verifica que mostrar_info imprime el tipo de habitacion."""
        tc = TipoCuarto(datos_tipo_cuarto_valido())
        with patch("builtins.print") as mock_print:
            tc.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("DOBLE", salida)

    def test_mostrar_info_imprime_costo(self):
        """Verifica que mostrar_info imprime el costo del cuarto."""
        tc = TipoCuarto(datos_tipo_cuarto_valido())
        with patch("builtins.print") as mock_print:
            tc.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("1500", salida)


class TestTipoCuartoModificar(unittest.TestCase):
    """Pruebas para TipoCuarto.modificar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        self.tc = TipoCuarto.crear(datos_tipo_cuarto_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_modificar_costo_exitoso(self):
        """Verifica que se modifica el costo correctamente."""
        resultado = self.tc.modificar(costo=2000.00)
        self.assertTrue(resultado)
        self.assertEqual(self.tc.costo, 2000.00)

    def test_modificar_costo_persiste_en_archivo(self):
        """Verifica que el cambio de costo se persiste en archivo."""
        self.tc.modificar(costo=2000.00)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(
            datos["CAM123456ABC_DOBLE"]["costo"], 2000.00
        )

    def test_modificar_tipo_invalido(self):
        """Verifica que tipo no es modificable."""
        with patch("builtins.print") as mock_print:
            self.tc.modificar(tipo="SUITE")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_modificar_tipo_no_cambia(self):
        """Verifica que el tipo no se modifica aunque se intente."""
        self.tc.modificar(tipo="SUITE")
        self.assertEqual(self.tc.tipo, TipoHabitacion.DOBLE)

    def test_modificar_rfc_hotel_invalido(self):
        """Verifica que rfc_hotel no es modificable."""
        with patch("builtins.print") as mock_print:
            self.tc.modificar(rfc_hotel="OTRO_RFC")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_modificar_no_encontrado(self):
        """Verifica que retorna False si el tipo cuarto no esta en archivo."""
        os.remove(ARCHIVO_TEST)
        resultado = self.tc.modificar(costo=2000.00)
        self.assertFalse(resultado)

    def test_modificar_costo_cero_lanza_error(self):
        """Verifica que no se modifica el costo a cero."""
        with self.assertRaises(ValueError):
            self.tc.modificar(costo=0)

    def test_modificar_costo_negativo_lanza_error(self):
        """Verifica que no se modifica el costo a valor negativo."""
        with self.assertRaises(ValueError):
            self.tc.modificar(costo=-500.00)

def test_modificar_costo_invalido_no_persiste(self):
    """Verifica que costo invalido no se persiste en archivo."""
    try:
        self.tc.modificar(costo=-500.00)
    except ValueError:
        pass
    with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
        datos = json.load(f)
    self.assertEqual(datos["CAM123456ABC_DOBLE"]["costo"], 1500.00)


class TestTipoCuartoArchivocorrupto(unittest.TestCase):
    """Pruebas para comportamiento con archivo corrupto y sin archivo."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_eliminar_sin_archivo_retorna_false(self):
        """Verifica que eliminar funciona correctamente sin archivo."""
        resultado = TipoCuarto.eliminar("CAM123456ABC", "DOBLE")
        self.assertFalse(resultado)

    def test_crear_con_archivo_corrupto_retorna_tipo_cuarto(self):
        """Verifica que crear maneja JSON invalido y crea el tipo cuarto."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        resultado = TipoCuarto.crear(datos_tipo_cuarto_valido())
        self.assertIsNotNone(resultado)

    def test_crear_con_archivo_corrupto_muestra_error(self):
        """Verifica que se muestra error en consola con JSON invalido."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        with patch("builtins.print") as mock_print:
            TipoCuarto.crear(datos_tipo_cuarto_valido())
            llamadas = [
                str(c) for c in mock_print.call_args_list
            ]
            self.assertTrue(
                any("ERROR" in c for c in llamadas)
            )


if __name__ == "__main__":
    unittest.main()
