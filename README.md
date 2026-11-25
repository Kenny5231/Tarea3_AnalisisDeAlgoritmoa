# Laboratorio de ordenamiento en Python

Programa de consola para Python 3.12, usando solo la biblioteca estándar. No requiere descargas, pip, compilación ni Windows SDK.

## Ejecutar

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
python .\ordenamiento.py
```

## Uso

1. Elige **1 a 6** para Merge, Selection, Bubble, Quick, Heap o Insertion Sort, o **7** para comparar los seis.
2. Escribe o pega tu lista. Ejemplo: `38, 27, -5, 3, 9, 27`.
3. Termina con una **línea vacía**: presiona Enter dos veces después del último número.
4. Consulta el resultado ordenado y el tiempo en milisegundos y segundos.
5. La lista original se conserva para ejecutar otro algoritmo. Elige **8** para cambiarla o **0** para salir. Ctrl+C también termina el programa.

Puedes usar varias líneas, espacios, comas, punto y coma y corchetes opcionales. Se aceptan negativos y repetidos; se rechazan letras y decimales. No hay un límite programado de cantidad de enteros ni de caracteres: el tamaño depende de la memoria disponible. Cada valor sigue siendo un entero de 32 bits.

Para listas de más de 100 elementos se muestran los primeros 50 y los últimos 50 del resultado; todos los elementos se ordenan y se verifican. Esto evita llenar la terminal con millones de números.

Selection, Bubble e Insertion tienen casos de tiempo cuadrático y pueden tardar muchísimo con millones de elementos. Quick Sort también puede ser cuadrático con datos ya ordenados o repetidos porque conserva el pivote final del Excel. La opción 7 ejecuta los seis de forma secuencial. Puedes detener el programa con Ctrl+C.

## Medición

Se usa `time.perf_counter()` alrededor de cada llamada al algoritmo. El tiempo excluye la captura, la copia inicial, la verificación y la salida en pantalla. Cada algoritmo recibe una copia de la misma lista original. Son mediciones individuales y pueden variar entre ejecuciones, especialmente para listas pequeñas. El estado verifica que el resultado esté ordenado de menor a mayor.

Estas son adaptaciones a Python de los algoritmos del Excel. Quick Sort conserva el pivote final y la partición con `<=`, pero usa una pila explícita en lugar de recursión para evitar el límite de Python. Los tiempos corresponden a estas implementaciones de Python, no a las de C++.

Los archivos previos de C++ se conservan como referencia y no intervienen al ejecutar Python.

## Verificación

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
```

Las pruebas comparan los seis algoritmos contra `sorted`, verifican listas ascendentes, descendentes, repetidas, aleatorias y extremos de enteros. También cubren entradas inválidas, la conservación de la lista original y el flujo del menú por consola. Una prueba lee un millón de enteros y ejecuta Merge Sort sobre un millón de valores descendentes, verificando la salida resumida.
