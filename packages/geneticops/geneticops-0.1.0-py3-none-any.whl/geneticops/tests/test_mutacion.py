"""
Pruebas para el módulo mutacion.py
================================

Este módulo contiene las pruebas unitarias para las funciones de mutación.
"""

import unittest
import numpy as np
from geneticops.mutacion import (
    mutacion_bit_flip,
    mutacion_uniforme,
    mutacion_gaussiana,
    mutacion_swap,
    mutacion_inversion,
    mutacion_insertion,
    mutacion_scramble,
    mutacion_adaptativa
)


class TestMutacion(unittest.TestCase):
    """Pruebas para las funciones del módulo mutacion."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Individuos para representación binaria
        self.individuo_bin = np.array([1, 1, 1, 1, 1])
        
        # Individuos para representación real
        self.individuo_real = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        
        # Individuos para representación de permutación
        self.individuo_perm = np.array([0, 1, 2, 3, 4])
        
        # Probabilidad de mutación
        self.prob_mutacion = 1.0  # 100% para garantizar que ocurra la mutación
    
    def test_mutacion_bit_flip(self):
        """Prueba que la mutación bit-flip funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación
        individuo_mutado = mutacion_bit_flip(self.individuo_bin, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_bin))
        
        # Con probabilidad 1.0, todos los bits deberían cambiar
        np.testing.assert_array_equal(individuo_mutado, 1 - self.individuo_bin)
        
        # Prueba con probabilidad menor
        individuo_mutado = mutacion_bit_flip(self.individuo_bin, 0.5)
        
        # Comprobar que sólo algunos bits han cambiado
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_bin))
        self.assertFalse(np.array_equal(individuo_mutado, 1 - self.individuo_bin))
        
        # Comprobar que siguen siendo bits
        for gen in individuo_mutado:
            self.assertIn(gen, [0, 1])
        
        # Prueba con un individuo no binario (debería advertir pero no mutar)
        with self.assertWarns(Warning):
            individuo_mutado = mutacion_bit_flip(self.individuo_real, self.prob_mutacion)
            np.testing.assert_array_equal(individuo_mutado, self.individuo_real)
    
    def test_mutacion_uniforme(self):
        """Prueba que la mutación uniforme funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación con límites por defecto [0, 1]
        individuo_mutado = mutacion_uniforme(self.individuo_real, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_real))
        
        # Con probabilidad 1.0, todos los genes deberían cambiar
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_real))
        
        # Comprobar que los nuevos valores están en el rango [0, 1]
        for gen in individuo_mutado:
            self.assertGreaterEqual(gen, 0.0)
            self.assertLessEqual(gen, 1.0)
        
        # Prueba con límites personalizados
        limite_inferior = -10.0
        limite_superior = 10.0
        individuo_mutado = mutacion_uniforme(
            self.individuo_real, 
            self.prob_mutacion,
            limite_inferior=limite_inferior,
            limite_superior=limite_superior
        )
        
        # Comprobar que los nuevos valores están en el rango personalizado
        for gen in individuo_mutado:
            self.assertGreaterEqual(gen, limite_inferior)
            self.assertLessEqual(gen, limite_superior)
    
    def test_mutacion_gaussiana(self):
        """Prueba que la mutación gaussiana funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación con parámetros por defecto
        individuo_mutado = mutacion_gaussiana(self.individuo_real, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_real))
        
        # Con probabilidad 1.0, todos los genes deberían cambiar
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_real))
        
        # Es difícil comprobar los valores exactos debido a la naturaleza aleatoria,
        # pero podemos verificar que los cambios son relativamente pequeños
        for i, gen in enumerate(individuo_mutado):
            self.assertLess(abs(gen - self.individuo_real[i]), 0.5)  # Con desviación 0.1, es muy improbable tener diferencias > 0.5
        
        # Prueba con parámetros personalizados
        media = 5.0
        desviacion = 2.0
        individuo_original = np.zeros(5)  # Iniciar en ceros para facilitar la comprobación
        individuo_mutado = mutacion_gaussiana(
            individuo_original, 
            self.prob_mutacion,
            media=media,
            desviacion=desviacion
        )
        
        # Los valores deberían estar cerca de la media (aproximadamente en el rango [1, 9])
        for gen in individuo_mutado:
            self.assertGreater(gen, media - 3 * desviacion)
            self.assertLess(gen, media + 3 * desviacion)
    
    def test_mutacion_swap(self):
        """Prueba que la mutación swap funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación
        individuo_mutado = mutacion_swap(self.individuo_perm, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_perm))
        
        # Comprobar que el individuo sigue siendo una permutación válida
        self.assertEqual(set(individuo_mutado), set(self.individuo_perm))
        
        # Con probabilidad 1.0, debería haber ocurrido al menos un swap
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_perm))
    
    def test_mutacion_inversion(self):
        """Prueba que la mutación por inversión funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación
        individuo_mutado = mutacion_inversion(self.individuo_perm, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_perm))
        
        # Comprobar que el individuo sigue siendo una permutación válida
        self.assertEqual(set(individuo_mutado), set(self.individuo_perm))
        
        # Con probabilidad 1.0, debería haber ocurrido inversión
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_perm))
    
    def test_mutacion_insertion(self):
        """Prueba que la mutación por inserción funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación
        individuo_mutado = mutacion_insertion(self.individuo_perm, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_perm))
        
        # Comprobar que el individuo sigue siendo una permutación válida
        self.assertEqual(set(individuo_mutado), set(self.individuo_perm))
        
        # Con probabilidad 1.0, debería haber ocurrido inserción
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_perm))
    
    def test_mutacion_scramble(self):
        """Prueba que la mutación por barajado funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación
        individuo_mutado = mutacion_scramble(self.individuo_perm, self.prob_mutacion)
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_perm))
        
        # Comprobar que el individuo sigue siendo una permutación válida
        self.assertEqual(set(individuo_mutado), set(self.individuo_perm))
        
        # Con probabilidad 1.0, debería haber ocurrido barajado
        self.assertFalse(np.array_equal(individuo_mutado, self.individuo_perm))
    
    def test_mutacion_adaptativa(self):
        """Prueba que la mutación adaptativa funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar mutación con diferentes tipos de genoma
        
        # Binario
        individuo_mutado = mutacion_adaptativa(
            self.individuo_bin, 
            self.prob_mutacion,
            generacion_actual=50,
            max_generaciones=100,
            tipo_genoma='binario'
        )
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_bin))
        
        # Comprobar que siguen siendo bits
        for gen in individuo_mutado:
            self.assertIn(gen, [0, 1])
        
        # Real
        individuo_mutado = mutacion_adaptativa(
            self.individuo_real, 
            self.prob_mutacion,
            generacion_actual=50,
            max_generaciones=100,
            tipo_genoma='real'
        )
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_real))
        
        # Permutación
        individuo_mutado = mutacion_adaptativa(
            self.individuo_perm, 
            self.prob_mutacion,
            generacion_actual=50,
            max_generaciones=100,
            tipo_genoma='permutacion'
        )
        
        # Comprobar que el individuo tiene la longitud correcta
        self.assertEqual(len(individuo_mutado), len(self.individuo_perm))
        
        # Comprobar que el individuo sigue siendo una permutación válida
        self.assertEqual(set(individuo_mutado), set(self.individuo_perm))
        
        # Prueba con tipo de genoma no reconocido
        with self.assertRaises(ValueError):
            mutacion_adaptativa(
                self.individuo_bin, 
                self.prob_mutacion,
                generacion_actual=50,
                max_generaciones=100,
                tipo_genoma='tipo_invalido'
            )


if __name__ == '__main__':
    unittest.main()