"""
Funciones de prueba estándar para optimización continua.
Estas funciones son ampliamente utilizadas para evaluar algoritmos de optimización.
"""

import numpy as np

def sphere(x):
    """
    Función Sphere (De Jong's function 1).
    Mínimo global: f(0,...,0) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    return -np.sum(x**2)

def rosenbrock(x):
    """
    Función Rosenbrock (De Jong's function 2).
    Mínimo global: f(1,...,1) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    result = 0
    for i in range(len(x) - 1):
        result += 100 * (x[i+1] - x[i]**2)**2 + (x[i] - 1)**2
    return -result

def rastrigin(x):
    """
    Función Rastrigin.
    Mínimo global: f(0,...,0) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    n = len(x)
    result = 10 * n
    for i in range(n):
        result += x[i]**2 - 10 * np.cos(2 * np.pi * x[i])
    return -result

def schwefel(x):
    """
    Función Schwefel.
    Mínimo global: f(420.9687,...,420.9687) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    n = len(x)
    result = 0
    for i in range(n):
        result += x[i] * np.sin(np.sqrt(np.abs(x[i])))
    return -418.9829 * n + result

def griewank(x):
    """
    Función Griewank.
    Mínimo global: f(0,...,0) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    part1 = np.sum(x**2) / 4000
    part2 = 1
    for i in range(len(x)):
        part2 *= np.cos(x[i] / np.sqrt(i+1))
    return -(part1 - part2 + 1)

def ackley(x):
    """
    Función Ackley.
    Mínimo global: f(0,...,0) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    a = 20
    b = 0.2
    c = 2 * np.pi
    n = len(x)
    
    part1 = -a * np.exp(-b * np.sqrt(np.sum(x**2) / n))
    part2 = -np.exp(np.sum(np.cos(c * x)) / n)
    
    return -(part1 + part2 + a + np.exp(1))

def levy(x):
    """
    Función Levy.
    Mínimo global: f(1,...,1) = 0
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    n = len(x)
    z = 1 + (x - 1) / 4
    
    term1 = np.sin(np.pi * z[0])**2
    
    term2 = np.sum((z[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * z[:-1] + 1)**2))
    
    term3 = (z[-1] - 1)**2 * (1 + np.sin(2 * np.pi * z[-1])**2)
    
    return -(term1 + term2 + term3)

def michalewicz(x):
    """
    Función Michalewicz.
    Es un problema de minimización con múltiples mínimos locales.
    
    Parámetros:
    -----------
    x : array-like
        Vector de variables de decisión
        
    Retorna:
    --------
    float
        Valor de la función (negativo para maximización)
    """
    m = 10  # Parámetro de control de la pendiente
    result = 0
    for i in range(len(x)):
        result += np.sin(x[i]) * np.sin((i+1) * x[i]**2 / np.pi)**(2*m)
    return -result

def get_function(name):
    """
    Obtiene una función de prueba por su nombre.
    
    Parámetros:
    -----------
    name : str
        Nombre de la función de prueba
        
    Retorna:
    --------
    callable
        Función de prueba
    """
    functions = {
        "sphere": sphere,
        "rosenbrock": rosenbrock,
        "rastrigin": rastrigin,
        "schwefel": schwefel,
        "griewank": griewank,
        "ackley": ackley,
        "levy": levy,
        "michalewicz": michalewicz
    }
    
    if name not in functions:
        raise ValueError(f"Función '{name}' no reconocida")
    
    return functions[name]