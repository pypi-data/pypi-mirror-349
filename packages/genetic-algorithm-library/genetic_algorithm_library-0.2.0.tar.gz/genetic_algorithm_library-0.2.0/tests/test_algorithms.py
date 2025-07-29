import unittest
import numpy as np
from genetic_algorithm import (
    run_genetic_algorithm, 
    run_multi_objective_ga, 
    run_island_model_ga
)

class TestAlgorithms(unittest.TestCase):
    
    def test_run_genetic_algorithm(self):
        """Prueba la ejecución del algoritmo genético básico."""
        # Función objetivo simple (maximizar)
        def objective_function(x):
            return -(x[0]**2 + x[1]**2)  # Minimizar la suma de cuadrados
        
        result = run_genetic_algorithm(
            objective_function=objective_function,
            gene_length=2,
            bounds=(-10, 10),
            pop_size=20,
            num_generations=5,
            verbose=False
        )
        
        # Verificar estructura de resultados
        self.assertIn('best_individual', result)
        self.assertIn('best_fitness', result)
        self.assertIn('history', result)
        self.assertIn('best_fitness', result['history'])
        self.assertIn('avg_fitness', result['history'])
        self.assertIn('best_individual', result['history'])
        
        # Verificar tamaños
        self.assertEqual(len(result['best_individual']), 2)
        self.assertEqual(len(result['history']['best_fitness']), 5)
    
    def test_run_multi_objective_ga(self):
        """Prueba la ejecución del algoritmo genético multi-objetivo."""
        # Funciones objetivo para un problema multi-objetivo simple
        def objective1(x):
            return -(x[0]**2 + x[1]**2)  # Minimizar suma de cuadrados
        
        def objective2(x):
            return -((x[0]-1)**2 + (x[1]-1)**2)  # Minimizar distancia a (1,1)
        
        result = run_multi_objective_ga(
            objective_functions=[objective1, objective2],
            gene_length=2,
            bounds=(-5, 5),
            pop_size=20,
            num_generations=5,
            verbose=False
        )
        
        # Verificar estructura de resultados
        self.assertIn('pareto_front', result)
        self.assertIn('pareto_fitness', result)
        self.assertIn('history', result)
        
        # Verificar que existe al menos una solución en el frente de Pareto
        self.assertGreater(len(result['pareto_front']), 0)
        
        # Verificar dimensiones de fitness
        self.assertEqual(result['pareto_fitness'].shape[1], 2)  # 2 objetivos
    
    def test_run_island_model_ga(self):
        """Prueba la ejecución del algoritmo genético con modelo de islas."""
        # Función objetivo simple (maximizar)
        def objective_function(x):
            return -(x[0]**2 + x[1]**2 + x[2]**2)  # Minimizar la suma de cuadrados
    
        result = run_island_model_ga(
            objective_function=objective_function,
            gene_length=3,  # Aumentar a 3 genes para evitar problemas con crossover
            bounds=(-10, 10),
            num_islands=3,
            pop_size_per_island=10,
            num_generations=5,
            migration_interval=2,
            verbose=False
        )
    
        # Verificar estructura de resultados
        self.assertIn('best_individual', result)
        self.assertIn('best_fitness', result)
        self.assertIn('history', result)
        self.assertIn('final_islands', result)
    
        # Verificar número de islas
        self.assertEqual(len(result['final_islands']), 3)
        self.assertEqual(len(result['history']['island_best_fitness']), 3)

if __name__ == '__main__':
    unittest.main()