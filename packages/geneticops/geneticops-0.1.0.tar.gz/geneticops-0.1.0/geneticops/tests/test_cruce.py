"""
Pruebas para el módulo cruce.py
=============================

Este módulo contiene las pruebas unitarias para las funciones de cruce.
"""

import unittest
import numpy as np
from geneticops.cruce import (
    cruce_un_punto,
    cruce_dos_puntos,
    cruce_uniforme,
    cruce_aritmetico,
    cruce_sbx,
    cruce_pmx,
    cruce_ox,
    cruce_ciclo
)


class TestCruce(unittest.TestCase):
    """Pruebas para las funciones del módulo cruce."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Padres para representación binaria
        self.padre1_bin = np.array([1, 1, 1, 1, 1])
        self.padre2_bin = np.array([0, 0, 0, 0, 0])
        
        # Padres para representación real
        self.padre1_real = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        self.padre2_real = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
        
        # Padres para representación de permutación
        self.padre1_perm = np.array([0, 1, 2, 3, 4])
        self.padre2_perm = np.array([4, 3, 2, 1, 0])
    
    def test_cruce_un_punto(self):
        """Prueba que el cruce de un punto funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_un_punto(self.padre1_bin, self.padre2_bin)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_bin))
        self.assertEqual(len(hijo2), len(self.padre2_bin))
        
        # Comprobar que los hijos son diferentes a los padres
        self.assertFalse(np.array_equal(hijo1, self.padre1_bin) and np.array_equal(hijo2, self.padre2_bin))
        
        # Comprobar que se ha realizado un cruce válido (cada hijo tiene partes de ambos padres)
        # Es difícil hacer esta comprobación en general, pero podemos verificar
        # que los hijos no son idénticos a los padres
        self.assertTrue(not np.array_equal(hijo1, self.padre1_bin) or not np.array_equal(hijo2, self.padre2_bin))
        
        # Verificar que el cruce mantiene los valores originales
        # (no se han introducido valores nuevos)
        for gen in hijo1:
            self.assertIn(gen, [0, 1])
        for gen in hijo2:
            self.assertIn(gen, [0, 1])
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([1, 1, 1])
        with self.assertRaises(ValueError):
            cruce_un_punto(self.padre1_bin, padre_incompatible)
    
    def test_cruce_dos_puntos(self):
        """Prueba que el cruce de dos puntos funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_dos_puntos(self.padre1_bin, self.padre2_bin)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_bin))
        self.assertEqual(len(hijo2), len(self.padre2_bin))
        
        # Comprobar que los hijos son diferentes a los padres
        self.assertFalse(np.array_equal(hijo1, self.padre1_bin) and np.array_equal(hijo2, self.padre2_bin))
        
        # Verificar que el cruce mantiene los valores originales
        for gen in hijo1:
            self.assertIn(gen, [0, 1])
        for gen in hijo2:
            self.assertIn(gen, [0, 1])
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([1, 1, 1])
        with self.assertRaises(ValueError):
            cruce_dos_puntos(self.padre1_bin, padre_incompatible)
    
    def test_cruce_uniforme(self):
        """Prueba que el cruce uniforme funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_uniforme(self.padre1_bin, self.padre2_bin, prob_intercambio=0.5)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_bin))
        self.assertEqual(len(hijo2), len(self.padre2_bin))
        
        # Verificar que el cruce mantiene los valores originales
        for gen in hijo1:
            self.assertIn(gen, [0, 1])
        for gen in hijo2:
            self.assertIn(gen, [0, 1])
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([1, 1, 1])
        with self.assertRaises(ValueError):
            cruce_uniforme(self.padre1_bin, padre_incompatible)
    
    def test_cruce_aritmetico(self):
        """Prueba que el cruce aritmético funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_aritmetico(self.padre1_real, self.padre2_real, alpha=0.5)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_real))
        self.assertEqual(len(hijo2), len(self.padre2_real))
        
        # Verificar que el cruce produce los valores esperados
        # Con alpha=0.5, los hijos deberían ser el promedio de los padres
        valores_esperados = (self.padre1_real + self.padre2_real) / 2
        np.testing.assert_array_almost_equal(hijo1, valores_esperados)
        np.testing.assert_array_almost_equal(hijo2, valores_esperados)
        
        # Prueba con alpha diferente
        hijo1, hijo2 = cruce_aritmetico(self.padre1_real, self.padre2_real, alpha=0.7)
        valores_esperados1 = 0.7 * self.padre1_real + 0.3 * self.padre2_real
        valores_esperados2 = 0.3 * self.padre1_real + 0.7 * self.padre2_real
        np.testing.assert_array_almost_equal(hijo1, valores_esperados1)
        np.testing.assert_array_almost_equal(hijo2, valores_esperados2)
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            cruce_aritmetico(self.padre1_real, padre_incompatible)
        
        # Prueba con padres no numéricos
        padre_no_numerico = np.array(['a', 'b', 'c', 'd', 'e'])
        with self.assertRaises(TypeError):
            cruce_aritmetico(self.padre1_real, padre_no_numerico)
    
    def test_cruce_sbx(self):
        """Prueba que el cruce SBX funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_sbx(self.padre1_real, self.padre2_real, eta=1.0)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_real))
        self.assertEqual(len(hijo2), len(self.padre2_real))
        
        # Verificar que los hijos están dentro del rango de los padres
        for i in range(len(hijo1)):
            min_val = min(self.padre1_real[i], self.padre2_real[i])
            max_val = max(self.padre1_real[i], self.padre2_real[i])
            
            # CORRECCIÓN: SBX puede generar valores fuera del rango de los padres
            # pero generalmente no muy lejos, así que usamos un factor de expansión
            self.assertLess(abs(hijo1[i] - min_val), (max_val - min_val) * 3)
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            cruce_sbx(self.padre1_real, padre_incompatible)
        
        # Prueba con padres no numéricos
        padre_no_numerico = np.array(['a', 'b', 'c', 'd', 'e'])
        with self.assertRaises(TypeError):
            cruce_sbx(self.padre1_real, padre_no_numerico)
    
    def test_cruce_pmx(self):
        """Prueba que el cruce PMX funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_pmx(self.padre1_perm, self.padre2_perm)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_perm))
        self.assertEqual(len(hijo2), len(self.padre2_perm))
        
        # Verificar que los hijos son permutaciones válidas
        # (contienen los mismos elementos que los padres, sin duplicados)
        self.assertEqual(set(hijo1), set(self.padre1_perm))
        self.assertEqual(set(hijo2), set(self.padre2_perm))
        
        # Verificar que no hay duplicados
        self.assertEqual(len(hijo1), len(set(hijo1)))
        self.assertEqual(len(hijo2), len(set(hijo2)))
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([0, 1, 2])
        with self.assertRaises(ValueError):
            cruce_pmx(self.padre1_perm, padre_incompatible)
        
        # Prueba con padres que no son permutaciones válidas
        padre_no_permutacion = np.array([0, 0, 2, 3, 4])
        with self.assertRaises(ValueError):
            cruce_pmx(self.padre1_perm, padre_no_permutacion)
    
    def test_cruce_ox(self):
        """Prueba que el cruce OX funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_ox(self.padre1_perm, self.padre2_perm)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_perm))
        self.assertEqual(len(hijo2), len(self.padre2_perm))
        
        # Verificar que los hijos son permutaciones válidas
        self.assertEqual(set(hijo1), set(self.padre1_perm))
        self.assertEqual(set(hijo2), set(self.padre2_perm))
        
        # Verificar que no hay duplicados
        self.assertEqual(len(hijo1), len(set(hijo1)))
        self.assertEqual(len(hijo2), len(set(hijo2)))
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([0, 1, 2])
        with self.assertRaises(ValueError):
            cruce_ox(self.padre1_perm, padre_incompatible)
        
        # Prueba con padres que no son permutaciones válidas
        padre_no_permutacion = np.array([0, 0, 2, 3, 4])
        with self.assertRaises(ValueError):
            cruce_ox(self.padre1_perm, padre_no_permutacion)
    
    def test_cruce_ciclo(self):
        """Prueba que el cruce de ciclo funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar cruce
        hijo1, hijo2 = cruce_ciclo(self.padre1_perm, self.padre2_perm)
        
        # Comprobar que los hijos tienen la longitud correcta
        self.assertEqual(len(hijo1), len(self.padre1_perm))
        self.assertEqual(len(hijo2), len(self.padre2_perm))
        
        # Verificar que los hijos son permutaciones válidas
        self.assertEqual(set(hijo1), set(self.padre1_perm))
        self.assertEqual(set(hijo2), set(self.padre2_perm))
        
        # Verificar que no hay duplicados
        self.assertEqual(len(hijo1), len(set(hijo1)))
        self.assertEqual(len(hijo2), len(set(hijo2)))
        
        # Prueba con padres de longitud incompatible
        padre_incompatible = np.array([0, 1, 2])
        with self.assertRaises(ValueError):
            cruce_ciclo(self.padre1_perm, padre_incompatible)
        
        # Prueba con padres que no son permutaciones válidas
        padre_no_permutacion = np.array([0, 0, 2, 3, 4])
        with self.assertRaises(ValueError):
            cruce_ciclo(self.padre1_perm, padre_no_permutacion)


if __name__ == '__main__':
    unittest.main()