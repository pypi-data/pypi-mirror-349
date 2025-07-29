"""
Módulo core para componentes fundamentales del algoritmo genético.
"""

from .population import create_population, initialize_from_samples, check_population_diversity
from .selection import selection
from .crossover import crossover, crossover_permutation
from .mutation import mutation, adaptive_mutation, self_adaptation
from .fitness import (
    fitness_function, rank_fitness, constrained_fitness, 
    multi_objective_fitness, pareto_dominance, get_pareto_front
)