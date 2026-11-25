#pragma once
#include <cstddef>
#include <string>
#include <vector>

namespace tarea {
constexpr std::size_t limiteNumeros = 5000;
constexpr int cantidadAlgoritmos = 6;
struct Algoritmo { const wchar_t* nombre; const wchar_t* complejidad; };
extern const Algoritmo algoritmos[cantidadAlgoritmos];
std::vector<int> leerLista(const std::wstring& texto);
std::wstring mostrarLista(const std::vector<int>& lista);
void ordenar(int algoritmo, std::vector<int>& lista);
}
