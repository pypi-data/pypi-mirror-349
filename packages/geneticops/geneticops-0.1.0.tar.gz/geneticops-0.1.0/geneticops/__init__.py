"""
geneticops - Librería de Algoritmos Genéticos en Python
====================================================

La librería geneticops proporciona una implementación modular y extensible
de algoritmos genéticos para optimización y búsqueda.
"""

from .algoritmo import AlgoritmoGenetico
from .poblacion import (
    inicializar_poblacion_binaria,
    inicializar_poblacion_real,
    inicializar_poblacion_permutacion,
    inicializar_poblacion_desde_semilla,
    evaluar_poblacion
)
from .seleccion import (
    seleccion_ruleta,
    seleccion_torneo,
    seleccion_ranking,
    seleccion_truncamiento,
    seleccion_estocastica_universal
)
from .cruce import (
    cruce_un_punto,
    cruce_dos_puntos,
    cruce_uniforme,
    cruce_aritmetico,
    cruce_sbx,
    cruce_pmx,
    cruce_ox,
    cruce_ciclo
)
from .mutacion import (
    mutacion_bit_flip,
    mutacion_uniforme,
    mutacion_gaussiana,
    mutacion_swap,
    mutacion_inversion,
    mutacion_insertion,
    mutacion_scramble,
    mutacion_adaptativa
)
from .reemplazo import (
    reemplazo_generacional,
    reemplazo_elitismo,
    reemplazo_estado_estacionario,
    reemplazo_torneo,
    reemplazo_aleatorio,
    reemplazo_adaptativo
)
from .condiciones_parada import (
    condicion_max_generaciones,
    condicion_convergencia,
    condicion_fitness_objetivo,
    condicion_tiempo_limite,
    condicion_estancamiento,
    condicion_combinada,
    condicion_personalizada
)
from .utilidades import (
    graficar_convergencia,
    guardar_resultados,
    cargar_mejor_individuo,
    calcular_estadisticas_poblacion,
    calcular_diversidad_poblacion,
    decodificar_binario_a_real,
    codificar_real_a_binario,
    CacheDecorador
)

__version__ = "0.1.0"
