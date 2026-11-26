# Laboratorio de ordenamiento en Python

Programa de consola para Python 3.12, usando solo la biblioteca estándar. No requiere descargas, pip, compilación ni Windows SDK.

## Ejecutar

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
python .\ordenamiento.py
```

## Uso con archivos

1. Ejecuta `python .\ordenamiento.py`.
2. Elige **9**, ingresa la cantidad de enteros (por ejemplo `1000000`) y el nombre del archivo (por ejemplo `prueba_millon`).
3. Se crea `arreglos/prueba_millon.txt` junto al programa. Se agrega `.txt` si no lo escribes. Los nombres existentes no se sobrescriben.
4. Elige **1 a 6** para un algoritmo, o **7** para comparar los seis.
5. El programa muestra los archivos disponibles: escribe el número del archivo que quieras utilizar. Elige **0** para cancelar la selección.
6. Verás el resultado y el tiempo en milisegundos y segundos. Cada ejecución vuelve a leer el archivo original; el archivo no se modifica al ordenar.
7. Usa **8** para ver los archivos guardados, o **0** en el menú principal para salir.

La generación usa enteros aleatorios entre -1000000 y 1000000. No tiene máximo programado de cantidad; escribe el número sin separadores de miles. Se genera por bloques para no mantener todo el arreglo en memoria al escribirlo. La capacidad depende de la memoria y del espacio en disco disponibles. Ya no se utiliza el portapapeles.

También puedes colocar tus propios archivos `.txt` en `arreglos`. Usa enteros de 32 bits separados por espacios, comas, punto y coma o saltos de línea. Para archivos de varias líneas, omite los corchetes. Un archivo vacío o con datos inválidos muestra un mensaje de error.

Para listas de más de 100 elementos se muestran los primeros 50 y los últimos 50 del resultado; todos los elementos se ordenan y verifican.

Selection, Bubble e Insertion tienen casos de tiempo cuadrático y pueden tardar muchísimo con millones de elementos. Quick Sort también puede ser cuadrático con datos ordenados o repetidos porque conserva el pivote final del Excel. La opción 7 ejecuta los seis de forma secuencial. Puedes detener el programa con Ctrl+C.

## Medición del tiempo

Los seis algoritmos muestran una barra de progreso con porcentaje, que se actualiza como máximo cada 0.2 segundos y llega al 100% cuando termina. El porcentaje representa etapas completadas, no una predicción del tiempo restante; algunas etapas pueden tardar mucho más que otras.

Se usa `time.perf_counter()` alrededor de cada llamada al algoritmo. El tiempo incluye la instrumentación y las actualizaciones de la barra, por lo que no equivale a una medición sin progreso. El tiempo excluye la generación, la lectura del archivo, la copia inicial, la verificación y la impresión del resultado; incluye la actualización de la barra. Cada algoritmo recibe una copia de la misma lista original. Son mediciones individuales y pueden variar entre ejecuciones, especialmente para listas pequeñas. El estado verifica que el resultado esté ordenado de menor a mayor.

Estas son adaptaciones a Python de los algoritmos del Excel. Quick Sort conserva el pivote final y la partición con `<=`, pero usa una pila explícita en lugar de recursión para evitar el límite de Python. Los tiempos corresponden a estas implementaciones de Python, no a las de C++.

Los archivos previos de C++ se conservan como referencia y no intervienen al ejecutar Python.

## Verificación

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
```

Las pruebas comparan los seis algoritmos contra `sorted`, verifican listas ascendentes, descendentes, repetidas, aleatorias y extremos de enteros. También cubren entradas inválidas, la conservación de la lista original y el flujo del menú por consola. Una prueba lee un millón de enteros y ejecuta Merge Sort sobre un millón de valores descendentes, verificando la salida resumida.
