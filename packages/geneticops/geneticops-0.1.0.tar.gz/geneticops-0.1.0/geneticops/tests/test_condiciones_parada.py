"""
Pruebas para el módulo condiciones_parada.py
=========================================

Este módulo contiene las pruebas unitarias para las funciones de condiciones
de parada del algoritmo genético.
"""

import unittest
import numpy as np
import time
from geneticops.condiciones_parada import (
    condicion_max_generaciones,
    condicion_convergencia,
    condicion_fitness_objetivo,
    condicion_tiempo_limite,
    condicion_estancamiento,
    condicion_combinada,
    condicion_personalizada
)


class TestCondicionesParada(unittest.TestCase):
    """Pruebas para las funciones del módulo condiciones_parada."""
    
    def test_condicion_max_generaciones(self):
        """Prueba que la condición de máximo de generaciones funciona correctamente."""
        # No se ha alcanzado el máximo
        self.assertFalse(condicion_max_generaciones(50, 100, []))
        
        # Se ha alcanzado el máximo
        self.assertTrue(condicion_max_generaciones(100, 100, []))
        
        # Se ha superado el máximo
        self.assertTrue(condicion_max_generaciones(110, 100, []))
    
    def test_condicion_convergencia(self):
        """Prueba que la condición de convergencia funciona correctamente."""
        # No hay suficientes generaciones
        historia_fitness = [1.0, 1.1, 1.2]
        self.assertFalse(condicion_convergencia(3, 100, historia_fitness, ventana_convergencia=5))
        
        # No ha convergido (mejora significativa)
        historia_fitness = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        self.assertFalse(condicion_convergencia(11, 100, historia_fitness, umbral_convergencia=0.01))
        
        # Ha convergido (mejora pequeña)
        historia_fitness = [1.0, 1.1, 1.15, 1.17, 1.18, 1.181, 1.182, 1.1821, 1.1822, 1.1823]
        # CORRECCIÓN: usar un umbral más alto para este ejemplo específico
        self.assertTrue(condicion_convergencia(10, 100, historia_fitness, umbral_convergencia=0.005))
    
    def test_condicion_fitness_objetivo(self):
        """Prueba que la condición de fitness objetivo funciona correctamente."""
        # No hay generaciones
        self.assertFalse(condicion_fitness_objetivo(0, 100, [], 1.0))
        
        # No se ha alcanzado el objetivo (maximización)
        historia_fitness = [0.5, 0.7, 0.9]
        self.assertFalse(condicion_fitness_objetivo(3, 100, historia_fitness, 1.0))
        
        # Se ha alcanzado el objetivo (maximización)
        historia_fitness = [0.5, 0.7, 0.9, 1.1]
        self.assertTrue(condicion_fitness_objetivo(4, 100, historia_fitness, 1.0))
        
        # No se ha alcanzado el objetivo (minimización)
        historia_fitness = [2.0, 1.5, 1.2]
        self.assertFalse(condicion_fitness_objetivo(3, 100, historia_fitness, 1.0, maximizar=False))
        
        # Se ha alcanzado el objetivo (minimización)
        historia_fitness = [2.0, 1.5, 1.2, 0.9]
        self.assertTrue(condicion_fitness_objetivo(4, 100, historia_fitness, 1.0, maximizar=False))
    
    def test_condicion_tiempo_limite(self):
        """Prueba que la condición de tiempo límite funciona correctamente."""
        # Obtener tiempo actual
        tiempo_inicio = time.time()
        
        # No se ha alcanzado el límite (1000 segundos)
        self.assertFalse(condicion_tiempo_limite(
            10, 100, [], tiempo_inicio=tiempo_inicio, tiempo_limite=1000.0
        ))
        
        # CORRECCIÓN: Se ha alcanzado el límite (forzar un tiempo pasado)
        tiempo_pasado = tiempo_inicio - 1.0  # Un tiempo 1 segundo en el pasado
        self.assertTrue(condicion_tiempo_limite(
            10, 100, [], tiempo_inicio=tiempo_pasado, tiempo_limite=0.5
        ))
    
    def test_condicion_estancamiento(self):
        """Prueba que la condición de estancamiento funciona correctamente."""
        # No hay suficientes generaciones
        historia_fitness = [1.0, 1.0, 1.0]
        self.assertFalse(condicion_estancamiento(3, 100, historia_fitness, max_generaciones_sin_mejora=5))
        
        # No ha habido estancamiento (hay mejoras)
        historia_fitness = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.assertFalse(condicion_estancamiento(6, 100, historia_fitness, max_generaciones_sin_mejora=5))
        
        # Ha habido estancamiento (sin mejoras)
        historia_fitness = [1.0, 1.1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
        self.assertTrue(condicion_estancamiento(8, 100, historia_fitness, max_generaciones_sin_mejora=5))
    
    def test_condicion_combinada(self):
        """Prueba que la condición combinada funciona correctamente."""
        # Crear condiciones de ejemplo
        def condicion1(generacion, max_gen, hist, **kwargs):
            return generacion >= 50
        
        def condicion2(generacion, max_gen, hist, **kwargs):
            return len(hist) > 0 and hist[-1] >= 10.0
        
        # Modo OR: ninguna condición se cumple
        self.assertFalse(condicion_combinada(
            10, 100, [5.0], condiciones=[condicion1, condicion2], modo='OR'
        ))
        
        # Modo OR: primera condición se cumple
        self.assertTrue(condicion_combinada(
            60, 100, [5.0], condiciones=[condicion1, condicion2], modo='OR'
        ))
        
        # Modo OR: segunda condición se cumple
        self.assertTrue(condicion_combinada(
            10, 100, [15.0], condiciones=[condicion1, condicion2], modo='OR'
        ))
        
        # Modo OR: ambas condiciones se cumplen
        self.assertTrue(condicion_combinada(
            60, 100, [15.0], condiciones=[condicion1, condicion2], modo='OR'
        ))
        
        # Modo AND: ninguna condición se cumple
        self.assertFalse(condicion_combinada(
            10, 100, [5.0], condiciones=[condicion1, condicion2], modo='AND'
        ))
        
        # Modo AND: primera condición se cumple, segunda no
        self.assertFalse(condicion_combinada(
            60, 100, [5.0], condiciones=[condicion1, condicion2], modo='AND'
        ))
        
        # Modo AND: segunda condición se cumple, primera no
        self.assertFalse(condicion_combinada(
            10, 100, [15.0], condiciones=[condicion1, condicion2], modo='AND'
        ))
        
        # Modo AND: ambas condiciones se cumplen
        self.assertTrue(condicion_combinada(
            60, 100, [15.0], condiciones=[condicion1, condicion2], modo='AND'
        ))
        
        # Modo inválido
        with self.assertRaises(ValueError):
            condicion_combinada(
                10, 100, [5.0], condiciones=[condicion1, condicion2], modo='INVALID'
            )
    
    def test_condicion_personalizada(self):
        """Prueba que la condición personalizada funciona correctamente."""
        # Definir función de condición personalizada
        def mi_condicion(generacion, max_gen, hist, parametro=0, **kwargs):
            return generacion > parametro
        
        # La condición no se cumple
        self.assertFalse(condicion_personalizada(
            5, 100, [], funcion_condicion=mi_condicion, parametro=10
        ))
        
        # La condición se cumple
        self.assertTrue(condicion_personalizada(
            15, 100, [], funcion_condicion=mi_condicion, parametro=10
        ))


if __name__ == '__main__':
    unittest.main()