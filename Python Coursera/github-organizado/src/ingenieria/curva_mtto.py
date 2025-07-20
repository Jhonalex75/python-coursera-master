# -----------------------------------------------------------------------------
# Purpose: Plot the "bathtub curve" representing failure rates over equipment life (infant mortality, useful life, wear-out).
# Application: Maintenance engineering, reliability analysis.
# Dependencies: numpy, matplotlib
# Usage: Run the script to display the bathtub curve.
# -----------------------------------------------------------------------------
# Script de análisis de confiabilidad y mantenimiento
# Especialidad: Ingeniería de Mantenimiento

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min, expon, norm
from typing import Dict, List, Tuple, Optional
import pandas as pd

class AnalizadorConfiabilidad:
    """
    Clase para análisis de confiabilidad y curvas de falla
    Incluye la curva de bañera y análisis de distribución de fallas
    """
    
    def __init__(self):
        """Inicializa el analizador de confiabilidad."""
        self.datos_fallas = []
        self.parametros_curva = {}
        
    def curva_banera(self, tiempo_max: float = 100, 
                    tasa_falla_inicial: float = 0.1,
                    tasa_falla_estable: float = 0.02,
                    tasa_falla_desgaste: float = 0.15,
                    tiempo_transicion_1: float = 10,
                    tiempo_transicion_2: float = 70) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera la curva de bañera (bathtub curve) para análisis de confiabilidad.
        
        Args:
            tiempo_max: Tiempo máximo de análisis
            tasa_falla_inicial: Tasa de falla en mortalidad infantil
            tasa_falla_estable: Tasa de falla en vida útil
            tasa_falla_desgaste: Tasa de falla en desgaste
            tiempo_transicion_1: Tiempo de transición a vida útil
            tiempo_transicion_2: Tiempo de inicio del desgaste
            
        Returns:
            Tuple con tiempos y tasas de falla
        """
        tiempo = np.linspace(0, tiempo_max, 1000)
        tasa_falla = np.zeros_like(tiempo)
        
        # Fase 1: Mortalidad infantil (decreciente)
        mask_1 = tiempo <= tiempo_transicion_1
        tasa_falla[mask_1] = tasa_falla_inicial * np.exp(-tiempo[mask_1] / tiempo_transicion_1)
        
        # Fase 2: Vida útil (constante)
        mask_2 = (tiempo > tiempo_transicion_1) & (tiempo <= tiempo_transicion_2)
        tasa_falla[mask_2] = tasa_falla_estable
        
        # Fase 3: Desgaste (creciente)
        mask_3 = tiempo > tiempo_transicion_2
        tiempo_desgaste = tiempo[mask_3] - tiempo_transicion_2
        tasa_falla[mask_3] = tasa_falla_estable + (tasa_falla_desgaste - tasa_falla_estable) * \
                            (tiempo_desgaste / (tiempo_max - tiempo_transicion_2))**2
        
        return tiempo, tasa_falla
    
    def graficar_curva_banera(self, tiempo: np.ndarray, tasa_falla: np.ndarray,
                             titulo: str = "Curva de Bañera - Análisis de Confiabilidad",
                             mostrar_fases: bool = True) -> plt.Figure:
        """
        Grafica la curva de bañera con análisis de fases.
        
        Args:
            tiempo: Vector de tiempo
            tasa_falla: Vector de tasas de falla
            titulo: Título del gráfico
            mostrar_fases: Si mostrar las fases de la curva
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Curva principal
        ax.plot(tiempo, tasa_falla, 'b-', linewidth=3, label='Tasa de Falla')
        
        # Identificar fases
        if mostrar_fases:
            # Encontrar puntos de transición
            tasa_min = np.min(tasa_falla)
            idx_min = np.argmin(tasa_falla)
            
            # Fase 1: Mortalidad infantil
            ax.fill_between(tiempo[:idx_min], 0, tasa_falla[:idx_min], 
                           alpha=0.3, color='red', label='Mortalidad Infantil')
            
            # Fase 2: Vida útil
            ax.fill_between(tiempo[idx_min:], 0, tasa_falla[idx_min:], 
                           alpha=0.3, color='green', label='Vida Útil')
            
            # Líneas de referencia
            ax.axhline(y=tasa_min, color='g', linestyle='--', alpha=0.7, 
                      label=f'Vida Útil (λ={tasa_min:.3f})')
            
            # Anotaciones
            ax.annotate('Fase 1:\nMortalidad\nInfantil', 
                       xy=(tiempo[idx_min//2], tasa_falla[idx_min//2]),
                       xytext=(tiempo[idx_min//2], tasa_falla[idx_min//2] + 0.05),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       fontsize=10, ha='center')
            
            ax.annotate('Fase 2:\nVida Útil', 
                       xy=(tiempo[idx_min + len(tiempo)//4], tasa_falla[idx_min]),
                       xytext=(tiempo[idx_min + len(tiempo)//4], tasa_falla[idx_min] + 0.03),
                       arrowprops=dict(arrowstyle='->', color='green'),
                       fontsize=10, ha='center')
            
            ax.annotate('Fase 3:\nDesgaste', 
                       xy=(tiempo[-len(tiempo)//4], tasa_falla[-len(tiempo)//4]),
                       xytext=(tiempo[-len(tiempo)//4], tasa_falla[-len(tiempo)//4] + 0.05),
                       arrowprops=dict(arrowstyle='->', color='blue'),
                       fontsize=10, ha='center')
        
        # Configuración del gráfico
        ax.set_xlabel('Tiempo (unidades)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tasa de Falla λ(t)', fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    
    def analizar_distribucion_fallas(self, datos_fallas: np.ndarray, 
                                   distribucion: str = 'weibull') -> Dict:
        """
        Analiza la distribución de fallas usando diferentes modelos.
        
        Args:
            datos_fallas: Datos de tiempo hasta falla
            distribucion: Tipo de distribución ('weibull', 'exponential', 'normal')
            
        Returns:
            Diccionario con parámetros y estadísticas
        """
        resultados = {}
        
        if distribucion == 'weibull':
            # Ajuste de distribución de Weibull
            params = weibull_min.fit(datos_fallas)
            forma, escala, loc = params
            
            resultados = {
                'distribucion': 'Weibull',
                'parametros': {
                    'forma': forma,
                    'escala': escala,
                    'localizacion': loc
                },
                'mtbf': weibull_min.mean(forma, loc=loc, scale=escala),
                'confiabilidad_50h': weibull_min.sf(50, forma, loc=loc, scale=escala),
                'confiabilidad_100h': weibull_min.sf(100, forma, loc=loc, scale=escala)
            }
            
        elif distribucion == 'exponential':
            # Ajuste de distribución exponencial
            params = expon.fit(datos_fallas)
            loc, escala = params
            
            resultados = {
                'distribucion': 'Exponencial',
                'parametros': {
                    'localizacion': loc,
                    'escala': escala
                },
                'mtbf': expon.mean(loc=loc, scale=escala),
                'confiabilidad_50h': expon.sf(50, loc=loc, scale=escala),
                'confiabilidad_100h': expon.sf(100, loc=loc, scale=escala)
            }
            
        elif distribucion == 'normal':
            # Ajuste de distribución normal
            params = norm.fit(datos_fallas)
            media, desv_std = params
            
            resultados = {
                'distribucion': 'Normal',
                'parametros': {
                    'media': media,
                    'desviacion_estandar': desv_std
                },
                'mtbf': norm.mean(media, desv_std),
                'confiabilidad_50h': norm.sf(50, media, desv_std),
                'confiabilidad_100h': norm.sf(100, media, desv_std)
            }
        
        return resultados
    
    def graficar_distribucion_fallas(self, datos_fallas: np.ndarray,
                                   distribucion: str = 'weibull',
                                   titulo: str = "Análisis de Distribución de Fallas") -> plt.Figure:
        """
        Grafica el análisis de distribución de fallas.
        
        Args:
            datos_fallas: Datos de tiempo hasta falla
            distribucion: Tipo de distribución a ajustar
            titulo: Título del gráfico
            
        Returns:
            Figura de matplotlib
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histograma de datos
        ax1.hist(datos_fallas, bins=20, alpha=0.7, density=True, 
                color='skyblue', edgecolor='black', label='Datos')
        
        # Curva de distribución ajustada
        x = np.linspace(0, np.max(datos_fallas), 100)
        
        if distribucion == 'weibull':
            params = weibull_min.fit(datos_fallas)
            y = weibull_min.pdf(x, *params)
            ax1.plot(x, y, 'r-', linewidth=2, label='Weibull')
        elif distribucion == 'exponential':
            params = expon.fit(datos_fallas)
            y = expon.pdf(x, *params)
            ax1.plot(x, y, 'r-', linewidth=2, label='Exponencial')
        elif distribucion == 'normal':
            params = norm.fit(datos_fallas)
            y = norm.pdf(x, *params)
            ax1.plot(x, y, 'r-', linewidth=2, label='Normal')
        
        ax1.set_xlabel('Tiempo hasta Falla', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Densidad de Probabilidad', fontsize=12, fontweight='bold')
        ax1.set_title('Distribución de Fallas', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de confiabilidad
        tiempo = np.linspace(0, np.max(datos_fallas), 100)
        
        if distribucion == 'weibull':
            params = weibull_min.fit(datos_fallas)
            confiabilidad = weibull_min.sf(tiempo, *params)
        elif distribucion == 'exponential':
            params = expon.fit(datos_fallas)
            confiabilidad = expon.sf(tiempo, *params)
        elif distribucion == 'normal':
            params = norm.fit(datos_fallas)
            confiabilidad = norm.sf(tiempo, *params)
        
        ax2.plot(tiempo, confiabilidad, 'g-', linewidth=2, label='Confiabilidad')
        ax2.set_xlabel('Tiempo', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Confiabilidad R(t)', fontsize=12, fontweight='bold')
        ax2.set_title('Función de Confiabilidad', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.suptitle(titulo, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def calcular_mantenimiento_preventivo(self, tiempo_operacion: float,
                                        tasa_falla_critica: float,
                                        costo_mtto_preventivo: float,
                                        costo_mtto_correctivo: float) -> Dict:
        """
        Calcula la estrategia óptima de mantenimiento preventivo.
        
        Args:
            tiempo_operacion: Tiempo de operación planificado
            tasa_falla_critica: Tasa de falla considerada crítica
            costo_mtto_preventivo: Costo del mantenimiento preventivo
            costo_mtto_correctivo: Costo del mantenimiento correctivo
            
        Returns:
            Diccionario con análisis de costos y recomendaciones
        """
        # Análisis simplificado de costos
        tiempo_optimo = tiempo_operacion * 0.7  # Regla empírica
        
        # Calcular probabilidad de falla
        prob_falla = 1 - np.exp(-tasa_falla_critica * tiempo_optimo)
        
        # Costos esperados
        costo_preventivo = costo_mtto_preventivo
        costo_correctivo_esperado = prob_falla * costo_mtto_correctivo
        
        # Recomendación
        if costo_preventivo < costo_correctivo_esperado:
            recomendacion = "Mantenimiento Preventivo"
            ahorro = costo_correctivo_esperado - costo_preventivo
        else:
            recomendacion = "Mantenimiento Correctivo"
            ahorro = 0
        
        return {
            'tiempo_optimo_mtto': tiempo_optimo,
            'probabilidad_falla': prob_falla,
            'costo_preventivo': costo_preventivo,
            'costo_correctivo_esperado': costo_correctivo_esperado,
            'recomendacion': recomendacion,
            'ahorro_esperado': ahorro
        }

# Ejemplos de uso
def ejemplo_curva_banera():
    """Ejemplo de análisis de curva de bañera."""
    print("=== Ejemplo: Análisis de Curva de Bañera ===")
    
    analizador = AnalizadorConfiabilidad()
    
    # Generar curva de bañera
    tiempo, tasa_falla = analizador.curva_banera(
        tiempo_max=100,
        tasa_falla_inicial=0.15,
        tasa_falla_estable=0.02,
        tasa_falla_desgaste=0.20,
        tiempo_transicion_1=15,
        tiempo_transicion_2=75
    )
    
    # Graficar
    fig = analizador.graficar_curva_banera(tiempo, tasa_falla)
    plt.show()
    
    return fig

def ejemplo_analisis_fallas():
    """Ejemplo de análisis de distribución de fallas."""
    print("\n=== Ejemplo: Análisis de Distribución de Fallas ===")
    
    # Generar datos de ejemplo (tiempos hasta falla)
    np.random.seed(42)
    datos_fallas = weibull_min.rvs(2.5, scale=50, size=100)
    
    analizador = AnalizadorConfiabilidad()
    
    # Analizar distribución
    resultados = analizador.analizar_distribucion_fallas(datos_fallas, 'weibull')
    
    print("Resultados del análisis:")
    for key, value in resultados.items():
        print(f"{key}: {value}")
    
    # Graficar
    fig = analizador.graficar_distribucion_fallas(datos_fallas, 'weibull')
    plt.show()
    
    return fig

def ejemplo_mantenimiento_preventivo():
    """Ejemplo de análisis de mantenimiento preventivo."""
    print("\n=== Ejemplo: Análisis de Mantenimiento Preventivo ===")
    
    analizador = AnalizadorConfiabilidad()
    
    # Análisis de costos
    resultados = analizador.calcular_mantenimiento_preventivo(
        tiempo_operacion=1000,  # horas
        tasa_falla_critica=0.001,  # fallas/hora
        costo_mtto_preventivo=5000,  # USD
        costo_mtto_correctivo=25000  # USD
    )
    
    print("Análisis de Mantenimiento Preventivo:")
    for key, value in resultados.items():
        print(f"{key}: {value}")
    
    return resultados

if __name__ == "__main__":
    # Ejecutar ejemplos
    ejemplo_curva_banera()
    ejemplo_analisis_fallas()
    ejemplo_mantenimiento_preventivo()
