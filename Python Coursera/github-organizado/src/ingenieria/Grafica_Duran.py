# Script de gráficos y visualización de datos
# Especialidad: Ingeniería / Visualización
# Herramientas para crear gráficos profesionales de ingeniería

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
import seaborn as sns
from typing import List, Tuple, Optional, Dict, Any
import pandas as pd

class VisualizadorIngenieria:
    """
    Clase para crear visualizaciones profesionales de ingeniería
    Incluye gráficos técnicos, diagramas y análisis visual de datos
    """
    
    def __init__(self, estilo: str = "ingenieria"):
        """
        Inicializa el visualizador con un estilo específico.
        
        Args:
            estilo: Estilo de gráficos ('ingenieria', 'presentacion', 'publicacion')
        """
        self.estilo = estilo
        self.configurar_estilo()
        self.colores_ingenieria = {
            'azul_tecnico': '#1f77b4',
            'naranja_energia': '#ff7f0e',
            'verde_eficiencia': '#2ca02c',
            'rojo_alerta': '#d62728',
            'purpura_control': '#9467bd',
            'marron_material': '#8c564b',
            'gris_analisis': '#7f7f7f',
            'amarillo_optimizacion': '#bcbd22'
        }
    
    def configurar_estilo(self):
        """Configura el estilo de matplotlib para gráficos de ingeniería."""
        if self.estilo == "ingenieria":
            plt.style.use('default')
            plt.rcParams.update({
                'font.size': 10,
                'font.family': 'serif',
                'axes.linewidth': 1.2,
                'axes.grid': True,
                'grid.alpha': 0.3,
                'grid.linestyle': '--',
                'figure.dpi': 300,
                'savefig.dpi': 300,
                'savefig.bbox': 'tight'
            })
        elif self.estilo == "presentacion":
            plt.style.use('seaborn-v0_8')
            plt.rcParams.update({
                'font.size': 12,
                'figure.dpi': 150
            })
        elif self.estilo == "publicacion":
            plt.style.use('default')
            plt.rcParams.update({
                'font.size': 8,
                'font.family': 'serif',
                'axes.linewidth': 0.8,
                'figure.dpi': 600,
                'savefig.dpi': 600
            })
    
    def grafico_curva_caracteristica(self, x: np.ndarray, y: np.ndarray, 
                                   titulo: str = "Curva Característica",
                                   xlabel: str = "Variable X", 
                                   ylabel: str = "Variable Y",
                                   punto_operacion: Optional[Tuple[float, float]] = None,
                                   zona_optima: Optional[Tuple[float, float]] = None) -> plt.Figure:
        """
        Crea un gráfico de curva característica con elementos técnicos.
        
        Args:
            x: Datos del eje X
            y: Datos del eje Y
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            punto_operacion: Punto de operación (x, y)
            zona_optima: Zona óptima (x_min, x_max)
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Curva principal
        ax.plot(x, y, color=self.colores_ingenieria['azul_tecnico'], 
               linewidth=2, label='Curva Característica')
        
        # Punto de operación
        if punto_operacion:
            x_op, y_op = punto_operacion
            ax.plot(x_op, y_op, 'ro', markersize=8, label='Punto de Operación')
            ax.annotate(f'({x_op:.2f}, {y_op:.2f})', 
                       xy=(x_op, y_op), xytext=(10, 10),
                       textcoords='offset points', fontsize=9,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Zona óptima
        if zona_optima:
            x_min, x_max = zona_optima
            y_min = np.min(y)
            y_max = np.max(y)
            
            rect = Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                           facecolor=self.colores_ingenieria['verde_eficiencia'],
                           alpha=0.2, label='Zona Óptima')
            ax.add_patch(rect)
            
            # Líneas verticales de límites
            ax.axvline(x=x_min, color=self.colores_ingenieria['verde_eficiencia'], 
                      linestyle='--', alpha=0.7)
            ax.axvline(x=x_max, color=self.colores_ingenieria['verde_eficiencia'], 
                      linestyle='--', alpha=0.7)
        
        # Configuración del gráfico
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def grafico_comparativo_multiples(self, datos: Dict[str, Tuple[np.ndarray, np.ndarray]], 
                                    titulo: str = "Comparación de Curvas",
                                    xlabel: str = "Variable X",
                                    ylabel: str = "Variable Y") -> plt.Figure:
        """
        Crea un gráfico comparativo de múltiples curvas.
        
        Args:
            datos: Diccionario con {nombre: (x, y)} para cada curva
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colores = list(self.colores_ingenieria.values())
        
        for i, (nombre, (x, y)) in enumerate(datos.items()):
            color = colores[i % len(colores)]
            ax.plot(x, y, color=color, linewidth=2, label=nombre, marker='o', markersize=4)
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        return fig
    
    def grafico_contorno_2d(self, x: np.ndarray, y: np.ndarray, z: np.ndarray,
                           titulo: str = "Mapa de Contorno",
                           xlabel: str = "Variable X",
                           ylabel: str = "Variable Y",
                           niveles: int = 20) -> plt.Figure:
        """
        Crea un mapa de contorno 2D para análisis de campos escalares.
        
        Args:
            x: Coordenadas X (1D o 2D)
            y: Coordenadas Y (1D o 2D)
            z: Valores de la función (2D)
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            niveles: Número de niveles de contorno
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Crear malla si es necesario
        if x.ndim == 1:
            X, Y = np.meshgrid(x, y)
        else:
            X, Y = x, y
        
        # Mapa de contorno
        contour = ax.contourf(X, Y, z, levels=niveles, cmap='viridis', alpha=0.8)
        contour_lines = ax.contour(X, Y, z, levels=niveles, colors='black', alpha=0.5, linewidths=0.5)
        
        # Barra de color
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('Valor', fontsize=12, fontweight='bold')
        
        # Configuración
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        return fig
    
    def grafico_histograma_estadistico(self, datos: np.ndarray, 
                                     titulo: str = "Distribución de Datos",
                                     xlabel: str = "Valor",
                                     ylabel: str = "Frecuencia",
                                     bins: int = 30) -> plt.Figure:
        """
        Crea un histograma con análisis estadístico.
        
        Args:
            datos: Datos a analizar
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            bins: Número de bins del histograma
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Histograma
        n, bins_edges, patches = ax.hist(datos, bins=bins, alpha=0.7, 
                                       color=self.colores_ingenieria['azul_tecnico'],
                                       edgecolor='black', linewidth=0.5)
        
        # Línea de media
        media = np.mean(datos)
        ax.axvline(media, color=self.colores_ingenieria['rojo_alerta'], 
                  linewidth=2, linestyle='--', label=f'Media: {media:.2f}')
        
        # Línea de mediana
        mediana = np.median(datos)
        ax.axvline(mediana, color=self.colores_ingenieria['verde_eficiencia'], 
                  linewidth=2, linestyle='--', label=f'Mediana: {mediana:.2f}')
        
        # Estadísticas en texto
        desv_std = np.std(datos)
        stats_text = f'Media: {media:.2f}\nDesv. Est.: {desv_std:.2f}\nMin: {np.min(datos):.2f}\nMax: {np.max(datos):.2f}'
        
        ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, 
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def grafico_diagrama_fase(self, x: np.ndarray, y: np.ndarray,
                             titulo: str = "Diagrama de Fase",
                             xlabel: str = "Variable X",
                             ylabel: str = "Variable Y",
                             puntos_equilibrio: Optional[List[Tuple[float, float]]] = None) -> plt.Figure:
        """
        Crea un diagrama de fase para análisis de sistemas dinámicos.
        
        Args:
            x: Coordenadas X de las trayectorias
            y: Coordenadas Y de las trayectorias
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            puntos_equilibrio: Lista de puntos de equilibrio
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Trayectorias
        ax.plot(x, y, color=self.colores_ingenieria['azul_tecnico'], 
               linewidth=1.5, alpha=0.8)
        
        # Puntos de equilibrio
        if puntos_equilibrio:
            for i, (x_eq, y_eq) in enumerate(puntos_equilibrio):
                ax.plot(x_eq, y_eq, 'ro', markersize=8, 
                       label=f'Equilibrio {i+1}' if i == 0 else f'')
                ax.annotate(f'E{i+1}', xy=(x_eq, y_eq), xytext=(5, 5),
                           textcoords='offset points', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.axis('equal')
        
        return fig
    
    def grafico_serie_temporal(self, tiempo: np.ndarray, valores: np.ndarray,
                              titulo: str = "Serie Temporal",
                              xlabel: str = "Tiempo",
                              ylabel: str = "Valor",
                              eventos: Optional[Dict[str, float]] = None) -> plt.Figure:
        """
        Crea un gráfico de serie temporal con análisis de eventos.
        
        Args:
            tiempo: Vector de tiempo
            valores: Valores de la serie temporal
            titulo: Título del gráfico
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            eventos: Diccionario de eventos {nombre: tiempo}
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Serie temporal
        ax.plot(tiempo, valores, color=self.colores_ingenieria['azul_tecnico'], 
               linewidth=2, label='Serie Temporal')
        
        # Eventos
        if eventos:
            for nombre, t_evento in eventos.items():
                # Encontrar el valor más cercano al tiempo del evento
                idx = np.argmin(np.abs(tiempo - t_evento))
                valor_evento = valores[idx]
                
                ax.plot(t_evento, valor_evento, 'ro', markersize=8)
                ax.annotate(nombre, xy=(t_evento, valor_evento), 
                           xytext=(10, 10), textcoords='offset points',
                           fontsize=9, bbox=dict(boxstyle='round,pad=0.3', 
                                               facecolor='white', alpha=0.8))
        
        # Líneas de referencia
        media = np.mean(valores)
        ax.axhline(media, color=self.colores_ingenieria['gris_analisis'], 
                  linestyle='--', alpha=0.7, label=f'Media: {media:.2f}')
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def guardar_grafico(self, fig: plt.Figure, nombre_archivo: str, 
                       formato: str = 'png', dpi: int = 300):
        """
        Guarda el gráfico en un archivo.
        
        Args:
            fig: Figura de matplotlib
            nombre_archivo: Nombre del archivo
            formato: Formato de salida ('png', 'pdf', 'svg')
            dpi: Resolución para formatos raster
        """
        fig.savefig(f"{nombre_archivo}.{formato}", dpi=dpi, bbox_inches='tight')
        print(f"Gráfico guardado como: {nombre_archivo}.{formato}")

# Ejemplos de uso
def ejemplo_curva_caracteristica():
    """Ejemplo de curva característica de una bomba."""
    print("=== Ejemplo: Curva Característica de Bomba ===")
    
    # Datos de ejemplo
    caudal = np.linspace(0, 100, 50)  # L/min
    altura = 50 * (1 - (caudal/100)**2)  # m
    
    # Crear visualizador
    vis = VisualizadorIngenieria()
    
    # Gráfico con punto de operación y zona óptima
    fig = vis.grafico_curva_caracteristica(
        caudal, altura,
        titulo="Curva Característica de Bomba Centrífuga",
        xlabel="Caudal (L/min)",
        ylabel="Altura (m)",
        punto_operacion=(60, 32),
        zona_optima=(40, 80)
    )
    
    plt.show()
    return fig

def ejemplo_comparacion_curvas():
    """Ejemplo de comparación de múltiples curvas."""
    print("\n=== Ejemplo: Comparación de Curvas ===")
    
    # Datos de ejemplo
    x = np.linspace(0, 10, 100)
    
    datos = {
        'Bomba A': (x, 50 * np.exp(-x/5)),
        'Bomba B': (x, 40 * np.exp(-x/3)),
        'Bomba C': (x, 60 * np.exp(-x/7))
    }
    
    vis = VisualizadorIngenieria()
    fig = vis.grafico_comparativo_multiples(
        datos,
        titulo="Comparación de Eficiencias de Bombas",
        xlabel="Tiempo (horas)",
        ylabel="Eficiencia (%)"
    )
    
    plt.show()
    return fig

if __name__ == "__main__":
    # Ejecutar ejemplos
    ejemplo_curva_caracteristica()
    ejemplo_comparacion_curvas()
