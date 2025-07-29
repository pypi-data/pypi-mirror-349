import unittest
import numpy as np
from genetic_algorithm.core.selection import selection
from genetic_algorithm.core.crossover import crossover, crossover_permutation
from genetic_algorithm.core.mutation import mutation, adaptive_mutation

class TestOperators(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Población para pruebas (10 individuos con 3 genes cada uno)
        self.population = np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [10.0, 11.0, 12.0],
            [13.0, 14.0, 15.0],
            [16.0, 17.0, 18.0],
            [19.0, 20.0, 21.0],
            [22.0, 23.0, 24.0],
            [25.0, 26.0, 27.0],
            [28.0, 29.0, 30.0]
        ])
        
        # Valores de fitness simulados (crecientes)
        self.fitness_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    def test_selection_tournament(self):
        """Prueba la selección por torneo."""
        num_parents = 5
        
        parents = selection(
            self.population, 
            self.fitness_values, 
            num_parents, 
            selection_type="tournament"
        )
        
        self.assertEqual(parents.shape, (num_parents, 3))
        
        # Verificar que todos los padres seleccionados están en la población original
        for parent in parents:
            found = False
            for ind in self.population:
                if np.array_equal(parent, ind):
                    found = True
                    break
            self.assertTrue(found)
    
    def test_selection_roulette(self):
        """Prueba la selección por ruleta."""
        num_parents = 5
        
        parents = selection(
            self.population, 
            self.fitness_values, 
            num_parents, 
            selection_type="roulette"
        )
        
        self.assertEqual(parents.shape, (num_parents, 3))
    
    def test_selection_rank(self):
        """Prueba la selección por rango."""
        num_parents = 5
        
        parents = selection(
            self.population, 
            self.fitness_values, 
            num_parents, 
            selection_type="rank"
        )
        
        self.assertEqual(parents.shape, (num_parents, 3))
    
    def test_crossover_uniform(self):
        """Prueba el cruce uniforme."""
        parents = self.population[:5]
        offspring_size = (8, 3)
        
        offspring = crossover(
            parents, 
            offspring_size, 
            crossover_type="uniform"
        )
        
        self.assertEqual(offspring.shape, offspring_size)
    
    def test_crossover_single_point(self):
        """Prueba el cruce de un punto."""
        parents = self.population[:5]
        offspring_size = (8, 3)
        
        offspring = crossover(
            parents, 
            offspring_size, 
            crossover_type="single_point"
        )
        
        self.assertEqual(offspring.shape, offspring_size)
    
    def test_crossover_blend(self):
        """Prueba el cruce blend."""
        parents = self.population[:5]
        offspring_size = (8, 3)
        
        offspring = crossover(
            parents, 
            offspring_size, 
            crossover_type="blend"
        )
        
        self.assertEqual(offspring.shape, offspring_size)
    
    def test_crossover_permutation(self):
        """Prueba el cruce para permutaciones."""
        # Crear población de permutaciones
        perm_population = np.array([
            np.random.permutation(5) for _ in range(6)
        ])
        
        offspring_size = (4, 5)
        
        offspring = crossover_permutation(
            perm_population, 
            offspring_size, 
            crossover_type="pmx"
        )
        
        self.assertEqual(offspring.shape, offspring_size)
        
        # Verificar que cada fila es una permutación
        for row in offspring:
            self.assertEqual(sorted(row), list(range(5)))
    
    def test_mutation_gaussian(self):
        """Prueba la mutación gaussiana."""
        offspring = self.population.copy()
        
        mutated = mutation(
            offspring, 
            mutation_rate=0.5, 
            mutation_type="gaussian", 
            min_val=0, 
            max_val=100
        )
        
        self.assertEqual(mutated.shape, offspring.shape)
        
        # Asegurar que se han producido cambios
        self.assertFalse(np.array_equal(mutated, offspring))
        
        # Verificar límites
        self.assertTrue(np.all(mutated >= 0))
        self.assertTrue(np.all(mutated <= 100))
    
    def test_mutation_permutation(self):
        """Prueba la mutación para permutaciones."""
        # Crear descendencia de permutaciones
        perm_offspring = np.array([
            np.random.permutation(5) for _ in range(4)
        ])
        
        mutated = mutation(
            perm_offspring, 
            mutation_rate=0.5, 
            mutation_type="swap", 
            encoding="permutation"
        )
        
        self.assertEqual(mutated.shape, perm_offspring.shape)
        
        # Verificar que cada fila sigue siendo una permutación
        for row in mutated:
            self.assertEqual(sorted(row), list(range(5)))
    
    def test_adaptive_mutation(self):
        """Prueba la mutación adaptativa."""
        offspring = self.population[:5].copy()
        fitness_values = self.fitness_values[:5]
        
        mutated = adaptive_mutation(
            offspring, 
            fitness_values, 
            best_fitness=10, 
            avg_fitness=5, 
            min_val=0, 
            max_val=100, 
            base_rate=0.1
        )
        
        self.assertEqual(mutated.shape, offspring.shape)
        
        # Verificar límites
        self.assertTrue(np.all(mutated >= 0))
        self.assertTrue(np.all(mutated <= 100))

if __name__ == '__main__':
    unittest.main()