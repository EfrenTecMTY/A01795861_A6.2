# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 01:43:07 2026

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
from unittest.mock import patch, MagicMock

import persistencia
from reservacion_bridge import crear_reservacion, cancelar_reservacion


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")


class TestCrearReservacion(unittest.TestCase):
    """Pruebas para crear_reservacion."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)

    def test_crear_reservacion_delega_a_reservacion(self):
        """Verifica que delega a Reservacion.crear."""
        with patch(
            "reservacion_bridge.Reservacion.crear"
        ) as mock_crear:
            mock_crear.return_value = "reservacion_mock"
            datos = {"rfc_hotel": "CAM123456ABC"}
            resultado = crear_reservacion(datos)
            mock_crear.assert_called_once_with(datos)
            self.assertEqual(resultado, "reservacion_mock")

    def test_crear_reservacion_retorna_none_si_falla(self):
        """Verifica que retorna None si Reservacion.crear retorna None."""
        with patch(
            "reservacion_bridge.Reservacion.crear"
        ) as mock_crear:
            mock_crear.return_value = None
            resultado = crear_reservacion({})
            self.assertIsNone(resultado)


class TestCancelarReservacion(unittest.TestCase):
    """Pruebas para cancelar_reservacion."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)

    def test_cancelar_reservacion_delega_a_cancelar(self):
        """Verifica que delega a reservacion.cancelar."""
        reservacion_mock = MagicMock()
        reservacion_mock.cancelar.return_value = True
        resultado = cancelar_reservacion(reservacion_mock)
        reservacion_mock.cancelar.assert_called_once()
        self.assertTrue(resultado)

    def test_cancelar_reservacion_retorna_false_si_falla(self):
        """Verifica que retorna False si cancelar retorna False."""
        reservacion_mock = MagicMock()
        reservacion_mock.cancelar.return_value = False
        resultado = cancelar_reservacion(reservacion_mock)
        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
