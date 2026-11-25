#include "Algoritmos.h"
#include <algorithm>
#include <iostream>
#include <random>
#include <stdexcept>

void comprobar(bool condicion, const char* mensaje) {
    if (!condicion) throw std::runtime_error(mensaje);
}
int main() {
    try {
        comprobar(tarea::leerLista(L" [8, -3; +2\r\n0 8] ") == std::vector<int>({8,-3,2,0,8}), "Separadores");
        comprobar(tarea::leerLista(L"-2147483648,2147483647") == std::vector<int>({(-2147483647-1),2147483647}), "Limites int");
        for (const auto* texto : {L"", L"[]", L"1.5", L"1x", L"1-2", L"+", L"[1,2", L"1,2]", L"2147483648", L"-2147483649", L"[[1]]"}) {
            bool rechazo = false;
            try { tarea::leerLista(texto); } catch (const std::invalid_argument&) { rechazo = true; }
            comprobar(rechazo, "Entrada invalida aceptada");
        }
        std::wstring limite;
        for (std::size_t i = 0; i < tarea::limiteNumeros; ++i) limite += L"1 ";
        comprobar(tarea::leerLista(limite).size() == tarea::limiteNumeros, "Limite valido");
        bool rechazo = false;
        try { tarea::leerLista(limite + L"1"); } catch (const std::invalid_argument&) { rechazo = true; }
        comprobar(rechazo, "Exceso de elementos");
        std::mt19937 generador(1234);
        std::uniform_int_distribution<int> numero(-10000, 10000);
        std::vector<std::vector<int>> casos = {{}, {1}, {2,1}, {1,1,1}, {0,-1,2,-1}, {(-2147483647-1),2147483647,0}};
        for (int n : {10,100,1000}) {
            std::vector<int> datos(n);
            for (auto& v : datos) v = numero(generador);
            casos.push_back(datos);
        }
        std::vector<int> asc(tarea::limiteNumeros), iguales(tarea::limiteNumeros, 7);
        for (std::size_t i = 0; i < asc.size(); ++i) asc[i] = static_cast<int>(i);
        casos.push_back(asc);
        std::reverse(asc.begin(), asc.end()); casos.push_back(asc); casos.push_back(iguales);
        int total = 0;
        for (int algoritmo = 0; algoritmo < tarea::cantidadAlgoritmos; ++algoritmo) {
            for (auto entrada : casos) {
                auto esperado = entrada; std::sort(esperado.begin(), esperado.end());
                tarea::ordenar(algoritmo, entrada);
                comprobar(entrada == esperado, "Resultado incorrecto"); ++total;
            }
        }
        std::cout << total << " casos de ordenamiento correctos; validacion de entrada correcta.\n";
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
}
