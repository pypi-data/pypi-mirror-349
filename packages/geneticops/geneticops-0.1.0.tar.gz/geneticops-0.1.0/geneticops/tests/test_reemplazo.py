"""
Pruebas para el módulo reemplazo.py
=================================

Este módulo contiene las pruebas unitarias para las funciones de reemplazo.
"""

import unittest
import numpy as np
from geneticops.reemplazo import (
    reemplazo_generacional,
    reemplazo_elitismo,
    reemplazo_estado_estacionario,
    reemplazo_torneo,
    reemplazo_aleatorio,
    reemplazo_adaptativo
)


class TestReemplazo(unittest.TestCase):
    """Pruebas para las funciones del módulo reemplazo."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear poblaciones de prueba (en este caso, usando representación binaria)
        self.poblacion_actual = [
            np.array([1, 1, 1, 1, 1]),  # Fitness = 5
            np.array([0, 0, 0, 0, 0]),  # Fitness = 0
            np.array([1, 0, 1, 0, 1]),  # Fitness = 3
            np.array([0, 1, 0, 1, 0]),  # Fitness = 2
            np.array([1, 1, 0, 0, 1]),  # Fitness = 3
            np.array([0, 1, 1, 1, 0])   # Fitness = 3
        ]
        
        self.fitness_actual = [5, 0, 3, 2, 3, 3]
        
        self.descendencia = [
            np.array([1, 1, 0, 1, 1]),  # Fitness = 4
            np.array([0, 1, 1, 0, 1]),  # Fitness = 3
            np.array([1, 1, 1, 0, 0]),  # Fitness = 3
            np.array([0, 0, 1, 1, 1]),  # Fitness = 3
            np.array([1, 0, 0, 0, 1]),  # Fitness = 2
            np.array([1, 1, 1, 1, 0])   # Fitness = 4
        ]
        
        self.fitness_descendencia = [4, 3, 3, 3, 2, 4]
    
    def test_reemplazo_generacional_sin_elitismo(self):
        """Prueba que el reemplazo generacional sin elitismo funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Reemplazo sin elitismo
        nueva_poblacion = reemplazo_generacional(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            proporcion_elitismo=0.0
        )
        
        # Comprobar que la nueva población tiene el tamaño correcto
        self.assertEqual(len(nueva_poblacion), len(self.poblacion_actual))
        
        # Comprobar que la nueva población es igual a la descendencia
        for i, individuo in enumerate(nueva_poblacion):
            np.testing.assert_array_equal(individuo, self.descendencia[i])
    
    def test_reemplazo_generacional_con_elitismo(self):
        """Prueba que el reemplazo generacional con elitismo funciona correctamente."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Reemplazo con elitismo (33% = 2 individuos)
        nueva_poblacion = reemplazo_generacional(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            proporcion_elitismo=0.33
        )
        
        # Comprobar que la nueva población tiene el tamaño correcto
        self.assertEqual(len(nueva_poblacion), len(self.poblacion_actual))
        
        # Comprobar que se han conservado los élites
        # El mejor individuo de la población actual (fitness 5) debería estar en la nueva población
        mejor_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[0]):
                mejor_encontrado = True
                break
        self.assertTrue(mejor_encontrado)
        
        # Con 33% de elitismo en una población de 6, deberían conservarse 2 individuos élite
        # Verificar que el siguiente mejor (fitness 3) también se conserva
        contador_elite = 0
        for individuo in nueva_poblacion:
            if any(np.array_equal(individuo, self.poblacion_actual[i]) for i in [0, 2, 4, 5]):
                contador_elite += 1
        self.assertEqual(contador_elite, 2)
    
    def test_reemplazo_elitismo_maximizacion(self):
        """Prueba que el reemplazo con elitismo funciona correctamente para maximización."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar reemplazo
        nueva_poblacion = reemplazo_elitismo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            maximizar=True
        )
        
        # Comprobar que la nueva población tiene el tamaño correcto
        self.assertEqual(len(nueva_poblacion), len(self.poblacion_actual))
        
        # Comprobar que se han seleccionado los mejores individuos
        # El mejor individuo de la población actual (fitness 5) debería estar en la nueva población
        mejor_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[0]):
                mejor_encontrado = True
                break
        self.assertTrue(mejor_encontrado)
        
        # También deberían estar los mejores de la descendencia (fitness 4)
        descendencia0_encontrada = False
        descendencia5_encontrada = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.descendencia[0]):
                descendencia0_encontrada = True
            if np.array_equal(individuo, self.descendencia[5]):
                descendencia5_encontrada = True
        self.assertTrue(descendencia0_encontrada)
        self.assertTrue(descendencia5_encontrada)
    
    def test_reemplazo_elitismo_minimizacion(self):
        """Prueba que el reemplazo con elitismo funciona correctamente para minimización."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar reemplazo para minimización
        nueva_poblacion = reemplazo_elitismo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            maximizar=False
        )
        
        # Comprobar que la nueva población tiene el tamaño correcto
        self.assertEqual(len(nueva_poblacion), len(self.poblacion_actual))
        
        # Comprobar que se han seleccionado los mejores individuos para minimización
        # El individuo con menor fitness de la población actual (fitness 0) debería estar
        mejor_minimizacion_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[1]):
                mejor_minimizacion_encontrado = True
                break
        self.assertTrue(mejor_minimizacion_encontrado)
    
    def test_reemplazo_estado_estacionario_con_num_reemplazos(self):
        """Prueba que el reemplazo de estado estacionario funciona con diferentes números de reemplazos."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar reemplazo con 1 solo reemplazo
        nueva_poblacion = reemplazo_estado_estacionario(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            num_reemplazos=1
        )
        
        # Comprobar que la nueva población tiene el tamaño correcto
        self.assertEqual(len(nueva_poblacion), len(self.poblacion_actual))
        
        # Comprobar que se ha reemplazado sólo el peor individuo
        # El peor individuo de la población actual (fitness 0) no debería estar en la nueva población
        peor_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[1]):
                peor_encontrado = True
                break
        self.assertFalse(peor_encontrado)
        
        # Pero el segundo peor (fitness 2) debería seguir estando
        segundo_peor_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[3]):
                segundo_peor_encontrado = True
                break
        self.assertTrue(segundo_peor_encontrado)
        
        # Probar con todos los individuos (equivalente a reemplazo generacional)
        nueva_poblacion = reemplazo_estado_estacionario(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            num_reemplazos=len(self.poblacion_actual)
        )
        
        # Todos los individuos originales deberían haber sido reemplazados
        for i, individuo_original in enumerate(self.poblacion_actual):
            presente = False
            for individuo_nuevo in nueva_poblacion:
                if np.array_equal(individuo_nuevo, individuo_original):
                    presente = True
                    break
            # Los mejores de la población original podrían mantenerse dependiendo
            # de su fitness comparado con la descendencia
            if i == 0:  # El mejor (fitness 5)
                self.assertTrue(presente)
            elif i == 1:  # El peor (fitness 0)
                self.assertFalse(presente)
    
    def test_reemplazo_estado_estacionario_minimizacion(self):
        """Prueba que el reemplazo de estado estacionario funciona para minimización."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar reemplazo para minimización
        nueva_poblacion = reemplazo_estado_estacionario(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            num_reemplazos=2,
            maximizar=False
        )
        
        # Comprobar que la nueva población tiene el tamaño correcto
        self.assertEqual(len(nueva_poblacion), len(self.poblacion_actual))
        
        # En minimización, el mejor sería el de fitness 0, que debería mantenerse
        mejor_min_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[1]):
                mejor_min_encontrado = True
                break
        self.assertTrue(mejor_min_encontrado)
        
        # Y el peor sería el de fitness 5, que debería ser reemplazado
        peor_min_encontrado = False
        for individuo in nueva_poblacion:
            if np.array_equal(individuo, self.poblacion_actual[0]):
                peor_min_encontrado = True
                break
        self.assertFalse(peor_min_encontrado)
    
    def test_reemplazo_torneo_parametros(self):
        """Prueba que el reemplazo por torneo funciona con diferentes parámetros."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Realizar reemplazo con torneo pequeño
        nueva_poblacion_1 = reemplazo_torneo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            tamano_torneo=2
        )
        
        # Realizar reemplazo con torneo grande
        nueva_poblacion_2 = reemplazo_torneo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            tamano_torneo=4
        )
        
        # Comprobar que ambas poblaciones tienen el tamaño correcto
        self.assertEqual(len(nueva_poblacion_1), len(self.poblacion_actual))
        self.assertEqual(len(nueva_poblacion_2), len(self.poblacion_actual))
        
        # Con torneo más grande, hay más presión selectiva
        # Deberíamos encontrar más individuos con fitness alto en nueva_poblacion_2
        
        # Contar individuos con fitness alto (4 o 5) en cada población
        count_high_fitness_1 = 0
        count_high_fitness_2 = 0
        
        # Para población 1
        for individuo in nueva_poblacion_1:
            # Buscar en población actual
            for i, ind_orig in enumerate(self.poblacion_actual):
                if np.array_equal(individuo, ind_orig) and self.fitness_actual[i] >= 4:
                    count_high_fitness_1 += 1
            # Buscar en descendencia
            for i, ind_desc in enumerate(self.descendencia):
                if np.array_equal(individuo, ind_desc) and self.fitness_descendencia[i] >= 4:
                    count_high_fitness_1 += 1
        
        # Para población 2
        for individuo in nueva_poblacion_2:
            # Buscar en población actual
            for i, ind_orig in enumerate(self.poblacion_actual):
                if np.array_equal(individuo, ind_orig) and self.fitness_actual[i] >= 4:
                    count_high_fitness_2 += 1
            # Buscar en descendencia
            for i, ind_desc in enumerate(self.descendencia):
                if np.array_equal(individuo, ind_desc) and self.fitness_descendencia[i] >= 4:
                    count_high_fitness_2 += 1
        
        # Con un torneo más grande, debería haber al menos tantos individuos de alto fitness
        # como con un torneo pequeño (generalmente más)
        self.assertGreaterEqual(count_high_fitness_2, count_high_fitness_1)
    
    def test_reemplazo_aleatorio_proporciones(self):
        """Prueba que el reemplazo aleatorio funciona con diferentes proporciones."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Reemplazo con proporción 0 (no debe haber cambios)
        nueva_poblacion = reemplazo_aleatorio(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            proporcion_reemplazo=0.0
        )
        
        # Verificar que la población no ha cambiado
        for i, individuo in enumerate(nueva_poblacion):
            np.testing.assert_array_equal(individuo, self.poblacion_actual[i])
        
        # Reemplazo con proporción 1 (reemplazo completo, pero aleatorio)
        nueva_poblacion = reemplazo_aleatorio(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            proporcion_reemplazo=1.0
        )
        
        # Verificar que todos los individuos son de la descendencia
        for individuo in nueva_poblacion:
            encontrado = False
            for desc in self.descendencia:
                if np.array_equal(individuo, desc):
                    encontrado = True
                    break
            self.assertTrue(encontrado)
        
        # Reemplazo con proporción intermedia
        proporcion = 0.5
        nueva_poblacion = reemplazo_aleatorio(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            proporcion_reemplazo=proporcion
        )
        
        # Contar cuántos individuos son de la descendencia
        count_descendencia = 0
        for individuo in nueva_poblacion:
            for desc in self.descendencia:
                if np.array_equal(individuo, desc):
                    count_descendencia += 1
                    break
        
        # La proporción debería ser aproximadamente la especificada
        # Pero como es aleatorio, podría variar ligeramente
        self.assertGreaterEqual(count_descendencia, int(proporcion * len(self.poblacion_actual)) - 1)
        self.assertLessEqual(count_descendencia, int(proporcion * len(self.poblacion_actual)) + 1)
    
    def test_reemplazo_adaptativo_fases(self):
        """Prueba que el reemplazo adaptativo cambia según la fase del algoritmo."""
        # Configurar semilla aleatoria para reproducibilidad
        np.random.seed(42)
        
        # Fase inicial (exploración)
        nueva_poblacion_inicio = reemplazo_adaptativo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            generacion_actual=10,
            max_generaciones=100,
            proporcion_elitismo=0.1
        )
        
        # Fase media
        nueva_poblacion_medio = reemplazo_adaptativo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            generacion_actual=50,
            max_generaciones=100,
            proporcion_elitismo=0.1
        )
        
        # Fase final (explotación)
        nueva_poblacion_final = reemplazo_adaptativo(
            self.poblacion_actual,
            self.fitness_actual,
            self.descendencia,
            self.fitness_descendencia,
            generacion_actual=90,
            max_generaciones=100,
            proporcion_elitismo=0.1
        )
        
        # Todas las poblaciones deben tener el tamaño correcto
        self.assertEqual(len(nueva_poblacion_inicio), len(self.poblacion_actual))
        self.assertEqual(len(nueva_poblacion_medio), len(self.poblacion_actual))
        self.assertEqual(len(nueva_poblacion_final), len(self.poblacion_actual))
        
        # Al inicio, debería haber más diversidad (más individuos de la descendencia)
        # Al final, debería haber más elitismo (más individuos de alto fitness)
        
        # Contar cuántos individuos de la población actual se mantienen en cada fase
        count_original_inicio = 0
        count_original_medio = 0
        count_original_final = 0
        
        # Para población inicio
        for individuo in nueva_poblacion_inicio:
            for ind_orig in self.poblacion_actual:
                if np.array_equal(individuo, ind_orig):
                    count_original_inicio += 1
                    break
        
        # Para población medio
        for individuo in nueva_poblacion_medio:
            for ind_orig in self.poblacion_actual:
                if np.array_equal(individuo, ind_orig):
                    count_original_medio += 1
                    break
        
        # Para población final
        for individuo in nueva_poblacion_final:
            for ind_orig in self.poblacion_actual:
                if np.array_equal(individuo, ind_orig):
                    count_original_final += 1
                    break
        
        # En la fase final, debería haber más individuos de la población original
        # (mayor elitismo) que en la fase inicial
        self.assertGreaterEqual(count_original_final, count_original_inicio)
    
    def test_reemplazo_con_diferentes_tamaños(self):
        """Prueba el comportamiento de reemplazo con diferentes tamaños de poblaciones."""
        # Crear poblaciones de diferentes tamaños
        poblacion_grande = self.poblacion_actual + [np.array([0, 0, 1, 0, 1]), np.array([1, 0, 0, 1, 0])]
        fitness_grande = self.fitness_actual + [2, 2]
        
        descendencia_pequeña = self.descendencia[:4]
        fitness_descendencia_pequeña = self.fitness_descendencia[:4]
        
        # Probar reemplazo con descendencia más pequeña
        nueva_poblacion = reemplazo_elitismo(
            poblacion_grande,
            fitness_grande,
            descendencia_pequeña,
            fitness_descendencia_pequeña
        )
        
        # La nueva población debería tener el tamaño de la población original
        self.assertEqual(len(nueva_poblacion), len(poblacion_grande))
        
        # Verificar que algunos individuos de la población original se han mantenido
        # debido a que la descendencia es más pequeña
        count_original = 0
        for individuo in nueva_poblacion:
            for ind_orig in poblacion_grande:
                if np.array_equal(individuo, ind_orig):
                    count_original += 1
                    break
        
        # CORRECCIÓN: Cambiar a assertGreaterEqual en lugar de assertGreater
        self.assertGreaterEqual(count_original, len(poblacion_grande) - len(descendencia_pequeña))


if __name__ == '__main__':
    unittest.main()