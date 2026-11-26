"""Algoritmos del Excel adaptados a Python. Sin dependencias externas."""
import re
import random
from pathlib import Path
from time import perf_counter


class BarraProgreso:
    """Progreso por etapas terminadas; refresco como maximo cada 0.2 segundos."""
    def __init__(self, nombre):
        self.nombre = nombre
        self.ultimo_refresco = 0.0
        self.terminada = False
        self.actualizar(0, 1, forzar=True)

    def actualizar(self, actual, total, forzar=False):
        ahora = perf_counter()
        if not forzar and ahora - self.ultimo_refresco < 0.2:
            return
        self.ultimo_refresco = ahora
        fraccion = min(1.0, max(0.0, actual / max(1, total)))
        # El 100% solo se imprime despues de que la funcion regresa.
        porcentaje = min(99.9, fraccion * 100) if not self.terminada else 100.0
        llenos = int(porcentaje * 30 / 100)
        barra = "#" * llenos + "-" * (30 - llenos)
        print(f"\r{self.nombre}: [{barra}] {porcentaje:5.1f}%", end="", flush=True)

    def finalizar(self):
        self.terminada = True
        self.actualizar(1, 1, forzar=True)
        print()


def generar_arreglo(cantidad):
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")
    return [random.randint(-1_000_000, 1_000_000) for _ in range(cantidad)]


CARPETA_ARREGLOS = Path(__file__).resolve().parent / "arreglos"


def guardar_arreglo_aleatorio(cantidad, nombre):
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")
    nombre = nombre.strip()
    if not nombre or any(c in nombre for c in '<>:"/\\|?*') or nombre in (".", ".."):
        raise ValueError("Escribe un nombre de archivo valido, sin carpetas.")
    if not nombre.lower().endswith(".txt"):
        nombre += ".txt"
    CARPETA_ARREGLOS.mkdir(parents=True, exist_ok=True)
    ruta = CARPETA_ARREGLOS / nombre
    # Modo x evita reemplazar un archivo existente. Generacion por bloques.
    with ruta.open("x", encoding="utf-8") as archivo:
        restantes = cantidad
        while restantes:
            bloque = generar_arreglo(min(restantes, 10000))
            archivo.write(", ".join(map(str, bloque)) + "\n")
            restantes -= len(bloque)
    return ruta


def pedir_arreglo_aleatorio():
    while True:
        try:
            cantidad = int(input("Cantidad de enteros a generar (ejemplo: 1000000): "))
            if cantidad <= 0:
                raise ValueError
            break
        except ValueError:
            print("Escribe una cantidad entera mayor que cero.")
    nombre = input("Nombre del archivo (ejemplo: prueba_millon): ")
    print(f"Generando {cantidad} numeros...")
    ruta = guardar_arreglo_aleatorio(cantidad, nombre)
    print(f"Archivo creado: {ruta}")
    return ruta


def cargar_archivo(ruta):
    # Lee por lineas para evitar mantener todo el texto en memoria.
    lista = []
    with Path(ruta).open(encoding="utf-8-sig") as archivo:
        for numero_linea, linea in enumerate(archivo, 1):
            if linea.strip():
                try:
                    lista.extend(leer_lista(linea))
                except ValueError as error:
                    raise ValueError(f"Linea {numero_linea}: {error}") from error
    if not lista:
        raise ValueError("El archivo no contiene numeros.")
    return lista


def elegir_archivo():
    archivos = sorted(CARPETA_ARREGLOS.glob("*.txt"))
    if not archivos:
        print("No hay archivos. Usa la opcion 9 para generar uno.")
        return None
    print("\nArchivos disponibles:")
    for i, ruta in enumerate(archivos, 1):
        print(f"  {i}. {ruta.name}")
    print("  0. Cancelar")
    while True:
        opcion = input("Numero del archivo: ").strip()
        if opcion == "0":
            return None
        if opcion.isdecimal() and 1 <= int(opcion) <= len(archivos):
            return archivos[int(opcion) - 1]
        print("Selecciona un archivo de la lista.")


def merge_sort(arr, progreso=None):
    terminadas = 0
    def ordenar(izquierda, derecha):
        nonlocal terminadas
        if izquierda >= derecha:
            return
        medio = (izquierda + derecha) // 2
        ordenar(izquierda, medio)
        ordenar(medio + 1, derecha)
        l, r = arr[izquierda:medio + 1], arr[medio + 1:derecha + 1]
        i = j = 0
        k = izquierda
        while i < len(l) and j < len(r):
            if l[i] <= r[j]:
                arr[k] = l[i]
                i += 1
            else:
                arr[k] = r[j]
                j += 1
            k += 1
        while i < len(l):
            arr[k] = l[i]
            i += 1
            k += 1
        while j < len(r):
            arr[k] = r[j]
            j += 1
            k += 1
        terminadas += 1
        if progreso:
            progreso(terminadas, len(arr) - 1)
    ordenar(0, len(arr) - 1)


def selection_sort(arr, progreso=None):
    for i in range(len(arr) - 1):
        minimo = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minimo]:
                minimo = j
        arr[i], arr[minimo] = arr[minimo], arr[i]
        if progreso:
            progreso(i + 1, len(arr) - 1)


def bubble_sort(arr, progreso=None):
    for i in range(len(arr) - 1):
        intercambio = False
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if progreso:
            progreso(i + 1, len(arr) - 1)
        if not intercambio:
            break


def quick_sort(arr, progreso=None):
    # Pila explicita para evitar el limite de recursion de Python.
    # Conserva el pivote final y la particion <= del codigo del Excel.
    pendientes = [(0, len(arr) - 1)]
    terminados = 0
    while pendientes:
        izquierda, derecha = pendientes.pop()
        if izquierda >= derecha:
            if izquierda == derecha:
                terminados += 1
                if progreso:
                    progreso(terminados, len(arr))
            continue
        pivote = arr[derecha]
        i = izquierda - 1
        for j in range(izquierda, derecha):
            if arr[j] <= pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        i += 1
        arr[i], arr[derecha] = arr[derecha], arr[i]
        terminados += 1
        if progreso:
            progreso(terminados, len(arr))
        pendientes.append((i + 1, derecha))
        pendientes.append((izquierda, i - 1))


def heap_sort(arr, progreso=None):
    def heapify(n, i):
        mayor = i
        izquierda, derecha = 2 * i + 1, 2 * i + 2
        if izquierda < n and arr[izquierda] > arr[mayor]:
            mayor = izquierda
        if derecha < n and arr[derecha] > arr[mayor]:
            mayor = derecha
        if mayor != i:
            arr[i], arr[mayor] = arr[mayor], arr[i]
            heapify(n, mayor)
    pasos = 0
    total = len(arr) // 2 + max(0, len(arr) - 1)
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(len(arr), i)
        pasos += 1
        if progreso:
            progreso(pasos, total)
    for i in range(len(arr) - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
        pasos += 1
        if progreso:
            progreso(pasos, total)


def insertion_sort(arr, progreso=None):
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave
        if progreso:
            progreso(i, len(arr) - 1)


ALGORITMOS = (
    ("Merge Sort", merge_sort, "O(n log n)"),
    ("Selection Sort", selection_sort, "O(n^2)"),
    ("Bubble Sort", bubble_sort, "O(n^2); mejor caso O(n)"),
    ("Quick Sort", quick_sort, "promedio O(n log n); peor caso O(n^2)"),
    ("Heap Sort", heap_sort, "O(n log n)"),
    ("Insertion Sort", insertion_sort, "O(n^2); mejor caso O(n)"),
)


def leer_lista(texto):
    texto = texto.strip()
    if texto.startswith("["):
        if not texto.endswith("]"):
            raise ValueError("Falta el corchete de cierre ].")
        texto = texto[1:-1].strip()
    lista = []
    # Procesa un token a la vez para no crear otra lista con millones de textos.
    for coincidencia in re.finditer(r"[^\s,;]+", texto):
        token = coincidencia.group()
        if not re.fullmatch(r"[+-]?[0-9]+", token):
            raise ValueError("Usa enteros separados por espacios, comas o punto y coma.")
        valor = int(token)
        if not -2147483648 <= valor <= 2147483647:
            raise ValueError("Cada entero debe estar entre -2147483648 y 2147483647.")
        lista.append(valor)
    if not lista:
        raise ValueError("Ingresa al menos un numero entero.")
    return lista


def pedir_lista():
    while True:
        print("\nPega tu lista de enteros, sin limite de cantidad. Puedes usar varias lineas.")
        print("Ejemplo: 38, 27, -5, 3, 9, 27")
        print("Termina con una linea vacia: Enter dos veces despues del ultimo numero.")
        lineas = []
        while True:
            linea = input()
            if not linea.strip():
                break
            lineas.append(linea)
        try:
            return leer_lista("\n".join(lineas))
        except ValueError as error:
            print(f"Entrada invalida: {error}")


def ejecutar(original, opcion):
    seleccion = ALGORITMOS if opcion == 7 else (ALGORITMOS[opcion - 1],)
    print(f"\nElementos: {len(original)}")
    for nombre, algoritmo, complejidad in seleccion:
        copia = original.copy()
        barra = BarraProgreso(nombre)
        inicio = perf_counter()
        try:
            algoritmo(copia, barra.actualizar)
        except BaseException:
            print("\nOrdenamiento interrumpido.")
            raise
        segundos = perf_counter() - inicio
        barra.finalizar()
        correcto = all(copia[i] <= copia[i + 1] for i in range(len(copia) - 1))
        print(f"\n--- {nombre} ---")
        print(f"Complejidad: {complejidad}")
        if len(copia) <= 100:
            print("Lista ordenada:", ", ".join(map(str, copia)))
        else:
            print("Lista ordenada (primeros 50 y ultimos 50):")
            print(", ".join(map(str, copia[:50])), "...", ", ".join(map(str, copia[-50:])))
        print(f"Tiempo de ordenamiento: {segundos * 1000:.6f} ms")
        print(f"Tiempo en segundos: {segundos:.9f} s")
        print("Estado:", "Correcto" if correcto else "Error")
    print("\nEl tiempo incluye el seguimiento de progreso; excluye lectura, copia inicial y salida de resultados.")


def main():
    try:
        while True:
            print("\n========== LABORATORIO DE ORDENAMIENTO ==========")
            for i, (nombre, _, _) in enumerate(ALGORITMOS, 1):
                print(f"  {i}. {nombre}")
            print("  7. Comparar los 6 algoritmos")
            print("  8. Ver archivos disponibles")
            print("  9. Generar arreglo y guardar archivo\n  0. Salir")
            opcion = input("Opcion: ").strip()
            if opcion not in tuple(map(str, range(10))):
                print("Opcion invalida. Escribe un numero de 0 a 9.")
                continue
            opcion = int(opcion)
            if opcion == 0:
                break
            try:
                if opcion == 9:
                    pedir_arreglo_aleatorio()
                    continue
                if opcion == 8:
                    archivos = sorted(CARPETA_ARREGLOS.glob("*.txt"))
                    print(f"Carpeta: {CARPETA_ARREGLOS}")
                    for ruta in archivos:
                        print(f"  {ruta.name} ({ruta.stat().st_size:,} bytes)")
                    if not archivos:
                        print("No hay archivos. Usa la opcion 9 para generar uno.")
                    continue
                ruta = elegir_archivo()
                if ruta is None:
                    continue
                print(f"Cargando {ruta.name}...")
                lista = cargar_archivo(ruta)
                ejecutar(lista, opcion)
                del lista
            except FileExistsError:
                print("Ese archivo ya existe. Elige otro nombre para conservarlo.")
            except (OSError, ValueError) as error:
                print(f"No se pudo completar: {error}")
            except MemoryError:
                print("No hay memoria suficiente para completar esta operacion.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Programa finalizado.")


if __name__ == "__main__":
    main()
