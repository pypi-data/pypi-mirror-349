import unittest
import numpy as np
from genetic_algorithm.core.population import (
    create_population, initialize_from_samples, check_population_diversity
)

class TestPopulation(unittest.TestCase):
    
    def test_create_population_real(self):
        """Prueba la creación de población con codificación real."""
        pop_size = 50
        gene_length = 5
        min_val = -10
        max_val = 10
        
        population = create_population(pop_size, gene_length, min_val, max_val, encoding="real")
        
        self.assertEqual(population.shape, (pop_size, gene_length))
        self.assertTrue(np.all(population >= min_val))
        self.assertTrue(np.all(population <= max_val))
    
    def test_create_population_binary(self):
        """Prueba la creación de población con codificación binaria."""
        pop_size = 30
        gene_length = 8
        
        population = create_population(pop_size, gene_length, encoding="binary")
        
        self.assertEqual(population.shape, (pop_size, gene_length))
        self.assertTrue(np.all((population == 0) | (population == 1)))
    
    def test_create_population_integer(self):
        """Prueba la creación de población con codificación entera."""
        pop_size = 40
        gene_length = 4
        min_val = 1
        max_val = 10
        
        population = create_population(pop_size, gene_length, min_val, max_val, encoding="integer")
        
        self.assertEqual(population.shape, (pop_size, gene_length))
        self.assertTrue(np.all(population >= min_val))
        self.assertTrue(np.all(population <= max_val))
        self.assertTrue(np.all(population.astype(int) == population))
    
    def test_create_population_permutation(self):
        """Prueba la creación de población con codificación de permutación."""
        pop_size = 20
        gene_length = 10
        
        population = create_population(pop_size, gene_length, encoding="permutation")
        
        self.assertEqual(population.shape, (pop_size, gene_length))
        
        # Verificar que cada fila es una permutación de 0 a gene_length-1
        for row in population:
            self.assertEqual(sorted(row), list(range(gene_length)))
    
    def test_initialize_from_samples(self):
        """Prueba la inicialización a partir de muestras conocidas."""
        samples = np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0]
        ])
        
        pop_size = 10
        
        population = initialize_from_samples(samples, pop_size, noise=0.1)
        
        self.assertEqual(population.shape, (pop_size, 3))
        
        # Las primeras filas deben ser iguales a las muestras
        np.testing.assert_array_equal(population[0], samples[0])
        np.testing.assert_array_equal(population[1], samples[1])
    
    def test_check_population_diversity(self):
        """Prueba la evaluación de diversidad de población."""
        # Población con baja diversidad
        low_diversity = np.ones((20, 5)) + np.random.normal(0, 0.001, (20, 5))
        
        # Población con alta diversidad
        high_diversity = np.random.uniform(-10, 10, (20, 5))
        
        low_div_score = check_population_diversity(low_diversity)
        high_div_score = check_population_diversity(high_diversity)
        
        self.assertTrue(low_div_score < high_div_score)

if __name__ == '__main__':
    unittest.main()