"""Pruebas automatizadas del Laboratorio 01 (Encapsulamiento e Invariantes)."""

from __future__ import annotations

import unittest
from labs.lab_01_encapsulamiento import app


class TestLab01Encapsulamiento(unittest.TestCase):
    def test_marimo_app_ejecuta_sin_errores(self) -> None:
        """Verifica que el grafo reactivo completo del notebook ejecute sin excepciones."""
        outputs, defs = app.run()
        self.assertIsNotNone(outputs)
        self.assertIn("CuentaBancaria", defs)
        self.assertIn("ejecutar_comparativa", defs)

    def test_invariante_cuenta_bancaria(self) -> None:
        """Comprueba que CuentaBancaria preserve saldo >= 0 ante entradas válidas e inválidas."""
        _, defs = app.run()
        CuentaBancaria = defs["CuentaBancaria"]

        # Constructor rechaza saldo negativo
        with self.assertRaises(ValueError):
            CuentaBancaria("Ana", -100.0)

        cuenta = CuentaBancaria("Ana", 30_000.0)
        self.assertEqual(cuenta.saldo, 30_000.0)

        # Extracción válida
        cuenta.extraer(10_000.0)
        self.assertEqual(cuenta.saldo, 20_000.0)

        # Sobregiro rechazado sin alterar estado interno
        with self.assertRaises(ValueError):
            cuenta.extraer(25_000.0)
        self.assertEqual(cuenta.saldo, 20_000.0)

        # Propiedad de solo lectura rechaza mutación directa
        with self.assertRaises(AttributeError):
            cuenta.saldo = -9_999.0  # type: ignore[misc]
        self.assertEqual(cuenta.saldo, 20_000.0)


if __name__ == "__main__":
    unittest.main()
