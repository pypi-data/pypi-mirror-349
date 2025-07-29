"""
Módulo de mutación
===============

Este módulo contiene las funciones relacionadas con los operadores de mutación
para algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np


def mutacion_bit_flip(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación de inversión de bits (bit-flip) para genomas binarios.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de mutación para cada gen.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([1, 0, 1, 0, 1])
    >>> mutado = mutacion_bit_flip(ind, 0.2)
    >>> len(mutado) == len(ind)
    True
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Generar una máscara de mutación según la probabilidad
    mascara_mutacion = np.random.random(len(individuo)) < probabilidad_mutacion
    
    # Aplicar la mutación solo si el individuo es binario
    if np.all(np.logical_or(individuo == 0, individuo == 1)):
        individuo_mutado[mascara_mutacion] = 1 - individuo_mutado[mascara_mutacion]
    else:
        # Si no es binario, lanzar una advertencia y no mutar
        import warnings
        warnings.warn("mutacion_bit_flip se aplicó a un individuo no binario. No se realizará mutación.")
    
    return individuo_mutado


def mutacion_uniforme(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    limite_inferior: float = 0.0,
    limite_superior: float = 1.0,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación uniforme para genomas de valores reales.
    
    Los genes seleccionados para mutación reciben un nuevo valor aleatorio
    dentro de los límites especificados.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de mutación para cada gen.
    limite_inferior : float, optional
        Límite inferior para los valores mutados. Por defecto es 0.0.
    limite_superior : float, optional
        Límite superior para los valores mutados. Por defecto es 1.0.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    >>> mutado = mutacion_uniforme(ind, 0.2, 0.0, 1.0)
    >>> len(mutado) == len(ind)
    True
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Generar una máscara de mutación según la probabilidad
    mascara_mutacion = np.random.random(len(individuo)) < probabilidad_mutacion
    
    # Generar nuevos valores aleatorios para los genes seleccionados
    nuevos_valores = np.random.uniform(limite_inferior, limite_superior, np.sum(mascara_mutacion))
    
    # Aplicar la mutación
    individuo_mutado[mascara_mutacion] = nuevos_valores
    
    return individuo_mutado


def mutacion_gaussiana(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    media: float = 0.0,
    desviacion: float = 0.1,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación gaussiana para genomas de valores reales.
    
    Añade ruido gaussiano a los genes seleccionados para mutación.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de mutación para cada gen.
    media : float, optional
        Media de la distribución gaussiana. Por defecto es 0.0.
    desviacion : float, optional
        Desviación estándar de la distribución gaussiana. Por defecto es 0.1.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    >>> mutado = mutacion_gaussiana(ind, 0.2, 0.0, 0.1)
    >>> len(mutado) == len(ind)
    True
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Generar una máscara de mutación según la probabilidad
    mascara_mutacion = np.random.random(len(individuo)) < probabilidad_mutacion
    
    # Generar ruido gaussiano para los genes seleccionados
    ruido = np.random.normal(media, desviacion, np.sum(mascara_mutacion))
    
    # Aplicar la mutación
    individuo_mutado[mascara_mutacion] += ruido
    
    return individuo_mutado


def mutacion_swap(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación de intercambio (swap) para genomas de permutación.
    
    Intercambia pares de genes con una probabilidad dada.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de realizar un intercambio.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0, 1, 2, 3, 4])
    >>> mutado = mutacion_swap(ind, 0.5)
    >>> len(mutado) == len(ind)
    True
    >>> sorted(mutado)
    [0, 1, 2, 3, 4]
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Número de posibles intercambios (n-1 para evitar duplicados)
    n_swaps = len(individuo) - 1
    
    # Calcular el número esperado de intercambios
    num_intercambios = int(n_swaps * probabilidad_mutacion) + (1 if np.random.random() < (n_swaps * probabilidad_mutacion % 1) else 0)
    
    # Realizar los intercambios
    for _ in range(num_intercambios):
        # Seleccionar dos posiciones aleatorias diferentes
        i, j = np.random.choice(len(individuo), 2, replace=False)
        
        # Intercambiar los valores
        individuo_mutado[i], individuo_mutado[j] = individuo_mutado[j], individuo_mutado[i]
    
    return individuo_mutado


def mutacion_inversion(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación de inversión para genomas de permutación o binarios.
    
    Invierte un segmento del genoma con una probabilidad dada.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de realizar una inversión.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0, 1, 2, 3, 4])
    >>> mutado = mutacion_inversion(ind, 0.5)
    >>> len(mutado) == len(ind)
    True
    >>> sorted(mutado)
    [0, 1, 2, 3, 4]
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Decidir si se realiza la inversión
    if np.random.random() < probabilidad_mutacion:
        # Seleccionar dos posiciones aleatorias diferentes
        i, j = sorted(np.random.choice(len(individuo), 2, replace=False))
        
        # Invertir el segmento
        individuo_mutado[i:j+1] = individuo_mutado[i:j+1][::-1]
    
    return individuo_mutado


def mutacion_insertion(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación de inserción para genomas de permutación.
    
    Selecciona un gen y lo inserta en otra posición, desplazando los demás.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de realizar una inserción.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0, 1, 2, 3, 4])
    >>> mutado = mutacion_insertion(ind, 0.5)
    >>> len(mutado) == len(ind)
    True
    >>> sorted(mutado)
    [0, 1, 2, 3, 4]
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Decidir si se realiza la inserción
    if np.random.random() < probabilidad_mutacion:
        # Seleccionar dos posiciones aleatorias diferentes
        origen, destino = np.random.choice(len(individuo), 2, replace=False)
        
        # Valor a mover
        valor = individuo_mutado[origen]
        
        # Si el destino está después del origen
        if destino > origen:
            # Desplazar los elementos entre origen+1 y destino una posición hacia atrás
            individuo_mutado[origen:destino] = individuo_mutado[origen+1:destino+1]
        else:
            # Desplazar los elementos entre destino y origen-1 una posición hacia adelante
            individuo_mutado[destino+1:origen+1] = individuo_mutado[destino:origen]
        
        # Insertar el valor en la posición de destino
        individuo_mutado[destino] = valor
    
    return individuo_mutado


def mutacion_scramble(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación de barajado (scramble) para genomas de permutación.
    
    Selecciona un segmento del genoma y mezcla aleatoriamente sus elementos.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad de realizar un barajado.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0, 1, 2, 3, 4])
    >>> mutado = mutacion_scramble(ind, 0.5)
    >>> len(mutado) == len(ind)
    True
    >>> sorted(mutado)
    [0, 1, 2, 3, 4]
    """
    # Crear una copia del individuo
    individuo_mutado = np.copy(individuo)
    
    # Decidir si se realiza el barajado
    if np.random.random() < probabilidad_mutacion:
        # Seleccionar dos posiciones aleatorias diferentes
        i, j = sorted(np.random.choice(len(individuo), 2, replace=False))
        
        # Obtener el segmento a barajar
        segmento = individuo_mutado[i:j+1].copy()
        
        # Barajar el segmento
        np.random.shuffle(segmento)
        
        # Reemplazar el segmento original
        individuo_mutado[i:j+1] = segmento
    
    return individuo_mutado


def mutacion_adaptativa(
    individuo: np.ndarray,
    probabilidad_mutacion: float,
    generacion_actual: int,
    max_generaciones: int,
    tipo_genoma: str = 'binario',
    **kwargs
) -> np.ndarray:
    """
    Realiza una mutación adaptativa que ajusta automáticamente el operador
    según el tipo de genoma y la fase del algoritmo.
    
    Parameters
    ----------
    individuo : np.ndarray
        Individuo a mutar.
    probabilidad_mutacion : float
        Probabilidad base de mutación.
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    tipo_genoma : str, optional
        Tipo de genoma ('binario', 'real' o 'permutacion'). Por defecto es 'binario'.
    **kwargs : dict
        Parámetros adicionales para los operadores de mutación internos.
        
    Returns
    -------
    np.ndarray
        Individuo mutado.
    
    Examples
    --------
    >>> ind = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    >>> mutado = mutacion_adaptativa(ind, 0.1, 50, 100, 'real')
    >>> len(mutado) == len(ind)
    True
    """
    # Ajustar probabilidad de mutación según la fase del algoritmo
    # Al principio exploración (alta probabilidad), al final explotación (baja probabilidad)
    fase = generacion_actual / max_generaciones
    prob_ajustada = probabilidad_mutacion * (1.0 - 0.5 * fase)
    
    # Seleccionar operador según tipo de genoma
    if tipo_genoma == 'binario':
        return mutacion_bit_flip(individuo, prob_ajustada, **kwargs)
    elif tipo_genoma == 'real':
        # Al principio más mutación uniforme, al final más gaussiana
        if np.random.random() < 0.5 + 0.5 * fase:
            return mutacion_gaussiana(
                individuo, 
                prob_ajustada, 
                desviacion=0.1 * (1.0 - fase),  # Reducir la desviación con el tiempo
                **kwargs
            )
        else:
            return mutacion_uniforme(individuo, prob_ajustada, **kwargs)
    elif tipo_genoma == 'permutacion':
        # Seleccionar aleatoriamente entre diferentes operadores
        operadores = [
            mutacion_swap,
            mutacion_inversion,
            mutacion_insertion,
            mutacion_scramble
        ]
        # Al principio más scramble, al final más swap (menos disruptivo)
        pesos = [
            0.25 + 0.25 * fase,  # swap: aumenta con el tiempo
            0.25,                 # inversion: constante
            0.25,                 # insertion: constante
            0.25 - 0.25 * fase    # scramble: disminuye con el tiempo
        ]
        operador = np.random.choice(operadores, p=pesos)
        return operador(individuo, prob_ajustada, **kwargs)
    else:
        raise ValueError(f"Tipo de genoma no reconocido: {tipo_genoma}")