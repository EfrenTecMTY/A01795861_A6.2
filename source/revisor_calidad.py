# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 11:03:33 2026

@author: Efrén Alejandro
"""
import subprocess
import sys
import os

MODULOS = [
    "catalogos.py",
    "cliente.py",
    "hotel.py",
    "persistencia.py",
    "reservacion.py",
    "reservacion_bridge.py",
    "tipo_cuarto.py",
    "validador.py",
    "lector_json.py",
    "config.py"
]

SOURCE_DIR = os.path.join(os.path.dirname(__file__))

HERRAMIENTAS = [
    ("pyflakes", [sys.executable, "-m", "pyflakes"]),
    ("flake8",   [sys.executable, "-m", "flake8"]),
    ("pylint",   [sys.executable, "-m", "pylint"]),
]

SEP_RESULT = '='*60


def ejecutar(herramienta, cmd, archivo):
    """Ejecuta una herramienta sobre un archivo y muestra el resultado."""
    ruta = os.path.join(SOURCE_DIR, archivo)
    resultado = subprocess.run(
        cmd + [ruta],
        capture_output=True,
        text=True,
        check=False  # No lanzar excepcion si el proceso retorna error
    )
    salida = resultado.stdout + resultado.stderr
    if salida.strip():
        print(f"\n{SEP_RESULT}")
        print(f"{herramienta.upper()} → {archivo}")
        print(SEP_RESULT)
        print(salida)
    else:
        print(f"  {herramienta:<10} {archivo:<30} OK")


def main():
    """Ejecuta todas las herramientas sobre todos los modulos."""
    print("\nIniciando revision de calidad de codigo...\n")
    for modulo in MODULOS:
        for nombre, cmd in HERRAMIENTAS:
            ejecutar(nombre, cmd, modulo)
    print(f"\n{SEP_RESULT}")
    print("Revision completada.")
    print(SEP_RESULT)


if __name__ == "__main__":
    main()
