# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 11:31:26 2026

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
import unittest
from unittest.mock import patch

import persistencia
from catalogos import ClasificacionHotel
from hotel import Hotel


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_TEST = os.path.join(TEST_DATA_DIR, "hoteles.json")


def datos_hotel_valido():
    """Retorna un diccionario con datos validos de hotel."""
    return {
        "nombre": "Hotel Camino Real",
        "nombre_fiscal": "Camino Real SA de CV",
        "rfc": "CAM123456ABC",
        "direccion": "Av. Principal 100",
        "estado": "Jalisco",
        "clasificacion": "5E",
        "estatus": "activo"
    }


class TestHotelInit(unittest.TestCase):
    """Pruebas para el constructor de Hotel."""

    def test_init_exitoso(self):
        """Verifica que el hotel se crea con datos validos."""
        hotel = Hotel(datos_hotel_valido())
        self.assertEqual(hotel.nombre, "Hotel Camino Real")
        self.assertEqual(hotel.rfc, "CAM123456ABC")
        self.assertEqual(
            hotel.clasificacion, ClasificacionHotel.CINCO_ESTRELLAS
        )

    def test_init_clasificacion_invalida(self):
        """Verifica que se lanza ValueError con clasificacion invalida."""
        datos = datos_hotel_valido()
        datos["clasificacion"] = "9E"
        with self.assertRaises(ValueError):
            Hotel(datos)

    def test_init_campo_faltante(self):
        """Verifica que se lanza KeyError si falta un campo requerido."""
        datos = datos_hotel_valido()
        del datos["rfc"]
        with self.assertRaises(KeyError):
            Hotel(datos)

    def test_init_clasificacion_sin_categoria(self):
        """Verifica creacion con clasificacion SC."""
        datos = datos_hotel_valido()
        datos["clasificacion"] = "SC"
        hotel = Hotel(datos)
        self.assertEqual(
            hotel.clasificacion, ClasificacionHotel.SIN_CATEGORIA
        )

    def test_init_clasificacion_gran_turismo(self):
        """Verifica creacion con clasificacion GT."""
        datos = datos_hotel_valido()
        datos["clasificacion"] = "GT"
        hotel = Hotel(datos)
        self.assertEqual(
            hotel.clasificacion, ClasificacionHotel.GRAN_TURISMO
        )


class TestHotelCrear(unittest.TestCase):
    """Pruebas para Hotel.crear."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_crear_hotel_exitoso(self):
        """Verifica que se crea y persiste un hotel correctamente."""
        hotel = Hotel.crear(datos_hotel_valido())
        self.assertIsNotNone(hotel)
        self.assertTrue(os.path.exists(ARCHIVO_TEST))
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertIn("CAM123456ABC", datos)

    def test_crear_hotel_duplicado(self):
        """Verifica que no se crea un hotel con RFC duplicado."""
        Hotel.crear(datos_hotel_valido())
        hotel2 = Hotel.crear(datos_hotel_valido())
        self.assertIsNone(hotel2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 1)

    def test_crear_hotel_duplicado_muestra_error(self):
        """Verifica que se muestra error en consola al crear duplicado."""
        Hotel.crear(datos_hotel_valido())
        with patch("builtins.print") as mock_print:
            Hotel.crear(datos_hotel_valido())
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_crear_dos_hoteles_distintos(self):
        """Verifica que se pueden crear dos hoteles con RFC distintos."""
        Hotel.crear(datos_hotel_valido())
        datos2 = datos_hotel_valido()
        datos2["rfc"] = "HOT987654XYZ"
        Hotel.crear(datos2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 2)

    def test_crear_retorna_instancia_hotel(self):
        """Verifica que crear retorna una instancia de Hotel."""
        hotel = Hotel.crear(datos_hotel_valido())
        self.assertIsInstance(hotel, Hotel)


class TestHotelEliminar(unittest.TestCase):
    """Pruebas para Hotel.eliminar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        Hotel.crear(datos_hotel_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_eliminar_hotel_exitoso(self):
        """Verifica que se elimina un hotel existente."""
        resultado = Hotel.eliminar("CAM123456ABC")
        self.assertTrue(resultado)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertNotIn("CAM123456ABC", datos)

    def test_eliminar_hotel_inexistente(self):
        """Verifica que retorna False al eliminar RFC que no existe."""
        resultado = Hotel.eliminar("RFC_INEXISTENTE")
        self.assertFalse(resultado)

    def test_eliminar_hotel_inexistente_muestra_error(self):
        """Verifica que se muestra error al eliminar RFC inexistente."""
        with patch("builtins.print") as mock_print:
            Hotel.eliminar("RFC_INEXISTENTE")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)


class TestHotelMostrarInfo(unittest.TestCase):
    """Pruebas para Hotel.mostrar_info."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_mostrar_info_imprime_nombre(self):
        """Verifica que mostrar_info imprime el nombre del hotel."""
        hotel = Hotel(datos_hotel_valido())
        with patch("builtins.print") as mock_print:
            hotel.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("Hotel Camino Real", salida)

    def test_mostrar_info_imprime_rfc(self):
        """Verifica que mostrar_info imprime el RFC del hotel."""
        hotel = Hotel(datos_hotel_valido())
        with patch("builtins.print") as mock_print:
            hotel.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("CAM123456ABC", salida)

    def test_mostrar_info_imprime_clasificacion(self):
        """Verifica que mostrar_info imprime la clasificacion del hotel."""
        hotel = Hotel(datos_hotel_valido())
        with patch("builtins.print") as mock_print:
            hotel.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("5E", salida)


class TestHotelModificar(unittest.TestCase):
    """Pruebas para Hotel.modificar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        self.hotel = Hotel.crear(datos_hotel_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_modificar_nombre_exitoso(self):
        """Verifica que se modifica el nombre correctamente."""
        resultado = self.hotel.modificar(nombre="Hotel Nuevo")
        self.assertTrue(resultado)
        self.assertEqual(self.hotel.nombre, "Hotel Nuevo")

    def test_modificar_persiste_en_archivo(self):
        """Verifica que el cambio se persiste en el archivo JSON."""
        self.hotel.modificar(nombre="Hotel Nuevo")
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(
            datos["CAM123456ABC"]["nombre"], "Hotel Nuevo"
        )

    def test_modificar_clasificacion_exitoso(self):
        """Verifica que se modifica la clasificacion correctamente."""
        resultado = self.hotel.modificar(
            clasificacion=ClasificacionHotel.TRES_ESTRELLAS
        )
        self.assertTrue(resultado)
        self.assertEqual(
            self.hotel.clasificacion, ClasificacionHotel.TRES_ESTRELLAS
        )

    def test_modificar_campo_invalido(self):
        """Verifica que campo invalido muestra error y continua."""
        with patch("builtins.print") as mock_print:
            self.hotel.modificar(rfc="NUEVO_RFC")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_modificar_campo_invalido_no_cambia_rfc(self):
        """Verifica que el RFC no se modifica aunque se intente."""
        self.hotel.modificar(rfc="NUEVO_RFC")
        self.assertEqual(self.hotel.rfc, "CAM123456ABC")

    def test_modificar_hotel_no_encontrado(self):
        """Verifica que retorna False si el hotel no esta en archivo."""
        os.remove(ARCHIVO_TEST)
        resultado = self.hotel.modificar(nombre="Hotel Nuevo")
        self.assertFalse(resultado)

    def test_modificar_multiples_campos(self):
        """Verifica que se pueden modificar varios campos en una llamada."""
        resultado = self.hotel.modificar(
            nombre="Hotel Nuevo",
            estado="Nuevo Leon",
            estatus="inactivo"
        )
        self.assertTrue(resultado)
        self.assertEqual(self.hotel.nombre, "Hotel Nuevo")
        self.assertEqual(self.hotel.estado, "Nuevo Leon")
        self.assertEqual(self.hotel.estatus, "inactivo")


class TestHotelCargar(unittest.TestCase):
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
        resultado = Hotel.eliminar("CAM123456ABC")
        self.assertFalse(resultado)

    def test_crear_con_archivo_corrupto_retorna_hotel(self):
        """Verifica que crear maneja JSON invalido y crea el hotel."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        resultado = Hotel.crear(datos_hotel_valido())
        self.assertIsNotNone(resultado)

    def test_crear_con_archivo_corrupto_muestra_error(self):
        """Verifica que se muestra error en consola con JSON invalido."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        with patch("builtins.print") as mock_print:
            Hotel.crear(datos_hotel_valido())
            llamadas = [
                str(c) for c in mock_print.call_args_list
            ]
            self.assertTrue(
                any("ERROR" in c for c in llamadas)
            )


class TestHotelBuscar(unittest.TestCase):
    """Pruebas para Hotel.buscar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        Hotel.crear(datos_hotel_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_buscar_hotel_existente(self):
        """Verifica que buscar retorna dict del hotel existente."""
        resultado = Hotel.buscar("CAM123456ABC")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["rfc"], "CAM123456ABC")

    def test_buscar_hotel_inexistente(self):
        """Verifica que buscar retorna None si no existe."""
        resultado = Hotel.buscar("RFC_INEXISTENTE")
        self.assertIsNone(resultado)

    def test_buscar_sin_archivo_retorna_none(self):
        """Verifica que buscar retorna None sin archivo."""
        os.remove(ARCHIVO_TEST)
        resultado = Hotel.buscar("CAM123456ABC")
        self.assertIsNone(resultado)


class TestHotelReservarCuarto(unittest.TestCase):
    """Pruebas para Hotel.reservar_cuarto."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        self.hotel = Hotel.crear(datos_hotel_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_reservar_cuarto_delega_a_bridge(self):
        """Verifica que reservar_cuarto delega a crear_reservacion."""
        with patch(
            "hotel.crear_reservacion"
        ) as mock_crear:
            mock_crear.return_value = "reservacion_mock"
            datos = {"rfc_hotel": "CAM123456ABC"}
            resultado = self.hotel.reservar_cuarto(datos)
            mock_crear.assert_called_once_with(datos)
            self.assertEqual(resultado, "reservacion_mock")

    def test_reservar_cuarto_retorna_resultado_bridge(self):
        """Verifica que reservar_cuarto retorna lo que retorna el bridge."""
        with patch("hotel.crear_reservacion") as mock_crear:
            mock_crear.return_value = None
            resultado = self.hotel.reservar_cuarto({})
            self.assertIsNone(resultado)


class TestHotelCancelarReservacion(unittest.TestCase):
    """Pruebas para Hotel.cancelar_reservacion."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        self.hotel = Hotel.crear(datos_hotel_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_cancelar_reservacion_delega_a_bridge(self):
        """Verifica que cancelar_reservacion delega a cancelar_reservacion."""
        with patch(
            "hotel.cancelar_reservacion"
        ) as mock_cancelar:
            mock_cancelar.return_value = True
            reservacion_mock = unittest.mock.MagicMock()
            resultado = self.hotel.cancelar_reservacion(reservacion_mock)
            mock_cancelar.assert_called_once_with(reservacion_mock)
            self.assertTrue(resultado)

    def test_cancelar_reservacion_retorna_false_si_falla(self):
        """Verifica que retorna False si el bridge retorna False."""
        with patch("hotel.cancelar_reservacion") as mock_cancelar:
            mock_cancelar.return_value = False
            reservacion_mock = unittest.mock.MagicMock()
            resultado = self.hotel.cancelar_reservacion(reservacion_mock)
            self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
