# GeneticOps

Una librería para algoritmos genéticos en Python, diseñada para ser modular, extensible y fácil de usar.

## Descripción

GeneticOps proporciona una implementación completa y flexible de algoritmos genéticos, permitiendo su aplicación a una amplia variedad de problemas de optimización. La librería está diseñada siguiendo principios de modularidad y extensibilidad, facilitando la personalización de cada componente del algoritmo genético.

## Características

- **Modularidad**: Todos los componentes (selección, cruce, mutación, etc.) son intercambiables.
- **Extensibilidad**: Fácil de extender con nuevos operadores y funcionalidades.
- **Tipado estático**: Uso de typing para mejorar la documentación y el desarrollo.
- **Documentación completa**: Docstrings detallados en estilo NumPy para todas las funciones.
- **Visualización integrada**: Funciones para visualizar la convergencia y los resultados.
- **Ejemplos incluidos**: Varios ejemplos de problemas clásicos resueltos con la librería.

## Instalación

```bash
pip install geneticops
```

## Uso básico

```python
import numpy as np
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

# Definir una función de fitness
def fitness(individuo):
    # Maximizar el número de unos
    return np.sum(individuo)

# Crear instancia del algoritmo genético
ag = AlgoritmoGenetico(
    tamano_poblacion=100,
    longitud_individuo=10,
    funcion_fitness=fitness,
    funcion_inicializacion=inicializar_poblacion_binaria,
    funcion_seleccion=seleccion_ruleta,
    funcion_cruce=cruce_un_punto,
    funcion_mutacion=mutacion_bit_flip,
    funcion_reemplazo=reemplazo_elitismo,
    condicion_parada=condicion_max_generaciones,
    probabilidad_cruce=0.8,
    probabilidad_mutacion=0.1,
    elitismo=0.1,
    max_generaciones=100,
    tipo_genoma='binario'
)

# Ejecutar el algoritmo
mejor_individuo, mejor_fitness, info = ag.ejecutar()

# Visualizar resultados
print(f"Mejor individuo: {mejor_individuo}")
print(f"Fitness: {mejor_fitness}")
graficar_convergencia(info['historia_fitness'])
```

## Componentes disponibles

### Inicialización de población
- `inicializar_poblacion_binaria`: Genomas binarios (0s y 1s)
- `inicializar_poblacion_real`: Genomas de valores reales
- `inicializar_poblacion_permutacion`: Genomas de permutación (para TSP)
- `inicializar_poblacion_desde_semilla`: Inicialización a partir de un individuo semilla

### Selección
- `seleccion_ruleta`: Selección proporcional al fitness
- `seleccion_torneo`: Selección por torneos
- `seleccion_ranking`: Selección basada en ranking
- `seleccion_truncamiento`: Selección de los mejores individuos
- `seleccion_estocastica_universal`: Muestreo estocástico universal

### Cruce
- `cruce_un_punto`: Cruce en un punto (binario)
- `cruce_dos_puntos`: Cruce en dos puntos (binario)
- `cruce_uniforme`: Cruce uniforme (binario)
- `cruce_aritmetico`: Cruce aritmético (valores reales)
- `cruce_sbx`: Simulated Binary Crossover (valores reales)
- `cruce_pmx`: Partially Mapped Crossover (permutación)
- `cruce_ox`: Order Crossover (permutación)
- `cruce_ciclo`: Cycle Crossover (permutación)

### Mutación
- `mutacion_bit_flip`: Inversión de bits (binario)
- `mutacion_uniforme`: Valores aleatorios uniformes (real)
- `mutacion_gaussiana`: Ruido gaussiano (real)
- `mutacion_swap`: Intercambio de posiciones (permutación)
- `mutacion_inversion`: Inversión de segmento (permutación)
- `mutacion_insertion`: Inserción (permutación)
- `mutacion_scramble`: Barajado de segmento (permutación)
- `mutacion_adaptativa`: Mutación que se adapta según la fase del algoritmo

### Reemplazo
- `reemplazo_generacional`: Reemplazo completo con posible elitismo
- `reemplazo_elitismo`: Selección de los mejores de ambas poblaciones
- `reemplazo_estado_estacionario`: Reemplazo de algunos individuos
- `reemplazo_torneo`: Torneos entre individuos de ambas poblaciones
- `reemplazo_aleatorio`: Reemplazo aleatorio
- `reemplazo_adaptativo`: Estrategia adaptativa según la fase del algoritmo

### Condiciones de parada
- `condicion_max_generaciones`: Número máximo de generaciones
- `condicion_convergencia`: Convergencia en fitness
- `condicion_fitness_objetivo`: Alcanzar un valor objetivo de fitness
- `condicion_tiempo_limite`: Tiempo límite de ejecución
- `condicion_estancamiento`: Detección de estancamiento
- `condicion_combinada`: Combinación de múltiples condiciones
- `condicion_personalizada`: Condición definida por el usuario

### Utilidades
- `graficar_convergencia`: Visualización de la evolución del fitness
- `guardar_resultados`: Guardar resultados en archivos
- `cargar_mejor_individuo`: Cargar individuo desde archivo
- `calcular_estadisticas_poblacion`: Estadísticas de la población
- `calcular_diversidad_poblacion`: Medida de diversidad
- `decodificar_binario_a_real`: Convertir genoma binario a valores reales
- `codificar_real_a_binario`: Convertir valores reales a genoma binario
- `CacheDecorador`: Decorador para cachear evaluaciones de fitness

## Ejemplos

La librería incluye ejemplos de aplicación a problemas clásicos:

- `maximizar_funcion.py`: Encontrar el máximo de una función.
- `problema_mochila.py`: Problema de la mochila (Knapsack Problem).
- `viajero_comercio.py`: Problema del viajante de comercio (TSP).

## Publicación en PyPI

Para publicar la librería en PyPI:

```bash
# Instalar herramientas necesarias
pip install setuptools wheel twine

# Generar distribución
python setup.py sdist bdist_wheel

# Publicar en TestPyPI (opcional, para pruebas)
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Publicar en PyPI
twine upload dist/*
```

## Requisitos

- Python 3.6+
- NumPy
- Matplotlib (para visualización)

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.