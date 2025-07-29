import numpy as np
import time
import random
import json
import os

def set_seed(seed):
    """
    Establece una semilla para reproducibilidad de los resultados.
    
    Parámetros:
    -----------
    seed : int
        Semilla para los generadores de números aleatorios
    """
    np.random.seed(seed)
    random.seed(seed)

def estimate_runtime(objective_function, gene_length, pop_size=100, num_gens=10):
    """
    Estima el tiempo de ejecución para el problema dado.
    
    Parámetros:
    -----------
    objective_function : callable
        Función objetivo
    gene_length : int
        Longitud del genoma
    pop_size : int
        Tamaño de población a probar
    num_gens : int
        Número de generaciones para la estimación
        
    Retorna:
    --------
    dict
        Estimaciones de tiempo de ejecución
    """
    # Crear población de prueba
    population = np.random.uniform(0, 1, (pop_size, gene_length))
    
    # Medir tiempo para evaluación de fitness
    start_time = time.time()
    for _ in range(num_gens):
        for ind in population:
            objective_function(ind)
    eval_time = time.time() - start_time
    
    # Estimaciones
    eval_per_gen = pop_size
    eval_time_per_ind = eval_time / (num_gens * pop_size)
    
    return {
        'eval_time_per_ind': eval_time_per_ind,
        'time_per_generation': eval_time_per_ind * pop_size,
        'estimated_total_time': eval_time_per_ind * pop_size * 100,  # 100 generaciones
    }

def save_results(results, filename):
    """
    Guarda los resultados en un archivo JSON.
    
    Parámetros:
    -----------
    results : dict
        Resultados a guardar
    filename : str
        Nombre del archivo
    """
    # Convertir arrays de numpy a listas para guardar en JSON
    results_serializable = {}
    
    for key, value in results.items():
        if key == 'history':
            history_serializable = {}
            for hist_key, hist_value in value.items():
                if isinstance(hist_value, list) and len(hist_value) > 0 and isinstance(hist_value[0], np.ndarray):
                    # Lista de arrays
                    history_serializable[hist_key] = [arr.tolist() for arr in hist_value]
                elif isinstance(hist_value, np.ndarray):
                    # Array simple
                    history_serializable[hist_key] = hist_value.tolist()
                else:
                    # Otros tipos
                    history_serializable[hist_key] = hist_value
            results_serializable['history'] = history_serializable
        elif isinstance(value, np.ndarray):
            # Arrays numpy
            results_serializable[key] = value.tolist()
        else:
            # Otros tipos
            results_serializable[key] = value
    
    # Guardar en archivo
    with open(filename, 'w') as f:
        json.dump(results_serializable, f, indent=2)

def load_results(filename):
    """
    Carga resultados desde un archivo JSON.
    
    Parámetros:
    -----------
    filename : str
        Nombre del archivo
        
    Retorna:
    --------
    dict
        Resultados cargados
    """
    # Cargar desde archivo
    with open(filename, 'r') as f:
        results_loaded = json.load(f)
    
    # Convertir listas a arrays de numpy
    results = {}
    
    for key, value in results_loaded.items():
        if key == 'history':
            history = {}
            for hist_key, hist_value in value.items():
                if isinstance(hist_value, list) and len(hist_value) > 0 and isinstance(hist_value[0], list):
                    # Lista de arrays
                    history[hist_key] = [np.array(arr) for arr in hist_value]
                elif isinstance(hist_value, list):
                    # Posible array
                    try:
                        history[hist_key] = np.array(hist_value)
                    except:
                        history[hist_key] = hist_value
                else:
                    # Otros tipos
                    history[hist_key] = hist_value
            results['history'] = history
        elif isinstance(value, list):
            # Posible array
            try:
                results[key] = np.array(value)
            except:
                results[key] = value
        else:
            # Otros tipos
            results[key] = value
    
    return results

def benchmark_operators(objective_function, gene_length, bounds=(0, 1), pop_size=50, num_gens=20):
    """
    Compara diferentes operadores genéticos.
    
    Parámetros:
    -----------
    objective_function : callable
        Función objetivo
    gene_length : int
        Longitud del genoma
    bounds : tuple
        Límites de los genes
    pop_size : int
        Tamaño de población
    num_gens : int
        Número de generaciones
        
    Retorna:
    --------
    dict
        Resultados comparativos
    """
    from ..core.population import create_population
    from ..core.selection import selection
    from ..core.crossover import crossover
    from ..core.mutation import mutation
    from ..core.fitness import fitness_function
    
    min_val, max_val = bounds
    
    # Operadores a comparar
    selection_types = ["tournament", "roulette", "rank", "sus"]
    crossover_types = ["uniform", "single_point", "two_point", "blend"]
    mutation_types = ["gaussian", "uniform", "reset", "creep"]
    
    # Resultados
    results = {
        'selection': {},
        'crossover': {},
        'mutation': {}
    }
    
    # Configuración por defecto
    default_sel = "tournament"
    default_cross = "uniform"
    default_mut = "gaussian"
    
    # Benchmark de operadores de selección
    print("Benchmarking operadores de selección...")
    for sel_type in selection_types:
        # Población inicial
        population = create_population(pop_size, gene_length, min_val, max_val)
        best_fitness = float('-inf')
        
        for gen in range(num_gens):
            # Evaluar fitness
            fitness_values = np.array([fitness_function(ind, objective_function) for ind in population])
            
            # Actualizar mejor fitness
            gen_best = np.max(fitness_values)
            best_fitness = max(best_fitness, gen_best)
            
            # Selección
            parents = selection(population, fitness_values, pop_size // 2, sel_type)
            
            # Cruce
            offspring_size = (pop_size, gene_length)
            offspring = crossover(parents, offspring_size, default_cross)
            
            # Mutación
            offspring = mutation(offspring, 0.01, default_mut, min_val, max_val)
            
            # Nueva población
            population = offspring
        
        # Guardar resultado
        results['selection'][sel_type] = best_fitness
    
    # Benchmark de operadores de cruce
    print("Benchmarking operadores de cruce...")
    for cross_type in crossover_types:
        # Población inicial
        population = create_population(pop_size, gene_length, min_val, max_val)
        best_fitness = float('-inf')
        
        for gen in range(num_gens):
            # Evaluar fitness
            fitness_values = np.array([fitness_function(ind, objective_function) for ind in population])
            
            # Actualizar mejor fitness
            gen_best = np.max(fitness_values)
            best_fitness = max(best_fitness, gen_best)
            
            # Selección
            parents = selection(population, fitness_values, pop_size // 2, default_sel)
            
            # Cruce
            offspring_size = (pop_size, gene_length)
            offspring = crossover(parents, offspring_size, cross_type)
            
            # Mutación
            offspring = mutation(offspring, 0.01, default_mut, min_val, max_val)
            
            # Nueva población
            population = offspring
        
        # Guardar resultado
        results['crossover'][cross_type] = best_fitness
    
    # Benchmark de operadores de mutación
    print("Benchmarking operadores de mutación...")
    for mut_type in mutation_types:
        # Población inicial
        population = create_population(pop_size, gene_length, min_val, max_val)
        best_fitness = float('-inf')
        
        for gen in range(num_gens):
            # Evaluar fitness
            fitness_values = np.array([fitness_function(ind, objective_function) for ind in population])
            
            # Actualizar mejor fitness
            gen_best = np.max(fitness_values)
            best_fitness = max(best_fitness, gen_best)
            
            # Selección
            parents = selection(population, fitness_values, pop_size // 2, default_sel)
            
            # Cruce
            offspring_size = (pop_size, gene_length)
            offspring = crossover(parents, offspring_size, default_cross)
            
            # Mutación
            offspring = mutation(offspring, 0.01, mut_type, min_val, max_val)
            
            # Nueva población
            population = offspring
        
        # Guardar resultado
        results['mutation'][mut_type] = best_fitness
    
    return results