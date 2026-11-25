#include "Algoritmos.h"
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <locale>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
// ASCII evita problemas con las paginas de codigos de terminales antiguas.
std::string textoConsola(const std::wstring& texto) {
    std::string salida;
    for (wchar_t c : texto) {
        if (c == L'\u00b2') salida += "^2";
        else salida += static_cast<char>(c);
    }
    return salida;
}

void menu(std::size_t cantidad) {
    std::cout << "\n========== LABORATORIO DE ORDENAMIENTO ==========\n";
    for (int i = 0; i < tarea::cantidadAlgoritmos; ++i)
        std::cout << "  " << i + 1 << ". " << textoConsola(tarea::algoritmos[i].nombre) << '\n';
    std::cout << "  7. Comparar los 6 algoritmos\n"
                 "  8. Ingresar / cambiar lista\n"
                 "  0. Salir\n"
              << "Lista actual: " << cantidad << " numeros\n"
                 "Opcion: " << std::flush;
}

bool pedirLista(std::vector<int>& lista) {
    while (true) {
        std::cout << "\nPega tu lista de enteros (maximo 5000).\n"
                     "Separa con espacios, comas, punto y coma o saltos de linea.\n"
                     "Termina con una linea vacia (Enter dos veces).\n"
                     "Ejemplo: 38, 27, -5, 3, 9, 27\n> " << std::flush;
        std::string texto, linea;
        bool exceso = false;
        while (std::getline(std::cin, linea)) {
            if (linea.find_first_not_of(" \t\r") == std::string::npos) break;
            if (texto.size() + linea.size() + 1 > 100000) exceso = true;
            if (!exceso) { texto += linea; texto += '\n'; }
        }
        if (std::cin.eof() && texto.empty()) return false;
        try {
            if (exceso) throw std::invalid_argument("El texto supera los 100000 caracteres.");
            auto nueva = tarea::leerLista(std::wstring(texto.begin(), texto.end()));
            lista = std::move(nueva);
            std::cout << "Lista guardada: " << lista.size() << " numeros.\n";
            return true;
        } catch (const std::exception& e) {
            std::cout << "Entrada invalida: " << e.what() << '\n';
            if (!std::cin) return false;
        }
    }
}

void ejecutar(const std::vector<int>& original, int opcion) {
    const int primero = opcion == 7 ? 0 : opcion - 1;
    const int ultimo = opcion == 7 ? tarea::cantidadAlgoritmos : opcion;
    std::cout << "\nElementos: " << original.size() << '\n';
    for (int i = primero; i < ultimo; ++i) {
        auto copia = original;
        const auto inicio = std::chrono::steady_clock::now();
        tarea::ordenar(i, copia);
        const auto fin = std::chrono::steady_clock::now();
        const double milisegundos = std::chrono::duration<double, std::milli>(fin - inicio).count();
        const bool correcto = std::is_sorted(copia.begin(), copia.end());
        std::cout << "\n--- " << textoConsola(tarea::algoritmos[i].nombre) << " ---\n"
                  << "Complejidad: " << textoConsola(tarea::algoritmos[i].complejidad) << '\n'
                  << "Lista ordenada: " << textoConsola(tarea::mostrarLista(copia)) << '\n'
                  << std::fixed << std::setprecision(6)
                  << "Tiempo de ordenamiento: " << milisegundos << " ms\n"
                  << std::setprecision(9)
                  << "Tiempo en segundos: " << milisegundos / 1000.0 << " s\n"
                  << "Estado: " << (correcto ? "Correcto" : "Error") << '\n';
    }
    std::cout << "\nEl tiempo excluye ingreso de datos, copia inicial y salida en pantalla.\n";
}
}

int main() {
    std::cout.imbue(std::locale::classic());
    std::vector<int> lista;
    std::string linea;
    while (true) {
        menu(lista.size());
        if (!std::getline(std::cin, linea)) break;
        std::istringstream entrada(linea);
        int opcion;
        char sobrante;
        if (!(entrada >> opcion) || (entrada >> sobrante) || opcion < 0 || opcion > 8) {
            std::cout << "Opcion invalida. Escribe un numero de 0 a 8.\n";
            continue;
        }
        if (opcion == 0) break;
        if (opcion == 8) {
            if (!pedirLista(lista)) break;
            continue;
        }
        if (lista.empty() && !pedirLista(lista)) break;
        try { ejecutar(lista, opcion); }
        catch (const std::exception& e) { std::cout << "No se pudo completar: " << e.what() << '\n'; }
    }
    std::cout << "Programa finalizado.\n";
    return 0;
}
