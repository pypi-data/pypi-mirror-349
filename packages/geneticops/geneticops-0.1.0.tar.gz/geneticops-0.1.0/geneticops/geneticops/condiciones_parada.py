"""
Módulo de condiciones de parada
============================

Este módulo contiene las funciones relacionadas con las condiciones de terminación
para algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np
import time


def condicion_max_generaciones(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    **kwargs
) -> bool:
    """
    Verifica si se ha alcanzado el número máximo de generaciones.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> condicion_max_generaciones(50, 100, [])
    False
    >>> condicion_max_generaciones(100, 100, [])
    True
    """
    return generacion_actual >= max_generaciones


def condicion_convergencia(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    umbral_convergencia: float = 1e-6,
    ventana_convergencia: int = 10,
    **kwargs
) -> bool:
    """
    Verifica si el algoritmo ha convergido, es decir, si el fitness no ha mejorado
    significativamente en las últimas generaciones.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    umbral_convergencia : float, optional
        Umbral de mejora relativa para considerar convergencia. Por defecto es 1e-6.
    ventana_convergencia : int, optional
        Número de generaciones a considerar para comprobar convergencia. Por defecto es 10.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> historia = [1.0, 1.1, 1.15, 1.17, 1.18, 1.181, 1.182, 1.1821, 1.1822, 1.1823]
    >>> condicion_convergencia(10, 100, historia, 1e-4, 5)
    True
    """
    # Si no hay suficientes generaciones, no se considera convergencia
    if len(historia_fitness) < ventana_convergencia:
        return False
    
    # Obtener el fitness de las últimas generaciones
    ultimos_fitness = historia_fitness[-ventana_convergencia:]
    
    # Calcular la mejora relativa
    mejor_inicial = ultimos_fitness[0]
    mejor_final = ultimos_fitness[-1]
    
    # Evitar división por cero
    if abs(mejor_inicial) < 1e-10:
        mejor_inicial = 1e-10
    
    # CORRECCIÓN: usar valor absoluto para asegurar que sea positivo
    mejora_relativa = abs((mejor_final - mejor_inicial) / mejor_inicial)
    
    # Verificar si la mejora es menor que el umbral
    return mejora_relativa < umbral_convergencia


def condicion_fitness_objetivo(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    valor_objetivo: float = 1.0,
    maximizar: bool = True,
    **kwargs
) -> bool:
    """
    Verifica si se ha alcanzado un valor objetivo de fitness.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    valor_objetivo : float, optional
        Valor objetivo de fitness a alcanzar. Por defecto es 1.0.
    maximizar : bool, optional
        Si es True, se detiene cuando el fitness es mayor o igual al objetivo.
        Si es False, se detiene cuando es menor o igual. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> historia = [0.5, 0.7, 0.9, 1.1]
    >>> condicion_fitness_objetivo(4, 100, historia, 1.0)
    True
    >>> condicion_fitness_objetivo(4, 100, historia, 1.5)
    False
    """
    # Si no hay generaciones, no se ha alcanzado el objetivo
    if not historia_fitness:
        return False
    
    # Obtener el mejor fitness actual
    mejor_fitness = historia_fitness[-1]
    
    # Verificar si se ha alcanzado el objetivo
    if maximizar:
        return mejor_fitness >= valor_objetivo
    else:
        return mejor_fitness <= valor_objetivo


def condicion_tiempo_limite(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    tiempo_inicio: float = 0.0,
    tiempo_limite: float = 60.0,
    **kwargs
) -> bool:
    """
    Verifica si se ha alcanzado un tiempo límite de ejecución.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    tiempo_inicio : float, optional
        Tiempo de inicio del algoritmo (en segundos). Por defecto es 0.0.
    tiempo_limite : float, optional
        Tiempo máximo de ejecución (en segundos). Por defecto es 60.0.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> import time
    >>> inicio = time.time()
    >>> condicion_tiempo_limite(10, 100, [], inicio, 0.001)
    True
    """
    import time
    tiempo_actual = time.time()
    return (tiempo_actual - tiempo_inicio) >= tiempo_limite


def condicion_estancamiento(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    max_generaciones_sin_mejora: int = 20,
    **kwargs
) -> bool:
    """
    Verifica si el algoritmo se ha estancado, es decir, si el fitness no ha
    mejorado durante un número determinado de generaciones.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    max_generaciones_sin_mejora : int, optional
        Número máximo de generaciones sin mejora. Por defecto es 20.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> historia = [1.0, 1.1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
    >>> condicion_estancamiento(11, 100, historia, 5)
    True
    """
    # Si no hay suficientes generaciones, no se considera estancamiento
    if len(historia_fitness) <= max_generaciones_sin_mejora:
        return False
    
    # Obtener el mejor fitness de las últimas generaciones
    ultimos_fitness = historia_fitness[-max_generaciones_sin_mejora:]
    
    # Verificar si todos los valores son iguales
    return len(set(ultimos_fitness)) == 1


def condicion_combinada(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    condiciones: List[callable],
    modo: str = 'OR',
    **kwargs
) -> bool:
    """
    Combina múltiples condiciones de parada.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    condiciones : List[callable]
        Lista de funciones de condición de parada a combinar.
    modo : str, optional
        Modo de combinación: 'OR' para detenerse si alguna condición es True,
        'AND' para detenerse solo si todas son True. Por defecto es 'OR'.
    **kwargs : dict
        Parámetros adicionales a pasar a las condiciones.
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> condiciones = [condicion_max_generaciones, condicion_convergencia]
    >>> condicion_combinada(50, 100, [1.0, 1.0, 1.0], condiciones, 'OR')
    False
    """
    resultados = [
        cond(generacion_actual, max_generaciones, historia_fitness, **kwargs)
        for cond in condiciones
    ]
    
    if modo.upper() == 'OR':
        return any(resultados)
    elif modo.upper() == 'AND':
        return all(resultados)
    else:
        raise ValueError(f"Modo no reconocido: {modo}. Use 'OR' o 'AND'.")


def condicion_personalizada(
    generacion_actual: int,
    max_generaciones: int,
    historia_fitness: List[float],
    funcion_condicion: callable,
    **kwargs
) -> bool:
    """
    Utiliza una función personalizada como condición de parada.
    
    Parameters
    ----------
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    funcion_condicion : callable
        Función que evalúa si el algoritmo debe detenerse.
    **kwargs : dict
        Parámetros adicionales a pasar a la función de condición.
        
    Returns
    -------
    bool
        True si se debe detener el algoritmo, False en caso contrario.
    
    Examples
    --------
    >>> def mi_condicion(gen, max_gen, hist, **kwargs):
    ...     return gen > max_gen // 2
    >>> condicion_personalizada(51, 100, [], mi_condicion)
    True
    """
    return funcion_condicion(generacion_actual, max_generaciones, historia_fitness, **kwargs)