"""
Módulo de utilidades
=================

Este módulo contiene funciones y clases auxiliares para los algoritmos genéticos.
"""

from typing import List, Tuple, Dict, Any, Optional, Union, TypeVar, Generic
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json
import pickle
import csv

# Definir tipos para mejorar la legibilidad
Individuo = np.ndarray
Poblacion = List[Individuo]
FitnessValues = List[float]


def crear_directorio_resultados(nombre_experimento: str = None) -> str:
    """
    Crea un directorio para guardar los resultados de la ejecución.
    
    Parameters
    ----------
    nombre_experimento : str, optional
        Nombre del experimento. Si no se proporciona, se usa la fecha y hora actual.
        
    Returns
    -------
    str
        Ruta al directorio creado.
    """
    # Crear directorio base si no existe
    directorio_base = "resultados"
    if not os.path.exists(directorio_base):
        os.makedirs(directorio_base)
    
    # Crear nombre de experimento si no se proporciona
    if nombre_experimento is None:
        nombre_experimento = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Crear directorio del experimento
    directorio_experimento = os.path.join(directorio_base, nombre_experimento)
    if not os.path.exists(directorio_experimento):
        os.makedirs(directorio_experimento)
    
    return directorio_experimento


def graficar_convergencia(
    historia_fitness: List[float],
    titulo: str = "Convergencia del Algoritmo Genético",
    ruta_guardado: Optional[str] = None,
    mostrar: bool = True
) -> None:
    """
    Genera un gráfico de la convergencia del algoritmo.
    
    Parameters
    ----------
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    titulo : str, optional
        Título del gráfico. Por defecto es "Convergencia del Algoritmo Genético".
    ruta_guardado : str, optional
        Ruta donde guardar el gráfico. Si es None, no se guarda.
    mostrar : bool, optional
        Si es True, muestra el gráfico. Por defecto es True.
        
    Returns
    -------
    None
    """
    plt.figure(figsize=(10, 6))
    plt.plot(historia_fitness, linewidth=2, color='blue')
    plt.title(titulo)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Fitness")
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Añadir etiquetas con los valores inicial y final
    if historia_fitness:
        plt.annotate(f'{historia_fitness[0]:.4f}', 
                    xy=(0, historia_fitness[0]), 
                    xytext=(10, 10),
                    textcoords='offset points')
        
        plt.annotate(f'{historia_fitness[-1]:.4f}', 
                    xy=(len(historia_fitness) - 1, historia_fitness[-1]), 
                    xytext=(-10, 10),
                    textcoords='offset points',
                    ha='right')
    
    # Guardar si se proporciona una ruta
    if ruta_guardado:
        plt.savefig(ruta_guardado, dpi=300, bbox_inches='tight')
    
    # Mostrar si se solicita
    if mostrar:
        plt.show()
    else:
        plt.close()


def guardar_resultados(
    mejor_individuo: Individuo,
    mejor_fitness: float,
    historia_fitness: List[float],
    parametros: Dict[str, Any],
    ruta_base: str,
    guardar_individuo: bool = True,
    guardar_historia: bool = True,
    guardar_parametros: bool = True,
    formato_individuo: str = 'pickle'
) -> None:
    """
    Guarda los resultados de la ejecución en archivos.
    
    Parameters
    ----------
    mejor_individuo : Individuo
        Mejor individuo encontrado.
    mejor_fitness : float
        Valor de fitness del mejor individuo.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    parametros : Dict[str, Any]
        Diccionario con los parámetros utilizados.
    ruta_base : str
        Directorio base donde guardar los resultados.
    guardar_individuo : bool, optional
        Si es True, guarda el mejor individuo. Por defecto es True.
    guardar_historia : bool, optional
        Si es True, guarda la historia de fitness. Por defecto es True.
    guardar_parametros : bool, optional
        Si es True, guarda los parámetros. Por defecto es True.
    formato_individuo : str, optional
        Formato para guardar el individuo: 'pickle', 'csv' o 'json'. Por defecto es 'pickle'.
        
    Returns
    -------
    None
    """
    # Crear directorio si no existe
    if not os.path.exists(ruta_base):
        os.makedirs(ruta_base)
    
    # Guardar mejor individuo
    if guardar_individuo:
        if formato_individuo == 'pickle':
            with open(os.path.join(ruta_base, 'mejor_individuo.pkl'), 'wb') as f:
                pickle.dump(mejor_individuo, f)
        elif formato_individuo == 'csv':
            np.savetxt(os.path.join(ruta_base, 'mejor_individuo.csv'), 
                      mejor_individuo, 
                      delimiter=',')
        elif formato_individuo == 'json':
            with open(os.path.join(ruta_base, 'mejor_individuo.json'), 'w') as f:
                json.dump(mejor_individuo.tolist(), f)
        else:
            raise ValueError(f"Formato no soportado: {formato_individuo}")
    
    # Guardar mejor fitness
    with open(os.path.join(ruta_base, 'mejor_fitness.txt'), 'w') as f:
        f.write(str(mejor_fitness))
    
    # Guardar historia de fitness
    if guardar_historia:
        np.savetxt(os.path.join(ruta_base, 'historia_fitness.csv'), 
                  historia_fitness, 
                  delimiter=',')
        
        # Generar gráfico de convergencia
        graficar_convergencia(
            historia_fitness,
            ruta_guardado=os.path.join(ruta_base, 'convergencia.png'),
            mostrar=False
        )
    
    # Guardar parámetros
    if guardar_parametros:
        # Convertir valores no serializables a string
        parametros_serializables = {}
        for k, v in parametros.items():
            if callable(v):
                parametros_serializables[k] = v.__name__
            elif isinstance(v, np.ndarray):
                parametros_serializables[k] = f"Array de forma {v.shape}"
            else:
                try:
                    json.dumps({k: v})
                    parametros_serializables[k] = v
                except (TypeError, OverflowError):
                    parametros_serializables[k] = str(v)
        
        with open(os.path.join(ruta_base, 'parametros.json'), 'w') as f:
            json.dump(parametros_serializables, f, indent=4)


def cargar_mejor_individuo(
    ruta: str,
    formato: str = 'pickle'
) -> Individuo:
    """
    Carga el mejor individuo desde un archivo.
    
    Parameters
    ----------
    ruta : str
        Ruta al archivo que contiene el individuo.
    formato : str, optional
        Formato del archivo: 'pickle', 'csv' o 'json'. Por defecto es 'pickle'.
        
    Returns
    -------
    Individuo
        Individuo cargado.
    """
    if formato == 'pickle':
        with open(ruta, 'rb') as f:
            return pickle.load(f)
    elif formato == 'csv':
        return np.loadtxt(ruta, delimiter=',')
    elif formato == 'json':
        with open(ruta, 'r') as f:
            return np.array(json.load(f))
    else:
        raise ValueError(f"Formato no soportado: {formato}")


def calcular_estadisticas_poblacion(
    poblacion: Poblacion,
    fitness_valores: FitnessValues
) -> Dict[str, float]:
    """
    Calcula estadísticas sobre la población actual.
    
    Parameters
    ----------
    poblacion : Poblacion
        Lista de individuos.
    fitness_valores : FitnessValues
        Lista con los valores de fitness de cada individuo.
        
    Returns
    -------
    Dict[str, float]
        Diccionario con estadísticas (mejor, peor, promedio, etc.).
    """
    if not poblacion or not fitness_valores:
        return {
            'mejor': None,
            'peor': None,
            'promedio': None,
            'mediana': None,
            'desviacion': None
        }
    
    fitness_array = np.array(fitness_valores)
    
    return {
        'mejor': np.max(fitness_array),
        'peor': np.min(fitness_array),
        'promedio': np.mean(fitness_array),
        'mediana': np.median(fitness_array),
        'desviacion': np.std(fitness_array)
    }


def calcular_diversidad_poblacion(
    poblacion: Poblacion,
    metrica: str = 'hamming'
) -> float:
    """
    Calcula la diversidad de la población utilizando diferentes métricas.
    
    Parameters
    ----------
    poblacion : Poblacion
        Lista de individuos.
    metrica : str, optional
        Métrica de diversidad: 'hamming', 'euclidiana' o 'coseno'. Por defecto es 'hamming'.
        
    Returns
    -------
    float
        Valor de diversidad de la población.
    """
    if not poblacion or len(poblacion) < 2:
        return 0.0
    
    n = len(poblacion)
    suma_distancias = 0.0
    
    # Calcular la suma de distancias entre todos los pares de individuos
    for i in range(n):
        for j in range(i+1, n):
            if metrica == 'hamming':
                # Para genomas binarios: proporción de genes diferentes
                if np.all(np.logical_or(poblacion[i] == 0, poblacion[i] == 1)) and \
                   np.all(np.logical_or(poblacion[j] == 0, poblacion[j] == 1)):
                    suma_distancias += np.mean(poblacion[i] != poblacion[j])
                else:
                    suma_distancias += np.mean(poblacion[i] != poblacion[j])
            elif metrica == 'euclidiana':
                # Distancia euclidiana
                suma_distancias += np.sqrt(np.sum((poblacion[i] - poblacion[j]) ** 2))
            elif metrica == 'coseno':
                # Similitud del coseno
                norma_i = np.linalg.norm(poblacion[i])
                norma_j = np.linalg.norm(poblacion[j])
                if norma_i > 0 and norma_j > 0:
                    similitud = np.dot(poblacion[i], poblacion[j]) / (norma_i * norma_j)
                    suma_distancias += 1 - similitud  # Convertir similitud a distancia
                else:
                    suma_distancias += 1.0
            else:
                raise ValueError(f"Métrica no soportada: {metrica}")
    
    # Normalizar la suma de distancias
    num_pares = n * (n - 1) / 2
    return suma_distancias / num_pares


def decodificar_binario_a_real(
    individuo_binario: Individuo,
    limites: List[Tuple[float, float]],
    bits_por_variable: Optional[int] = None
) -> np.ndarray:
    """
    Decodifica un individuo con genoma binario a valores reales.
    
    Parameters
    ----------
    individuo_binario : Individuo
        Individuo con genoma binario.
    limites : List[Tuple[float, float]]
        Lista de tuplas (min, max) con los límites para cada variable.
    bits_por_variable : int, optional
        Número de bits por variable. Si es None, se calcula automáticamente.
        
    Returns
    -------
    np.ndarray
        Array con los valores reales decodificados.
    """
    # Verificar que el individuo es binario
    if not np.all(np.logical_or(individuo_binario == 0, individuo_binario == 1)):
        raise ValueError("El individuo debe ser binario (solo 0s y 1s)")
    
    num_variables = len(limites)
    
    # Calcular bits por variable si no se proporciona
    if bits_por_variable is None:
        bits_por_variable = len(individuo_binario) // num_variables
    
    # Verificar que la longitud es compatible
    if len(individuo_binario) != bits_por_variable * num_variables:
        raise ValueError(f"La longitud del individuo ({len(individuo_binario)}) no es compatible con {num_variables} variables y {bits_por_variable} bits por variable")
    
    # Inicializar array para valores reales
    valores_reales = np.zeros(num_variables)
    
    # Decodificar cada variable
    for i in range(num_variables):
        # Extraer los bits correspondientes a esta variable
        inicio = i * bits_por_variable
        fin = (i + 1) * bits_por_variable
        bits = individuo_binario[inicio:fin]
        
        # Convertir bits a valor decimal
        valor_decimal = 0
        for j, bit in enumerate(reversed(bits)):
            valor_decimal += bit * (2 ** j)
        
        # Normalizar y escalar al rango deseado
        min_val, max_val = limites[i]
        max_decimal = 2 ** bits_por_variable - 1
        valores_reales[i] = min_val + (valor_decimal / max_decimal) * (max_val - min_val)
    
    return valores_reales


def codificar_real_a_binario(
    individuo_real: Individuo,
    limites: List[Tuple[float, float]],
    bits_por_variable: int
) -> np.ndarray:
    """
    Codifica un individuo con valores reales a genoma binario.
    
    Parameters
    ----------
    individuo_real : Individuo
        Individuo con valores reales.
    limites : List[Tuple[float, float]]
        Lista de tuplas (min, max) con los límites para cada variable.
    bits_por_variable : int
        Número de bits por variable.
        
    Returns
    -------
    np.ndarray
        Array con el genoma binario codificado.
    """
    # Verificar que la longitud es compatible
    if len(individuo_real) != len(limites):
        raise ValueError(f"La longitud del individuo ({len(individuo_real)}) no coincide con la cantidad de límites ({len(limites)})")
    
    num_variables = len(individuo_real)
    longitud_total = bits_por_variable * num_variables
    
    # Inicializar array para el genoma binario
    genoma_binario = np.zeros(longitud_total, dtype=int)
    
    # Codificar cada variable
    for i in range(num_variables):
        # Extraer límites para esta variable
        min_val, max_val = limites[i]
        
        # Normalizar el valor real al rango [0, 2^bits - 1]
        max_decimal = 2 ** bits_por_variable - 1
        valor_normalizado = (individuo_real[i] - min_val) / (max_val - min_val)
        valor_decimal = int(round(valor_normalizado * max_decimal))
        valor_decimal = max(0, min(valor_decimal, max_decimal))  # Asegurar límites
        
        # Convertir valor decimal a bits
        for j in range(bits_por_variable):
            bit = (valor_decimal >> j) & 1
            genoma_binario[i * bits_por_variable + (bits_por_variable - 1 - j)] = bit
    
    return genoma_binario


class CacheDecorador:
    """
    Decorador para cachear los resultados de la función de fitness.
    
    Útil para optimizar el cálculo cuando la evaluación de fitness es costosa.
    """
    
    def __init__(self, funcion: callable):
        self.funcion = funcion
        self.cache = {}
        self.llamadas_totales = 0
        self.aciertos_cache = 0
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Incrementar contador de llamadas
        self.llamadas_totales += 1
        
        # Obtener argumento principal (individuo)
        arg = args[0]
        
        # Convertir array a tupla para poder usarlo como clave
        key = tuple(arg.flatten())
        
        # Verificar si ya está en la caché
        if key in self.cache:
            self.aciertos_cache += 1
            return self.cache[key]
        
        # Calcular valor si no está en la caché
        value = self.funcion(*args, **kwargs)
        
        # Almacenar en la caché
        self.cache[key] = value
        
        return value
    
    def estadisticas(self) -> Dict[str, Union[int, float]]:
        """
        Obtiene estadísticas sobre el uso de la caché.
        
        Returns
        -------
        Dict[str, Union[int, float]]
            Diccionario con estadísticas de la caché.
        """
        tasa_aciertos = 0.0
        if self.llamadas_totales > 0:
            tasa_aciertos = self.aciertos_cache / self.llamadas_totales * 100
        
        return {
            'llamadas_totales': self.llamadas_totales,
            'aciertos_cache': self.aciertos_cache,
            'tasa_aciertos': tasa_aciertos,
            'tamanio_cache': len(self.cache)
        }
    
    def limpiar_cache(self) -> None:
        """
        Limpia la caché.
        """
        self.cache.clear()