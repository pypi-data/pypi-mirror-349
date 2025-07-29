import numpy as np
import random

def create_population(size, gene_length, min_val=0, max_val=1, encoding="real"):
    """
    Crea una población inicial de individuos con diferentes tipos de codificación.
    
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
    encoding : str
        Tipo de codificación: "real", "binary", "integer", "permutation"
        
    Retorna:
    --------
    ndarray
        Población inicial de tamaño (size, gene_length)
    """
    if encoding == "real":
        # Codificación de valores reales (float)
        return np.random.uniform(min_val, max_val, (size, gene_length))
    
    elif encoding == "binary":
        # Codificación binaria (0 o 1)
        return np.random.randint(0, 2, (size, gene_length))
    
    elif encoding == "integer":
        # Codificación de enteros
        return np.random.randint(int(min_val), int(max_val) + 1, (size, gene_length))
    
    elif encoding == "permutation":
        # Codificación de permutación (útil para TSP y problemas similares)
        population = np.zeros((size, gene_length), dtype=int)
        for i in range(size):
            population[i] = np.random.permutation(gene_length)
        return population
    
    else:
        raise ValueError(f"Tipo de codificación '{encoding}' no reconocido")

def initialize_from_samples(samples, size, noise=0.1):
    """
    Inicializa una población a partir de muestras conocidas.
    Útil cuando se tienen soluciones aproximadas o se quiere
    explorar alrededor de soluciones conocidas.
    
    Parámetros:
    -----------
    samples : ndarray
        Muestras conocidas que guiarán la inicialización
    size : int
        Tamaño de la población a crear
    noise : float
        Cantidad de ruido a añadir a las muestras (0.1 = 10%)
        
    Retorna:
    --------
    ndarray
        Población inicial basada en las muestras
    """
    if not isinstance(samples, np.ndarray):
        samples = np.array(samples)
    
    num_samples = samples.shape[0]
    gene_length = samples.shape[1]
    
    # Crear población inicial
    population = np.zeros((size, gene_length))
    
    # Copiar muestras directamente (elitismo)
    for i in range(min(num_samples, size)):
        population[i] = samples[i % num_samples]
    
    # Generar el resto con variaciones
    for i in range(num_samples, size):
        # Seleccionar una muestra aleatoria
        sample_idx = np.random.randint(0, num_samples)
        base_sample = samples[sample_idx].copy()
        
        # Añadir ruido gaussiano
        if noise > 0:
            noise_values = np.random.normal(0, noise, gene_length)
            population[i] = base_sample + noise_values
        else:
            population[i] = base_sample
    
    return population

def check_population_diversity(population, threshold=0.01):
    """
    Evalúa la diversidad de la población actual.
    
    Parámetros:
    -----------
    population : ndarray
        Población a evaluar
    threshold : float
        Umbral para considerar dos individuos como similares
        
    Retorna:
    --------
    float
        Índice de diversidad (0-1, donde 1 es máxima diversidad)
    """
    size = population.shape[0]
    unique_count = 0
    
    # Aproximación rápida: muestrear pares aleatorios
    sample_size = min(500, size * (size - 1) // 2)
    
    if size <= 1:
        return 0.0
    
    for _ in range(sample_size):
        i, j = np.random.choice(size, 2, replace=False)
        if np.mean(np.abs(population[i] - population[j])) > threshold:
            unique_count += 1
    
    return unique_count / sample_size