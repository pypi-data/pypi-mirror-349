# Genetic Algorithm Library

[![PyPI version](https://img.shields.io/badge/pypi-v0.1.0-blue.svg)](https://pypi.org/project/genetic-algorithm-library/)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Genetic Algorithm Library is a robust Python library implementing adaptive genetic algorithms for optimization problems. It provides a flexible framework for solving complex problems through evolutionary computing techniques.

## Features

- **Population Initialization**: Create diverse initial populations with various strategies
- **Multiple Selection Methods**: Tournament, Roulette Wheel, and Rank-based selection
- **Diverse Crossover Operations**: Single-point, Two-point, and Uniform crossover
- **Adaptive Mutation**: Automatically adjusts mutation rates for better convergence
- **Visualization Tools**: Plot evolution and convergence metrics
- **Easy-to-use API**: Simple interface for quick integration

## Installation

```bash
pip install genetic-algorithm-library
```

## Quick Start

```python
from genetic_algorithm import run_genetic_algorithm

# Define a simple objective function (maximizing)
def objective_function(x):
    return -(x[0]**2 + x[1]**2)  # Maximize negative of sum of squares

# Run the genetic algorithm
result = run_genetic_algorithm(
    objective_function=objective_function,
    gene_length=2,               # 2 parameters to optimize
    bounds=(-10, 10),            # Search bounds
    pop_size=100,                # Population size
    num_generations=50,          # Number of generations
    selection_type="tournament", # Selection method
    adaptive=True                # Enable adaptive mutation
)

# Display results
print(f"Best solution: {result['best_individual']}")
print(f"Best fitness: {result['best_fitness']}")

# Plot the evolution
from genetic_algorithm import plot_evolution
plot_evolution(result['history'])
```

## Advanced Usage

```python
import numpy as np
from genetic_algorithm import (
    create_population,
    fitness_function,
    selection,
    crossover,
    mutation
)

# Create initial population
population = create_population(size=50, gene_length=5, min_val=-5, max_val=5)

# Custom fitness function
def my_objective(x):
    return np.sin(x[0]) + np.cos(x[1]) + x[2]**2 - x[3] + x[4]

# Manual iteration
for generation in range(100):
    # Evaluate fitness
    fitness_values = np.array([fitness_function(ind, my_objective) for ind in population])
    
    # Select parents
    parents = selection(population, fitness_values, num_parents=25, selection_type="rank")
    
    # Create offspring through crossover
    offspring = crossover(parents, offspring_size=(25, 5), crossover_type="two_point")
    
    # Apply mutation
    offspring = mutation(offspring, mutation_rate=0.05, mutation_type="gaussian", min_val=-5, max_val=5)
    
    # Create new population with elitism (keeping the best individual)
    best_idx = np.argmax(fitness_values)
    population = np.vstack([population[best_idx:best_idx+1], parents[:-1], offspring])
```

## Documentation

For complete documentation, visit our [GitHub Wiki](https://github.com/Zaxazgames1/genetic-algorithm-library/wiki).

## Contributors

- Julian Lara
- Johan Rojas

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this library in your research, please cite:

```
@software{genetic_algorithm_library,
  author = {Lara, Julian and Rojas, Johan},
  title = {Genetic Algorithm Library},
  url = {https://github.com/Zaxazgames1/genetic-algorithm-library},
  version = {0.1.0},
  year = {2025},
}
```