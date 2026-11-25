#include "Algoritmos.h"
#include <cwctype>
#include <limits>
#include <sstream>
#include <stdexcept>

namespace tarea {
const Algoritmo algoritmos[cantidadAlgoritmos] = {
    {L"Merge Sort", L"O(n log n)"},
    {L"Selection Sort", L"O(n\u00b2)"},
    {L"Bubble Sort", L"O(n\u00b2); mejor caso O(n)"},
    {L"Quick Sort", L"Promedio O(n log n); peor O(n\u00b2)"},
    {L"Heap Sort", L"O(n log n)"},
    {L"Insertion Sort", L"O(n\u00b2); mejor caso O(n)"}
};

std::vector<int> leerLista(const std::wstring& texto) {
    std::size_t inicio = texto.find_first_not_of(L" \t\r\n");
    if (inicio == std::wstring::npos) throw std::invalid_argument("Ingresa una lista de numeros enteros.");
    std::size_t fin = texto.find_last_not_of(L" \t\r\n") + 1;
    if (texto[inicio] == L'[') {
        if (texto[fin - 1] != L']') throw std::invalid_argument("Falta el corchete de cierre ].");
        ++inicio; --fin;
    }
    std::vector<int> lista;
    const auto separador = [](wchar_t c) { return std::iswspace(c) || c == L',' || c == L';'; };
    for (std::size_t i = inicio; i < fin;) {
        if (separador(texto[i])) { ++i; continue; }
        const auto comienzo = i;
        if (texto[i] == L'+' || texto[i] == L'-') ++i;
        const auto digitos = i;
        while (i < fin && texto[i] >= L'0' && texto[i] <= L'9') ++i;
        if (i == digitos || (i < fin && !separador(texto[i]))) {
            throw std::invalid_argument("Usa solo enteros separados por espacios, comas, punto y coma o saltos de linea.");
        }
        try {
            const long long valor = std::stoll(texto.substr(comienzo, i - comienzo));
            if (valor < (std::numeric_limits<int>::min)() || valor > (std::numeric_limits<int>::max)())
                throw std::out_of_range("int");
            lista.push_back(static_cast<int>(valor));
        } catch (const std::out_of_range&) {
            throw std::invalid_argument("Cada entero debe estar entre -2147483648 y 2147483647.");
        }
        if (lista.size() > limiteNumeros) throw std::invalid_argument("El limite es de 5000 numeros por ejecucion.");
    }
    if (lista.empty()) throw std::invalid_argument("La lista debe contener al menos un numero entero.");
    return lista;
}

std::wstring mostrarLista(const std::vector<int>& lista) {
    std::wostringstream salida;
    for (std::size_t i = 0; i < lista.size(); ++i) {
        if (i) salida << L", ";
        salida << lista[i];
    }
    return salida.str();
}
}
