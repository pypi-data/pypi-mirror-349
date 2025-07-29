"""
Ejemplo del problema del viajante de comercio (TSP) con geneticops
==============================================================

Este ejemplo muestra cómo usar geneticops para resolver el problema del
viajante de comercio (TSP): encontrar la ruta más corta que visita
todas las ciudades exactamente una vez y regresa al origen.
"""

import numpy as np
import matplotlib.pyplot as plt
from geneticops import (
    AlgoritmoGenetico,
    inicializar_poblacion_permutacion,
    seleccion_torneo,
    cruce_ox,
    mutacion_inversion,
    reemplazo_elitismo,
    condicion_max_generaciones,
    graficar_convergencia
)

# Coordenadas de ciudades (ejemplo, 20 ciudades aleatorias)
np.random.seed(42)  # Para reproducibilidad
num_ciudades = 20
ciudades = np.random.rand(num_ciudades, 2) * 100  # Coordenadas en rango [0, 100]

# Nombres de las ciudades (para visualización)
nombres_ciudades = [f"Ciudad {i+1}" for i in range(num_ciudades)]

# Calcular matriz de distancias
def calcular_matriz_distancias(coordenadas):
    """
    Calcula la matriz de distancias euclidianas entre todas las ciudades.
    """
    n = len(coordenadas)
    distancias = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i+1, n):
            dist = np.sqrt(np.sum((coordenadas[i] - coordenadas[j])**2))
            distancias[i, j] = dist
            distancias[j, i] = dist  # Matriz simétrica
    
    return distancias

matriz_distancias = calcular_matriz_distancias(ciudades)

def fitness(individuo):
    """
    Función de fitness para el TSP.
    Calcula la longitud total de la ruta (a minimizar).
    """
    # Calcular la distancia total de la ruta
    distancia_total = 0
    
    for i in range(len(individuo)-1):
        ciudad_actual = individuo[i]
        ciudad_siguiente = individuo[i+1]
        distancia_total += matriz_distancias[ciudad_actual, ciudad_siguiente]
    
    # Añadir la distancia de regreso al origen
    distancia_total += matriz_distancias[individuo[-1], individuo[0]]
    
    # Como queremos minimizar la distancia, pero el AG maximiza el fitness,
    # devolvemos el negativo de la distancia
    return -distancia_total

def visualizar_resultado(mejor_individuo, mejor_fitness):
    """
    Visualiza la ruta óptima encontrada.
    """
    # Calcular la distancia total de la ruta (sin el negativo)
    distancia_total = -mejor_fitness
    
    # Imprimir resultado
    print(f"Distancia total de la ruta óptima: {distancia_total:.2f}")
    
    # Gráfico de la ruta
    plt.figure(figsize=(10, 8))
    
    # Añadir todas las ciudades
    plt.scatter(ciudades[:, 0], ciudades[:, 1], c='blue', s=100)
    
    # Añadir números a las ciudades
    for i, (x, y) in enumerate(ciudades):
        plt.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points')
    
    # Añadir líneas para la ruta
    # Crear lista de coordenadas ordenadas según la ruta
    ruta_coords = ciudades[mejor_individuo]
    
    # Añadir el regreso al origen
    ruta_completa = np.vstack([ruta_coords, ruta_coords[0]])
    
    # Dibujar la ruta
    plt.plot(ruta_completa[:, 0], ruta_completa[:, 1], 'r-', alpha=0.7)
    
    # Destacar la ciudad de inicio
    plt.scatter(ciudades[mejor_individuo[0], 0], ciudades[mejor_individuo[0], 1], 
               c='red', s=200, marker='*', label='Inicio')
    
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Ruta Óptima del Viajante de Comercio')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    # Imprimir la secuencia de la ruta
    print("\nSecuencia de ciudades en la ruta óptima:")
    ruta_con_regreso = list(mejor_individuo) + [mejor_individuo[0]]
    for i in range(len(ruta_con_regreso)-1):
        ciudad_actual = ruta_con_regreso[i]
        ciudad_siguiente = ruta_con_regreso[i+1]
        distancia = matriz_distancias[ciudad_actual, ciudad_siguiente]
        print(f"{ciudad_actual} -> {ciudad_siguiente}: {distancia:.2f}")

def main():
    # Definir parámetros del algoritmo genético
    tamano_poblacion = 100
    longitud_individuo = num_ciudades  # Una permutación de todas las ciudades
    max_generaciones = 500
    probabilidad_cruce = 0.9
    probabilidad_mutacion = 0.2
    
    # Crear instancia del algoritmo genético
    ag = AlgoritmoGenetico(
        tamano_poblacion=tamano_poblacion,
        longitud_individuo=longitud_individuo,
        funcion_fitness=fitness,
        funcion_inicializacion=inicializar_poblacion_permutacion,
        funcion_seleccion=seleccion_torneo,
        funcion_cruce=cruce_ox,
        funcion_mutacion=mutacion_inversion,
        funcion_reemplazo=reemplazo_elitismo,
        condicion_parada=condicion_max_generaciones,
        probabilidad_cruce=probabilidad_cruce,
        probabilidad_mutacion=probabilidad_mutacion,
        elitismo=0.1,
        max_generaciones=max_generaciones,
        tipo_genoma='permutacion',
        parametros_adicionales={
            'seleccion': {'tamano_torneo': 4, 'maximizar': True}
        }
    )
    
    # Ejecutar el algoritmo
    mejor_individuo, mejor_fitness, info = ag.ejecutar()
    
    # Visualizar resultados
    visualizar_resultado(mejor_individuo, mejor_fitness)
    graficar_convergencia(info['historia_fitness'], "Convergencia del AG en Problema TSP")
    
    print(f"\nTiempo de ejecución: {info['tiempo_ejecucion']:.2f} segundos")
    print(f"Generaciones ejecutadas: {info['generaciones']}")

if __name__ == "__main__":
    main()