// Funciones originales de las celdas A2 de las seis hojas del Excel.
#include "Algoritmos.h"
#include <stdexcept>
#include <utility>
#include <vector>
using std::vector;
using std::swap;

void merge(int arr[], int izquierda, int medio, int derecha) {
    int n1 = medio - izquierda + 1;
    int n2 = derecha - medio;

    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; i++)
        L[i] = arr[izquierda + i];

    for (int j = 0; j < n2; j++)
        R[j] = arr[medio + 1 + j];

    int i = 0, j = 0, k = izquierda;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[], int izquierda, int derecha) {
    if (izquierda < derecha) {
        int medio = izquierda + (derecha - izquierda) / 2;

        mergeSort(arr, izquierda, medio);
        mergeSort(arr, medio + 1, derecha);

        merge(arr, izquierda, medio, derecha);
    }
}

void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int minimo = i;

        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minimo]) {
                minimo = j;
            }
        }

        swap(arr[i], arr[minimo]);
    }
}

void bubbleSort(int arr[], int n) {
    bool intercambio;

    for (int i = 0; i < n - 1; i++) {
        intercambio = false;

        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                intercambio = true;
            }
        }

        if (!intercambio) {
            break;
        }
    }
}

int particion(int arr[], int izquierda, int derecha) {
    int pivote = arr[derecha];
    int i = izquierda - 1;

    for (int j = izquierda; j < derecha; j++) {
        if (arr[j] <= pivote) {
            i++;
            swap(arr[i], arr[j]);
        }
    }

    swap(arr[i + 1], arr[derecha]);

    return i + 1;
}

void quickSort(int arr[], int izquierda, int derecha) {
    if (izquierda < derecha) {
        int pivote = particion(arr, izquierda, derecha);

        quickSort(arr, izquierda, pivote - 1);
        quickSort(arr, pivote + 1, derecha);
    }
}

void heapify(int arr[], int n, int i) {
    int mayor = i;
    int izquierda = 2 * i + 1;
    int derecha = 2 * i + 2;

    if (izquierda < n && arr[izquierda] > arr[mayor]) {
        mayor = izquierda;
    }

    if (derecha < n && arr[derecha] > arr[mayor]) {
        mayor = derecha;
    }

    if (mayor != i) {
        swap(arr[i], arr[mayor]);

        heapify(arr, n, mayor);
    }
}

void heapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }

    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);

        heapify(arr, i, 0);
    }
}

void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int clave = arr[i];
        int j = i - 1;

        while (j >= 0 && arr[j] > clave) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = clave;
    }
}

namespace tarea {
void ordenar(int algoritmo, std::vector<int>& lista) {
    if (algoritmo < 0 || algoritmo >= cantidadAlgoritmos) throw std::invalid_argument("Algoritmo invalido.");
    if (lista.empty()) return;
    const int n = static_cast<int>(lista.size());
    switch (algoritmo) {
    case 0: mergeSort(lista.data(), 0, n - 1); break;
    case 1: selectionSort(lista.data(), n); break;
    case 2: bubbleSort(lista.data(), n); break;
    case 3: quickSort(lista.data(), 0, n - 1); break;
    case 4: heapSort(lista.data(), n); break;
    case 5: insertionSort(lista.data(), n); break;
    }
}
}