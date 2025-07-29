"""
Pruebas para el módulo poblacion.py
=================================

Este módulo contiene las pruebas unitarias para las funciones de inicialización
y manejo de poblaciones.
"""

import unittest
import numpy as np
from geneticops.poblacion import (
    inicializar_poblacion_binaria,
    inicializar_poblacion_real,
    inicializar_poblacion_permutacion,
    inicializar_poblacion_desde_semilla,
    evaluar_poblacion
)


class TestPoblacion(unittest.TestCase):
    """Pruebas para las funciones del módulo poblacion."""
    
    def test_inicializar_poblacion_binaria(self):
        """Prueba que la inicialización de población binaria funciona correctamente."""
        tamano_poblacion = 10
        longitud_individuo = 5
        
        # Inicializar población
        poblacion = inicializar_poblacion_binaria(tamano_poblacion, longitud_individuo)
        
        # Comprobar que se ha creado el número correcto de individuos
        self.assertEqual(len(poblacion), tamano_poblacion)
        
        # Comprobar que cada individuo tiene la longitud correcta
        for individuo in poblacion:
            self.assertEqual(len(individuo), longitud_individuo)
        
        # Comprobar que todos los genes son 0 o 1
        for individuo in poblacion:
            for gen in individuo:
                self.assertIn(gen, [0, 1])
    
    def test_inicializar_poblacion_real(self):
        """Prueba que la inicialización de población real funciona correctamente."""
        tamano_poblacion = 10
        longitud_individuo = 5
        limite_inferior = -5.0
        limite_superior = 5.0
        
        # Inicializar población
        poblacion = inicializar_poblacion_real(
            tamano_poblacion, 
            longitud_individuo, 
            limite_inferior, 
            limite_superior
        )
        
        # Comprobar que se ha creado el número correcto de individuos
        self.assertEqual(len(poblacion), tamano_poblacion)
        
        # Comprobar que cada individuo tiene la longitud correcta
        for individuo in poblacion:
            self.assertEqual(len(individuo), longitud_individuo)
        
        # Comprobar que todos los genes están dentro de los límites
        for individuo in poblacion:
            for gen in individuo:
                self.assertGreaterEqual(gen, limite_inferior)
                self.assertLessEqual(gen, limite_superior)
    
    def test_inicializar_poblacion_permutacion(self):
        """Prueba que la inicialización de población de permutación funciona correctamente."""
        tamano_poblacion = 10
        longitud_individuo = 5
        
        # Inicializar población
        poblacion = inicializar_poblacion_permutacion(tamano_poblacion, longitud_individuo)
        
        # Comprobar que se ha creado el número correcto de individuos
        self.assertEqual(len(poblacion), tamano_poblacion)
        
        # Comprobar que cada individuo tiene la longitud correcta
        for individuo in poblacion:
            self.assertEqual(len(individuo), longitud_individuo)
        
        # Comprobar que cada individuo es una permutación válida
        for individuo in poblacion:
            # Ordenar los valores y comparar con el rango esperado
            valores_ordenados = sorted(individuo)
            valores_esperados = list(range(longitud_individuo))
            np.testing.assert_array_equal(valores_ordenados, valores_esperados)
    
    def test_inicializar_poblacion_desde_semilla(self):
        """Prueba que la inicialización desde semilla funciona correctamente."""
        tamano_poblacion = 10
        longitud_individuo = 5
        semilla = np.array([1, 0, 1, 0, 1])
        tasa_variacion = 0.2
        
        # Inicializar población
        poblacion = inicializar_poblacion_desde_semilla(
            tamano_poblacion, 
            longitud_individuo, 
            semilla, 
            tasa_variacion
        )
        
        # Comprobar que se ha creado el número correcto de individuos
        self.assertEqual(len(poblacion), tamano_poblacion)
        
        # Comprobar que cada individuo tiene la longitud correcta
        for individuo in poblacion:
            self.assertEqual(len(individuo), longitud_individuo)
        
        # Comprobar que el primer individuo es igual a la semilla
        np.testing.assert_array_equal(poblacion[0], semilla)
        
        # Comprobar que los demás individuos son variaciones de la semilla
        for i in range(1, tamano_poblacion):
            # No debería ser exactamente igual a la semilla
            self.assertFalse(np.array_equal(poblacion[i], semilla))
            
            # Debería tener al menos un gen diferente
            diferencias = np.sum(poblacion[i] != semilla)
            self.assertGreater(diferencias, 0)
            
            # El número de diferencias no debería ser mayor que el esperado según la tasa
            max_diferencias = int(longitud_individuo * tasa_variacion) + 1  # +1 por posible redondeo
            self.assertLessEqual(diferencias, max_diferencias)
    
    def test_evaluar_poblacion(self):
        """Prueba que la evaluación de la población funciona correctamente."""
        # Crear una población de prueba
        poblacion = [
            np.array([1, 1, 1, 1, 1]),  # Suma = 5
            np.array([0, 0, 0, 0, 0]),  # Suma = 0
            np.array([1, 0, 1, 0, 1])   # Suma = 3
        ]
        
        # Función de fitness: suma de los genes
        funcion_fitness = lambda x: np.sum(x)
        
        # Evaluar la población
        fitness_valores = evaluar_poblacion(poblacion, funcion_fitness)
        
        # Comprobar que los valores de fitness son correctos
        self.assertEqual(fitness_valores[0], 5)
        self.assertEqual(fitness_valores[1], 0)
        self.assertEqual(fitness_valores[2], 3)
    
    def test_error_longitud_semilla(self):
        """Prueba que se lanza un error si la longitud de la semilla no coincide."""
        tamano_poblacion = 10
        longitud_individuo = 5
        semilla = np.array([1, 0, 1])  # Longitud incorrecta
        
        # Debería lanzar un ValueError
        with self.assertRaises(ValueError):
            inicializar_poblacion_desde_semilla(tamano_poblacion, longitud_individuo, semilla)


if __name__ == '__main__':
    unittest.main()