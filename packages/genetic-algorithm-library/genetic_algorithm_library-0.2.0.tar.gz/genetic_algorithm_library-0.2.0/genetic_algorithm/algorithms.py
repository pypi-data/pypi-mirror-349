import numpy as np
import time
from .core.population import create_population, check_population_diversity
from .core.selection import selection
from .core.crossover import crossover
from .core.mutation import mutation, adaptive_mutation
from .core.fitness import fitness_function, multi_objective_fitness, get_pareto_front

def run_genetic_algorithm(objective_function, gene_length, bounds=(0, 1), 
                         pop_size=100, num_generations=100, 
                         selection_type="tournament", crossover_type="uniform",
                         mutation_type="gaussian", mutation_rate=0.01,
                         encoding="real", adaptive=True, elitism=True,
                         verbose=True, early_stopping=None, callbacks=None):
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
        Método de selección: "tournament", "roulette", "rank", "sus"
    crossover_type : str
        Tipo de cruce: "uniform", "single_point", "two_point", "blend"
    mutation_type : str
        Tipo de mutación: "gaussian", "uniform", "reset", "swap" (para permutación)
    mutation_rate : float
        Tasa inicial de mutación
    encoding : str
        Tipo de codificación: "real", "binary", "integer", "permutation"
    adaptive : bool
        Si es True, la tasa de mutación se adapta durante la ejecución
    elitism : bool
        Si es True, conserva el mejor individuo en cada generación
    verbose : bool
        Si es True, muestra información durante la ejecución
    early_stopping : int
        Detener el algoritmo si no hay mejora después de cierto número de generaciones
    callbacks : list
        Lista de funciones a llamar en cada generación
        
    Retorna:
    --------
    dict
        Diccionario con resultados: mejor individuo, mejor fitness, historia
    """
    min_val, max_val = bounds
    
    # Crear población inicial
    population = create_population(pop_size, gene_length, min_val, max_val, encoding=encoding)
    
    # Historial para seguimiento
    history = {
        'best_fitness': [],
        'avg_fitness': [],
        'best_individual': [],
        'mutation_rate': [],
        'diversity': [],
        'execution_time': []
    }
    
    best_individual = None
    best_fitness = float('-inf')
    generations_without_improvement = 0
    
    # Tiempo de inicio
    start_time = time.time()
    
    # Algoritmo principal
    for generation in range(num_generations):
        # Tiempo de esta generación
        gen_start_time = time.time()
        
        # Calcular aptitud para cada individuo
        fitness_values = np.array([fitness_function(ind, objective_function) for ind in population])
        
        # Encontrar el mejor individuo de esta generación
        gen_best_idx = np.argmax(fitness_values)
        gen_best_individual = population[gen_best_idx].copy()
        gen_best_fitness = fitness_values[gen_best_idx]
        
        # Calcular diversidad de la población
        diversity = check_population_diversity(population)
        
        # Actualizar el mejor global si es necesario
        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best_individual = gen_best_individual.copy()
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        
        # Tiempo de ejecución de esta generación
        gen_time = time.time() - gen_start_time
        
        # Guardar historial
        history['best_fitness'].append(gen_best_fitness)
        history['avg_fitness'].append(np.mean(fitness_values))
        history['best_individual'].append(gen_best_individual.copy())
        history['mutation_rate'].append(mutation_rate)
        history['diversity'].append(diversity)
        history['execution_time'].append(gen_time)
        
        # Mostrar progreso
        if verbose and (generation % 10 == 0 or generation == num_generations - 1):
            print(f"Generación {generation+1}/{num_generations}: "
                  f"Mejor Fitness = {gen_best_fitness:.6f}, "
                  f"Fitness Promedio = {np.mean(fitness_values):.6f}, "
                  f"Diversidad = {diversity:.4f}, "
                  f"Tasa de Mutación = {mutation_rate:.6f}")
        
        # Ejecutar callbacks personalizados
        if callbacks:
            for callback in callbacks:
                callback(generation, population, fitness_values, best_individual, 
                        best_fitness, history)
        
        # Verificar early stopping
        if early_stopping and generations_without_improvement >= early_stopping:
            if verbose:
                print(f"Early stopping después de {generations_without_improvement} "
                      f"generaciones sin mejora.")
            break
        
        # Seleccionar padres
        parents = selection(population, fitness_values, pop_size // 2, selection_type)
        
        # Cruce
        if elitism:
            # Reservar espacio para el mejor individuo (elitismo)
            offspring_size = (pop_size - 1, gene_length)
        else:
            offspring_size = (pop_size, gene_length)
            
        offspring = crossover(parents, offspring_size, crossover_type)
        
        # Mutación
        if adaptive:
            # Mutación adaptativa basada en fitness
            offspring = adaptive_mutation(
                offspring, 
                np.array([fitness_function(ind, objective_function) for ind in offspring]),
                best_fitness, 
                np.mean(fitness_values),
                min_val, 
                max_val,
                mutation_rate,
                encoding
            )
        else:
            # Mutación estándar
            offspring = mutation(offspring, mutation_rate, mutation_type, min_val, max_val, encoding)
        
        # Adaptación de la tasa de mutación global
        if adaptive:
            # Si hay mejora, reducir la tasa de mutación
            if len(history['best_fitness']) > 1 and history['best_fitness'][-1] > history['best_fitness'][-2]:
                mutation_rate = max(0.001, mutation_rate * 0.95)
            else:
                # Si no hay mejora, aumentar la tasa de mutación
                mutation_rate = min(0.2, mutation_rate * 1.05)
        
        # Crear nueva población
        if elitism:
            # Incluir el mejor individuo (elitismo)
            population = np.vstack([best_individual.reshape(1, -1), offspring])
        else:
            population = offspring
    
    # Tiempo total de ejecución
    total_time = time.time() - start_time
    
    # Resultados finales
    results = {
        'best_individual': best_individual,
        'best_fitness': best_fitness,
        'history': history,
        'generations': generation + 1,
        'execution_time': total_time,
        'final_diversity': history['diversity'][-1]
    }
    
    if verbose:
        print("\nOptimización completada:")
        print(f"Generaciones ejecutadas: {generation + 1}")
        print(f"Tiempo total: {total_time:.2f} segundos")
        print(f"Mejor Fitness: {best_fitness:.6f}")
        print(f"Mejor Individuo: {best_individual}")
        print(f"Diversidad Final: {history['diversity'][-1]:.4f}")
    
    return results

def run_multi_objective_ga(objective_functions, gene_length, bounds=(0, 1),
                          pop_size=100, num_generations=100,
                          selection_type="tournament", crossover_type="uniform",
                          mutation_type="gaussian", mutation_rate=0.01,
                          encoding="real", verbose=True):
    """
    Ejecuta un algoritmo genético multi-objetivo.
    
    Parámetros:
    -----------
    objective_functions : list
        Lista de funciones objetivo a optimizar
    gene_length : int
        Longitud del genoma de cada individuo
    bounds : tuple
        Límites de valores para los genes (min, max)
    pop_size : int
        Tamaño de la población
    num_generations : int
        Número de generaciones a ejecutar
    selection_type : str
        Método de selección
    crossover_type : str
        Tipo de cruce
    mutation_type : str
        Tipo de mutación
    mutation_rate : float
        Tasa de mutación
    encoding : str
        Tipo de codificación
    verbose : bool
        Si es True, muestra información durante la ejecución
        
    Retorna:
    --------
    dict
        Diccionario con resultados
    """
    min_val, max_val = bounds
    
    # Crear población inicial
    population = create_population(pop_size, gene_length, min_val, max_val, encoding=encoding)
    
    # Historial
    history = {
        'pareto_front': [],
        'pareto_fitness': [],
        'diversity': []
    }
    
    # Algoritmo principal
    for generation in range(num_generations):
        # Evaluar individuos en todos los objetivos
        fitness_matrix = np.array([
            multi_objective_fitness(ind, objective_functions) for ind in population
        ])
        
        # Obtener frente de Pareto
        _, pareto_front, pareto_fitness = get_pareto_front(population, fitness_matrix)
        
        # Calcular diversidad
        diversity = check_population_diversity(population)
        
        # Guardar historial
        history['pareto_front'].append(pareto_front.copy())
        history['pareto_fitness'].append(pareto_fitness.copy())
        history['diversity'].append(diversity)
        
        # Mostrar progreso
        if verbose and (generation % 10 == 0 or generation == num_generations - 1):
            print(f"Generación {generation+1}/{num_generations}: "
                  f"Tamaño del frente de Pareto = {len(pareto_front)}, "
                  f"Diversidad = {diversity:.4f}")
        
        # Selección basada en no-dominancia
        # (Implementación simplificada de NSGA-II)
        
        # Calcular rangos basados en dominancia de Pareto
        ranks = np.zeros(pop_size)
        remaining = list(range(pop_size))
        
        rank_idx = 0
        while remaining:
            # Encontrar frente actual
            current_front = []
            for i in remaining:
                dominated = False
                for j in remaining:
                    if i != j and np.all(fitness_matrix[j] >= fitness_matrix[i]) and np.any(fitness_matrix[j] > fitness_matrix[i]):
                        dominated = True
                        break
                if not dominated:
                    current_front.append(i)
            
            # Asignar rango actual
            for idx in current_front:
                ranks[idx] = rank_idx
                remaining.remove(idx)
            
            rank_idx += 1
        
        # Seleccionar padres con mayor probabilidad para rangos menores
        weights = 1.0 / (ranks + 1.0)
        parents_idx = np.random.choice(
            pop_size, size=pop_size // 2, replace=True, 
            p=weights / np.sum(weights)
        )
        parents = population[parents_idx]
        
        # Cruce
        offspring_size = (pop_size, gene_length)
        offspring = crossover(parents, offspring_size, crossover_type)
        
        # Mutación
        offspring = mutation(offspring, mutation_rate, mutation_type, min_val, max_val, encoding)
        
        # Nueva población
        population = offspring
    
    # Evaluar población final
    final_fitness_matrix = np.array([
        multi_objective_fitness(ind, objective_functions) for ind in population
    ])
    
    # Obtener frente de Pareto final
    _, final_pareto_front, final_pareto_fitness = get_pareto_front(population, final_fitness_matrix)
    
    # Resultados finales
    results = {
        'pareto_front': final_pareto_front,
        'pareto_fitness': final_pareto_fitness,
        'history': history
    }
    
    if verbose:
        print("\nOptimización Multi-objetivo completada:")
        print(f"Tamaño del frente de Pareto final: {len(final_pareto_front)}")
    
    return results

def run_island_model_ga(objective_function, gene_length, bounds=(0, 1),
                       num_islands=4, pop_size_per_island=50, num_generations=100,
                       migration_interval=10, migration_rate=0.1,
                       selection_types=None, crossover_types=None, mutation_types=None,
                       encoding="real", verbose=True):
    """
    Ejecuta un algoritmo genético con modelo de islas.
    
    Parámetros:
    -----------
    objective_function : callable
        Función objetivo a optimizar
    gene_length : int
        Longitud del genoma de cada individuo
    bounds : tuple
        Límites de valores para los genes (min, max)
    num_islands : int
        Número de islas (subpoblaciones)
    pop_size_per_island : int
        Tamaño de población en cada isla
    num_generations : int
        Número de generaciones a ejecutar
    migration_interval : int
        Intervalo de generaciones entre migraciones
    migration_rate : float
        Proporción de individuos que migran
    selection_types : list
        Lista de métodos de selección para cada isla
    crossover_types : list
        Lista de tipos de cruce para cada isla
    mutation_types : list
        Lista de tipos de mutación para cada isla
    encoding : str
        Tipo de codificación
    verbose : bool
        Si es True, muestra información durante la ejecución
        
    Retorna:
    --------
    dict
        Diccionario con resultados
    """
    min_val, max_val = bounds
    
    # Configurar operadores por isla
    if selection_types is None:
        selection_types = ["tournament", "roulette", "rank", "sus"]
    if crossover_types is None:
        crossover_types = ["uniform", "single_point", "two_point", "blend"]
    if mutation_types is None:
        mutation_types = ["gaussian", "uniform", "reset", "creep"]
    
    # Asegurar que hay suficientes operadores
    selection_types = (selection_types * num_islands)[:num_islands]
    crossover_types = (crossover_types * num_islands)[:num_islands]
    mutation_types = (mutation_types * num_islands)[:num_islands]
    
    # Inicializar islas
    islands = [create_population(pop_size_per_island, gene_length, min_val, max_val, encoding=encoding) 
              for _ in range(num_islands)]
    
    # Tasas de mutación por isla (algunas más exploradoras, otras más explotadoras)
    mutation_rates = [0.01 * (1 + 0.5 * i / num_islands) for i in range(num_islands)]
    
    # Historial global
    global_history = {
        'best_fitness': [],
        'avg_fitness': [],
        'best_individual': [],
        'island_best_fitness': [[] for _ in range(num_islands)]
    }
    
    # Mejor individuo global
    best_individual = None
    best_fitness = float('-inf')
    
    # Algoritmo principal
    for generation in range(num_generations):
        # Procesar cada isla
        for island_idx in range(num_islands):
            # Población actual
            population = islands[island_idx]
            
            # Evaluar fitness
            fitness_values = np.array([fitness_function(ind, objective_function) for ind in population])
            
            # Mejor individuo de esta isla
            island_best_idx = np.argmax(fitness_values)
            island_best_individual = population[island_best_idx].copy()
            island_best_fitness = fitness_values[island_best_idx]
            
            # Actualizar mejor global si es necesario
            if island_best_fitness > best_fitness:
                best_fitness = island_best_fitness
                best_individual = island_best_individual.copy()
            
            # Guardar historial de esta isla
            global_history['island_best_fitness'][island_idx].append(island_best_fitness)
            
            # Seleccionar padres
            parents = selection(
                population, 
                fitness_values, 
                pop_size_per_island // 2, 
                selection_types[island_idx]
            )
            
            # Cruce
            offspring_size = (pop_size_per_island, gene_length)
            offspring = crossover(
                parents, 
                offspring_size, 
                crossover_types[island_idx]
            )
            
            # Mutación
            offspring = mutation(
                offspring, 
                mutation_rates[island_idx], 
                mutation_types[island_idx], 
                min_val, 
                max_val, 
                encoding
            )
            
            # Actualizar población de esta isla
            islands[island_idx] = offspring
        
        # Migración entre islas
        if generation % migration_interval == 0 and generation > 0:
            # Número de individuos para migrar
            num_migrants = max(1, int(pop_size_per_island * migration_rate))
            
            # Realizar migración en anillo (isla i -> isla i+1)
            for island_idx in range(num_islands):
                # Origen y destino
                source_island = islands[island_idx]
                target_island_idx = (island_idx + 1) % num_islands
                
                # Seleccionar mejores individuos para migrar
                source_fitness = np.array([fitness_function(ind, objective_function) for ind in source_island])
                migrant_indices = np.argsort(source_fitness)[-num_migrants:]
                migrants = source_island[migrant_indices].copy()
                
                # Seleccionar individuos a reemplazar en la isla destino
                target_fitness = np.array([fitness_function(ind, objective_function) for ind in islands[target_island_idx]])
                replace_indices = np.argsort(target_fitness)[:num_migrants]
                
                # Realizar migración
                for i, migrant in enumerate(migrants):
                    islands[target_island_idx][replace_indices[i]] = migrant
        
        # Estadísticas globales
        all_individuals = np.vstack(islands)
        all_fitness = np.array([fitness_function(ind, objective_function) for ind in all_individuals])
        avg_fitness = np.mean(all_fitness)
        
        # Guardar historial global
        global_history['best_fitness'].append(best_fitness)
        global_history['avg_fitness'].append(avg_fitness)
        global_history['best_individual'].append(best_individual.copy())
        
        # Mostrar progreso
        if verbose and (generation % 10 == 0 or generation == num_generations - 1):
            island_bests = [max(global_history['island_best_fitness'][i]) for i in range(num_islands)]
            print(f"Generación {generation+1}/{num_generations}: "
                  f"Mejor Fitness Global = {best_fitness:.6f}, "
                  f"Fitness Promedio = {avg_fitness:.6f}")
            if verbose > 1:
                print(f"Mejores por isla: {[f'{x:.4f}' for x in island_bests]}")
    
    # Resultados finales
    results = {
        'best_individual': best_individual,
        'best_fitness': best_fitness,
        'history': global_history,
        'final_islands': islands
    }
    
    if verbose:
        print("\nOptimización con Modelo de Islas completada:")
        print(f"Mejor Fitness: {best_fitness:.6f}")
        print(f"Mejor Individuo: {best_individual}")
    
    return results