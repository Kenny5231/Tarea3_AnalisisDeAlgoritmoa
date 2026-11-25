import contextlib
import io
import random
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ordenamiento as app


class Pruebas(unittest.TestCase):
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
        self.assertLess(len(captura.getvalue()), 3000)
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
        archivo = Path(app.__file__).resolve()
        resultado = subprocess.run([sys.executable, str(archivo)],
            input="x\n7\n8, -3\n2 8\n\n8\n5 1\n\n1\n0\n",
            text=True, capture_output=True, timeout=20)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Opcion invalida", resultado.stdout)
        self.assertEqual(resultado.stdout.count("Estado: Correcto"), 7)
        self.assertIn("Lista ordenada: -3, 2, 8, 8", resultado.stdout)
        self.assertIn("Lista ordenada: 1, 5", resultado.stdout)
        self.assertIn("Programa finalizado.", resultado.stdout)


if __name__ == "__main__":
    unittest.main()
