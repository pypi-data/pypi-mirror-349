"""
GeneticAlgorithm
===============

Este módulo contiene la clase principal que integra todas las operaciones
de algoritmos genéticos.
"""

from typing import Callable, List, Tuple, Dict, Any, Optional, Type, Union
import numpy as np
import time
from geneticops.poblacion import inicializar_poblacion_binaria, inicializar_poblacion_real
from geneticops.seleccion import seleccion_ruleta, seleccion_torneo, seleccion_ranking
from geneticops.cruce import cruce_un_punto, cruce_dos_puntos, cruce_uniforme
from geneticops.mutacion import mutacion_bit_flip, mutacion_swap, mutacion_inversion
from geneticops.reemplazo import reemplazo_elitismo, reemplazo_generacional
from geneticops.condiciones_parada import condicion_max_generaciones, condicion_convergencia
from geneticops.utilidades import Individuo, Poblacion


class AlgoritmoGenetico:
    """
    Clase principal que implementa un algoritmo genético configurable.
    
    Esta clase integra todas las operaciones genéticas como métodos modulares
    y permite la ejecución completa de un algoritmo genético.
    
    Parameters
    ----------
    tamano_poblacion : int
        Número de individuos en la población.
    longitud_individuo : int
        Longitud del genoma de cada individuo.
    funcion_fitness : Callable
        Función que evalúa la aptitud de un individuo.
    funcion_inicializacion : Callable, optional
        Función para inicializar la población. Por defecto es inicializar_poblacion_binaria.
    funcion_seleccion : Callable, optional
        Función de selección de individuos. Por defecto es seleccion_ruleta.
    funcion_cruce : Callable, optional
        Función de cruce entre individuos. Por defecto es cruce_un_punto.
    funcion_mutacion : Callable, optional
        Función de mutación de individuos. Por defecto es mutacion_bit_flip.
    funcion_reemplazo : Callable, optional
        Función de reemplazo generacional. Por defecto es reemplazo_elitismo.
    condicion_parada : Callable, optional
        Función que determina cuándo terminar el algoritmo. Por defecto es condicion_max_generaciones.
    probabilidad_cruce : float, optional
        Probabilidad de aplicar cruce entre individuos. Por defecto es 0.8.
    probabilidad_mutacion : float, optional
        Probabilidad de mutación para cada gen. Por defecto es 0.1.
    elitismo : float, optional
        Proporción de individuos élite a conservar en cada generación. Por defecto es 0.1.
    max_generaciones : int, optional
        Número máximo de generaciones. Por defecto es 100.
    tipo_genoma : str, optional
        Tipo de genoma: 'binario' o 'real'. Por defecto es 'binario'.
    parametros_adicionales : Dict, optional
        Parámetros adicionales para funciones específicas.
    
    Attributes
    ----------
    poblacion : List[Individuo]
        Población actual de individuos.
    mejor_individuo : Individuo
        Mejor individuo encontrado hasta el momento.
    mejor_fitness : float
        Valor de aptitud del mejor individuo.
    historia_fitness : List[float]
        Lista con el mejor valor de fitness de cada generación.
    generacion_actual : int
        Número de la generación actual.
    tiempo_ejecucion : float
        Tiempo de ejecución del algoritmo en segundos.
    """
    
    def __init__(
        self, 
        tamano_poblacion: int,
        longitud_individuo: int,
        funcion_fitness: Callable[[np.ndarray], float],
        funcion_inicializacion: Callable = inicializar_poblacion_binaria,
        funcion_seleccion: Callable = seleccion_ruleta,
        funcion_cruce: Callable = cruce_un_punto,
        funcion_mutacion: Callable = mutacion_bit_flip,
        funcion_reemplazo: Callable = reemplazo_elitismo,
        condicion_parada: Callable = condicion_max_generaciones,
        probabilidad_cruce: float = 0.8,
        probabilidad_mutacion: float = 0.1,
        elitismo: float = 0.1,
        max_generaciones: int = 100,
        tipo_genoma: str = 'binario',
        parametros_adicionales: Dict[str, Any] = None
    ):
        # Parámetros principales
        self.tamano_poblacion = tamano_poblacion
        self.longitud_individuo = longitud_individuo
        self.funcion_fitness = funcion_fitness
        self.funcion_inicializacion = funcion_inicializacion
        self.funcion_seleccion = funcion_seleccion
        self.funcion_cruce = funcion_cruce
        self.funcion_mutacion = funcion_mutacion
        self.funcion_reemplazo = funcion_reemplazo
        self.condicion_parada = condicion_parada
        self.probabilidad_cruce = probabilidad_cruce
        self.probabilidad_mutacion = probabilidad_mutacion
        self.elitismo = elitismo
        self.max_generaciones = max_generaciones
        self.tipo_genoma = tipo_genoma
        self.parametros_adicionales = parametros_adicionales or {}
        
        # Estado del algoritmo
        self.poblacion: Poblacion = []
        self.fitness_poblacion: List[float] = []
        self.mejor_individuo: Optional[Individuo] = None
        self.mejor_fitness: float = float('-inf')
        self.historia_fitness: List[float] = []
        self.generacion_actual: int = 0
        self.tiempo_ejecucion: float = 0.0
        self.inicializado: bool = False
    
    def inicializar(self) -> None:
        """
        Inicializa la población y evalúa la aptitud inicial de cada individuo.
        
        Returns
        -------
        None
        """
        # Inicializar población según el tipo de genoma
        if self.tipo_genoma == 'binario':
            self.poblacion = self.funcion_inicializacion(
                self.tamano_poblacion, 
                self.longitud_individuo, 
                **self.parametros_adicionales.get('inicializacion', {})
            )
        elif self.tipo_genoma == 'real':
            # Para genomas de valores reales, necesitamos límites
            limites = self.parametros_adicionales.get('limites', [0, 1])
            self.poblacion = inicializar_poblacion_real(
                self.tamano_poblacion, 
                self.longitud_individuo, 
                limites[0], 
                limites[1],
                **self.parametros_adicionales.get('inicializacion', {})
            )
        else:
            raise ValueError(f"Tipo de genoma no soportado: {self.tipo_genoma}")
        
        # Evaluar fitness inicial
        self.evaluar_poblacion()
        
        # Encontrar el mejor individuo inicial
        self.actualizar_mejor_individuo()
        
        self.inicializado = True
        self.generacion_actual = 0
    
    def evaluar_poblacion(self) -> None:
        """
        Evalúa la aptitud de todos los individuos en la población actual.
        
        Returns
        -------
        None
        """
        self.fitness_poblacion = [self.funcion_fitness(individuo) for individuo in self.poblacion]
    
    def actualizar_mejor_individuo(self) -> None:
        """
        Actualiza el mejor individuo encontrado hasta el momento.
        
        Returns
        -------
        None
        """
        mejor_idx = np.argmax(self.fitness_poblacion)
        if self.fitness_poblacion[mejor_idx] > self.mejor_fitness:
            self.mejor_fitness = self.fitness_poblacion[mejor_idx]
            self.mejor_individuo = np.copy(self.poblacion[mejor_idx])
            
        self.historia_fitness.append(self.mejor_fitness)
    
    def seleccionar_padres(self) -> Tuple[List[Individuo], List[float]]:
        """
        Selecciona individuos para reproducción utilizando la función de selección configurada.
        
        Returns
        -------
        Tuple[List[Individuo], List[float]]
            Tupla con la lista de padres seleccionados y sus valores de fitness.
        """
        padres, fitness_padres = self.funcion_seleccion(
            self.poblacion, 
            self.fitness_poblacion, 
            self.tamano_poblacion, 
            **self.parametros_adicionales.get('seleccion', {})
        )
        return padres, fitness_padres
    
    def reproducir(self, padres: List[Individuo]) -> List[Individuo]:
        """
        Aplica operadores de cruce y mutación para generar nueva descendencia.
        
        Parameters
        ----------
        padres : List[Individuo]
            Lista de individuos padres seleccionados para reproducción.
            
        Returns
        -------
        List[Individuo]
            Lista de individuos de la nueva generación.
        """
        descendencia = []
        
        # Aplicar cruce
        for i in range(0, len(padres), 2):
            if i+1 < len(padres):  # Asegurar que hay un par
                if np.random.random() < self.probabilidad_cruce:
                    hijo1, hijo2 = self.funcion_cruce(
                        padres[i], 
                        padres[i+1], 
                        **self.parametros_adicionales.get('cruce', {})
                    )
                    descendencia.extend([hijo1, hijo2])
                else:
                    descendencia.extend([np.copy(padres[i]), np.copy(padres[i+1])])
        
        # Aplicar mutación
        for i in range(len(descendencia)):
            descendencia[i] = self.funcion_mutacion(
                descendencia[i], 
                self.probabilidad_mutacion, 
                **self.parametros_adicionales.get('mutacion', {})
            )
        
        return descendencia
    
    def reemplazar_poblacion(self, descendencia: List[Individuo]) -> None:
        """
        Reemplaza la población anterior con la nueva generación.
        
        Parameters
        ----------
        descendencia : List[Individuo]
            Lista de individuos de la nueva generación.
            
        Returns
        -------
        None
        """
        self.poblacion = self.funcion_reemplazo(
            self.poblacion, 
            self.fitness_poblacion, 
            descendencia, 
            [self.funcion_fitness(ind) for ind in descendencia],
            self.elitismo,
            **self.parametros_adicionales.get('reemplazo', {})
        )
        
        # Actualizar fitness de la nueva población
        self.evaluar_poblacion()
    
    def verificar_condicion_parada(self) -> bool:
        """
        Verifica si se cumple la condición de parada del algoritmo.
        
        Returns
        -------
        bool
            True si se debe detener el algoritmo, False en caso contrario.
        """
        return self.condicion_parada(
            self.generacion_actual,
            self.max_generaciones,
            self.historia_fitness,
            **self.parametros_adicionales.get('condicion_parada', {})
        )
    
    def ejecutar(self) -> Tuple[Individuo, float, Dict[str, Any]]:
        """
        Ejecuta el algoritmo genético completo.
        
        Returns
        -------
        Tuple[Individuo, float, Dict[str, Any]]
            Tupla con el mejor individuo encontrado, su fitness y un diccionario
            con información adicional sobre la ejecución.
        """
        tiempo_inicio = time.time()
        
        if not self.inicializado:
            self.inicializar()
        
        # Ciclo principal del algoritmo genético
        while not self.verificar_condicion_parada():
            # Selección de padres
            padres, _ = self.seleccionar_padres()
            
            # Reproducción (cruce y mutación)
            descendencia = self.reproducir(padres)
            
            # Reemplazo generacional
            self.reemplazar_poblacion(descendencia)
            
            # Actualizar mejor individuo
            self.actualizar_mejor_individuo()
            
            # Incrementar contador de generación
            self.generacion_actual += 1
        
        self.tiempo_ejecucion = time.time() - tiempo_inicio
        
        # Información adicional sobre la ejecución
        info_ejecucion = {
            'generaciones': self.generacion_actual,
            'tiempo_ejecucion': self.tiempo_ejecucion,
            'historia_fitness': self.historia_fitness,
            'convergencia': self.historia_fitness[-10:] if len(self.historia_fitness) >= 10 else self.historia_fitness
        }
        
        return self.mejor_individuo, self.mejor_fitness, info_ejecucion
    
    def reiniciar(self) -> None:
        """
        Reinicia el estado del algoritmo para una nueva ejecución.
        
        Returns
        -------
        None
        """
        self.poblacion = []
        self.fitness_poblacion = []
        self.mejor_individuo = None
        self.mejor_fitness = float('-inf')
        self.historia_fitness = []
        self.generacion_actual = 0
        self.tiempo_ejecucion = 0.0
        self.inicializado = False