import numpy as np

def fitness_function(individual, objective_function):
    """
    Evalúa la aptitud de un individuo.
    
    Parámetros:
    -----------
    individual : array-like
        Individuo a evaluar
    objective_function : callable
        Función objetivo que determina la aptitud
        
    Retorna:
    --------
    float
        Valor de aptitud del individuo
    """
    return objective_function(individual)

def rank_fitness(fitness_values):
    """
    Convierte valores de fitness a rangos.
    Útil para problemas donde la escala de fitness puede variar mucho.
    
    Parámetros:
    -----------
    fitness_values : ndarray
        Valores originales de aptitud
        
    Retorna:
    --------
    ndarray
        Valores de aptitud convertidos a rangos
    """
    # Ordenar índices de mayor a menor fitness
    sorted_indices = np.argsort(-fitness_values)
    
    # Crear rangos (el mejor tiene rango 0, el peor rango n-1)
    ranks = np.zeros_like(fitness_values)
    for i, idx in enumerate(sorted_indices):
        ranks[idx] = i
    
    # Invertir para que el mejor tenga el valor más alto
    max_rank = len(fitness_values) - 1
    ranks = max_rank - ranks
    
    return ranks

def constrained_fitness(individual, objective_function, constraint_functions, penalty_factor=1e6):
    """
    Evalúa fitness con manejo de restricciones mediante penalización.
    
    Parámetros:
    -----------
    individual : array-like
        Individuo a evaluar
    objective_function : callable
        Función objetivo principal
    constraint_functions : list
        Lista de funciones de restricción que deben ser >= 0 para ser válidas
    penalty_factor : float
        Factor de penalización para restricciones violadas
        
    Retorna:
    --------
    float
        Valor de aptitud penalizado
    """
    # Calcular fitness base
    fitness = objective_function(individual)
    
    # Calcular penalización por restricciones violadas
    penalty = 0.0
    for constraint_func in constraint_functions:
        constraint_value = constraint_func(individual)
        # Penalizar si la restricción es violada (valor < 0)
        if constraint_value < 0:
            penalty += penalty_factor * abs(constraint_value)
    
    # Devolver fitness penalizado
    return fitness - penalty

def multi_objective_fitness(individual, objective_functions):
    """
    Evalúa fitness en problemas multi-objetivo.
    
    Parámetros:
    -----------
    individual : array-like
        Individuo a evaluar
    objective_functions : list
        Lista de funciones objetivo
        
    Retorna:
    --------
    ndarray
        Vector de valores de aptitud para cada objetivo
    """
    # Calcular vector de fitness
    fitness_vector = np.zeros(len(objective_functions))
    
    for i, obj_func in enumerate(objective_functions):
        fitness_vector[i] = obj_func(individual)
    
    return fitness_vector

def pareto_dominance(fitness1, fitness2):
    """
    Determina si una solución domina a otra en el sentido de Pareto.
    
    Parámetros:
    -----------
    fitness1 : array-like
        Vector de fitness de la primera solución
    fitness2 : array-like
        Vector de fitness de la segunda solución
        
    Retorna:
    --------
    bool
        True si fitness1 domina a fitness2, False en caso contrario
    """
    # Comprobar si fitness1 es al menos igual a fitness2 en todos los objetivos
    at_least_equal = np.all(fitness1 >= fitness2)
    
    # Comprobar si fitness1 es mejor que fitness2 en al menos un objetivo
    better_in_one = np.any(fitness1 > fitness2)
    
    # fitness1 domina a fitness2 si ambas condiciones son verdaderas
    return at_least_equal and better_in_one

def get_pareto_front(population, fitness_values):
    """
    Obtiene el frente de Pareto de una población.
    
    Parámetros:
    -----------
    population : ndarray
        Población de individuos
    fitness_values : ndarray
        Matriz de valores de fitness (individuos x objetivos)
        
    Retorna:
    --------
    tuple
        (índices del frente de Pareto, individuos en el frente, valores de fitness)
    """
    pareto_indices = []
    
    # Encontrar soluciones no dominadas
    for i in range(len(population)):
        is_dominated = False
        for j in range(len(population)):
            if i != j and pareto_dominance(fitness_values[j], fitness_values[i]):
                is_dominated = True
                break
        
        if not is_dominated:
            pareto_indices.append(i)
    
    # Convertir a array numpy
    pareto_indices = np.array(pareto_indices)
    
    # Extraer soluciones y fitness
    pareto_front = population[pareto_indices]
    pareto_fitness = fitness_values[pareto_indices]
    
    return pareto_indices, pareto_front, pareto_fitness