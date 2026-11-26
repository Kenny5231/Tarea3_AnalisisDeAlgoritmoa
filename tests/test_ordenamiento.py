import contextlib
import io
import random
import subprocess
import sys
import unittest
import tempfile
from itertools import product
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ordenamiento as app


class Pruebas(unittest.TestCase):
    def test_progreso_en_todos_los_algoritmos(self):
        for nombre, funcion, _ in app.ALGORITMOS:
            pasos = []
            lista = [5, -1, 3, 3, 0, 2]
            funcion(lista, lambda actual, total: pasos.append((actual, total)))
            self.assertEqual(lista, [-1, 0, 2, 3, 3, 5], nombre)
            self.assertTrue(pasos, nombre)
            self.assertTrue(all(0 <= actual <= total for actual, total in pasos), nombre)
            self.assertEqual(pasos, sorted(pasos), nombre)
            captura = io.StringIO()
            with contextlib.redirect_stdout(captura):
                app.ejecutar([2, 1], next(i for i, a in enumerate(app.ALGORITMOS, 1) if a[0] == nombre))
            self.assertIn("100.0%", captura.getvalue())

    def test_selection_sort_exhaustivo_y_opcion_2(self):
        self.assertIs(app.ALGORITMOS[1][1], app.selection_sort)
        for n in range(7):
            for valores in product((-1, 0, 1), repeat=n):
                lista = list(valores)
                app.selection_sort(lista)
                self.assertEqual(lista, sorted(valores))
        with tempfile.TemporaryDirectory() as temporal, patch.object(app, "CARPETA_ARREGLOS", Path(temporal)):
            ruta = Path(temporal) / "seleccion.txt"
            original = "42, -7, 15, 0, 15, -34"
            ruta.write_text(original, encoding="utf-8")
            with patch("builtins.input", side_effect=["2", "1", "0"]):
                captura = io.StringIO()
                with contextlib.redirect_stdout(captura):
                    app.main()
            self.assertIn("--- Selection Sort ---", captura.getvalue())
            self.assertIn("Lista ordenada: -34, -7, 0, 15, 15, 42", captura.getvalue())
            self.assertIn("Estado: Correcto", captura.getvalue())
            self.assertIn("Tiempo de ordenamiento:", captura.getvalue())
            self.assertEqual(ruta.read_text(encoding="utf-8"), original)

    def test_generador_y_archivo(self):
        with tempfile.TemporaryDirectory() as temporal, patch.object(app, "CARPETA_ARREGLOS", Path(temporal)):
            ruta = app.guardar_arreglo_aleatorio(1_000_000, "millon")
            lista = app.cargar_archivo(ruta)
            self.assertEqual(len(lista), 1_000_000)
            self.assertTrue(all(-1_000_000 <= n <= 1_000_000 for n in lista))
            with self.assertRaises(FileExistsError):
                app.guardar_arreglo_aleatorio(1, "millon")
            self.assertEqual(len(app.cargar_archivo(ruta)), 1_000_000)
            with self.assertRaises(ValueError):
                app.guardar_arreglo_aleatorio(5, "../otro")
            ruta.write_text("1, 2\nno valido", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Linea 2"):
                app.cargar_archivo(ruta)

    def test_algoritmos(self):
        rng = random.Random(1234)
        casos = [[], [1], [2, 1], [7] * 1000, list(range(1000)),
                 list(range(1000, 0, -1)), [-2147483648, 2147483647, 0],
                 [rng.randint(-100, 100) for _ in range(400)]]
        for nombre, funcion, _ in app.ALGORITMOS:
            for caso in casos:
                with self.subTest(algoritmo=nombre, cantidad=len(caso)):
                    copia = caso.copy()
                    funcion(copia)
                    self.assertEqual(copia, sorted(caso))

    def test_entrada(self):
        self.assertEqual(app.leer_lista(" [8, -3; +2\n0 8] "), [8, -3, 2, 0, 8])
        self.assertEqual(len(app.leer_lista("1 " * 5000)), 5000)
        for texto in ["", "[]", "1.5", "1x", "1-2", "+", "[1,2", "1,2]",
                      "2147483648", "-2147483649", "[[1]]"]:
            with self.subTest(texto=texto[:30]), self.assertRaises(ValueError):
                app.leer_lista(texto)

    def test_millon_de_enteros(self):
        lista = app.leer_lista("123456 " * 1_000_000)
        self.assertEqual(len(lista), 1_000_000)
        self.assertEqual(lista[-1], 123456)
        del lista
        lista = list(range(1_000_000, 0, -1))
        captura = io.StringIO()
        with contextlib.redirect_stdout(captura):
            app.ejecutar(lista, 1)
        self.assertIn("Estado: Correcto", captura.getvalue())
        self.assertIn("primeros 50 y ultimos 50", captura.getvalue())
        # La terminal reemplaza la barra con \r; comprueba la salida final,
        # sin sumar los refrescos acumulados por StringIO.
        self.assertLess(len(captura.getvalue().rsplit("\r", 1)[-1]), 3000)
        self.assertEqual(lista[0], 1_000_000)

    def test_comparacion_no_modifica_original(self):
        original = [4, -2, 4, 0]
        captura = io.StringIO()
        with contextlib.redirect_stdout(captura):
            app.ejecutar(original, 7)
        self.assertEqual(original, [4, -2, 4, 0])
        self.assertEqual(captura.getvalue().count("Estado: Correcto"), 6)
        self.assertEqual(captura.getvalue().count("Tiempo de ordenamiento:"), 6)

    def test_menu(self):
        with tempfile.TemporaryDirectory() as temporal, patch.object(app, "CARPETA_ARREGLOS", Path(temporal)):
            with patch("builtins.input", side_effect=["x", "9", "5", "prueba", "7", "1", "1", "0", "8", "0"]):
                captura = io.StringIO()
                with contextlib.redirect_stdout(captura):
                    app.main()
            salida = captura.getvalue()
            self.assertIn("Opcion invalida", salida)
            self.assertIn("Archivo creado:", salida)
            self.assertEqual(salida.count("Estado: Correcto"), 6)
            self.assertIn("Programa finalizado.", salida)
            self.assertEqual(len(app.cargar_archivo(Path(temporal) / "prueba.txt")), 5)


if __name__ == "__main__":
    unittest.main()
