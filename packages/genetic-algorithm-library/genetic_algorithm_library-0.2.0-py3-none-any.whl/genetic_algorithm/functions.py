import numpy as np
import random
import matplotlib.pyplot as plt

"""
Librería de Algoritmos Genéticos para Optimización
-------------------------------------------------
Autor: Julian Lara
Fecha: Mayo 2025

Esta librería implementa un algoritmo genético adaptativo para resolver
problemas de optimización. Incluye funciones para crear poblaciones,
evaluar aptitud, selección, cruce, mutación y ejecución completa.
"""

def create_population(size, gene_length, min_val=0, max_val=1):
    """
    Crea una población inicial de individuos.
    
    Parámetros:
    -----------
    size : int
        Tamaño de la población
    gene_length : int
        Longitud del genoma de cada individuo
    min_val : float
        Valor mínimo para los genes
    max_val : float
        Valor máximo para los genes
        
    Retorna:
    --------
    ndarray
        Población inicial de tamaño (size, gene_length)
    """
    return np.random.uniform(min_val, max_val, (size, gene_length))

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

def selection(population, fitness_values, num_parents, selection_type="tournament"):
    """
    Selecciona individuos para reproducción.
    
    Parámetros:
    -----------
    population : ndarray
        Población actual
    fitness_values : ndarray
        Valores de aptitud correspondientes a la población
    num_parents : int
        Número de padres a seleccionar
    selection_type : str
        Método de selección: "tournament", "roulette", "rank"
        
    Retorna:
    --------
    ndarray
        Padres seleccionados
    """
    parents = np.zeros((num_parents, population.shape[1]))
    
    if selection_type == "tournament":
        for i in range(num_parents):
            # Selección por torneo (tamaño 3)
            indices = np.random.choice(len(population), 3, replace=False)
            tournament_fitness = [fitness_values[idx] for idx in indices]
            winner_idx = indices[np.argmax(tournament_fitness)]
            parents[i] = population[winner_idx]
    
    elif selection_type == "roulette":
        # Normalizar fitness para valores positivos
        fitness_min = min(0, np.min(fitness_values))
        normalized_fitness = fitness_values - fitness_min
        
        # Evitar división por cero
        if np.sum(normalized_fitness) == 0:
            return population[np.random.choice(len(population), num_parents, replace=False)]
            
        # Selección por ruleta
        probs = normalized_fitness / np.sum(normalized_fitness)
        indices = np.random.choice(len(population), num_parents, p=probs)
        parents = population[indices]
    
    elif selection_type == "rank":
        # Selección por rango
        ranks = np.argsort(np.argsort(-fitness_values))
        rank_probs = (len(population) - ranks) / np.sum(len(population) - ranks)
        indices = np.random.choice(len(population), num_parents, p=rank_probs)
        parents = population[indices]
    
    return parents

def crossover(parents, offspring_size, crossover_type="uniform"):
    """
    Realiza el cruce entre padres para crear descendencia.
    
    Parámetros:
    -----------
    parents : ndarray
        Arreglo de padres seleccionados
    offspring_size : tuple
        Tamaño de la descendencia: (n_offspring, n_genes)
    crossover_type : str
        Tipo de cruce: "uniform", "single_point", "two_point"
        
    Retorna:
    --------
    ndarray
        Descendencia generada
    """
    offspring = np.zeros(offspring_size)
    
    for i in range(offspring_size[0]):
        # Seleccionar padres aleatoriamente
        parent1_idx = i % parents.shape[0]
        parent2_idx = (i + 1) % parents.shape[0]
        
        if crossover_type == "uniform":
            # Cruce uniforme
            mask = np.random.random(offspring_size[1]) < 0.5
            offspring[i, mask] = parents[parent1_idx, mask]
            offspring[i, ~mask] = parents[parent2_idx, ~mask]
            
        elif crossover_type == "single_point":
            # Cruce de un punto
            crossover_point = np.random.randint(1, offspring_size[1])
            offspring[i, :crossover_point] = parents[parent1_idx, :crossover_point]
            offspring[i, crossover_point:] = parents[parent2_idx, crossover_point:]
            
        elif crossover_type == "two_point":
            # Cruce de dos puntos
            points = sorted(np.random.choice(offspring_size[1] - 1, 2, replace=False) + 1)
            offspring[i, :points[0]] = parents[parent1_idx, :points[0]]
            offspring[i, points[0]:points[1]] = parents[parent2_idx, points[0]:points[1]]
            offspring[i, points[1]:] = parents[parent1_idx, points[1]:]
    
    return offspring

def mutation(offspring, mutation_rate=0.01, mutation_type="gaussian", min_val=0, max_val=1):
    """
    Aplica mutación a la descendencia.
    
    Parámetros:
    -----------
    offspring : ndarray
        Descendencia a mutar
    mutation_rate : float
        Tasa de mutación (probabilidad de que un gen mute)
    mutation_type : str
        Tipo de mutación: "gaussian", "uniform", "reset"
    min_val : float
        Valor mínimo para los genes (para mutación uniforme o reset)
    max_val : float
        Valor máximo para los genes (para mutación uniforme o reset)
        
    Retorna:
    --------
    ndarray
        Descendencia mutada
    """
    mutated_offspring = offspring.copy()
    
    # Crear máscara de mutación
    mutation_mask = np.random.random(offspring.shape) < mutation_rate
    
    if mutation_type == "gaussian":
        # Mutación gaussiana (añadir ruido normal)
        sigma = 0.1 * (max_val - min_val)
        noise = np.random.normal(0, sigma, offspring.shape)
        mutated_offspring[mutation_mask] += noise[mutation_mask]
        
    elif mutation_type == "uniform":
        # Mutación uniforme (reemplazar con valores aleatorios uniformes)
        random_values = np.random.uniform(min_val, max_val, offspring.shape)
        mutated_offspring[mutation_mask] = random_values[mutation_mask]
        
    elif mutation_type == "reset":
        # Mutación de reseteo (50% probabilidad de ir a extremos)
        reset_values = np.random.choice([min_val, max_val], offspring.shape)
        mutated_offspring[mutation_mask] = reset_values[mutation_mask]
    
    # Asegurar que los valores estén dentro de los límites
    np.clip(mutated_offspring, min_val, max_val, out=mutated_offspring)
    
    return mutated_offspring

def run_genetic_algorithm(objective_function, gene_length, bounds=(0, 1), 
                         pop_size=100, num_generations=100, 
                         selection_type="tournament", crossover_type="uniform",
                         mutation_type="gaussian", mutation_rate=0.01,
                         adaptive=True, verbose=True):
    """
    Ejecuta el algoritmo genético completo.
    
    Parámetros:
    -----------
    objective_function : callable
        Función objetivo a optimizar
    gene_length : int
        Longitud del genoma de cada individuo
    bounds : tuple
        Límites de valores para los genes (min, max)
    pop_size : int
        Tamaño de la población
    num_generations : int
        Número de generaciones a ejecutar
    selection_type : str
        Método de selección: "tournament", "roulette", "rank"
    crossover_type : str
        Tipo de cruce: "uniform", "single_point", "two_point"
    mutation_type : str
        Tipo de mutación: "gaussian", "uniform", "reset"
    mutation_rate : float
        Tasa inicial de mutación
    adaptive : bool
        Si es True, la tasa de mutación se adapta durante la ejecución
    verbose : bool
        Si es True, muestra información durante la ejecución
        
    Retorna:
    --------
    dict
        Diccionario con resultados: mejor individuo, mejor fitness, historia
    """
    min_val, max_val = bounds
    
    # Crear población inicial
    population = create_population(pop_size, gene_length, min_val, max_val)
    
    # Historial para seguimiento
    history = {
        'best_fitness': [],
        'avg_fitness': [],
        'best_individual': [],
        'mutation_rate': []
    }
    
    best_individual = None
    best_fitness = float('-inf')
    
    # Algoritmo principal
    for generation in range(num_generations):
        # Calcular aptitud para cada individuo
        fitness_values = np.array([fitness_function(ind, objective_function) for ind in population])
        
        # Encontrar el mejor individuo de esta generación
        gen_best_idx = np.argmax(fitness_values)
        gen_best_individual = population[gen_best_idx]
        gen_best_fitness = fitness_values[gen_best_idx]
        
        # Actualizar el mejor global si es necesario
        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best_individual = gen_best_individual.copy()
        
        # Guardar historial
        history['best_fitness'].append(gen_best_fitness)
        history['avg_fitness'].append(np.mean(fitness_values))
        history['best_individual'].append(gen_best_individual)
        history['mutation_rate'].append(mutation_rate)
        
        # Mostrar progreso
        if verbose and (generation % 10 == 0 or generation == num_generations - 1):
            print(f"Generación {generation+1}/{num_generations}: "
                  f"Mejor Fitness = {gen_best_fitness:.6f}, "
                  f"Fitness Promedio = {np.mean(fitness_values):.6f}, "
                  f"Tasa de Mutación = {mutation_rate:.6f}")
        
        # Seleccionar padres
        parents = selection(population, fitness_values, pop_size // 2, selection_type)
        
        # Cruce
        offspring_size = (pop_size - parents.shape[0], gene_length)
        offspring = crossover(parents, offspring_size, crossover_type)
        
        # Mutación
        offspring = mutation(offspring, mutation_rate, mutation_type, min_val, max_val)
        
        # Adaptación de la tasa de mutación
        if adaptive:
            # Si hay mejora, reducir la tasa de mutación
            if len(history['best_fitness']) > 1 and history['best_fitness'][-1] > history['best_fitness'][-2]:
                mutation_rate = max(0.001, mutation_rate * 0.95)
            else:
                # Si no hay mejora, aumentar la tasa de mutación
                mutation_rate = min(0.2, mutation_rate * 1.05)
        
        # Crear nueva población
        population[0] = best_individual  # Elitismo
        population[1:parents.shape[0]] = parents[1:]
        population[parents.shape[0]:] = offspring
    
    # Resultados finales
    results = {
        'best_individual': best_individual,
        'best_fitness': best_fitness,
        'history': history
    }
    
    if verbose:
        print("\nOptimización completada:")
        print(f"Mejor Fitness: {best_fitness:.6f}")
        print(f"Mejor Individuo: {best_individual}")
    
    return results

def plot_evolution(history):
    """
    Visualiza la evolución del algoritmo genético.
    
    Parámetros:
    -----------
    history : dict
        Diccionario con historiales de la ejecución
    """
    generations = range(1, len(history['best_fitness']) + 1)
    
    plt.figure(figsize=(12, 8))
    
    # Gráfica de fitness
    plt.subplot(2, 1, 1)
    plt.plot(generations, history['best_fitness'], 'b-', label='Mejor Fitness')
    plt.plot(generations, history['avg_fitness'], 'r--', label='Fitness Promedio')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del Fitness')
    plt.legend()
    plt.grid(True)
    
    # Gráfica de tasa de mutación
    plt.subplot(2, 1, 2)
    plt.plot(generations, history['mutation_rate'], 'g-')
    plt.xlabel('Generación')
    plt.ylabel('Tasa de Mutación')
    plt.title('Adaptación de la Tasa de Mutación')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()