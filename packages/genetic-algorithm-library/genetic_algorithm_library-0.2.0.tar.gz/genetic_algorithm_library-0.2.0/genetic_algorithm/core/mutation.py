import numpy as np
import random

def mutation(offspring, mutation_rate=0.01, mutation_type="gaussian", min_val=0, max_val=1, encoding="real"):
    """
    Aplica mutación a la descendencia.
    
    Parámetros:
    -----------
    offspring : ndarray
        Descendencia a mutar
    mutation_rate : float
        Tasa de mutación (probabilidad de que un gen mute)
    mutation_type : str
        Tipo de mutación: "gaussian", "uniform", "reset", "swap", "inversion"
    min_val : float
        Valor mínimo para los genes (para mutación uniforme o reset)
    max_val : float
        Valor máximo para los genes (para mutación uniforme o reset)
    encoding : str
        Tipo de codificación: "real", "binary", "integer", "permutation"
        
    Retorna:
    --------
    ndarray
        Descendencia mutada
    """
    mutated_offspring = offspring.copy()
    
    # Crear máscara de mutación
    mutation_mask = np.random.random(offspring.shape) < mutation_rate
    
    if encoding == "permutation":
        # Mutación para problemas de permutación
        for i in range(len(offspring)):
            if np.random.random() < mutation_rate:
                if mutation_type == "swap":
                    # Mutación por intercambio
                    idx1, idx2 = np.random.choice(len(offspring[i]), 2, replace=False)
                    mutated_offspring[i, idx1], mutated_offspring[i, idx2] = \
                        mutated_offspring[i, idx2], mutated_offspring[i, idx1]
                
                elif mutation_type == "inversion":
                    # Mutación por inversión
                    idx1, idx2 = sorted(np.random.choice(len(offspring[i]), 2, replace=False))
                    mutated_offspring[i, idx1:idx2+1] = mutated_offspring[i, idx1:idx2+1][::-1]
                
                elif mutation_type == "insertion":
                    # Mutación por inserción
                    idx1, idx2 = np.random.choice(len(offspring[i]), 2, replace=False)
                    if idx1 > idx2:
                        idx1, idx2 = idx2, idx1
                    
                    # Extraer valor y reorganizar
                    value = mutated_offspring[i, idx2]
                    mutated_offspring[i] = np.roll(mutated_offspring[i], -1, axis=0)
                    mutated_offspring[i, idx1] = value
    
    elif encoding == "binary":
        # Mutación para codificación binaria
        mutated_offspring[mutation_mask] = 1 - mutated_offspring[mutation_mask]
    
    else:
        # Mutación para codificación real o entera
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
        
        elif mutation_type == "creep":
            # Mutación de tipo "creep" (pequeño incremento o decremento)
            creep_size = 0.05 * (max_val - min_val)
            creep_values = np.random.uniform(-creep_size, creep_size, offspring.shape)
            mutated_offspring[mutation_mask] += creep_values[mutation_mask]
    
    # Asegurar que los valores estén dentro de los límites
    if encoding != "permutation":
        np.clip(mutated_offspring, min_val, max_val, out=mutated_offspring)
    
    # Convertir a entero si es necesario
    if encoding == "integer":
        mutated_offspring = np.round(mutated_offspring).astype(int)
    
    return mutated_offspring

def adaptive_mutation(offspring, fitness_values, best_fitness, avg_fitness, min_val=0, max_val=1, 
                      base_rate=0.01, encoding="real"):
    """
    Aplica mutación adaptativa basada en el fitness.
    
    Parámetros:
    -----------
    offspring : ndarray
        Descendencia a mutar
    fitness_values : ndarray
        Valores de aptitud correspondientes a la descendencia
    best_fitness : float
        Mejor valor de fitness en la población
    avg_fitness : float
        Valor promedio de fitness en la población
    min_val : float
        Valor mínimo para los genes
    max_val : float
        Valor máximo para los genes
    base_rate : float
        Tasa base de mutación
    encoding : str
        Tipo de codificación
        
    Retorna:
    --------
    ndarray
        Descendencia mutada con tasa adaptativa
    """
    mutated_offspring = offspring.copy()
    
    # Para cada individuo en la descendencia
    for i in range(len(offspring)):
        # Calcular tasa adaptativa
        if fitness_values[i] <= avg_fitness:
            # Aumentar mutación para individuos debajo del promedio
            k = 1.0
        else:
            # Disminuir mutación para los mejores individuos
            k = (best_fitness - fitness_values[i]) / (best_fitness - avg_fitness + 1e-10)
        
        # Calcular tasa adaptativa (más alta para individuos peores)
        adaptive_rate = base_rate * (1 + 0.5 * k)
        
        # Aplicar mutación con tasa adaptativa
        mutation_mask = np.random.random(offspring[i].shape) < adaptive_rate
        
        if encoding == "binary":
            # Mutación binaria
            mutated_offspring[i, mutation_mask] = 1 - mutated_offspring[i, mutation_mask]
        
        elif encoding == "permutation":
            # Para permutaciones, aplicar swap
            if np.sum(mutation_mask) > 0:
                # Al menos un gen para mutar
                idx1 = np.random.choice(np.where(mutation_mask)[0])
                idx2 = np.random.choice(len(offspring[i]))
                while idx2 == idx1:
                    idx2 = np.random.choice(len(offspring[i]))
                
                # Intercambiar valores
                mutated_offspring[i, idx1], mutated_offspring[i, idx2] = \
                    mutated_offspring[i, idx2], mutated_offspring[i, idx1]
        
        else:
            # Mutación gaussiana adaptativa
            if np.sum(mutation_mask) > 0:
                # La intensidad de la mutación también es adaptativa
                sigma = 0.1 * (max_val - min_val) * (1 + k)
                noise = np.random.normal(0, sigma, offspring[i].shape)
                mutated_offspring[i, mutation_mask] += noise[mutation_mask]
                
                # Mantener dentro de límites
                np.clip(mutated_offspring[i], min_val, max_val, out=mutated_offspring[i])
                
                # Convertir a entero si es necesario
                if encoding == "integer":
                    mutated_offspring[i] = np.round(mutated_offspring[i]).astype(int)
    
    return mutated_offspring

def self_adaptation(offspring, mutation_params, learning_rate=0.1):
    """
    Implementa auto-adaptación donde los parámetros de mutación
    evolucionan junto con los individuos.
    
    Parámetros:
    -----------
    offspring : ndarray
        Descendencia a mutar
    mutation_params : ndarray
        Parámetros de mutación actuales para cada individuo
    learning_rate : float
        Tasa de aprendizaje para la adaptación
        
    Retorna:
    --------
    tuple
        (offspring_mutada, nuevos_parametros_mutacion)
    """
    mutated_offspring = offspring.copy()
    new_params = mutation_params.copy()
    
    # Actualizar parámetros de mutación usando regla log-normal
    for i in range(len(offspring)):
        # Auto-adaptación de los parámetros
        new_params[i] *= np.exp(learning_rate * np.random.normal())
        
        # Limitar los parámetros de mutación
        new_params[i] = np.clip(new_params[i], 0.001, 0.5)
        
        # Aplicar mutación usando los nuevos parámetros
        mutation_mask = np.random.random(offspring[i].shape) < new_params[i]
        if np.sum(mutation_mask) > 0:
            # Mutación gaussiana con intensidad adaptativa
            noise = np.random.normal(0, 0.1, offspring[i].shape)
            mutated_offspring[i, mutation_mask] += noise[mutation_mask]
    
    return mutated_offspring, new_params