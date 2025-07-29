"""
Módulo de cruce
=============

Este módulo contiene las funciones relacionadas con los operadores de cruce
(recombinación) para algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np


def cruce_un_punto(
    padre1: np.ndarray,
    padre2: np.ndarray,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce de un punto entre dos individuos.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([1, 1, 1, 1, 1])
    >>> padre2 = np.array([0, 0, 0, 0, 0])
    >>> hijo1, hijo2 = cruce_un_punto(padre1, padre2)
    >>> len(hijo1) == len(padre1)
    True
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Seleccionar punto de cruce (entre 1 y longitud-1)
    punto_cruce = np.random.randint(1, len(padre1))
    
    # Crear los hijos intercambiando segmentos
    hijo1 = np.concatenate([padre1[:punto_cruce], padre2[punto_cruce:]])
    hijo2 = np.concatenate([padre2[:punto_cruce], padre1[punto_cruce:]])
    
    return hijo1, hijo2


def cruce_dos_puntos(
    padre1: np.ndarray,
    padre2: np.ndarray,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce de dos puntos entre dos individuos.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([1, 1, 1, 1, 1])
    >>> padre2 = np.array([0, 0, 0, 0, 0])
    >>> hijo1, hijo2 = cruce_dos_puntos(padre1, padre2)
    >>> len(hijo1) == len(padre1)
    True
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Asegurarse de que la longitud sea suficiente para dos puntos
    if len(padre1) <= 2:
        return cruce_un_punto(padre1, padre2)
    
    # Seleccionar dos puntos de cruce diferentes
    punto1, punto2 = sorted(np.random.choice(len(padre1) - 1, 2, replace=False) + 1)
    
    # Crear los hijos intercambiando segmentos
    hijo1 = np.concatenate([padre1[:punto1], padre2[punto1:punto2], padre1[punto2:]])
    hijo2 = np.concatenate([padre2[:punto1], padre1[punto1:punto2], padre2[punto2:]])
    
    return hijo1, hijo2


def cruce_uniforme(
    padre1: np.ndarray,
    padre2: np.ndarray,
    prob_intercambio: float = 0.5,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce uniforme entre dos individuos.
    
    En cada posición, hay una probabilidad 'prob_intercambio' de que los hijos
    intercambien los genes de los padres.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    prob_intercambio : float, optional
        Probabilidad de intercambio en cada posición. Por defecto es 0.5.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([1, 1, 1, 1, 1])
    >>> padre2 = np.array([0, 0, 0, 0, 0])
    >>> hijo1, hijo2 = cruce_uniforme(padre1, padre2, 0.5)
    >>> len(hijo1) == len(padre1)
    True
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Generar máscara de cruce aleatoria
    mascara = np.random.random(len(padre1)) < prob_intercambio
    
    # Crear los hijos usando la máscara
    hijo1 = np.where(mascara, padre2, padre1)
    hijo2 = np.where(mascara, padre1, padre2)
    
    return hijo1, hijo2


def cruce_aritmetico(
    padre1: np.ndarray,
    padre2: np.ndarray,
    alpha: float = 0.5,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce aritmético entre dos individuos de valores reales.
    
    Los genes de los hijos son combinaciones lineales de los genes de los padres.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    alpha : float, optional
        Factor de combinación. Por defecto es 0.5.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([1.0, 2.0, 3.0])
    >>> padre2 = np.array([4.0, 5.0, 6.0])
    >>> hijo1, hijo2 = cruce_aritmetico(padre1, padre2, 0.5)
    >>> np.allclose(hijo1, np.array([2.5, 3.5, 4.5]))
    True
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Asegurarse de que los padres sean de tipo numérico
    if not np.issubdtype(padre1.dtype, np.number) or not np.issubdtype(padre2.dtype, np.number):
        raise TypeError("Los padres deben ser de tipo numérico para cruce aritmético")
    
    # Crear los hijos como combinaciones lineales
    hijo1 = alpha * padre1 + (1 - alpha) * padre2
    hijo2 = (1 - alpha) * padre1 + alpha * padre2
    
    return hijo1, hijo2


def cruce_sbx(
    padre1: np.ndarray,
    padre2: np.ndarray,
    eta: float = 1.0,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce SBX (Simulated Binary Crossover) entre dos individuos de valores reales.
    
    Este operador simula el comportamiento del cruce de un punto en codificación binaria
    pero para individuos con valores reales.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    eta : float, optional
        Índice de distribución. Valores mayores producen hijos más cercanos a los padres.
        Por defecto es 1.0.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([1.0, 2.0, 3.0])
    >>> padre2 = np.array([4.0, 5.0, 6.0])
    >>> hijo1, hijo2 = cruce_sbx(padre1, padre2, 2.0)
    >>> len(hijo1) == len(padre1)
    True
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Asegurarse de que los padres sean de tipo numérico
    if not np.issubdtype(padre1.dtype, np.number) or not np.issubdtype(padre2.dtype, np.number):
        raise TypeError("Los padres deben ser de tipo numérico para cruce SBX")
    
    # Inicializar arrays para los hijos
    hijo1 = np.zeros_like(padre1)
    hijo2 = np.zeros_like(padre2)
    
    # Aplicar SBX en cada dimensión
    for i in range(len(padre1)):
        # Si los padres son iguales, los hijos son iguales a los padres
        if abs(padre1[i] - padre2[i]) < 1e-10:
            hijo1[i] = padre1[i]
            hijo2[i] = padre2[i]
            continue
        
        # Asegurar que padre1[i] < padre2[i]
        if padre1[i] > padre2[i]:
            padre1[i], padre2[i] = padre2[i], padre1[i]
        
        # Diferencia entre padres
        y1, y2 = padre1[i], padre2[i]
        
        # Generar número aleatorio para determinar la distribución
        r = np.random.random()
        
        # Factor beta para la distribución
        if r <= 0.5:
            beta = (2 * r) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - r))) ** (1 / (eta + 1))
        
        # Calcular hijos
        hijo1[i] = 0.5 * ((y1 + y2) - beta * (y2 - y1))
        hijo2[i] = 0.5 * ((y1 + y2) + beta * (y2 - y1))
    
    return hijo1, hijo2


def cruce_pmx(
    padre1: np.ndarray,
    padre2: np.ndarray,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce PMX (Partially Mapped Crossover) entre dos individuos de permutación.
    
    Este operador es especialmente útil para problemas como el TSP donde las soluciones
    son permutaciones y se deben mantener como permutaciones después del cruce.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> padre2 = np.array([8, 7, 6, 5, 4, 3, 2, 1, 0])
    >>> hijo1, hijo2 = cruce_pmx(padre1, padre2)
    >>> sorted(hijo1)
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Verificar que los padres sean permutaciones válidas
    if not (np.sort(padre1) == np.arange(len(padre1))).all() or not (np.sort(padre2) == np.arange(len(padre2))).all():
        raise ValueError("Los padres deben ser permutaciones completas")
    
    # Tamaño del genoma
    n = len(padre1)
    
    # Seleccionar dos puntos de cruce
    punto1, punto2 = sorted(np.random.choice(n - 1, 2, replace=False) + 1)
    
    # Crear hijos como copias de los padres
    hijo1 = np.copy(padre1)
    hijo2 = np.copy(padre2)
    
    # Segmento de mapeo
    segmento1 = hijo1[punto1:punto2]
    segmento2 = hijo2[punto1:punto2]
    
    # Mapeo de valores
    for i in range(punto1, punto2):
        # Valor de padre2 que se colocará en hijo1
        val1 = padre2[i]
        # Valor de padre1 que se colocará en hijo2
        val2 = padre1[i]
        
        # Si el valor ya está en el segmento, no hacer nada
        if val1 in segmento1:
            continue
        
        # Reemplazar todos los valores para mantener la permutación válida
        pos1 = np.where(hijo1 == val1)[0][0]
        hijo1[pos1] = hijo1[i]
        hijo1[i] = val1
        
        # Actualizar el segmento con el nuevo valor
        segmento1 = hijo1[punto1:punto2]
        
        # Similar para el hijo2
        if val2 in segmento2:
            continue
        
        pos2 = np.where(hijo2 == val2)[0][0]
        hijo2[pos2] = hijo2[i]
        hijo2[i] = val2
        
        # Actualizar el segmento con el nuevo valor
        segmento2 = hijo2[punto1:punto2]
    
    return hijo1, hijo2


def cruce_ox(
    padre1: np.ndarray,
    padre2: np.ndarray,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce OX (Order Crossover) entre dos individuos de permutación.
    
    Este operador mantiene el orden relativo de los elementos y es útil para
    problemas como el TSP.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> padre2 = np.array([8, 7, 6, 5, 4, 3, 2, 1, 0])
    >>> hijo1, hijo2 = cruce_ox(padre1, padre2)
    >>> sorted(hijo1)
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Verificar que los padres sean permutaciones válidas
    if not (np.sort(padre1) == np.arange(len(padre1))).all() or not (np.sort(padre2) == np.arange(len(padre2))).all():
        raise ValueError("Los padres deben ser permutaciones completas")
    
    # Tamaño del genoma
    n = len(padre1)
    
    # Seleccionar dos puntos de cruce
    punto1, punto2 = sorted(np.random.choice(n - 1, 2, replace=False) + 1)
    
    # Crear hijos
    hijo1 = np.full(n, -1)
    hijo2 = np.full(n, -1)
    
    # Copiar segmento entre puntos de cruce directamente
    hijo1[punto1:punto2] = padre1[punto1:punto2]
    hijo2[punto1:punto2] = padre2[punto1:punto2]
    
    # Completar el resto del hijo1 con los elementos de padre2 en orden
    elementos_restantes1 = [x for x in padre2 if x not in hijo1]
    idx1 = punto2
    for elem in elementos_restantes1:
        if idx1 == n:
            idx1 = 0
        while hijo1[idx1] != -1:
            idx1 = (idx1 + 1) % n
        hijo1[idx1] = elem
        idx1 = (idx1 + 1) % n
    
    # Completar el resto del hijo2 con los elementos de padre1 en orden
    elementos_restantes2 = [x for x in padre1 if x not in hijo2]
    idx2 = punto2
    for elem in elementos_restantes2:
        if idx2 == n:
            idx2 = 0
        while hijo2[idx2] != -1:
            idx2 = (idx2 + 1) % n
        hijo2[idx2] = elem
        idx2 = (idx2 + 1) % n
    
    return hijo1, hijo2


def cruce_ciclo(
    padre1: np.ndarray,
    padre2: np.ndarray,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Realiza un cruce de ciclo (Cycle Crossover) entre dos individuos de permutación.
    
    Este operador preserva la posición absoluta de los elementos y es útil para
    problemas donde la posición es importante.
    
    Parameters
    ----------
    padre1 : np.ndarray
        Primer individuo para el cruce.
    padre2 : np.ndarray
        Segundo individuo para el cruce.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        Tupla con los dos hijos resultantes del cruce.
    
    Examples
    --------
    >>> padre1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    >>> padre2 = np.array([8, 7, 6, 5, 4, 3, 2, 1, 0])
    >>> hijo1, hijo2 = cruce_ciclo(padre1, padre2)
    >>> sorted(hijo1)
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    """
    # Validar que los padres tengan la misma longitud
    if len(padre1) != len(padre2):
        raise ValueError("Los padres deben tener la misma longitud")
    
    # Verificar que los padres sean permutaciones válidas
    if not (np.sort(padre1) == np.arange(len(padre1))).all() or not (np.sort(padre2) == np.arange(len(padre2))).all():
        raise ValueError("Los padres deben ser permutaciones completas")
    
    # Tamaño del genoma
    n = len(padre1)
    
    # Crear hijos como copias de los padres
    hijo1 = np.full(n, -1)
    hijo2 = np.full(n, -1)
    
    # Determinar los ciclos
    ciclos = np.zeros(n, dtype=int)
    num_ciclo = 1
    
    # Encontrar todos los ciclos
    for i in range(n):
        if ciclos[i] == 0:
            j = i
            while ciclos[j] == 0:
                ciclos[j] = num_ciclo
                val = padre2[j]
                j = np.where(padre1 == val)[0][0]
            num_ciclo += 1
    
    # Asignar valores según los ciclos
    for i in range(n):
        if ciclos[i] % 2 == 1:  # Ciclo impar
            hijo1[i] = padre1[i]
            hijo2[i] = padre2[i]
        else:  # Ciclo par
            hijo1[i] = padre2[i]
            hijo2[i] = padre1[i]
    
    return hijo1, hijo2