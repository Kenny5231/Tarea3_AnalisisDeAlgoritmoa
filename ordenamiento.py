"""Algoritmos del Excel adaptados a Python. Sin dependencias externas."""
import re
from time import perf_counter

def merge_sort(arr):
    def ordenar(izquierda, derecha):
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
    ordenar(0, len(arr) - 1)


def selection_sort(arr):
    for i in range(len(arr) - 1):
        minimo = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minimo]:
                minimo = j
        arr[i], arr[minimo] = arr[minimo], arr[i]


def bubble_sort(arr):
    for i in range(len(arr) - 1):
        intercambio = False
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambio = True
        if not intercambio:
            break


def quick_sort(arr):
    # Pila explicita para evitar el limite de recursion de Python.
    # Conserva el pivote final y la particion <= del codigo del Excel.
    pendientes = [(0, len(arr) - 1)]
    while pendientes:
        izquierda, derecha = pendientes.pop()
        if izquierda >= derecha:
            continue
        pivote = arr[derecha]
        i = izquierda - 1
        for j in range(izquierda, derecha):
            if arr[j] <= pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        i += 1
        arr[i], arr[derecha] = arr[derecha], arr[i]
        if i + 1 < derecha:
            pendientes.append((i + 1, derecha))
        if izquierda < i - 1:
            pendientes.append((izquierda, i - 1))


def heap_sort(arr):
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
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(len(arr), i)
    for i in range(len(arr) - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)


def insertion_sort(arr):
    for i in range(1, len(arr)):
        clave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = clave


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
        inicio = perf_counter()
        algoritmo(copia)
        segundos = perf_counter() - inicio
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
    print("\nEl tiempo excluye ingreso de datos, copia inicial y salida en pantalla.")


def main():
    lista = []
    try:
        while True:
            print("\n========== LABORATORIO DE ORDENAMIENTO ==========")
            for i, (nombre, _, _) in enumerate(ALGORITMOS, 1):
                print(f"  {i}. {nombre}")
            print("  7. Comparar los 6 algoritmos\n  8. Ingresar / cambiar lista\n  0. Salir")
            print(f"Lista actual: {len(lista)} numeros")
            opcion = input("Opcion: ").strip()
            if opcion not in tuple(map(str, range(9))):
                print("Opcion invalida. Escribe un numero de 0 a 8.")
                continue
            opcion = int(opcion)
            if opcion == 0:
                break
            if opcion == 8 or not lista:
                lista = pedir_lista()
                print(f"Lista guardada: {len(lista)} numeros.")
            if opcion != 8:
                ejecutar(lista, opcion)
    except (EOFError, KeyboardInterrupt):
        print()
    print("Programa finalizado.")


if __name__ == "__main__":
    main()
