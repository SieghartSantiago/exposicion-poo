"""Pruebas automatizadas de los Laboratorios 02, 03 y 04."""

from __future__ import annotations

import unittest

from labs.lab_02_herencia_polimorfismo import app as app_02
from labs.lab_03_patron_strategy import app as app_03
from labs.lab_04_comparacion_paradigmas import app as app_04


class TestLab02HerenciaPolimorfismo(unittest.TestCase):
    def test_app_y_despacho_dinamico(self) -> None:
        outputs, defs = app_02.run()
        self.assertIsNotNone(outputs)

        EnvioEstandar = defs["EnvioEstandar"]
        EnvioExpres = defs["EnvioExpres"]
        EnvioRefrigerado = defs["EnvioRefrigerado"]
        procesar = defs["procesar_lote_envios"]

        with self.assertRaises(ValueError):
            EnvioEstandar("ERR", peso_kg=0.0, distancia_km=100.0)

        e1 = EnvioEstandar("E1", 5.0, 100.0)
        e2 = EnvioEstandar("E2", 10.0, 100.0)
        self.assertNotEqual(e1.calcular_costo(), e2.calcular_costo())

        lote = [e1, EnvioExpres("E3", 5.0, 100.0), EnvioRefrigerado("E4", 5.0, 100.0)]
        trazas, total = procesar(lote)
        self.assertEqual(len(trazas), 3)
        self.assertAlmostEqual(total, sum(t.costo for t in trazas))


class TestLab03PatronStrategy(unittest.TestCase):
    def test_app_e_intercambio_estrategia(self) -> None:
        outputs, defs = app_03.run()
        self.assertIsNotNone(outputs)

        Pedido = defs["Pedido"]
        SinDescuento = defs["SinDescuento"]
        DescuentoEstudiante = defs["DescuentoEstudiante"]
        EscalaMayorista = defs["EscalaMayorista"]

        pedido = Pedido("Ana", SinDescuento())
        pedido.agregar_item("Teclado", 10_000.0, 10)
        id_original = id(pedido)
        self.assertEqual(pedido.total_neto(), 100_000.0)

        pedido.cambiar_estrategia(DescuentoEstudiante(0.15))
        self.assertEqual(id(pedido), id_original)
        self.assertEqual(pedido.total_neto(), 85_000.0)

        pedido.cambiar_estrategia(EscalaMayorista())
        self.assertEqual(pedido.total_neto(), 80_000.0)


class TestLab04ComparacionParadigmas(unittest.TestCase):
    def test_equivalencia_tres_paradigmas(self) -> None:
        outputs, defs = app_04.run()
        self.assertIsNotNone(outputs)

        generar = defs["generar_lote_ventas"]
        imp = defs["liquidar_imperativo"]
        POO = defs["ProcesadorVentasPOO"]
        fun = defs["liquidar_funcional"]

        lote = generar(30, True)
        r_imp = imp(lote, 2500.0, 0.21)
        r_poo = POO(2500.0, 0.21).liquidar(lote)
        r_fun = fun(lote, 2500.0, 0.21)

        self.assertEqual(r_imp, r_poo)
        self.assertEqual(r_poo, r_fun)


if __name__ == "__main__":
    unittest.main()
