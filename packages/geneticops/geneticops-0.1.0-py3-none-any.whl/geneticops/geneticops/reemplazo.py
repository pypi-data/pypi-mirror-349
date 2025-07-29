"""
Módulo de reemplazo
================

Este módulo contiene las funciones relacionadas con las estrategias de reemplazo
generacional para algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np


def reemplazo_generacional(
    poblacion_actual: List[np.ndarray],
    fitness_actual: List[float],
    descendencia: List[np.ndarray],
    fitness_descendencia: List[float],
    proporcion_elitismo: float = 0.0,
    maximizar: bool = True,
    **kwargs
) -> List[np.ndarray]:
    """
    Realiza un reemplazo generacional donde la descendencia reemplaza completamente
    a la población actual, excepto posiblemente por algunos individuos élite.
    
    Parameters
    ----------
    poblacion_actual : List[np.ndarray]
        Lista de individuos de la población actual.
    fitness_actual : List[float]
        Lista con los valores de fitness de la población actual.
    descendencia : List[np.ndarray]
        Lista de individuos de la descendencia.
    fitness_descendencia : List[float]
        Lista con los valores de fitness de la descendencia.
    proporcion_elitismo : float, optional
        Proporción de individuos élite a conservar. Por defecto es 0.0.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    List[np.ndarray]
        Nueva población después del reemplazo.
    
    Examples
    --------
    >>> pob_actual = [np.array([1, 1]), np.array([0, 0])]
    >>> fit_actual = [2, 0]
    >>> descendencia = [np.array([1, 0]), np.array([0, 1])]
    >>> fit_descendencia = [1, 1]
    >>> nueva_pob = reemplazo_generacional(pob_actual, fit_actual, descendencia, fit_descendencia, 0.5)
    >>> len(nueva_pob)
    2
    """
    # CORRECCIÓN: Determinar el número de élites a conservar
    # Asegurarse de que el número de élites es correcto
    if proporcion_elitismo > 0:
        num_elites = max(1, int(len(poblacion_actual) * proporcion_elitismo))
    else:
        num_elites = 0
    
    # Si no hay elitismo, reemplazar toda la población
    if num_elites == 0:
        return descendencia
    
    # Encontrar los mejores individuos de la población actual
    if maximizar:
        indices_elite = np.argsort(fitness_actual)[::-1][:num_elites]
    else:
        indices_elite = np.argsort(fitness_actual)[:num_elites]
    
    # Obtener los individuos élite
    elites = [np.copy(poblacion_actual[i]) for i in indices_elite]
    
    # Encontrar los peores individuos de la descendencia para reemplazar
    if maximizar:
        indices_reemplazo = np.argsort(fitness_descendencia)[:num_elites]
    else:
        indices_reemplazo = np.argsort(fitness_descendencia)[::-1][:num_elites]
    
    # Crear la nueva población a partir de la descendencia
    nueva_poblacion = [np.copy(ind) for ind in descendencia]
    
    # Reemplazar los peores de la descendencia con los élites
    for i, idx in enumerate(indices_reemplazo):
        nueva_poblacion[idx] = elites[i]
    
    return nueva_poblacion


def reemplazo_elitismo(
    poblacion_actual: List[np.ndarray],
    fitness_actual: List[float],
    descendencia: List[np.ndarray],
    fitness_descendencia: List[float],
    proporcion_elitismo: float = 0.1,
    maximizar: bool = True,
    **kwargs
) -> List[np.ndarray]:
    """
    Realiza un reemplazo con elitismo, seleccionando los mejores individuos
    tanto de la población actual como de la descendencia.
    
    Parameters
    ----------
    poblacion_actual : List[np.ndarray]
        Lista de individuos de la población actual.
    fitness_actual : List[float]
        Lista con los valores de fitness de la población actual.
    descendencia : List[np.ndarray]
        Lista de individuos de la descendencia.
    fitness_descendencia : List[float]
        Lista con los valores de fitness de la descendencia.
    proporcion_elitismo : float, optional
        Proporción de individuos élite a conservar. Por defecto es 0.1.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    List[np.ndarray]
        Nueva población después del reemplazo.
    
    Examples
    --------
    >>> pob_actual = [np.array([1, 1]), np.array([0, 0])]
    >>> fit_actual = [2, 0]
    >>> descendencia = [np.array([1, 0]), np.array([0, 1])]
    >>> fit_descendencia = [1, 1]
    >>> nueva_pob = reemplazo_elitismo(pob_actual, fit_actual, descendencia, fit_descendencia, 0.5)
    >>> len(nueva_pob)
    2
    """
    # Combinar población actual y descendencia
    poblacion_combinada = poblacion_actual + descendencia
    fitness_combinado = fitness_actual + fitness_descendencia
    
    # Ordenar según fitness
    if maximizar:
        indices_ordenados = np.argsort(fitness_combinado)[::-1]
    else:
        indices_ordenados = np.argsort(fitness_combinado)
    
    # Seleccionar los mejores hasta llenar la nueva población
    nueva_poblacion = []
    tamano_poblacion = len(poblacion_actual)
    
    for i in range(tamano_poblacion):
        idx = indices_ordenados[i]
        if idx < len(poblacion_actual):
            nueva_poblacion.append(np.copy(poblacion_actual[idx]))
        else:
            nueva_poblacion.append(np.copy(descendencia[idx - len(poblacion_actual)]))
    
    return nueva_poblacion


def reemplazo_estado_estacionario(
    poblacion_actual: List[np.ndarray],
    fitness_actual: List[float],
    descendencia: List[np.ndarray],
    fitness_descendencia: List[float],
    num_reemplazos: int = 2,
    maximizar: bool = True,
    **kwargs
) -> List[np.ndarray]:
    """
    Realiza un reemplazo de estado estacionario, donde solo algunos individuos
    de la descendencia reemplazan a los peores de la población actual.
    
    Parameters
    ----------
    poblacion_actual : List[np.ndarray]
        Lista de individuos de la población actual.
    fitness_actual : List[float]
        Lista con los valores de fitness de la población actual.
    descendencia : List[np.ndarray]
        Lista de individuos de la descendencia.
    fitness_descendencia : List[float]
        Lista con los valores de fitness de la descendencia.
    num_reemplazos : int, optional
        Número de individuos a reemplazar. Por defecto es 2.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    List[np.ndarray]
        Nueva población después del reemplazo.
    
    Examples
    --------
    >>> pob_actual = [np.array([1, 1]), np.array([0, 0]), np.array([1, 0]), np.array([0, 1])]
    >>> fit_actual = [2, 0, 1, 1]
    >>> descendencia = [np.array([1, 1]), np.array([1, 1])]
    >>> fit_descendencia = [2, 2]
    >>> nueva_pob = reemplazo_estado_estacionario(pob_actual, fit_actual, descendencia, fit_descendencia, 2)
    >>> len(nueva_pob)
    4
    """
    # Crear una copia de la población actual
    nueva_poblacion = [np.copy(ind) for ind in poblacion_actual]
    
    # Limitar el número de reemplazos
    num_reemplazos = min(num_reemplazos, len(descendencia), len(poblacion_actual))
    
    if num_reemplazos == 0:
        return nueva_poblacion
    
    # Encontrar los mejores individuos de la descendencia
    if maximizar:
        indices_mejores_desc = np.argsort(fitness_descendencia)[::-1][:num_reemplazos]
    else:
        indices_mejores_desc = np.argsort(fitness_descendencia)[:num_reemplazos]
    
    # CORRECCIÓN: Encontrar los peores individuos de la población actual
    if maximizar:
        indices_peores_act = np.argsort(fitness_actual)[:num_reemplazos]
    else:
        indices_peores_act = np.argsort(fitness_actual)[::-1][:num_reemplazos]
    
    # Reemplazar los peores individuos actuales con los mejores de la descendencia
    for i, idx_act in enumerate(indices_peores_act):
        idx_desc = indices_mejores_desc[i]
        nueva_poblacion[idx_act] = np.copy(descendencia[idx_desc])
    
    return nueva_poblacion


def reemplazo_torneo(
    poblacion_actual: List[np.ndarray],
    fitness_actual: List[float],
    descendencia: List[np.ndarray],
    fitness_descendencia: List[float],
    tamano_torneo: int = 2,
    maximizar: bool = True,
    **kwargs
) -> List[np.ndarray]:
    """
    Realiza un reemplazo mediante torneos entre individuos de la población actual
    y la descendencia.
    
    Parameters
    ----------
    poblacion_actual : List[np.ndarray]
        Lista de individuos de la población actual.
    fitness_actual : List[float]
        Lista con los valores de fitness de la población actual.
    descendencia : List[np.ndarray]
        Lista de individuos de la descendencia.
    fitness_descendencia : List[float]
        Lista con los valores de fitness de la descendencia.
    tamano_torneo : int, optional
        Tamaño del torneo. Por defecto es 2.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    List[np.ndarray]
        Nueva población después del reemplazo.
    
    Examples
    --------
    >>> pob_actual = [np.array([1, 1]), np.array([0, 0])]
    >>> fit_actual = [2, 0]
    >>> descendencia = [np.array([1, 0]), np.array([0, 1])]
    >>> fit_descendencia = [1, 1]
    >>> nueva_pob = reemplazo_torneo(pob_actual, fit_actual, descendencia, fit_descendencia, 2)
    >>> len(nueva_pob)
    2
    """
    # Combinar población actual y descendencia
    poblacion_combinada = poblacion_actual + descendencia
    fitness_combinado = fitness_actual + fitness_descendencia
    
    # Nueva población resultante de los torneos
    nueva_poblacion = []
    tamano_poblacion = len(poblacion_actual)
    
    for _ in range(tamano_poblacion):
        # Seleccionar participantes aleatorios para el torneo
        indices_torneo = np.random.choice(len(poblacion_combinada), size=tamano_torneo, replace=False)
        
        # Obtener los fitness de los participantes
        fitness_participantes = [fitness_combinado[i] for i in indices_torneo]
        
        # Encontrar el mejor participante
        if maximizar:
            idx_mejor = np.argmax(fitness_participantes)
        else:
            idx_mejor = np.argmin(fitness_participantes)
        
        # Agregar el ganador a la nueva población
        idx_ganador = indices_torneo[idx_mejor]
        if idx_ganador < len(poblacion_actual):
            nueva_poblacion.append(np.copy(poblacion_actual[idx_ganador]))
        else:
            nueva_poblacion.append(np.copy(descendencia[idx_ganador - len(poblacion_actual)]))
    
    return nueva_poblacion


def reemplazo_aleatorio(
    poblacion_actual: List[np.ndarray],
    fitness_actual: List[float],
    descendencia: List[np.ndarray],
    fitness_descendencia: List[float],
    proporcion_reemplazo: float = 0.5,
    **kwargs
) -> List[np.ndarray]:
    """
    Realiza un reemplazo aleatorio, donde una proporción de la población actual
    es reemplazada por individuos de la descendencia seleccionados aleatoriamente.
    
    Parameters
    ----------
    poblacion_actual : List[np.ndarray]
        Lista de individuos de la población actual.
    fitness_actual : List[float]
        Lista con los valores de fitness de la población actual.
    descendencia : List[np.ndarray]
        Lista de individuos de la descendencia.
    fitness_descendencia : List[float]
        Lista con los valores de fitness de la descendencia.
    proporcion_reemplazo : float, optional
        Proporción de la población a reemplazar. Por defecto es 0.5.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    List[np.ndarray]
        Nueva población después del reemplazo.
    
    Examples
    --------
    >>> pob_actual = [np.array([1, 1]), np.array([0, 0]), np.array([1, 0]), np.array([0, 1])]
    >>> fit_actual = [2, 0, 1, 1]
    >>> descendencia = [np.array([1, 1]), np.array([1, 1]), np.array([1, 0]), np.array([0, 1])]
    >>> fit_descendencia = [2, 2, 1, 1]
    >>> nueva_pob = reemplazo_aleatorio(pob_actual, fit_actual, descendencia, fit_descendencia, 0.5)
    >>> len(nueva_pob)
    4
    """
    # Crear una copia de la población actual
    nueva_poblacion = [np.copy(ind) for ind in poblacion_actual]
    
    # Determinar el número de individuos a reemplazar
    num_reemplazos = int(len(poblacion_actual) * proporcion_reemplazo)
    
    # Limitar el número de reemplazos
    num_reemplazos = min(num_reemplazos, len(descendencia), len(poblacion_actual))
    
    if num_reemplazos == 0:
        return nueva_poblacion
    
    # Seleccionar aleatoriamente individuos de la población actual para reemplazar
    indices_reemplazo = np.random.choice(len(poblacion_actual), size=num_reemplazos, replace=False)
    
    # Seleccionar aleatoriamente individuos de la descendencia
    indices_descendencia = np.random.choice(len(descendencia), size=num_reemplazos, replace=False)
    
    # Reemplazar los individuos seleccionados
    for i, idx_act in enumerate(indices_reemplazo):
        idx_desc = indices_descendencia[i]
        nueva_poblacion[idx_act] = np.copy(descendencia[idx_desc])
    
    return nueva_poblacion


def reemplazo_adaptativo(
    poblacion_actual: List[np.ndarray],
    fitness_actual: List[float],
    descendencia: List[np.ndarray],
    fitness_descendencia: List[float],
    generacion_actual: int,
    max_generaciones: int,
    proporcion_elitismo: float = 0.1,
    maximizar: bool = True,
    **kwargs
) -> List[np.ndarray]:
    """
    Realiza un reemplazo adaptativo que cambia la estrategia según la fase del algoritmo.
    
    En las primeras generaciones se favorece la exploración con reemplazo más diverso,
    mientras que en las últimas generaciones se favorece la explotación con más elitismo.
    
    Parameters
    ----------
    poblacion_actual : List[np.ndarray]
        Lista de individuos de la población actual.
    fitness_actual : List[float]
        Lista con los valores de fitness de la población actual.
    descendencia : List[np.ndarray]
        Lista de individuos de la descendencia.
    fitness_descendencia : List[float]
        Lista con los valores de fitness de la descendencia.
    generacion_actual : int
        Generación actual del algoritmo.
    max_generaciones : int
        Número máximo de generaciones.
    proporcion_elitismo : float, optional
        Proporción base de individuos élite. Por defecto es 0.1.
    maximizar : bool, optional
        Si es True, se maximiza el fitness. Si es False, se minimiza. Por defecto es True.
    **kwargs : dict
        Parámetros adicionales (no utilizados en esta implementación).
        
    Returns
    -------
    List[np.ndarray]
        Nueva población después del reemplazo.
    
    Examples
    --------
    >>> pob_actual = [np.array([1, 1]), np.array([0, 0])]
    >>> fit_actual = [2, 0]
    >>> descendencia = [np.array([1, 0]), np.array([0, 1])]
    >>> fit_descendencia = [1, 1]
    >>> nueva_pob = reemplazo_adaptativo(pob_actual, fit_actual, descendencia, fit_descendencia, 50, 100, 0.1)
    >>> len(nueva_pob)
    2
    """
    # Calcular la fase del algoritmo (0 al inicio, 1 al final)
    fase = generacion_actual / max_generaciones
    
    # Ajustar la proporción de elitismo según la fase
    elitismo_ajustado = proporcion_elitismo + (1 - proporcion_elitismo) * (fase ** 2)
    
    # En las primeras generaciones, usar reemplazo más diverso
    if fase < 0.3:
        # Usar reemplazo aleatorio con baja proporción de reemplazo
        return reemplazo_aleatorio(
            poblacion_actual, 
            fitness_actual, 
            descendencia, 
            fitness_descendencia, 
            0.8 - 0.6 * fase, 
            **kwargs
        )
    elif fase < 0.7:
        # Usar reemplazo de estado estacionario
        num_reemplazos = max(2, int(len(poblacion_actual) * (0.5 - 0.3 * fase)))
        return reemplazo_estado_estacionario(
            poblacion_actual, 
            fitness_actual, 
            descendencia, 
            fitness_descendencia, 
            num_reemplazos, 
            maximizar,
            **kwargs
        )
    else:
        # En las últimas generaciones, aumentar el elitismo
        return reemplazo_elitismo(
            poblacion_actual, 
            fitness_actual, 
            descendencia, 
            fitness_descendencia, 
            elitismo_ajustado,
            maximizar,
            **kwargs
        )