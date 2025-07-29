"""
Genetic Algorithm Library
=========================

Una librería robusta y flexible para implementar algoritmos genéticos
y evolutivos en problemas de optimización.

Módulos principales:
-------------------
core : Componentes fundamentales del algoritmo genético
utils : Utilidades para visualización y análisis
problems : Implementaciones para tipos específicos de problemas
algorithms : Algoritmos genéticos completos y listos para usar
"""

from .core.population import create_population
from .core.selection import selection
from .core.crossover import crossover
from .core.mutation import mutation, adaptive_mutation
from .core.fitness import fitness_function

from .algorithms import (
    run_genetic_algorithm,
    run_multi_objective_ga,
    run_island_model_ga
)

from .utils.visualization import (
    plot_evolution,
    plot_pareto_front,
    plot_population_diversity
)

# Metadatos
__version__ = '0.2.0'
__author__ = 'Julian Lara, Johan Rojas'
__email__ = 'johansebastianrojasramirez7@gmail.com'
__license__ = 'MIT'