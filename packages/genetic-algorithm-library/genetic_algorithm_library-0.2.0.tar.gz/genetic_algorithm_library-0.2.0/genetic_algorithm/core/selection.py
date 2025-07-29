import numpy as np
import random

def selection(population, fitness_values, num_parents, selection_type="tournament", tournament_size=3):
    """
    Selecciona individuos para reproducción utilizando diferentes métodos.
    
    Parámetros:
    -----------
    population : ndarray
        Población actual
    fitness_values : ndarray
        Valores de aptitud correspondientes a la población
    num_parents : int
        Número de padres a seleccionar
    selection_type : str
        Método de selección: "tournament", "roulette", "rank", "sus", "boltzmann"
    tournament_size : int
        Tamaño del torneo para selección por torneo
        
    Retorna:
    --------
    ndarray
        Padres seleccionados
    """
    parents = np.zeros((num_parents, population.shape[1]))
    
    if selection_type == "tournament":
        for i in range(num_parents):
            # Selección por torneo
            indices = np.random.choice(len(population), tournament_size, replace=False)
            tournament_fitness = [fitness_values[idx] for idx in indices]
            winner_idx = indices[np.argmax(tournament_fitness)]
            parents[i] = population[winner_idx]
    
    elif selection_type == "roulette":
        # Normalizar fitness para valores positivos
        fitness_min = min(0, np.min(fitness_values))
        normalized_fitness = fitness_values - fitness_min + 1e-10  # Evitar valores exactamente en cero
        
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
    
    elif selection_type == "sus":
        # Selección Universal Estocástica
        fitness_min = min(0, np.min(fitness_values))
        normalized_fitness = fitness_values - fitness_min + 1e-10
        
        # Calcular proporción acumulada
        sum_fitness = np.sum(normalized_fitness)
        if sum_fitness == 0:
            return population[np.random.choice(len(population), num_parents, replace=False)]
            
        probs = normalized_fitness / sum_fitness
        cumsum = np.cumsum(probs)
        
        # Seleccionar con intervalos uniformes
        step = 1.0 / num_parents
        start = np.random.uniform(0, step)
        points = [start + i * step for i in range(num_parents)]
        
        indices = []
        for point in points:
            idx = np.searchsorted(cumsum, point)
            if idx >= len(population):
                idx = len(population) - 1
            indices.append(idx)
        
        parents = population[indices]
    
    elif selection_type == "boltzmann":
        # Selección de Boltzmann (con temp. adaptativa)
        # Temperatura alta (inicio) -> más exploración
        # Temperatura baja (final) -> más explotación
        temp = max(0.1, 1.0 - np.std(fitness_values) / (np.mean(fitness_values) + 1e-10))
        
        # Calcular probabilidades usando función exponencial
        exp_values = np.exp(fitness_values / temp)
        probs = exp_values / np.sum(exp_values)
        
        indices = np.random.choice(len(population), num_parents, p=probs)
        parents = population[indices]
    
    else:
        raise ValueError(f"Tipo de selección '{selection_type}' no reconocido")
    
    return parents