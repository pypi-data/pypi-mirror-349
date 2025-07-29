"""
Pruebas para el módulo utilidades.py
==================================

Este módulo contiene las pruebas unitarias para las funciones de utilidad.
"""

import unittest
import numpy as np
import os
import tempfile
from geneticops.utilidades import (
    calcular_estadisticas_poblacion,
    calcular_diversidad_poblacion,
    decodificar_binario_a_real,
    codificar_real_a_binario,
    CacheDecorador
)


class TestUtilidades(unittest.TestCase):
    """Pruebas para las funciones del módulo utilidades."""
    
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
    
    def test_calcular_estadisticas_poblacion(self):
        """Prueba que el cálculo de estadísticas de población funciona correctamente."""
        # Calcular estadísticas
        estadisticas = calcular_estadisticas_poblacion(self.poblacion, self.fitness)
        
        # Comprobar que se han calculado todas las estadísticas
        self.assertIn('mejor', estadisticas)
        self.assertIn('peor', estadisticas)
        self.assertIn('promedio', estadisticas)
        self.assertIn('mediana', estadisticas)
        self.assertIn('desviacion', estadisticas)
        
        # Comprobar que los valores son correctos
        self.assertEqual(estadisticas['mejor'], 5)
        self.assertEqual(estadisticas['peor'], 0)
        self.assertEqual(estadisticas['promedio'], 2.6)
        self.assertEqual(estadisticas['mediana'], 3)
        # CORRECCIÓN: Ajustar el valor esperado para la desviación estándar
        self.assertAlmostEqual(estadisticas['desviacion'], 1.62, places=2)
        
        # Probar con una población vacía
        estadisticas_vacias = calcular_estadisticas_poblacion([], [])
        self.assertIsNone(estadisticas_vacias['mejor'])
        self.assertIsNone(estadisticas_vacias['peor'])
        self.assertIsNone(estadisticas_vacias['promedio'])
        self.assertIsNone(estadisticas_vacias['mediana'])
        self.assertIsNone(estadisticas_vacias['desviacion'])
    
    def test_calcular_diversidad_poblacion(self):
        """Prueba que el cálculo de diversidad de población funciona correctamente."""
        # Calcular diversidad con diferentes métricas
        
        # Hamming
        diversidad_hamming = calcular_diversidad_poblacion(self.poblacion, 'hamming')
        self.assertGreater(diversidad_hamming, 0)
        self.assertLessEqual(diversidad_hamming, 1)
        
        # Euclidiana
        diversidad_euclidiana = calcular_diversidad_poblacion(self.poblacion, 'euclidiana')
        self.assertGreater(diversidad_euclidiana, 0)
        
        # Coseno
        diversidad_coseno = calcular_diversidad_poblacion(self.poblacion, 'coseno')
        self.assertGreater(diversidad_coseno, 0)
        self.assertLessEqual(diversidad_coseno, 1)
        
        # Métrica inválida
        with self.assertRaises(ValueError):
            calcular_diversidad_poblacion(self.poblacion, 'metrica_invalida')
        
        # Población vacía
        self.assertEqual(calcular_diversidad_poblacion([], 'hamming'), 0.0)
        
        # Población con un solo individuo
        self.assertEqual(calcular_diversidad_poblacion([self.poblacion[0]], 'hamming'), 0.0)
    
    def test_decodificar_binario_a_real(self):
        """Prueba que la decodificación de binario a real funciona correctamente."""
        # Genoma binario de ejemplo (4 bits por variable)
        individuo_binario = np.array([1, 0, 1, 1, 0, 0, 1, 0])
        # Con 4 bits, los valores decimales son 11 (1011) y 2 (0010)
        
        # Límites para las variables
        limites = [(0, 10), (0, 20)]
        
        # Decodificar
        valores_reales = decodificar_binario_a_real(individuo_binario, limites, bits_por_variable=4)
        
        # Comprobar que se ha decodificado correctamente
        self.assertEqual(len(valores_reales), 2)
        # 1011 en binario es 11, que normalizado a [0, 10] es 11/15 * 10 = 7.33
        self.assertAlmostEqual(valores_reales[0], 11 / 15 * 10, places=2)
        # 0010 en binario es 2, que normalizado a [0, 20] es 2/15 * 20 = 2.67
        self.assertAlmostEqual(valores_reales[1], 2 / 15 * 20, places=2)
        
        # Probar con bits_por_variable=None (cálculo automático)
        valores_reales_auto = decodificar_binario_a_real(individuo_binario, limites)
        self.assertEqual(len(valores_reales_auto), 2)
        
        # Probar con longitud incompatible
        with self.assertRaises(ValueError):
            decodificar_binario_a_real(individuo_binario, limites, bits_por_variable=3)
        
        # Probar con un individuo no binario
        individuo_no_binario = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        with self.assertRaises(ValueError):
            decodificar_binario_a_real(individuo_no_binario, limites)
    
    def test_codificar_real_a_binario(self):
        """Prueba que la codificación de real a binario funciona correctamente."""
        # Valores reales de ejemplo
        individuo_real = np.array([7.33, 2.67])
        
        # Límites para las variables
        limites = [(0, 10), (0, 20)]
        
        # Codificar
        individuo_binario = codificar_real_a_binario(individuo_real, limites, bits_por_variable=4)
        
        # Comprobar que se ha codificado correctamente
        self.assertEqual(len(individuo_binario), 8)  # 4 bits por variable, 2 variables
        
        # Decodificar de nuevo para comprobar
        valores_reales = decodificar_binario_a_real(individuo_binario, limites, bits_por_variable=4)
        
        # Los valores deberían ser aproximadamente los mismos
        self.assertAlmostEqual(valores_reales[0], individuo_real[0], delta=0.7)  # Delta mayor debido a la baja precisión con 4 bits
        self.assertAlmostEqual(valores_reales[1], individuo_real[1], delta=1.4)
        
        # Probar con longitud incompatible
        individuo_real_incompatible = np.array([7.33, 2.67, 5.0])
        with self.assertRaises(ValueError):
            codificar_real_a_binario(individuo_real_incompatible, limites, bits_por_variable=4)
    
    def test_cache_decorador(self):
        """Prueba que el decorador de caché funciona correctamente."""
        # Definir una función costosa de ejemplo
        @CacheDecorador
        def funcion_costosa(individuo):
            return np.sum(individuo)
        
        # Crear individuos de prueba
        ind1 = np.array([1, 2, 3, 4, 5])
        ind2 = np.array([5, 4, 3, 2, 1])
        
        # Primera llamada (no cacheada)
        resultado1 = funcion_costosa(ind1)
        self.assertEqual(resultado1, 15)
        
        # Segunda llamada (no cacheada)
        resultado2 = funcion_costosa(ind2)
        self.assertEqual(resultado2, 15)
        
        # Tercera llamada (cacheada)
        resultado3 = funcion_costosa(ind1)
        self.assertEqual(resultado3, 15)
        
        # Comprobar estadísticas de la caché
        estadisticas = funcion_costosa.estadisticas()
        self.assertEqual(estadisticas['llamadas_totales'], 3)
        self.assertEqual(estadisticas['aciertos_cache'], 1)
        self.assertEqual(estadisticas['tamanio_cache'], 2)
        
        # Limpiar caché
        funcion_costosa.limpiar_cache()
        
        # Comprobar que la caché está vacía
        estadisticas = funcion_costosa.estadisticas()
        self.assertEqual(estadisticas['tamanio_cache'], 0)


if __name__ == '__main__':
    unittest.main()