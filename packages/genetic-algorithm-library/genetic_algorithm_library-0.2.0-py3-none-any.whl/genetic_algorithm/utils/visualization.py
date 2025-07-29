import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm

def plot_evolution(history):
    """
    Visualiza la evolución del algoritmo genético.
    
    Parámetros:
    -----------
    history : dict
        Diccionario con historiales de la ejecución
    """
    generations = range(1, len(history['best_fitness']) + 1)
    
    plt.figure(figsize=(12, 10))
    
    # Gráfica de fitness
    plt.subplot(3, 1, 1)
    plt.plot(generations, history['best_fitness'], 'b-', label='Mejor Fitness')
    plt.plot(generations, history['avg_fitness'], 'r--', label='Fitness Promedio')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del Fitness')
    plt.legend()
    plt.grid(True)
    
    # Gráfica de tasa de mutación
    if 'mutation_rate' in history and history['mutation_rate']:
        plt.subplot(3, 1, 2)
        plt.plot(generations, history['mutation_rate'], 'g-')
        plt.xlabel('Generación')
        plt.ylabel('Tasa de Mutación')
        plt.title('Adaptación de la Tasa de Mutación')
        plt.grid(True)
    
    # Gráfica de diversidad
    if 'diversity' in history and history['diversity']:
        plt.subplot(3, 1, 3)
        plt.plot(generations, history['diversity'], 'm-')
        plt.xlabel('Generación')
        plt.ylabel('Índice de Diversidad')
        plt.title('Diversidad de la Población')
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def plot_pareto_front(pareto_fitness, objective_names=None, title="Frente de Pareto"):
    """
    Visualiza el frente de Pareto para problemas multi-objetivo.
    
    Parámetros:
    -----------
    pareto_fitness : ndarray
        Matriz con los valores de fitness de las soluciones no dominadas
    objective_names : list
        Nombres de los objetivos para las etiquetas
    title : str
        Título del gráfico
    """
    num_objectives = pareto_fitness.shape[1]
    
    if objective_names is None:
        objective_names = [f"Objetivo {i+1}" for i in range(num_objectives)]
    
    # Comprobar dimensiones
    if num_objectives == 2:
        # Caso 2D - gráfico simple
        plt.figure(figsize=(10, 8))
        plt.scatter(pareto_fitness[:, 0], pareto_fitness[:, 1], c='blue', s=50, alpha=0.7)
        plt.xlabel(objective_names[0])
        plt.ylabel(objective_names[1])
        plt.title(title)
        plt.grid(True)
        
    elif num_objectives == 3:
        # Caso 3D
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Colorear puntos según distancia al origen
        distances = np.sqrt(np.sum(pareto_fitness**2, axis=1))
        
        # Normalizar para colores
        min_dist, max_dist = np.min(distances), np.max(distances)
        if max_dist > min_dist:
            normalized = (distances - min_dist) / (max_dist - min_dist)
        else:
            normalized = np.zeros_like(distances)
        
        # Visualizar puntos
        sc = ax.scatter(
            pareto_fitness[:, 0],
            pareto_fitness[:, 1],
            pareto_fitness[:, 2],
            c=normalized,
            cmap='viridis',
            s=50,
            alpha=0.8
        )
        
        # Etiquetas
        ax.set_xlabel(objective_names[0])
        ax.set_ylabel(objective_names[1])
        ax.set_zlabel(objective_names[2])
        ax.set_title(title)
        
        # Barra de color
        cbar = plt.colorbar(sc, ax=ax, pad=0.1)
        cbar.set_label('Distancia Normalizada')
        
    else:
        # Más de 3 objetivos - matriz de dispersión
        fig, axes = plt.subplots(
            nrows=num_objectives, 
            ncols=num_objectives, 
            figsize=(3*num_objectives, 3*num_objectives)
        )
        
        # Dibujar gráficos
        for i in range(num_objectives):
            for j in range(num_objectives):
                ax = axes[i, j]
                
                if i == j:
                    # Diagonal - histograma
                    ax.hist(pareto_fitness[:, i], bins=10, alpha=0.7)
                    ax.set_title(objective_names[i])
                else:
                    # Fuera de la diagonal - dispersión
                    ax.scatter(pareto_fitness[:, j], pareto_fitness[:, i], alpha=0.5)
                    
                    # Solo poner etiquetas en los bordes
                    if i == num_objectives - 1:
                        ax.set_xlabel(objective_names[j])
                    if j == 0:
                        ax.set_ylabel(objective_names[i])
        
        plt.suptitle(title, fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    plt.show()

def plot_population_diversity(history, title="Diversidad de la Población"):
    """
    Visualiza la diversidad de la población a lo largo de las generaciones.
    
    Parámetros:
    -----------
    history : dict
        Diccionario con historiales de la ejecución
    title : str
        Título del gráfico
    """
    if 'diversity' not in history or not history['diversity']:
        print("Error: No hay datos de diversidad en el historial.")
        return
    
    generations = range(1, len(history['diversity']) + 1)
    
    plt.figure(figsize=(10, 6))
    
    # Gráfica de diversidad
    plt.plot(generations, history['diversity'], 'b-', linewidth=2)
    
    # Si hay datos de fitness, añadir eje secundario
    if 'best_fitness' in history and history['best_fitness']:
        ax1 = plt.gca()
        ax2 = ax1.twinx()
        
        # Graficar fitness en eje secundario
        ax2.plot(generations, history['best_fitness'], 'r--', linewidth=1.5, alpha=0.7)
        ax2.set_ylabel('Mejor Fitness', color='r')
        ax2.tick_params(axis='y', colors='r')
        
        # Leyenda combinada
        from matplotlib.lines import Line2D
        lines = [
            Line2D([0], [0], color='b', linewidth=2),
            Line2D([0], [0], color='r', linestyle='--', linewidth=1.5)
        ]
        labels = ['Diversidad', 'Mejor Fitness']
        plt.legend(lines, labels, loc='upper right')
    
    plt.xlabel('Generación')
    plt.ylabel('Índice de Diversidad')
    plt.title(title)
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def animate_evolution(history, interval=200, save_path=None):
    """
    Crea una animación de la evolución de la población.
    
    Parámetros:
    -----------
    history : dict
        Diccionario con historiales de la ejecución
    interval : int
        Intervalo entre frames (ms)
    save_path : str
        Ruta para guardar la animación (None = no guardar)
    """
    # Verificar si hay datos de individuos
    if 'best_individual' not in history or not history['best_individual']:
        print("Error: No hay datos de individuos en el historial.")
        return
    
    # Obtener dimensiones
    num_generations = len(history['best_individual'])
    gene_length = len(history['best_individual'][0])
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.tight_layout(pad=3.0)
    
    # Generar datos
    generations = list(range(1, num_generations + 1))
    
    # Inicializar gráficos
    line1, = ax1.plot([], [], 'b-', linewidth=2, label='Mejor Fitness')
    line2, = ax1.plot([], [], 'r--', linewidth=1.5, label='Fitness Promedio')
    
    # Barras para el mejor individuo
    bars = ax2.bar(
        range(gene_length), 
        [0] * gene_length, 
        color='green', 
        alpha=0.7
    )
    
    # Configuración de ejes
    ax1.set_xlim(1, num_generations)
    
    # Determinar límites de fitness
    max_fitness = max(history['best_fitness'])
    min_fitness = min([min(history['best_fitness']), min(history['avg_fitness'])])
    y_margin = (max_fitness - min_fitness) * 0.1
    
    ax1.set_ylim(min_fitness - y_margin, max_fitness + y_margin)
    ax1.set_xlabel('Generación')
    ax1.set_ylabel('Fitness')
    ax1.set_title('Evolución del Fitness')
    ax1.legend()
    ax1.grid(True)
    
    # Configuración para las barras de genes
    gene_values = np.array(history['best_individual'])
    min_gene, max_gene = np.min(gene_values), np.max(gene_values)
    y_margin_gene = (max_gene - min_gene) * 0.1
    
    ax2.set_ylim(min_gene - y_margin_gene, max_gene + y_margin_gene)
    ax2.set_xlabel('Gen')
    ax2.set_ylabel('Valor')
    ax2.set_title('Mejor Individuo')
    ax2.grid(True)
    
    # Función de inicialización
    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        for bar in bars:
            bar.set_height(0)
        return line1, line2, *bars
    
    # Función de animación
    def animate(i):
        # Datos para las líneas
        x = generations[:i+1]
        y1 = history['best_fitness'][:i+1]
        y2 = history['avg_fitness'][:i+1]
        
        line1.set_data(x, y1)
        line2.set_data(x, y2)
        
        # Datos para las barras
        best_individual = history['best_individual'][i]
        for j, bar in enumerate(bars):
            bar.set_height(best_individual[j])
        
        # Actualizar título con generación actual
        ax2.set_title(f'Mejor Individuo - Generación {i+1}')
        
        return line1, line2, *bars
    
    # Crear animación
    anim = FuncAnimation(
        fig, 
        animate, 
        frames=num_generations,
        init_func=init,
        interval=interval,
        blit=True
    )
    
    # Guardar si se especifica ruta
    if save_path:
        anim.save(save_path, writer='pillow', fps=10)
    
    plt.show()
    
    return anim

def plot_island_model(history, num_islands):
    """
    Visualiza los resultados del modelo de islas.
    
    Parámetros:
    -----------
    history : dict
        Diccionario con historiales de la ejecución
    num_islands : int
        Número de islas
    """
    generations = range(1, len(history['best_fitness']) + 1)
    
    plt.figure(figsize=(12, 9))
    
    # Gráfica de fitness global
    plt.subplot(2, 1, 1)
    plt.plot(generations, history['best_fitness'], 'k-', linewidth=2, label='Mejor Global')
    plt.plot(generations, history['avg_fitness'], 'k--', linewidth=1.5, label='Promedio Global')
    
    # Fitness por isla
    colors = cm.viridis(np.linspace(0, 1, num_islands))
    
    for i in range(num_islands):
        plt.plot(
            generations, 
            history['island_best_fitness'][i], 
            '-', 
            color=colors[i], 
            alpha=0.7,
            linewidth=1.2,
            label=f'Isla {i+1}'
        )
    
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Comparación de Fitness entre Islas')
    plt.legend()
    plt.grid(True)
    
    # Gráfico de radar para comparar islas
    if len(generations) > 0:
        ax = plt.subplot(2, 1, 2, polar=True)
        
        # Métricas para comparar (último valor de cada isla)
        metrics = ["Mejor Fitness", "Fitness Final", "Mejora", "Variabilidad"]
        num_metrics = len(metrics)
        
        # Calcular métricas para cada isla
        island_metrics = np.zeros((num_islands, num_metrics))
        
        for i in range(num_islands):
            # Mejor fitness alcanzado
            island_metrics[i, 0] = max(history['island_best_fitness'][i])
            
            # Fitness final
            island_metrics[i, 1] = history['island_best_fitness'][i][-1]
            
            # Mejora (final - inicial)
            if len(history['island_best_fitness'][i]) > 1:
                island_metrics[i, 2] = (history['island_best_fitness'][i][-1] - 
                                    history['island_best_fitness'][i][0])
            
            # Variabilidad (desviación estándar)
            island_metrics[i, 3] = np.std(history['island_best_fitness'][i])
        
        # Normalizar métricas para gráfico radar
        island_metrics_norm = island_metrics.copy()
        for j in range(num_metrics):
            min_val = np.min(island_metrics[:, j])
            max_val = np.max(island_metrics[:, j])
            if max_val > min_val:
                island_metrics_norm[:, j] = (island_metrics[:, j] - min_val) / (max_val - min_val)
            else:
                island_metrics_norm[:, j] = 0.5  # Valor por defecto si no hay variación
        
        # Ángulos para el gráfico radar
        angles = np.linspace(0, 2*np.pi, num_metrics, endpoint=False).tolist()
        angles += angles[:1]  # Cerrar el círculo
        
        # Completar valores para cerrar el polígono
        island_metrics_norm_closed = np.zeros((num_islands, num_metrics+1))
        for i in range(num_islands):
            values = island_metrics_norm[i].tolist()
            values += values[:1]
            island_metrics_norm_closed[i] = values
        
        # Dibujar para cada isla
        for i in range(num_islands):
            ax.plot(angles, island_metrics_norm_closed[i], '-', linewidth=2, color=colors[i], label=f'Isla {i+1}')
            ax.fill(angles, island_metrics_norm_closed[i], color=colors[i], alpha=0.1)
        
        # Configurar gráfico radar
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics)
        ax.set_title('Comparación de Rendimiento entre Islas')
        
        # Leyenda
        plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
    
    plt.tight_layout()
    plt.show()