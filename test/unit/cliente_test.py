# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 16:09:18 2026

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


from cliente import Cliente
import persistencia


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
ARCHIVO_TEST = os.path.join(TEST_DATA_DIR, "clientes.json")


def datos_cliente_valido():
    """Retorna un diccionario con datos válidos de cliente."""
    return {
        "nombre": "Juan Pérez",
        "rfc": "PEJJ800101ABC",
        "sexo": "M",
        "compania": "Empresa SA de CV",
        "forma_pago": "tarjeta",
        "estatus": "activo"
    }


class TestClienteInit(unittest.TestCase):
    """Pruebas para el constructor de Cliente."""

    def test_init_exitoso(self):
        """Verifica que el cliente se crea con datos validos."""
        cliente = Cliente(datos_cliente_valido())
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.rfc, "PEJJ800101ABC")

    def test_init_campo_faltante(self):
        """Verifica que se lanza KeyError si falta un campo requerido."""
        datos = datos_cliente_valido()
        del datos["rfc"]
        with self.assertRaises(KeyError):
            Cliente(datos)

    def test_init_campo_nombre_faltante(self):
        """Verifica que se lanza KeyError si falta el nombre."""
        datos = datos_cliente_valido()
        del datos["nombre"]
        with self.assertRaises(KeyError):
            Cliente(datos)

    def test_init_campo_faltante_muestra_error(self):
        """Verifica que se muestra error en consola si falta un campo."""
        datos = datos_cliente_valido()
        del datos["rfc"]
        with patch("builtins.print") as mock_print:
            with self.assertRaises(KeyError):
                Cliente(datos)
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)


class TestClienteCrear(unittest.TestCase):
    """Pruebas para Cliente.crear."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_crear_cliente_exitoso(self):
        """Verifica que se crea y persiste un cliente correctamente."""
        cliente = Cliente.crear(datos_cliente_valido())
        self.assertIsNotNone(cliente)
        self.assertTrue(os.path.exists(ARCHIVO_TEST))
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertIn("PEJJ800101ABC", datos)

    def test_crear_cliente_duplicado(self):
        """Verifica que no se crea un cliente con RFC duplicado."""
        Cliente.crear(datos_cliente_valido())
        cliente2 = Cliente.crear(datos_cliente_valido())
        self.assertIsNone(cliente2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 1)

    def test_crear_cliente_duplicado_muestra_error(self):
        """Verifica que se muestra error en consola al crear duplicado."""
        Cliente.crear(datos_cliente_valido())
        with patch("builtins.print") as mock_print:
            Cliente.crear(datos_cliente_valido())
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_crear_dos_clientes_distintos(self):
        """Verifica que se pueden crear dos clientes con RFC distintos."""
        Cliente.crear(datos_cliente_valido())
        datos2 = datos_cliente_valido()
        datos2["rfc"] = "GOLA900202XYZ"
        Cliente.crear(datos2)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(len(datos), 2)

    def test_crear_retorna_instancia_cliente(self):
        """Verifica que crear retorna una instancia de Cliente."""
        cliente = Cliente.crear(datos_cliente_valido())
        self.assertIsInstance(cliente, Cliente)


class TestClienteEliminar(unittest.TestCase):
    """Pruebas para Cliente.eliminar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        Cliente.crear(datos_cliente_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_eliminar_cliente_exitoso(self):
        """Verifica que se elimina un cliente existente."""
        resultado = Cliente.eliminar("PEJJ800101ABC")
        self.assertTrue(resultado)
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertNotIn("PEJJ800101ABC", datos)

    def test_eliminar_cliente_inexistente(self):
        """Verifica que retorna False al eliminar RFC que no existe."""
        resultado = Cliente.eliminar("RFC_INEXISTENTE")
        self.assertFalse(resultado)

    def test_eliminar_cliente_inexistente_muestra_error(self):
        """Verifica que se muestra error al eliminar RFC inexistente."""
        with patch("builtins.print") as mock_print:
            Cliente.eliminar("RFC_INEXISTENTE")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)


class TestClienteMostrarInfo(unittest.TestCase):
    """Pruebas para Cliente.mostrar_info."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_mostrar_info_imprime_nombre(self):
        """Verifica que mostrar_info imprime el nombre del cliente."""
        cliente = Cliente(datos_cliente_valido())
        with patch("builtins.print") as mock_print:
            cliente.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("Juan Pérez", salida)

    def test_mostrar_info_imprime_rfc(self):
        """Verifica que mostrar_info imprime el RFC del cliente."""
        cliente = Cliente(datos_cliente_valido())
        with patch("builtins.print") as mock_print:
            cliente.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("PEJJ800101ABC", salida)

    def test_mostrar_info_imprime_compania(self):
        """Verifica que mostrar_info imprime la compania del cliente."""
        cliente = Cliente(datos_cliente_valido())
        with patch("builtins.print") as mock_print:
            cliente.mostrar_info()
            salida = " ".join(
                str(c) for call in mock_print.call_args_list
                for c in call[0]
            )
            self.assertIn("Empresa SA de CV", salida)


class TestClienteModificar(unittest.TestCase):
    """Pruebas para Cliente.modificar."""

    def setUp(self):
        persistencia.DATA_DIR = TEST_DATA_DIR
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)
        self.cliente = Cliente.crear(datos_cliente_valido())

    def tearDown(self):
        if os.path.exists(ARCHIVO_TEST):
            os.remove(ARCHIVO_TEST)

    def test_modificar_nombre_exitoso(self):
        """Verifica que se modifica el nombre correctamente."""
        resultado = self.cliente.modificar(nombre="Pedro López")
        self.assertTrue(resultado)
        self.assertEqual(self.cliente.nombre, "Pedro López")

    def test_modificar_persiste_en_archivo(self):
        """Verifica que el cambio se persiste en el archivo JSON."""
        self.cliente.modificar(nombre="Pedro López")
        with open(ARCHIVO_TEST, "r", encoding="utf-8") as f:
            datos = json.load(f)
        self.assertEqual(
            datos["PEJJ800101ABC"]["nombre"], "Pedro López"
        )

    def test_modificar_campo_invalido(self):
        """Verifica que campo inválido muestra error y continua."""
        with patch("builtins.print") as mock_print:
            self.cliente.modificar(rfc="NUEVO_RFC")
            mock_print.assert_called_once()
            args = mock_print.call_args[0][0]
            self.assertIn("ERROR", args)

    def test_modificar_campo_invalido_no_cambia_rfc(self):
        """Verifica que el RFC no se modifica aunque se intente."""
        self.cliente.modificar(rfc="NUEVO_RFC")
        self.assertEqual(self.cliente.rfc, "PEJJ800101ABC")

    def test_modificar_cliente_no_encontrado(self):
        """Verifica que retorna False si el cliente no esta en archivo."""
        os.remove(ARCHIVO_TEST)
        resultado = self.cliente.modificar(nombre="Pedro López")
        self.assertFalse(resultado)

    def test_modificar_multiples_campos(self):
        """Verifica que se pueden modificar varios campos en una llamada."""
        resultado = self.cliente.modificar(
            nombre="Pedro López",
            compania="Nueva Empresa",
            estatus="inactivo"
        )
        self.assertTrue(resultado)
        self.assertEqual(self.cliente.nombre, "Pedro López")
        self.assertEqual(self.cliente.compania, "Nueva Empresa")
        self.assertEqual(self.cliente.estatus, "inactivo")


class TestClienteArchivocorrupto(unittest.TestCase):
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
        resultado = Cliente.eliminar("PEJJ800101ABC")
        self.assertFalse(resultado)

    def test_crear_con_archivo_corrupto_retorna_cliente(self):
        """Verifica que el maneja de JSON inválido y crea el cliente."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        resultado = Cliente.crear(datos_cliente_valido())
        self.assertIsNotNone(resultado)

    def test_crear_con_archivo_corrupto_muestra_error(self):
        """Verifica que se muestra error en consola con JSON inválido."""
        with open(ARCHIVO_TEST, "w", encoding="utf-8") as f:
            f.write("esto no es json {{{")
        with patch("builtins.print") as mock_print:
            Cliente.crear(datos_cliente_valido())
            llamadas = [
                str(c) for c in mock_print.call_args_list
            ]
            self.assertTrue(
                any("ERROR" in c for c in llamadas)
            )


if __name__ == "__main__":
    unittest.main()
