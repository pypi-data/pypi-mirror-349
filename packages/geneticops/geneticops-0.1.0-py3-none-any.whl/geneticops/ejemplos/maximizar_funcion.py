"""
Ejemplo de maximización de una función con geneticops
===================================================

Este ejemplo muestra cómo usar geneticops para encontrar el máximo
de una función simple de dos variables.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from geneticops import (
    AlgoritmoGenetico, 
    inicializar_poblacion_real,
    seleccion_torneo,
    cruce_aritmetico,
    mutacion_gaussiana,
    reemplazo_elitismo,
    condicion_max_generaciones,
    graficar_convergencia
)

def funcion_objetivo(x, y):
    """
    Función a maximizar: f(x,y) = sin(x) * cos(y) * exp(-sqrt(x^2 + y^2)/5)
    Tiene múltiples máximos locales en el rango [-10, 10] para ambas variables.
    """
    return np.sin(x) * np.cos(y) * np.exp(-np.sqrt(x**2 + y**2)/5)

def fitness(individuo):
    """
    Función de fitness: evalúa la función objetivo con los valores del individuo.
    """
    x, y = individuo
    return funcion_objetivo(x, y)

def visualizar_funcion():
    """
    Visualiza la función objetivo en 3D.
    """
    # Crear malla de puntos
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = funcion_objetivo(X, Y)
    
    # Crear gráfico 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(X,Y)')
    ax.set_title('Función Objetivo: sin(x) * cos(y) * exp(-sqrt(x^2 + y^2)/5)')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def visualizar_resultado(mejor_individuo, mejor_fitness):
    """
    Visualiza el resultado final.
    """
    x, y = mejor_individuo
    print(f"Mejor solución encontrada:")
    print(f"x = {x:.6f}, y = {y:.6f}")
    print(f"Valor de fitness = {mejor_fitness:.6f}")
    
    # Crear malla de puntos
    x_range = np.linspace(-10, 10, 100)
    y_range = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = funcion_objetivo(X, Y)
    
    # Crear gráfico de contorno con la solución
    plt.figure(figsize=(10, 8))
    contour = plt.contourf(X, Y, Z, 50, cmap='viridis')
    plt.colorbar(contour)
    plt.plot(x, y, 'ro', markersize=10)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Solución Óptima: f({x:.4f}, {y:.4f}) = {mejor_fitness:.4f}')
    plt.grid(True)
    plt.show()

def main():
    # Definir parámetros del algoritmo genético
    tamano_poblacion = 100
    longitud_individuo = 2  # Dos variables: x e y
    max_generaciones = 100
    probabilidad_cruce = 0.8
    probabilidad_mutacion = 0.1
    
    # Crear instancia del algoritmo genético
    ag = AlgoritmoGenetico(
        tamano_poblacion=tamano_poblacion,
        longitud_individuo=longitud_individuo,
        funcion_fitness=fitness,
        funcion_inicializacion=inicializar_poblacion_real,
        funcion_seleccion=seleccion_torneo,
        funcion_cruce=cruce_aritmetico,
        funcion_mutacion=mutacion_gaussiana,
        funcion_reemplazo=reemplazo_elitismo,
        condicion_parada=condicion_max_generaciones,
        probabilidad_cruce=probabilidad_cruce,
        probabilidad_mutacion=probabilidad_mutacion,
        elitismo=0.1,
        max_generaciones=max_generaciones,
        tipo_genoma='real',
        parametros_adicionales={
            'limites': [-10, 10],  # Límites para las variables
            'seleccion': {'tamano_torneo': 3},
            'cruce': {'alpha': 0.5},
            'mutacion': {'media': 0.0, 'desviacion': 0.5}
        }
    )
    
    # Ejecutar el algoritmo
    mejor_individuo, mejor_fitness, info = ag.ejecutar()
    
    # Visualizar resultados
    visualizar_funcion()
    visualizar_resultado(mejor_individuo, mejor_fitness)
    graficar_convergencia(info['historia_fitness'], "Convergencia del AG en Maximización de Función")
    
    print(f"\nTiempo de ejecución: {info['tiempo_ejecucion']:.2f} segundos")
    print(f"Generaciones ejecutadas: {info['generaciones']}")

if __name__ == "__main__":
    main()