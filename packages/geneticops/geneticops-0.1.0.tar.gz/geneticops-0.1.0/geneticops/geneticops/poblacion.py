"""
Módulo de población
==================

Este módulo contiene las funciones relacionadas con la inicialización
y manejo de poblaciones para algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np

# Definir tipos para mejorar la legibilidad
Individuo = np.ndarray
Poblacion = List[Individuo]


def inicializar_poblacion_binaria(
    tamano_poblacion: int, 
    longitud_individuo: int,
    **kwargs
) -> Poblacion:
    """
    Inicializa una población de individuos con genoma binario.
    
    Parameters
    ----------
    tamano_poblacion : int
        Número de individuos en la población.
    longitud_individuo : int
        Longitud del genoma de cada individuo.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Poblacion
        Lista de individuos con genoma binario aleatorio.
    
    Examples
    --------
    >>> poblacion = inicializar_poblacion_binaria(100, 10)
    >>> len(poblacion)
    100
    >>> poblacion[0].shape
    (10,)
    """
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = np.random.randint(0, 2, size=longitud_individuo)
        poblacion.append(individuo)
    return poblacion


def inicializar_poblacion_real(
    tamano_poblacion: int, 
    longitud_individuo: int,
    limite_inferior: float = 0.0,
    limite_superior: float = 1.0,
    **kwargs
) -> Poblacion:
    """
    Inicializa una población de individuos con genoma de valores reales.
    
    Parameters
    ----------
    tamano_poblacion : int
        Número de individuos en la población.
    longitud_individuo : int
        Longitud del genoma de cada individuo.
    limite_inferior : float, optional
        Límite inferior para los valores del genoma. Por defecto es 0.0.
    limite_superior : float, optional
        Límite superior para los valores del genoma. Por defecto es 1.0.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Poblacion
        Lista de individuos con genoma de valores reales aleatorio.
    
    Examples
    --------
    >>> poblacion = inicializar_poblacion_real(100, 10, -5.0, 5.0)
    >>> len(poblacion)
    100
    >>> poblacion[0].shape
    (10,)
    """
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = np.random.uniform(limite_inferior, limite_superior, size=longitud_individuo)
        poblacion.append(individuo)
    return poblacion


def inicializar_poblacion_permutacion(
    tamano_poblacion: int, 
    longitud_individuo: int,
    **kwargs
) -> Poblacion:
    """
    Inicializa una población de individuos con genoma de permutación (útil para TSP y similares).
    
    Parameters
    ----------
    tamano_poblacion : int
        Número de individuos en la población.
    longitud_individuo : int
        Longitud del genoma de cada individuo.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Poblacion
        Lista de individuos con genoma de permutación aleatorio.
    
    Examples
    --------
    >>> poblacion = inicializar_poblacion_permutacion(100, 10)
    >>> len(poblacion)
    100
    >>> sorted(poblacion[0])
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    poblacion = []
    for _ in range(tamano_poblacion):
        individuo = np.arange(longitud_individuo)
        np.random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion


def inicializar_poblacion_desde_semilla(
    tamano_poblacion: int,
    longitud_individuo: int,
    semilla: Individuo,
    tasa_variacion: float = 0.1,
    **kwargs
) -> Poblacion:
    """
    Inicializa una población basada en un individuo semilla, con variaciones.
    
    Parameters
    ----------
    tamano_poblacion : int
        Número de individuos en la población.
    longitud_individuo : int
        Longitud del genoma de cada individuo.
    semilla : Individuo
        Individuo semilla a partir del cual se genera la población.
    tasa_variacion : float, optional
        Proporción de genes que se modifican aleatoriamente. Por defecto es 0.1.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Poblacion
        Lista de individuos basados en la semilla con variaciones.
    
    Examples
    --------
    >>> semilla = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    >>> poblacion = inicializar_poblacion_desde_semilla(100, 10, semilla, 0.2)
    >>> len(poblacion)
    100
    """
    if len(semilla) != longitud_individuo:
        raise ValueError(f"La longitud de la semilla ({len(semilla)}) no coincide con longitud_individuo ({longitud_individuo})")
    
    poblacion = []
    # El primer individuo es exactamente la semilla
    poblacion.append(np.copy(semilla))
    
    # El resto son variaciones
    for _ in range(tamano_poblacion - 1):
        nuevo_individuo = np.copy(semilla)
        # Seleccionar índices para modificar
        num_cambios = int(longitud_individuo * tasa_variacion)
        indices_cambio = np.random.choice(longitud_individuo, num_cambios, replace=False)
        
        # Si la semilla es binaria
        if np.all(np.logical_or(semilla == 0, semilla == 1)):
            nuevo_individuo[indices_cambio] = 1 - nuevo_individuo[indices_cambio]  # Invertir bits
        # Si la semilla tiene valores reales
        elif np.issubdtype(semilla.dtype, np.floating):
            variacion = np.random.normal(0, 0.1, num_cambios)
            nuevo_individuo[indices_cambio] += variacion
        # Si la semilla es una permutación
        elif len(np.unique(semilla)) == longitud_individuo:
            for _ in range(num_cambios // 2):  # Hacemos algunos swaps
                i, j = np.random.choice(longitud_individuo, 2, replace=False)
                nuevo_individuo[i], nuevo_individuo[j] = nuevo_individuo[j], nuevo_individuo[i]
                
        poblacion.append(nuevo_individuo)
    
    return poblacion


def evaluar_poblacion(
    poblacion: Poblacion,
    funcion_fitness: callable
) -> List[float]:
    """
    Evalúa la aptitud (fitness) de todos los individuos en la población.
    
    Parameters
    ----------
    poblacion : Poblacion
        Lista de individuos a evaluar.
    funcion_fitness : callable
        Función que evalúa la aptitud de un individuo.
        
    Returns
    -------
    List[float]
        Lista con los valores de fitness de cada individuo.
    
    Examples
    --------
    >>> def fitness_suma(individuo):
    ...     return np.sum(individuo)
    >>> poblacion = inicializar_poblacion_binaria(5, 10)
    >>> fitness = evaluar_poblacion(poblacion, fitness_suma)
    >>> len(fitness)
    5
    """
    return [funcion_fitness(individuo) for individuo in poblacion]