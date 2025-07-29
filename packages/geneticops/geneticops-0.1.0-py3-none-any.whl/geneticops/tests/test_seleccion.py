"""
Pruebas para el módulo seleccion.py
=================================

Este módulo contiene las pruebas unitarias para las funciones de selección.
"""

import unittest
import numpy as np
from geneticops.seleccion import (
    seleccion_ruleta,
    seleccion_torneo,
    seleccion_ranking,
    seleccion_truncamiento,
    seleccion_estocastica_universal
)


class TestSeleccion(unittest.TestCase):
    """Pruebas para las funciones del módulo seleccion."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear una población de prueba
        self.poblacion = [
            np.array([1, 1, 1, 1, 1]),  # Fitness = 5
            np.array([0, 0, 0, 0, 0]),  # Fitness = 0
            np.array([1, 0, 1, 0, 1]),  # Fitness = 3
            np.array([0, 1, 0, 1, 0]),  # Fitness = 2
            np.array([1, 1, 0, 0, 1])   # Fitness = 3
        ]
        
        # Valores de fitness correspondientes
        self.fitness = [5, 0, 3, 2, 3]
        
        # Número de individuos a seleccionar
        self.num_seleccionados = 3
    
    def test_seleccion_ruleta(self):
        """Prueba que la selección por ruleta funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Seleccionar individuos usando ruleta
        seleccionados, fitness_seleccionados = seleccion_ruleta(
            self.poblacion, 
            self.fitness, 
            self.num_seleccionados
        )
        
        # Comprobar que se ha seleccionado el número correcto de individuos
        self.assertEqual(len(seleccionados), self.num_seleccionados)
        self.assertEqual(len(fitness_seleccionados), self.num_seleccionados)
        
        # Comprobar que todos los individuos seleccionados tienen el fitness correcto
        for i, individuo in enumerate(seleccionados):
            idx = None
            for j, ind_original in enumerate(self.poblacion):
                if np.array_equal(individuo, ind_original):
                    idx = j
                    break
            if idx is not None:
                self.assertEqual(fitness_seleccionados[i], self.fitness[idx])
        
        # Comprobar que la selección funciona para valores negativos
        fitness_negativos = [-10, -5, -20, -15, -8]
        seleccionados_neg, fitness_seleccionados_neg = seleccion_ruleta(
            self.poblacion, 
            fitness_negativos, 
            self.num_seleccionados,
            maximizar=False
        )
        self.assertEqual(len(seleccionados_neg), self.num_seleccionados)
    
    def test_seleccion_torneo(self):
        """Prueba que la selección por torneo funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Seleccionar individuos usando torneo
        seleccionados, fitness_seleccionados = seleccion_torneo(
            self.poblacion, 
            self.fitness, 
            self.num_seleccionados,
            tamano_torneo=2
        )
        
        # Comprobar que se ha seleccionado el número correcto de individuos
        self.assertEqual(len(seleccionados), self.num_seleccionados)
        self.assertEqual(len(fitness_seleccionados), self.num_seleccionados)
        
        # Comprobar que todos los individuos seleccionados tienen el fitness correcto
        for i, individuo in enumerate(seleccionados):
            idx = None
            for j, ind_original in enumerate(self.poblacion):
                if np.array_equal(individuo, ind_original):
                    idx = j
                    break
            if idx is not None:
                self.assertEqual(fitness_seleccionados[i], self.fitness[idx])
        
        # Comprobar que la selección funciona para minimización
        seleccionados_min, fitness_seleccionados_min = seleccion_torneo(
            self.poblacion, 
            self.fitness, 
            self.num_seleccionados,
            tamano_torneo=2,
            maximizar=False
        )
        self.assertEqual(len(seleccionados_min), self.num_seleccionados)
    
    def test_seleccion_ranking(self):
        """Prueba que la selección por ranking funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Seleccionar individuos usando ranking
        seleccionados, fitness_seleccionados = seleccion_ranking(
            self.poblacion, 
            self.fitness, 
            self.num_seleccionados,
            presion_selectiva=1.5
        )
        
        # Comprobar que se ha seleccionado el número correcto de individuos
        self.assertEqual(len(seleccionados), self.num_seleccionados)
        self.assertEqual(len(fitness_seleccionados), self.num_seleccionados)
        
        # Comprobar que todos los individuos seleccionados tienen el fitness correcto
        for i, individuo in enumerate(seleccionados):
            idx = None
            for j, ind_original in enumerate(self.poblacion):
                if np.array_equal(individuo, ind_original):
                    idx = j
                    break
            if idx is not None:
                self.assertEqual(fitness_seleccionados[i], self.fitness[idx])
    
    def test_seleccion_truncamiento(self):
        """Prueba que la selección por truncamiento funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Seleccionar individuos usando truncamiento
        seleccionados, fitness_seleccionados = seleccion_truncamiento(
            self.poblacion, 
            self.fitness, 
            self.num_seleccionados,
            tasa_truncamiento=0.6
        )
        
        # Comprobar que se ha seleccionado el número correcto de individuos
        self.assertEqual(len(seleccionados), self.num_seleccionados)
        self.assertEqual(len(fitness_seleccionados), self.num_seleccionados)
        
        # Comprobar que todos los individuos seleccionados tienen el fitness correcto
        for i, individuo in enumerate(seleccionados):
            idx = None
            for j, ind_original in enumerate(self.poblacion):
                if np.array_equal(individuo, ind_original):
                    idx = j
                    break
            if idx is not None:
                self.assertEqual(fitness_seleccionados[i], self.fitness[idx])
        
        # Verificar que se están seleccionando los mejores individuos
        # En este caso, deberíamos tener más probabilidades de seleccionar individuos
        # con fitness 5, 3 o 3
        indices_seleccionados = []
        for individuo in seleccionados:
            for i, ind_original in enumerate(self.poblacion):
                if np.array_equal(individuo, ind_original):
                    indices_seleccionados.append(i)
                    break
        
        # Con tasa_truncamiento=0.6, se consideran los 3 mejores individuos
        # Esos son los índices 0, 2 y 4 (con fitness 5, 3 y 3 respectivamente)
        for idx in indices_seleccionados:
            self.assertIn(idx, [0, 2, 4])
    
    def test_seleccion_estocastica_universal(self):
        """Prueba que la selección estocástica universal funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Seleccionar individuos usando SUS
        seleccionados, fitness_seleccionados = seleccion_estocastica_universal(
            self.poblacion, 
            self.fitness, 
            self.num_seleccionados
        )
        
        # Comprobar que se ha seleccionado el número correcto de individuos
        self.assertEqual(len(seleccionados), self.num_seleccionados)
        self.assertEqual(len(fitness_seleccionados), self.num_seleccionados)
        
        # Comprobar que todos los individuos seleccionados tienen el fitness correcto
        for i, individuo in enumerate(seleccionados):
            idx = None
            for j, ind_original in enumerate(self.poblacion):
                if np.array_equal(individuo, ind_original):
                    idx = j
                    break
            if idx is not None:
                self.assertEqual(fitness_seleccionados[i], self.fitness[idx])


if __name__ == '__main__':
    unittest.main()