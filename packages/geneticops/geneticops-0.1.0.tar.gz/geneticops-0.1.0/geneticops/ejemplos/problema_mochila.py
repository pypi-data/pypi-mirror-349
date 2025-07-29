"""
Ejemplo del problema de la mochila con geneticops
===============================================

Este ejemplo muestra cómo usar geneticops para resolver el problema de la mochila.
Problema: Tenemos n objetos, cada uno con un peso y un valor. Queremos maximizar
el valor total sin exceder un peso máximo.
"""

import numpy as np
import matplotlib.pyplot as plt
from geneticops import (
    AlgoritmoGenetico,
    inicializar_poblacion_binaria,
    seleccion_ruleta,
    cruce_un_punto,
    mutacion_bit_flip,
    reemplazo_elitismo,
    condicion_max_generaciones,
    graficar_convergencia
)

# Definir los datos del problema
objetos = [
    {"nombre": "Laptop", "peso": 3.0, "valor": 2000},
    {"nombre": "Teléfono", "peso": 0.3, "valor": 800},
    {"nombre": "Cámara", "peso": 1.0, "valor": 1500},
    {"nombre": "Disco Duro", "peso": 0.5, "valor": 300},
    {"nombre": "Tablet", "peso": 0.7, "valor": 1200},
    {"nombre": "Libro", "peso": 1.5, "valor": 150},
    {"nombre": "Reloj", "peso": 0.2, "valor": 500},
    {"nombre": "Joya", "peso": 0.1, "valor": 2500},
    {"nombre": "Altavoz", "peso": 2.0, "valor": 400},
    {"nombre": "Batería Externa", "peso": 0.4, "valor": 250},
    {"nombre": "Ropa", "peso": 2.0, "valor": 350},
    {"nombre": "Zapatos", "peso": 1.5, "valor": 400},
    {"nombre": "Botella de Agua", "peso": 0.8, "valor": 50},
    {"nombre": "Comida", "peso": 1.0, "valor": 200},
    {"nombre": "Kit de Primeros Auxilios", "peso": 1.2, "valor": 600}
]

# Peso máximo de la mochila
peso_maximo = 10.0

# Extraer listas de pesos y valores para facilitar el cálculo
pesos = np.array([objeto["peso"] for objeto in objetos])
valores = np.array([objeto["valor"] for objeto in objetos])
nombres = [objeto["nombre"] for objeto in objetos]

def fitness(individuo):
    """
    Función de fitness para el problema de la mochila.
    - Si la solución es factible (no excede el peso máximo), el fitness es el valor total.
    - Si la solución no es factible, se penaliza.
    """
    peso_total = np.sum(pesos * individuo)
    valor_total = np.sum(valores * individuo)
    
    # Si excede el peso máximo, penalizar
    if peso_total > peso_maximo:
        # Penalización proporcional al exceso de peso
        return 0  # Penalización severa
    
    return valor_total

def visualizar_resultado(mejor_individuo, mejor_fitness):
    """
    Visualiza la solución óptima encontrada.
    """
    seleccionados = []
    peso_total = 0
    valor_total = 0
    
    print(f"Solución óptima (Fitness: {mejor_fitness}):")
    print("-" * 50)
    print(f"{'Objeto':<20} {'Peso':<10} {'Valor':<10} {'Seleccionado':<10}")
    print("-" * 50)
    
    for i, (nombre, peso, valor) in enumerate(zip(nombres, pesos, valores)):
        seleccionado = "Sí" if mejor_individuo[i] == 1 else "No"
        print(f"{nombre:<20} {peso:<10.1f} {valor:<10} {seleccionado:<10}")
        
        if mejor_individuo[i] == 1:
            seleccionados.append(nombre)
            peso_total += peso
            valor_total += valor
    
    print("-" * 50)
    print(f"Peso total: {peso_total:.1f} / {peso_maximo:.1f}")
    print(f"Valor total: {valor_total}")
    
    # Gráfico de barras de los objetos seleccionados y no seleccionados
    plt.figure(figsize=(10, 6))
    colores = ['green' if sel == 1 else 'red' for sel in mejor_individuo]
    indices = np.arange(len(objetos))
    
    plt.bar(indices, valores, color=colores)
    plt.xticks(indices, nombres, rotation=90)
    plt.xlabel('Objetos')
    plt.ylabel('Valor')
    plt.title('Solución del Problema de la Mochila')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Añadir leyenda
    import matplotlib.patches as mpatches
    verde = mpatches.Patch(color='green', label='Seleccionado')
    rojo = mpatches.Patch(color='red', label='No seleccionado')
    plt.legend(handles=[verde, rojo])
    
    plt.tight_layout()
    plt.show()

def main():
    # Definir parámetros del algoritmo genético
    tamano_poblacion = 100
    longitud_individuo = len(objetos)  # Un bit por objeto
    max_generaciones = 100
    probabilidad_cruce = 0.8
    probabilidad_mutacion = 0.1
    
    # Crear instancia del algoritmo genético
    ag = AlgoritmoGenetico(
        tamano_poblacion=tamano_poblacion,
        longitud_individuo=longitud_individuo,
        funcion_fitness=fitness,
        funcion_inicializacion=inicializar_poblacion_binaria,
        funcion_seleccion=seleccion_ruleta,
        funcion_cruce=cruce_un_punto,
        funcion_mutacion=mutacion_bit_flip,
        funcion_reemplazo=reemplazo_elitismo,
        condicion_parada=condicion_max_generaciones,
        probabilidad_cruce=probabilidad_cruce,
        probabilidad_mutacion=probabilidad_mutacion,
        elitismo=0.1,
        max_generaciones=max_generaciones,
        tipo_genoma='binario'
    )
    
    # Ejecutar el algoritmo
    mejor_individuo, mejor_fitness, info = ag.ejecutar()
    
    # Visualizar resultados
    visualizar_resultado(mejor_individuo, mejor_fitness)
    graficar_convergencia(info['historia_fitness'], "Convergencia del AG en Problema de la Mochila")
    
    print(f"\nTiempo de ejecución: {info['tiempo_ejecucion']:.2f} segundos")
    print(f"Generaciones ejecutadas: {info['generaciones']}")

if __name__ == "__main__":
    main()