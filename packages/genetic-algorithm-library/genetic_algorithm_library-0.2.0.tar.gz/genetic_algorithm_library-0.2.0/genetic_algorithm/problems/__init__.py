"""
Módulo problems para funciones de prueba estándar y problemas específicos.
"""

from .continuous import (
    sphere, rosenbrock, rastrigin, schwefel, griewank, 
    ackley, levy, michalewicz, get_function
)

from .discrete import (
    knapsack_problem, max_cut_problem, bin_packing_problem,
    vehicle_routing_problem
)

from .combinatorial import (
    tsp_create_cities, tsp_distance, tsp_plot_solution,
    tsp_create_distance_matrix
)