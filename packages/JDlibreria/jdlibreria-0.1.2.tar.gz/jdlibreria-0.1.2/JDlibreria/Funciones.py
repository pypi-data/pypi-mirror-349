#Funciones.py
import random   # Importar random para generar numeros aleatorios
import numpy as np

# Funcion objetivo a minimizar
def funcion_objetivo(x):
    # """ calcula el cuadrado del valor de x. """
    return x ** 2

# Crear un individuo aleatorio
def crear_individuo(valor_min, valor_max):
    # """ Genera un numero aleatorio dentro de un rango especifico """
    return random.uniform(valor_min, valor_max)
print (crear_individuo)   

# crear una poblacion inicial
def crear_poblacion(tamano, valor_min, valor_max):
    # Genera una lista de individuos aleatorios
    return [crear_individuo(valor_min, valor_max) for _ in range(tamano)]

# Ángulo de altura solar mínima
def calcular_Hmin(latitud, invierno):
    return (90 - latitud) - invierno

# Distancia mínima entre paneles
def calcular_DM(B, beta_grados, latitud, invierno):
    beta = np.radians(beta_grados)
    Hmin = np.radians(calcular_Hmin(latitud, invierno))
    return B * np.cos(beta) + (B * np.sin(beta)) / np.tan(Hmin)

# Función de aptitud para una población de betas
def fitness(beta_array, B, latitud, invierno):
    return -np.array([calcular_DM(B, beta, latitud, invierno) for beta in beta_array])

def seleccion_torneo_binario(poblacion, aptitudes):
    seleccionados = []
    tam_poblacion = len(poblacion)
    for _ in range(tam_poblacion):
        a, b = random.sample(range(tam_poblacion), 2)
        ganador = poblacion[a] if aptitudes[a] > aptitudes[b] else poblacion[b]
        seleccionados.append(ganador)
    return seleccionados

# Cruce por un punto para dos individuos (números reales)
def cruce_un_punto(padre1, padre2):
    # Como tus individuos son números reales, el cruce puede ser un promedio ponderado
    alpha = random.random()
    hijo1 = alpha * padre1 + (1 - alpha) * padre2
    hijo2 = alpha * padre2 + (1 - alpha) * padre1
    return hijo1, hijo2

# Cruce por cruce (blend crossover) - mezcla aleatoria dentro de un rango
def cruce_blend(padre1, padre2, alpha=0.5):
    d = abs(padre1 - padre2)
    min_val = min(padre1, padre2) - alpha * d
    max_val = max(padre1, padre2) + alpha * d
    hijo = random.uniform(min_val, max_val)
    return hijo

# Mutación: suma un pequeño ruido gaussiano al individuo
def mutacion(individuo, sigma=0.1):
    return individuo + random.gauss(0, sigma)