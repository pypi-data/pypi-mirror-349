import numpy as np
import random

def crossover(parents, offspring_size, crossover_type="uniform", crossover_rate=0.8):
    """
    Realiza el cruce entre padres para crear descendencia.
    
    Parámetros:
    -----------
    parents : ndarray
        Arreglo de padres seleccionados
    offspring_size : tuple
        Tamaño de la descendencia: (n_offspring, n_genes)
    crossover_type : str
        Tipo de cruce: "uniform", "single_point", "two_point", "blend", "sbx", "pmx"
    crossover_rate : float
        Probabilidad de que ocurra el cruce
        
    Retorna:
    --------
    ndarray
        Descendencia generada
    """
    offspring = np.zeros(offspring_size)
    
    # Determinar tipo de datos para manejar correctamente los diferentes encodings
    dtype = parents.dtype
    offspring = offspring.astype(dtype)
    
    for i in range(offspring_size[0]):
        # Seleccionar padres aleatoriamente
        parent1_idx = i % parents.shape[0]
        parent2_idx = (i + 1) % parents.shape[0]
        
        # Aplicar crossover con cierta probabilidad
        if np.random.random() < crossover_rate:
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
            
            elif crossover_type == "blend":
                # Cruce por mezcla (blend) - para variables reales
                alpha = 0.5  # Parámetro de mezcla
                parent1 = parents[parent1_idx]
                parent2 = parents[parent2_idx]
                
                # Crear hijos como combinación lineal de los padres
                offspring[i] = parent1 + alpha * (parent2 - parent1)
            
            elif crossover_type == "sbx":
                # Cruce binario simulado (SBX) - para variables reales
                eta = 1.0  # Índice de distribución (más bajo = más diversidad)
                parent1 = parents[parent1_idx]
                parent2 = parents[parent2_idx]
                
                # Implementación simplificada de SBX
                for j in range(offspring_size[1]):
                    # Evitar división por cero
                    if abs(parent1[j] - parent2[j]) > 1e-10:
                        x1, x2 = min(parent1[j], parent2[j]), max(parent1[j], parent2[j])
                        beta = 1.0 + 2.0 * (x1 - 0) / (x2 - x1)
                        alpha = 2.0 - beta ** (-(eta + 1))
                        
                        u = np.random.random()
                        if u <= 1.0 / alpha:
                            beta_q = (u * alpha) ** (1.0 / (eta + 1))
                        else:
                            beta_q = (1.0 / (2.0 - u * alpha)) ** (1.0 / (eta + 1))
                        
                        # Crear hijo
                        if np.random.random() < 0.5:
                            offspring[i, j] = 0.5 * ((1 + beta_q) * x1 + (1 - beta_q) * x2)
                        else:
                            offspring[i, j] = 0.5 * ((1 - beta_q) * x1 + (1 + beta_q) * x2)
                    else:
                        offspring[i, j] = parent1[j]  # Padres iguales, copiar directamente
            
            elif crossover_type == "pmx":
                # Partially Mapped Crossover - para problemas de permutación (TSP)
                parent1 = parents[parent1_idx].copy()
                parent2 = parents[parent2_idx].copy()
                
                # Convertir a int para permutaciones
                parent1 = parent1.astype(int)
                parent2 = parent2.astype(int)
                
                # Puntos de cruce
                cx1, cx2 = sorted(np.random.choice(offspring_size[1] - 1, 2, replace=False) + 1)
                
                # Crear mapa de correspondencia
                mapping = {}
                for k in range(cx1, cx2):
                    mapping[parent2[k]] = parent1[k]
                    mapping[parent1[k]] = parent2[k]
                
                # Crear hijo
                child = np.full(offspring_size[1], -1, dtype=int)
                
                # Copiar segmento intermedio de parent2
                child[cx1:cx2] = parent2[cx1:cx2]
                
                # Rellenar el resto
                for k in range(offspring_size[1]):
                    if k < cx1 or k >= cx2:
                        item = parent1[k]
                        while item in child:
                            item = mapping.get(item, item)
                        child[k] = item
                
                offspring[i] = child
        else:
            # Si no hay cruce, copiar uno de los padres
            offspring[i] = parents[parent1_idx if np.random.random() < 0.5 else parent2_idx]
    
    return offspring

def crossover_permutation(parents, offspring_size, crossover_type="pmx"):
    """
    Función especializada para cruce de permutaciones (problemas como TSP).
    
    Parámetros:
    -----------
    parents : ndarray
        Arreglo de padres seleccionados (permutaciones)
    offspring_size : tuple
        Tamaño de la descendencia: (n_offspring, n_genes)
    crossover_type : str
        Tipo de cruce: "pmx", "ox", "cx"
        
    Retorna:
    --------
    ndarray
        Descendencia generada (permutaciones válidas)
    """
    offspring = np.zeros(offspring_size, dtype=int)
    
    for i in range(offspring_size[0]):
        # Seleccionar padres aleatoriamente
        parent1_idx = i % parents.shape[0]
        parent2_idx = (i + 1) % parents.shape[0]
        
        parent1 = parents[parent1_idx].copy()
        parent2 = parents[parent2_idx].copy()
        
        if crossover_type == "pmx":
            # Partially Mapped Crossover
            cx1, cx2 = sorted(np.random.choice(offspring_size[1] - 1, 2, replace=False) + 1)
            
            # Crear mapa de correspondencia
            mapping = {}
            for k in range(cx1, cx2):
                mapping[parent2[k]] = parent1[k]
                mapping[parent1[k]] = parent2[k]
            
            # Crear hijo
            child = np.full(offspring_size[1], -1, dtype=int)
            
            # Copiar segmento intermedio de parent2
            child[cx1:cx2] = parent2[cx1:cx2]
            
            # Rellenar el resto
            for k in range(offspring_size[1]):
                if k < cx1 or k >= cx2:
                    item = parent1[k]
                    while item in child:
                        item = mapping.get(item, item)
                    child[k] = item
        
        elif crossover_type == "ox":
            # Order Crossover
            cx1, cx2 = sorted(np.random.choice(offspring_size[1] - 1, 2, replace=False) + 1)
            
            # Crear hijo con -1 como marcador
            child = np.full(offspring_size[1], -1, dtype=int)
            
            # Paso 1: Copiar segmento de parent1
            child[cx1:cx2] = parent1[cx1:cx2]
            
            # Paso 2: Rellenar desde parent2 preservando el orden relativo
            remaining = [item for item in parent2 if item not in child]
            idx = 0
            
            for k in range(offspring_size[1]):
                if child[k] == -1:
                    child[k] = remaining[idx]
                    idx += 1
        
        elif crossover_type == "cx":
            # Cycle Crossover
            child = np.full(offspring_size[1], -1, dtype=int)
            
            # Implementación de Cycle Crossover
            cycles = []
            visited = np.zeros(offspring_size[1], dtype=bool)
            
            # Encontrar ciclos
            for i in range(offspring_size[1]):
                if not visited[i]:
                    cycle = []
                    j = i
                    while not visited[j]:
                        visited[j] = True
                        cycle.append(j)
                        # Encontrar posición del valor de parent2[j] en parent1
                        j = np.where(parent1 == parent2[j])[0][0]
                    
                    if cycle:
                        cycles.append(cycle)
            
            # Alternar ciclos entre los padres
            for idx, cycle in enumerate(cycles):
                if idx % 2 == 0:
                    for pos in cycle:
                        child[pos] = parent1[pos]
                else:
                    for pos in cycle:
                        child[pos] = parent2[pos]
            
            # Rellenar posiciones vacías (si existen)
            for k in range(offspring_size[1]):
                if child[k] == -1:
                    child[k] = parent1[k]
        
        offspring[i] = child
    
    return offspring