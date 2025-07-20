"""
Sistema de Graficación Avanzado para Ingeniería - Graph Durant
=============================================================

Este módulo proporciona herramientas avanzadas de visualización para aplicaciones de ingeniería,
incluyendo gráficos 2D y 3D, análisis de datos, y presentación profesional de resultados.

Aplicaciones:
- Visualización de datos de ingeniería
- Análisis de tendencias
- Presentación de resultados técnicos
- Creación de reportes profesionales

Autor: Ingeniería Mecánica
Versión: 2.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, Circle, Polygon
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple, Dict, Optional, Union
import pandas as pd


class GraphDurant:
    """
    Sistema avanzado de graficación para ingeniería
    """
    
    def __init__(self, estilo: str = "ingenieria"):
        """
        Inicializa el sistema de graficación
        
        Args:
            estilo: Estilo de gráficos ('ingenieria', 'presentacion', 'publicacion')
        """
        self.estilo = estilo
        self.configurar_estilo()
        self.figuras = {}
        self.datos = {}
        
    def configurar_estilo(self):
        """Configura el estilo de los gráficos según el tipo seleccionado"""
        if self.estilo == "ingenieria":
            plt.style.use('default')
            plt.rcParams.update({
                'figure.figsize': (10, 6),
                'font.size': 12,
                'axes.grid': True,
                'grid.alpha': 0.3,
                'axes.labelsize': 14,
                'axes.titlesize': 16,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
                'legend.fontsize': 12,
                'lines.linewidth': 2,
                'lines.markersize': 6
            })
        elif self.estilo == "presentacion":
            plt.style.use('seaborn-v0_8')
            plt.rcParams.update({
                'figure.figsize': (12, 8),
                'font.size': 14,
                'axes.grid': True,
                'grid.alpha': 0.2,
                'axes.labelsize': 16,
                'axes.titlesize': 18,
                'xtick.labelsize': 14,
                'ytick.labelsize': 14,
                'legend.fontsize': 14,
                'lines.linewidth': 3,
                'lines.markersize': 8
            })
        elif self.estilo == "publicacion":
            plt.style.use('seaborn-v0_8-paper')
            plt.rcParams.update({
                'figure.figsize': (8, 6),
                'font.size': 10,
                'axes.grid': False,
                'axes.labelsize': 12,
                'axes.titlesize': 14,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'legend.fontsize': 10,
                'lines.linewidth': 1.5,
                'lines.markersize': 4
            })
    
    def grafico_lineal_avanzado(self, x: List[float], y: List[float], 
                               titulo: str = "", etiqueta_x: str = "", etiqueta_y: str = "",
                               color: str = "blue", marcador: str = "o", 
                               mostrar_grid: bool = True, guardar: bool = False) -> None:
        """
        Crea un gráfico lineal avanzado con múltiples opciones de personalización
        
        Args:
            x: Datos del eje X
            y: Datos del eje Y
            titulo: Título del gráfico
            etiqueta_x: Etiqueta del eje X
            etiqueta_y: Etiqueta del eje Y
            color: Color de la línea
            marcador: Tipo de marcador
            mostrar_grid: Si mostrar cuadrícula
            guardar: Si guardar el gráfico
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Crear gráfico
        ax.plot(x, y, color=color, marker=marcador, linewidth=2, markersize=6, 
                label=f'Datos ({len(x)} puntos)')
        
        # Configurar ejes
        ax.set_xlabel(etiqueta_x, fontsize=14, fontweight='bold')
        ax.set_ylabel(etiqueta_y, fontsize=14, fontweight='bold')
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        
        # Configurar grid
        if mostrar_grid:
            ax.grid(True, alpha=0.3, linestyle='--')
        
        # Configurar leyenda
        ax.legend(fontsize=12, loc='best')
        
        # Ajustar límites
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y) * 0.95, max(y) * 1.05)
        
        # Agregar estadísticas
        stats_text = f'Media: {np.mean(y):.2f}\nDesv. Est.: {np.std(y):.2f}\nMín: {np.min(y):.2f}\nMáx: {np.max(y):.2f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        if guardar:
            plt.savefig(f'grafico_{titulo.replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def grafico_multiple_lineas(self, datos: Dict[str, Tuple[List[float], List[float]]], 
                               titulo: str = "", etiqueta_x: str = "", etiqueta_y: str = "",
                               colores: List[str] = None) -> None:
        """
        Crea un gráfico con múltiples líneas
        
        Args:
            datos: Diccionario con {nombre: (x, y)} para cada línea
            titulo: Título del gráfico
            etiqueta_x: Etiqueta del eje X
            etiqueta_y: Etiqueta del eje Y
            colores: Lista de colores para las líneas
        """
        if colores is None:
            colores = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        for i, (nombre, (x, y)) in enumerate(datos.items()):
            color = colores[i % len(colores)]
            ax.plot(x, y, color=color, marker='o', linewidth=2, markersize=4, 
                    label=nombre, alpha=0.8)
        
        ax.set_xlabel(etiqueta_x, fontsize=14, fontweight='bold')
        ax.set_ylabel(etiqueta_y, fontsize=14, fontweight='bold')
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=12, loc='best')
        
        plt.tight_layout()
        plt.show()
    
    def grafico_dispersion_3d(self, x: List[float], y: List[float], z: List[float],
                             titulo: str = "", etiqueta_x: str = "", etiqueta_y: str = "",
                             etiqueta_z: str = "", color: str = "blue") -> None:
        """
        Crea un gráfico de dispersión 3D
        
        Args:
            x, y, z: Coordenadas de los puntos
            titulo: Título del gráfico
            etiqueta_x, etiqueta_y, etiqueta_z: Etiquetas de los ejes
            color: Color de los puntos
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        scatter = ax.scatter(x, y, z, c=color, marker='o', s=50, alpha=0.6)
        
        ax.set_xlabel(etiqueta_x, fontsize=12, fontweight='bold')
        ax.set_ylabel(etiqueta_y, fontsize=12, fontweight='bold')
        ax.set_zlabel(etiqueta_z, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        # Agregar barra de color
        plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
        
        plt.tight_layout()
        plt.show()
    
    def grafico_superficie_3d(self, x: np.ndarray, y: np.ndarray, z: np.ndarray,
                             titulo: str = "", etiqueta_x: str = "", etiqueta_y: str = "",
                             etiqueta_z: str = "", colormap: str = "viridis") -> None:
        """
        Crea un gráfico de superficie 3D
        
        Args:
            x, y, z: Arrays 2D para las coordenadas y valores
            titulo: Título del gráfico
            etiqueta_x, etiqueta_y, etiqueta_z: Etiquetas de los ejes
            colormap: Mapa de colores
        """
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(x, y, z, cmap=colormap, alpha=0.8, linewidth=0, antialiased=True)
        
        ax.set_xlabel(etiqueta_x, fontsize=12, fontweight='bold')
        ax.set_ylabel(etiqueta_y, fontsize=12, fontweight='bold')
        ax.set_zlabel(etiqueta_z, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        # Agregar barra de color
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        
        plt.tight_layout()
        plt.show()
    
    def grafico_barras_apiladas(self, categorias: List[str], datos: Dict[str, List[float]],
                               titulo: str = "", etiqueta_x: str = "", etiqueta_y: str = "") -> None:
        """
        Crea un gráfico de barras apiladas
        
        Args:
            categorias: Lista de categorías en el eje X
            datos: Diccionario con {serie: valores} para cada serie
            titulo: Título del gráfico
            etiqueta_x: Etiqueta del eje X
            etiqueta_y: Etiqueta del eje Y
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Preparar datos para gráfico apilado
        x = np.arange(len(categorias))
        width = 0.8
        
        # Crear barras apiladas
        bottom = np.zeros(len(categorias))
        for serie, valores in datos.items():
            ax.bar(x, valores, width, bottom=bottom, label=serie, alpha=0.8)
            bottom += valores
        
        ax.set_xlabel(etiqueta_x, fontsize=14, fontweight='bold')
        ax.set_ylabel(etiqueta_y, fontsize=14, fontweight='bold')
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categorias, rotation=45, ha='right')
        ax.legend(fontsize=12, loc='best')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    def grafico_circular_avanzado(self, datos: Dict[str, float], titulo: str = "",
                                 mostrar_porcentajes: bool = True) -> None:
        """
        Crea un gráfico circular avanzado
        
        Args:
            datos: Diccionario con {etiqueta: valor}
            titulo: Título del gráfico
            mostrar_porcentajes: Si mostrar porcentajes en las etiquetas
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(datos.keys())
        sizes = list(datos.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        if mostrar_porcentajes:
            total = sum(sizes)
            autopct = lambda pct: f'{pct:.1f}%\n({pct*total/100:.1f})'
        else:
            autopct = '%1.1f%%'
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct=autopct,
                                         colors=colors, startangle=90, explode=[0.05]*len(labels))
        
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        
        # Mejorar apariencia de textos
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.show()
    
    def grafico_heatmap(self, datos: np.ndarray, etiquetas_x: List[str] = None,
                       etiquetas_y: List[str] = None, titulo: str = "",
                       colormap: str = "viridis") -> None:
        """
        Crea un mapa de calor (heatmap)
        
        Args:
            datos: Array 2D con los datos
            etiquetas_x: Etiquetas para el eje X
            etiquetas_y: Etiquetas para el eje Y
            titulo: Título del gráfico
            colormap: Mapa de colores
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(datos, cmap=colormap, aspect='auto')
        
        # Configurar etiquetas
        if etiquetas_x:
            ax.set_xticks(range(len(etiquetas_x)))
            ax.set_xticklabels(etiquetas_x, rotation=45, ha='right')
        if etiquetas_y:
            ax.set_yticks(range(len(etiquetas_y)))
            ax.set_yticklabels(etiquetas_y)
        
        ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
        
        # Agregar barra de color
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Valor', fontsize=12, fontweight='bold')
        
        # Agregar valores en las celdas
        for i in range(datos.shape[0]):
            for j in range(datos.shape[1]):
                text = ax.text(j, i, f'{datos[i, j]:.2f}',
                              ha="center", va="center", color="white", fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def crear_dashboard(self, datos: Dict[str, any], titulo: str = "Dashboard de Ingeniería") -> None:
        """
        Crea un dashboard completo con múltiples gráficos
        
        Args:
            datos: Diccionario con diferentes tipos de datos
            titulo: Título del dashboard
        """
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(titulo, fontsize=20, fontweight='bold')
        
        # Crear subplots
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Gráfico 1: Línea temporal
        if 'temporal' in datos:
            ax1 = fig.add_subplot(gs[0, :2])
            x, y = datos['temporal']
            ax1.plot(x, y, 'b-o', linewidth=2, markersize=6)
            ax1.set_title('Evolución Temporal', fontweight='bold')
            ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Distribución
        if 'distribucion' in datos:
            ax2 = fig.add_subplot(gs[0, 2])
            valores = datos['distribucion']
            ax2.hist(valores, bins=20, alpha=0.7, color='green', edgecolor='black')
            ax2.set_title('Distribución', fontweight='bold')
            ax2.grid(True, alpha=0.3)
        
        # Gráfico 3: Comparación
        if 'comparacion' in datos:
            ax3 = fig.add_subplot(gs[1, :])
            categorias, valores = datos['comparacion']
            ax3.bar(categorias, valores, color='orange', alpha=0.8)
            ax3.set_title('Comparación', fontweight='bold')
            ax3.tick_params(axis='x', rotation=45)
            ax3.grid(True, alpha=0.3)
        
        # Gráfico 4: Correlación
        if 'correlacion' in datos:
            ax4 = fig.add_subplot(gs[2, :2])
            x, y = datos['correlacion']
            ax4.scatter(x, y, alpha=0.6, color='red')
            ax4.set_title('Correlación', fontweight='bold')
            ax4.grid(True, alpha=0.3)
            
            # Agregar línea de tendencia
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            ax4.plot(x, p(x), "r--", alpha=0.8)
        
        # Gráfico 5: Resumen estadístico
        if 'estadisticas' in datos:
            ax5 = fig.add_subplot(gs[2, 2])
            ax5.axis('off')
            stats = datos['estadisticas']
            stats_text = '\n'.join([f'{k}: {v:.2f}' for k, v in stats.items()])
            ax5.text(0.1, 0.5, stats_text, transform=ax5.transAxes, fontsize=12,
                    verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.show()


def ejemplo_graficos_ingenieria():
    """
    Ejemplo de uso del sistema Graph Durant
    """
    print("📊 SISTEMA GRAPH DURANT - EJEMPLOS DE INGENIERÍA")
    print("=" * 60)
    
    # Crear instancia del sistema
    graph = GraphDurant(estilo="ingenieria")
    
    # Ejemplo 1: Gráfico lineal avanzado
    print("\n1. Gráfico Lineal Avanzado")
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-x/5)
    graph.grafico_lineal_avanzado(x, y, "Función Amortiguada", "Tiempo (s)", "Amplitud", "red", "o")
    
    # Ejemplo 2: Múltiples líneas
    print("\n2. Gráfico de Múltiples Líneas")
    datos_multiple = {
        "Serie A": (x, np.sin(x)),
        "Serie B": (x, np.cos(x)),
        "Serie C": (x, np.sin(x) * 0.5)
    }
    graph.grafico_multiple_lineas(datos_multiple, "Comparación de Funciones", "X", "Y")
    
    # Ejemplo 3: Gráfico 3D
    print("\n3. Gráfico de Dispersión 3D")
    x_3d = np.random.randn(50)
    y_3d = np.random.randn(50)
    z_3d = x_3d**2 + y_3d**2
    graph.grafico_dispersion_3d(x_3d, y_3d, z_3d, "Dispersión 3D", "X", "Y", "Z")
    
    # Ejemplo 4: Gráfico circular
    print("\n4. Gráfico Circular Avanzado")
    datos_circular = {
        "Componente A": 30,
        "Componente B": 25,
        "Componente C": 20,
        "Componente D": 15,
        "Componente E": 10
    }
    graph.grafico_circular_avanzado(datos_circular, "Distribución de Componentes")
    
    # Ejemplo 5: Heatmap
    print("\n5. Mapa de Calor")
    datos_heatmap = np.random.rand(8, 8)
    etiquetas = [f"Var_{i+1}" for i in range(8)]
    graph.grafico_heatmap(datos_heatmap, etiquetas, etiquetas, "Matriz de Correlación")
    
    # Ejemplo 6: Dashboard
    print("\n6. Dashboard Completo")
    datos_dashboard = {
        'temporal': (np.linspace(0, 10, 50), np.sin(np.linspace(0, 10, 50))),
        'distribucion': np.random.normal(0, 1, 1000),
        'comparacion': (['A', 'B', 'C', 'D'], [25, 30, 15, 30]),
        'correlacion': (np.random.randn(100), np.random.randn(100)),
        'estadisticas': {'Media': 0.1, 'Desv. Est.': 1.2, 'Mín': -3.5, 'Máx': 3.8}
    }
    graph.crear_dashboard(datos_dashboard, "Dashboard de Análisis de Datos")


def main():
    """
    Función principal del módulo
    """
    print("🔧 SISTEMA GRAPH DURANT - VISUALIZACIÓN AVANZADA")
    print("=" * 60)
    
    # Ejecutar ejemplos
    ejemplo_graficos_ingenieria()
    
    print("\n" + "=" * 60)
    print("✅ Sistema Graph Durant completado exitosamente!")
    print("\n📚 Características principales:")
    print("• Gráficos 2D y 3D profesionales")
    print("• Múltiples estilos de presentación")
    print("• Análisis estadístico integrado")
    print("• Dashboards completos")
    print("• Exportación de gráficos")
    print("• Personalización avanzada")


if __name__ == "__main__":
    main()
