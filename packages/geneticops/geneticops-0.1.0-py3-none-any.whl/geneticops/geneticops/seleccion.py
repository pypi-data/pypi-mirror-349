"""
Módulo de selección
=================

Este módulo contiene las funciones relacionadas con la selección de individuos
para reproducción en algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np


def seleccion_ruleta(
    poblacion: List[np.ndarray],
    valores_fitness: List[float],
    num_seleccionados: int,
    maximizar: bool = True,
    **kwargs
) -> Tuple[List[np.ndarray], List[float]]:
    """
    Selecciona individuos mediante el método de ruleta.
    
    La probabilidad de selección de cada individuo es proporcional a su fitness.
    
    Parameters
    ----------
    poblacion : List[np.ndarray]
        Lista de individuos a seleccionar.
    valores_fitness : List[float]
        Lista con los valores de fitness de cada individuo.
    num_seleccionados : int
        Número de individuos a seleccionar.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[List[np.ndarray], List[float]]
        Tupla con la lista de individuos seleccionados y sus valores de fitness.
    
    Examples
    --------
    >>> poblacion = [np.array([1, 0, 1]), np.array([0, 1, 0]), np.array([1, 1, 1])]
    >>> fitness = [2, 1, 3]
    >>> seleccionados, sel_fitness = seleccion_ruleta(poblacion, fitness, 2)
    >>> len(seleccionados)
    2
    """
    # Asegurarse de que el fitness sea adecuado para maximización
    fitness_ajustado = np.array(valores_fitness)
    if not maximizar:
        # Para minimización, invertimos los valores
        fitness_ajustado = np.max(fitness_ajustado) + 1 - fitness_ajustado
    
    # Manejar valores negativos o cero
    if np.min(fitness_ajustado) <= 0:
        # Desplazar todos los valores para que sean positivos
        fitness_ajustado = fitness_ajustado - np.min(fitness_ajustado) + 1e-10
    
    # Calcular probabilidades de selección
    suma_fitness = np.sum(fitness_ajustado)
    probabilidades = fitness_ajustado / suma_fitness if suma_fitness > 0 else np.ones_like(fitness_ajustado) / len(fitness_ajustado)
    
    # Seleccionar individuos
    indices_seleccionados = np.random.choice(
        len(poblacion), 
        size=num_seleccionados, 
        replace=True, 
        p=probabilidades
    )
    
    # Obtener los individuos seleccionados y sus fitness
    seleccionados = [np.copy(poblacion[i]) for i in indices_seleccionados]
    fitness_seleccionados = [valores_fitness[i] for i in indices_seleccionados]
    
    return seleccionados, fitness_seleccionados


def seleccion_torneo(
    poblacion: List[np.ndarray],
    valores_fitness: List[float],
    num_seleccionados: int,
    tamano_torneo: int = 3,
    maximizar: bool = True,
    **kwargs
) -> Tuple[List[np.ndarray], List[float]]:
    """
    Selecciona individuos mediante el método de torneo.
    
    En cada torneo, se escogen aleatoriamente 'tamano_torneo' individuos
    y se selecciona el que tiene mejor fitness.
    
    Parameters
    ----------
    poblacion : List[np.ndarray]
        Lista de individuos a seleccionar.
    valores_fitness : List[float]
        Lista con los valores de fitness de cada individuo.
    num_seleccionados : int
        Número de individuos a seleccionar.
    tamano_torneo : int, optional
        Número de participantes en cada torneo. Por defecto es 3.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[List[np.ndarray], List[float]]
        Tupla con la lista de individuos seleccionados y sus valores de fitness.
    
    Examples
    --------
    >>> poblacion = [np.array([1, 0, 1]), np.array([0, 1, 0]), np.array([1, 1, 1])]
    >>> fitness = [2, 1, 3]
    >>> seleccionados, sel_fitness = seleccion_torneo(poblacion, fitness, 2, 2)
    >>> len(seleccionados)
    2
    """
    seleccionados = []
    fitness_seleccionados = []
    
    tamano_torneo = min(tamano_torneo, len(poblacion))
    
    for _ in range(num_seleccionados):
        # Seleccionar participantes aleatorios para el torneo
        indices_torneo = np.random.choice(len(poblacion), size=tamano_torneo, replace=False)
        
        # Obtener los fitness de los participantes
        fitness_participantes = [valores_fitness[i] for i in indices_torneo]
        
        # Encontrar el mejor participante
        if maximizar:
            idx_mejor = np.argmax(fitness_participantes)
        else:
            idx_mejor = np.argmin(fitness_participantes)
        
        # Agregar el mejor a los seleccionados
        idx_seleccionado = indices_torneo[idx_mejor]
        seleccionados.append(np.copy(poblacion[idx_seleccionado]))
        fitness_seleccionados.append(valores_fitness[idx_seleccionado])
    
    return seleccionados, fitness_seleccionados


def seleccion_ranking(
    poblacion: List[np.ndarray],
    valores_fitness: List[float],
    num_seleccionados: int,
    presion_selectiva: float = 1.5,
    maximizar: bool = True,
    **kwargs
) -> Tuple[List[np.ndarray], List[float]]:
    """
    Selecciona individuos mediante el método de ranking lineal.
    
    La probabilidad de selección se basa en el ranking del individuo, no en su valor
    absoluto de fitness, lo que permite mantener la diversidad.
    
    Parameters
    ----------
    poblacion : List[np.ndarray]
        Lista de individuos a seleccionar.
    valores_fitness : List[float]
        Lista con los valores de fitness de cada individuo.
    num_seleccionados : int
        Número de individuos a seleccionar.
    presion_selectiva : float, optional
        Controla la presión de selección. Valores entre 1.0 y 2.0. Por defecto es 1.5.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[List[np.ndarray], List[float]]
        Tupla con la lista de individuos seleccionados y sus valores de fitness.
    
    Examples
    --------
    >>> poblacion = [np.array([1, 0, 1]), np.array([0, 1, 0]), np.array([1, 1, 1])]
    >>> fitness = [2, 1, 3]
    >>> seleccionados, sel_fitness = seleccion_ranking(poblacion, fitness, 2)
    >>> len(seleccionados)
    2
    """
    n = len(poblacion)
    
    # Obtener los índices ordenados según fitness
    if maximizar:
        indices_ordenados = np.argsort(valores_fitness)[::-1]  # Mayor a menor
    else:
        indices_ordenados = np.argsort(valores_fitness)  # Menor a mayor
    
    # Calcular las probabilidades basadas en el ranking
    # El mejor individuo tiene probabilidad 'presion_selectiva'/n, el peor 1/n
    probabilidades = np.zeros(n)
    for rank, idx in enumerate(indices_ordenados):
        probabilidades[idx] = (2 - presion_selectiva) / n + (2 * (presion_selectiva - 1) * (n - rank - 1)) / (n * (n - 1))
    
    # Seleccionar individuos
    indices_seleccionados = np.random.choice(
        len(poblacion), 
        size=num_seleccionados, 
        replace=True, 
        p=probabilidades
    )
    
    # Obtener los individuos seleccionados y sus fitness
    seleccionados = [np.copy(poblacion[i]) for i in indices_seleccionados]
    fitness_seleccionados = [valores_fitness[i] for i in indices_seleccionados]
    
    return seleccionados, fitness_seleccionados


def seleccion_truncamiento(
    poblacion: List[np.ndarray],
    valores_fitness: List[float],
    num_seleccionados: int,
    tasa_truncamiento: float = 0.5,
    maximizar: bool = True,
    **kwargs
) -> Tuple[List[np.ndarray], List[float]]:
    """
    Selecciona los mejores individuos mediante truncamiento.
    
    Selecciona los individuos con mejor fitness en un porcentaje determinado
    y luego realiza selección aleatoria entre ellos.
    
    Parameters
    ----------
    poblacion : List[np.ndarray]
        Lista de individuos a seleccionar.
    valores_fitness : List[float]
        Lista con los valores de fitness de cada individuo.
    num_seleccionados : int
        Número de individuos a seleccionar.
    tasa_truncamiento : float, optional
        Proporción de la población que se considera para selección. Por defecto es 0.5.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[List[np.ndarray], List[float]]
        Tupla con la lista de individuos seleccionados y sus valores de fitness.
    
    Examples
    --------
    >>> poblacion = [np.array([1, 0, 1]), np.array([0, 1, 0]), np.array([1, 1, 1])]
    >>> fitness = [2, 1, 3]
    >>> seleccionados, sel_fitness = seleccion_truncamiento(poblacion, fitness, 2, 0.7)
    >>> len(seleccionados)
    2
    """
    n = len(poblacion)
    
    # Determinar cuántos individuos se consideran para la selección
    num_truncados = max(1, int(n * tasa_truncamiento))
    
    # Ordenar por fitness
    if maximizar:
        indices_ordenados = np.argsort(valores_fitness)[::-1]  # Mayor a menor
    else:
        indices_ordenados = np.argsort(valores_fitness)  # Menor a mayor
    
    # Seleccionar solo los mejores según la tasa de truncamiento
    indices_truncados = indices_ordenados[:num_truncados]
    
    # Seleccionar individuos aleatoriamente entre los mejores
    indices_seleccionados = np.random.choice(
        indices_truncados,
        size=num_seleccionados,
        replace=True
    )
    
    # Obtener los individuos seleccionados y sus fitness
    seleccionados = [np.copy(poblacion[i]) for i in indices_seleccionados]
    fitness_seleccionados = [valores_fitness[i] for i in indices_seleccionados]
    
    return seleccionados, fitness_seleccionados


def seleccion_estocastica_universal(
    poblacion: List[np.ndarray],
    valores_fitness: List[float],
    num_seleccionados: int,
    maximizar: bool = True,
    **kwargs
) -> Tuple[List[np.ndarray], List[float]]:
    """
    Selecciona individuos mediante muestreo estocástico universal (SUS).
    
    SUS es similar a la selección por ruleta, pero usa un solo giro con múltiples
    marcadores equidistantes, lo que puede reducir el sesgo de selección.
    
    Parameters
    ----------
    poblacion : List[np.ndarray]
        Lista de individuos a seleccionar.
    valores_fitness : List[float]
        Lista con los valores de fitness de cada individuo.
    num_seleccionados : int
        Número de individuos a seleccionar.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[List[np.ndarray], List[float]]
        Tupla con la lista de individuos seleccionados y sus valores de fitness.
    
    Examples
    --------
    >>> poblacion = [np.array([1, 0, 1]), np.array([0, 1, 0]), np.array([1, 1, 1])]
    >>> fitness = [2, 1, 3]
    >>> seleccionados, sel_fitness = seleccion_estocastica_universal(poblacion, fitness, 2)
    >>> len(seleccionados)
    2
    """
    # Asegurarse de que el fitness sea adecuado para maximización
    fitness_ajustado = np.array(valores_fitness)
    if not maximizar:
        # Para minimización, invertimos los valores
        fitness_ajustado = np.max(fitness_ajustado) + 1 - fitness_ajustado
    
    # Manejar valores negativos o cero
    if np.min(fitness_ajustado) <= 0:
        # Desplazar todos los valores para que sean positivos
        fitness_ajustado = fitness_ajustado - np.min(fitness_ajustado) + 1e-10
    
    # Calcular la suma total de fitness
    suma_fitness = np.sum(fitness_ajustado)
    
    # Calcular el paso entre marcadores
    paso = suma_fitness / num_seleccionados
    
    # Punto de inicio aleatorio entre [0, paso)
    inicio = np.random.uniform(0, paso)
    
    # Calcular todos los puntos de selección
    puntos = [inicio + i * paso for i in range(num_seleccionados)]
    
    # Seleccionar individuos
    seleccionados = []
    fitness_seleccionados = []
    
    for punto in puntos:
        # Acumular fitness hasta encontrar el individuo correspondiente
        suma_acumulada = 0
        for i, fit in enumerate(fitness_ajustado):
            suma_acumulada += fit
            if suma_acumulada > punto:
                seleccionados.append(np.copy(poblacion[i]))
                fitness_seleccionados.append(valores_fitness[i])
                break
    
    return seleccionados, fitness_seleccionados