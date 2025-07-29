# JDlibreria

JDlibreria es una librería de ejemplo en Python que incluye funciones para optimización, geometría solar y algoritmos genéticos básicos. Este módulo puede ser utilizado como base para experimentar con algoritmos evolutivos aplicados al diseño de paneles solares.

## 📁 Contenido del módulo

El archivo `Funciones.py` incluye funciones organizadas en las siguientes categorías:

### 🔧 Funciones de Optimización

- **`funcion_objetivo(x)`**  
  Calcula el valor de `x²`. Es una función de prueba comúnmente usada en algoritmos de optimización para minimizar.

- **`crear_individuo(valor_min, valor_max)`**  
  Genera un número aleatorio dentro de un rango dado. Representa un "individuo" en un algoritmo genético.

- **`crear_poblacion(tamano, valor_min, valor_max)`**  
  Crea una lista de individuos aleatorios dentro de un rango, simulando una población inicial.

### ☀️ Funciones de Geometría Solar

- **`calcular_Hmin(latitud, invierno)`**  
  Calcula el ángulo mínimo de altura solar (`Hmin`) en base a la latitud y la inclinación solar en invierno.

- **`calcular_DM(B, beta_grados, latitud, invierno)`**  
  Calcula la distancia mínima (`DM`) entre paneles solares basada en el ancho de los paneles (`B`), su inclinación (`beta`), y la ubicación geográfica.

### 🧬 Algoritmos Genéticos

- **`fitness(beta_array, B, latitud, invierno)`**  
  Evalúa la función de aptitud para un array de ángulos de inclinación (`beta`) con base en la distancia mínima entre paneles. Devuelve valores negativos de `DM` para aplicar técnicas de maximización.

- **`seleccion_torneo_binario(poblacion, aptitudes)`**  
  Implementa un torneo binario para seleccionar los mejores individuos de la población según sus aptitudes.

---

## 👥 Autores

*Jorge Ivan Salazar Gomez*  
*David Ricardo Contreras Espinosa*  
Machine Learning y Algoritmos Genéticos – Universidad de Cundinamarca

---

## 🚀 Requisitos

- Python 3.6 o superior
- `numpy`

Instalación de dependencias:
```bash
pip install numpy
