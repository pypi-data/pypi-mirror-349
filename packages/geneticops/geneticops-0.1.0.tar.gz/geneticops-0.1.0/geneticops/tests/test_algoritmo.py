"""
Pruebas para el módulo algoritmo.py
=================================

Este módulo contiene las pruebas unitarias para la clase AlgoritmoGenetico.
"""

import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from geneticops.algoritmo import AlgoritmoGenetico
from geneticops.poblacion import inicializar_poblacion_binaria
from geneticops.seleccion import seleccion_ruleta
from geneticops.cruce import cruce_un_punto
from geneticops.mutacion import mutacion_bit_flip
from geneticops.reemplazo import reemplazo_elitismo
from geneticops.condiciones_parada import condicion_max_generaciones


class TestAlgoritmoGenetico(unittest.TestCase):
    """Pruebas para la clase AlgoritmoGenetico."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Función de fitness simple: suma de los genes
        self.funcion_fitness = lambda x: np.sum(x)
        
        # Parámetros para el algoritmo genético
        self.tamano_poblacion = 10
        self.longitud_individuo = 5
        self.max_generaciones = 5
        
        # Crear instancia del algoritmo genético
        self.ag = AlgoritmoGenetico(
            tamano_poblacion=self.tamano_poblacion,
            longitud_individuo=self.longitud_individuo,
            funcion_fitness=self.funcion_fitness,
            funcion_inicializacion=inicializar_poblacion_binaria,
            funcion_seleccion=seleccion_ruleta,
            funcion_cruce=cruce_un_punto,
            funcion_mutacion=mutacion_bit_flip,
            funcion_reemplazo=reemplazo_elitismo,
            condicion_parada=condicion_max_generaciones,
            probabilidad_cruce=0.8,
            probabilidad_mutacion=0.1,
            elitismo=0.1,
            max_generaciones=self.max_generaciones,
            tipo_genoma='binario'
        )
    
    def test_inicializacion(self):
        """Prueba que la inicialización crea una población del tamaño correcto."""
        self.ag.inicializar()
        
        # Comprobar que la población tiene el tamaño correcto
        self.assertEqual(len(self.ag.poblacion), self.tamano_poblacion)
        
        # Comprobar que cada individuo tiene la longitud correcta
        for individuo in self.ag.poblacion:
            self.assertEqual(len(individuo), self.longitud_individuo)
        
        # Comprobar que se han evaluado los fitness
        self.assertEqual(len(self.ag.fitness_poblacion), self.tamano_poblacion)
        
        # Comprobar que el mejor individuo está definido
        self.assertIsNotNone(self.ag.mejor_individuo)
        self.assertIsNotNone(self.ag.mejor_fitness)
        
        # Comprobar que la historia de fitness se ha inicializado
        self.assertEqual(len(self.ag.historia_fitness), 1)
    
    def test_evaluar_poblacion(self):
        """Prueba que la evaluación de la población calcula correctamente los fitness."""
        self.ag.inicializar()
        
        # Guardar la población y los fitness originales
        poblacion_original = [np.copy(ind) for ind in self.ag.poblacion]
        fitness_original = self.ag.fitness_poblacion.copy()
        
        # Reemplazar la población con valores conocidos
        self.ag.poblacion = [
            np.array([1, 1, 1, 1, 1]),  # Fitness = 5
            np.array([0, 0, 0, 0, 0]),  # Fitness = 0
            np.array([1, 0, 1, 0, 1])   # Fitness = 3
        ]
        
        # Evaluar la nueva población
        self.ag.evaluar_poblacion()
        
        # Comprobar que los fitness se han calculado correctamente
        self.assertEqual(self.ag.fitness_poblacion[0], 5)
        self.assertEqual(self.ag.fitness_poblacion[1], 0)
        self.assertEqual(self.ag.fitness_poblacion[2], 3)
        
        # Restaurar la población y los fitness originales
        self.ag.poblacion = poblacion_original
        self.ag.fitness_poblacion = fitness_original
    
    def test_actualizar_mejor_individuo(self):
        """Prueba que la actualización del mejor individuo funciona correctamente."""
        self.ag.inicializar()
        
        # Guardar el mejor fitness original
        mejor_fitness_original = self.ag.mejor_fitness
        
        # Reemplazar la población y los fitness con valores conocidos
        self.ag.poblacion = [
            np.array([1, 1, 1, 1, 1]),  # Fitness = 5
            np.array([0, 0, 0, 0, 0]),  # Fitness = 0
            np.array([1, 0, 1, 0, 1])   # Fitness = 3
        ]
        self.ag.fitness_poblacion = [5, 0, 3]
        
        # Actualizar el mejor individuo
        self.ag.actualizar_mejor_individuo()
        
        # Comprobar que el mejor fitness y el mejor individuo se han actualizado
        self.assertEqual(self.ag.mejor_fitness, 5)
        np.testing.assert_array_equal(self.ag.mejor_individuo, np.array([1, 1, 1, 1, 1]))
        
        # Comprobar que la historia de fitness se ha actualizado
        self.assertEqual(self.ag.historia_fitness[-1], 5)
    
    def test_seleccionar_padres(self):
        """Prueba que la selección de padres devuelve el número correcto de individuos."""
        self.ag.inicializar()
        
        # Seleccionar padres
        padres, fitness_padres = self.ag.seleccionar_padres()
        
        # Comprobar que se han seleccionado el número correcto de padres
        self.assertEqual(len(padres), self.tamano_poblacion)
        self.assertEqual(len(fitness_padres), self.tamano_poblacion)
    
    def test_reproducir(self):
        """Prueba que la reproducción genera el número correcto de hijos."""
        self.ag.inicializar()
        
        # Crear padres de prueba
        padres = [
            np.array([1, 1, 1, 1, 1]),
            np.array([0, 0, 0, 0, 0]),
            np.array([1, 0, 1, 0, 1]),
            np.array([0, 1, 0, 1, 0])
        ]
        
        # Reproducir
        descendencia = self.ag.reproducir(padres)
        
        # Comprobar que se ha generado el número correcto de hijos
        self.assertEqual(len(descendencia), len(padres))
        
        # Comprobar que cada hijo tiene la longitud correcta
        for hijo in descendencia:
            self.assertEqual(len(hijo), self.longitud_individuo)
    
    def test_reemplazar_poblacion(self):
        """Prueba que el reemplazo de la población funciona correctamente."""
        self.ag.inicializar()
        
        # Crear descendencia de prueba
        descendencia = [
            np.array([1, 1, 1, 1, 1]),
            np.array([0, 0, 0, 0, 0]),
            np.array([1, 0, 1, 0, 1]),
            np.array([0, 1, 0, 1, 0])
        ]
        
        # Guardar la población original
        poblacion_original = len(self.ag.poblacion)
        
        # Reemplazar la población
        self.ag.reemplazar_poblacion(descendencia)
        
        # Comprobar que la población tiene el mismo tamaño que antes
        self.assertEqual(len(self.ag.poblacion), poblacion_original)
    
    def test_verificar_condicion_parada(self):
        """Prueba que la verificación de la condición de parada funciona correctamente."""
        self.ag.inicializar()
        
        # Al principio, la condición de parada debería ser False
        self.assertFalse(self.ag.verificar_condicion_parada())
        
        # Simular que se han completado todas las generaciones
        self.ag.generacion_actual = self.max_generaciones
        
        # Ahora la condición de parada debería ser True
        self.assertTrue(self.ag.verificar_condicion_parada())
    
    def test_ejecutar(self):
        """Prueba que la ejecución completa del algoritmo funciona correctamente."""
        # Ejecutar el algoritmo
        mejor_individuo, mejor_fitness, info = self.ag.ejecutar()
        
        # Comprobar que se han devuelto los resultados esperados
        self.assertIsNotNone(mejor_individuo)
        self.assertIsNotNone(mejor_fitness)
        self.assertIn('generaciones', info)
        self.assertIn('tiempo_ejecucion', info)
        self.assertIn('historia_fitness', info)
        
        # Comprobar que se han ejecutado el número correcto de generaciones
        self.assertEqual(info['generaciones'], self.max_generaciones)
        
        # Comprobar que la historia de fitness tiene la longitud correcta
        self.assertEqual(len(info['historia_fitness']), self.max_generaciones + 1)  # +1 por la inicialización
    
    def test_reiniciar(self):
        """Prueba que el reinicio del algoritmo funciona correctamente."""
        # Ejecutar el algoritmo
        self.ag.ejecutar()
        
        # Reiniciar el algoritmo
        self.ag.reiniciar()
        
        # Comprobar que el estado se ha reiniciado
        self.assertEqual(self.ag.generacion_actual, 0)
        self.assertEqual(len(self.ag.poblacion), 0)
        self.assertEqual(len(self.ag.fitness_poblacion), 0)
        self.assertIsNone(self.ag.mejor_individuo)
        self.assertEqual(self.ag.mejor_fitness, float('-inf'))
        self.assertEqual(len(self.ag.historia_fitness), 0)
        self.assertEqual(self.ag.tiempo_ejecucion, 0.0)
        self.assertFalse(self.ag.inicializado)


if __name__ == '__main__':
    unittest.main()