"""
Problemas de optimización combinatoria.
Herramientas específicas para problemas combinatorios como TSP, VRP, etc.
"""

import numpy as np
import matplotlib.pyplot as plt

def tsp_create_cities(num_cities, min_coord=0, max_coord=100, seed=None):
    """
    Genera ciudades aleatorias para el problema del viajante (TSP).
    
    Parámetros:
    -----------
    num_cities : int
        Número de ciudades a generar
    min_coord : float
        Coordenada mínima
    max_coord : float
        Coordenada máxima
    seed : int
        Semilla para reproducibilidad
        
    Retorna:
    --------
    ndarray
        Array de coordenadas (x, y) para cada ciudad
    """
    if seed is not None:
        np.random.seed(seed)
    
    cities = np.random.uniform(min_coord, max_coord, (num_cities, 2))
    return cities

def tsp_distance(route, cities):
    """
    Calcula la distancia total de una ruta TSP.
    
    Parámetros:
    -----------
    route : array-like
        Secuencia de ciudades a visitar (índices)
    cities : ndarray
        Coordenadas de las ciudades
        
    Retorna:
    --------
    float
        Distancia total de la ruta
    """
    total_distance = 0
    route = route.astype(int)
    
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1) % len(route)]
        
        distance = np.sqrt(np.sum((cities[city1] - cities[city2])**2))
        total_distance += distance
    
    return total_distance

def tsp_create_distance_matrix(cities):
    """
    Crea una matriz de distancias entre ciudades.
    
    Parámetros:
    -----------
    cities : ndarray
        Coordenadas de las ciudades
        
    Retorna:
    --------
    ndarray
        Matriz de distancias
    """
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i, j] = np.sqrt(np.sum((cities[i] - cities[j])**2))
    
    return distance_matrix

def tsp_plot_solution(cities, route, title="Solución TSP"):
    """
    Visualiza una solución al problema del viajante.
    
    Parámetros:
    -----------
    cities : ndarray
        Coordenadas de las ciudades
    route : array-like
        Secuencia de ciudades (índices)
    title : str
        Título del gráfico
    """
    plt.figure(figsize=(10, 8))
    
    # Convertir a enteros
    route = route.astype(int)
    
    # Dibujar ciudades
    plt.scatter(cities[:, 0], cities[:, 1], c='blue', s=100)
    
    # Numerar ciudades
    for i, (x, y) in enumerate(cities):
        plt.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points')
    
    # Dibujar ruta
    for i in range(len(route)):
        city1 = route[i]
        city2 = route[(i + 1) % len(route)]
        plt.plot([cities[city1, 0], cities[city2, 0]], 
                [cities[city1, 1], cities[city2, 1]], 'r-')
    
    # Destacar ciudad inicial/final
    plt.scatter(cities[route[0], 0], cities[route[0], 1], 
               c='green', s=200, alpha=0.5, label='Inicio/Fin')
    
    # Distancia total
    total_distance = tsp_distance(route, cities)
    
    plt.title(f"{title}\nDistancia Total: {total_distance:.2f}")
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()