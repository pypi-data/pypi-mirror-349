"""
Problemas de optimización discretos.
Implementaciones para problemas estándar con variables discretas.
"""

import numpy as np

def knapsack_problem(values, weights, capacity):
    """
    Crea una función objetivo para el problema de la mochila.
    
    Parámetros:
    -----------
    values : array-like
        Valores de los objetos
    weights : array-like
        Pesos de los objetos
    capacity : float
        Capacidad de la mochila
        
    Retorna:
    --------
    callable
        Función objetivo para el problema de la mochila
    """
    def objective_function(x):
        # x es un vector binario que indica si se incluye o no cada objeto
        x_bin = np.round(x).astype(int)  # Asegurar que es binario
        
        total_value = np.sum(values * x_bin)
        total_weight = np.sum(weights * x_bin)
        
        # Penalizar si se excede la capacidad
        if total_weight > capacity:
            return -1000  # Penalización severa
        
        return total_value
    
    return objective_function

def max_cut_problem(graph_matrix):
    """
    Crea una función objetivo para el problema Max-Cut.
    
    Parámetros:
    -----------
    graph_matrix : ndarray
        Matriz de adyacencia del grafo
        
    Retorna:
    --------
    callable
        Función objetivo para el problema Max-Cut
    """
    def objective_function(x):
        # x es un vector binario que indica a qué lado del corte pertenece cada nodo
        x_bin = np.round(x).astype(int)
        
        cut_size = 0
        n = len(x_bin)
        
        for i in range(n):
            for j in range(i+1, n):
                # Si están en lados diferentes y hay una arista entre ellos
                if x_bin[i] != x_bin[j] and graph_matrix[i, j] > 0:
                    cut_size += graph_matrix[i, j]
        
        return cut_size
    
    return objective_function

def bin_packing_problem(item_sizes, bin_capacity, num_bins):
    """
    Crea una función objetivo para el problema de empaquetado en contenedores.
    
    Parámetros:
    -----------
    item_sizes : array-like
        Tamaños de los elementos a empaquetar
    bin_capacity : float
        Capacidad de cada contenedor
    num_bins : int
        Número máximo de contenedores
        
    Retorna:
    --------
    callable
        Función objetivo para el problema de empaquetado
    """
    def objective_function(x):
        # x es un vector que indica a qué contenedor va cada elemento
        bin_assignment = np.round(x).astype(int) % num_bins
        
        # Calcular ocupación de cada contenedor
        bin_loads = np.zeros(num_bins)
        for i, bin_idx in enumerate(bin_assignment):
            bin_loads[bin_idx] += item_sizes[i]
        
        # Penalizar si se excede la capacidad
        overloaded = np.sum(np.maximum(0, bin_loads - bin_capacity))
        
        # Objetivo: minimizar el número de contenedores usados
        bins_used = len(np.where(bin_loads > 0)[0])
        
        # Maximizar equilibrio de carga (desviación estándar negativa)
        balance = -np.std(bin_loads)
        
        # Valor final: combinación ponderada
        if overloaded > 0:
            return -1000 * overloaded  # Penalización severa
        else:
            return -bins_used + 0.1 * balance
    
    return objective_function

def vehicle_routing_problem(distance_matrix, demands, vehicle_capacity):
    """
    Crea una función objetivo para el problema de enrutamiento de vehículos.
    
    Parámetros:
    -----------
    distance_matrix : ndarray
        Matriz de distancias entre nodos
    demands : array-like
        Demandas de cada cliente (nodo)
    vehicle_capacity : float
        Capacidad de cada vehículo
        
    Retorna:
    --------
    callable
        Función objetivo para el problema de enrutamiento
    """
    def objective_function(x):
        # x es una permutación de los nodos a visitar, con 0 representando el depósito
        # e inserciones de 0 indicando el inicio de una nueva ruta
        
        route = np.round(x).astype(int) % len(distance_matrix)
        
        # Asegurar que el primer nodo es el depósito (0)
        if route[0] != 0:
            route = np.hstack([[0], route])
        
        # Calcular distancia total
        total_distance = 0
        
        # Calcular carga de cada vehículo
        vehicle_load = 0
        overload = 0
        
        for i in range(len(route) - 1):
            node1 = route[i]
            node2 = route[i+1]
            
            # Añadir distancia
            total_distance += distance_matrix[node1, node2]
            
            # Si es el depósito, reiniciar la carga
            if node1 == 0:
                vehicle_load = 0
            
            # Actualizar carga
            vehicle_load += demands[node1]
            
            # Comprobar sobrecarga
            if vehicle_load > vehicle_capacity:
                overload += vehicle_load - vehicle_capacity
                
        # Asegurar que la ruta termina en el depósito
        if route[-1] != 0:
            total_distance += distance_matrix[route[-1], 0]
        
        # Objetivo: minimizar distancia sin sobrecargar
        if overload > 0:
            return -1000 * overload - total_distance
        else:
            return -total_distance
    
    return objective_function