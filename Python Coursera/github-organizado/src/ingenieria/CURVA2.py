# -----------------------------------------------------------------------------
# Módulo: CURVA2.py
# Propósito: Ajustar distribución Weibull de 2 parámetros a datos de falla y mostrar resultados
# Aplicación: Ingeniería de confiabilidad, análisis de fallas
# Dependencias: numpy, matplotlib, scipy
# Uso: Ejecutar el script para ajustar el modelo Weibull y mostrar el gráfico
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns

class AnalizadorWeibull:
    """
    Clase para análisis de confiabilidad usando distribución Weibull
    """
    
    def __init__(self):
        self.datos = None
        self.parametros = None
        self.resultados = {}
        
    def cargar_datos(self, datos):
        """
        Carga datos de falla
        
        Args:
            datos: array o lista con tiempos de falla
        """
        self.datos = np.array(datos)
        print(f"Datos cargados: {len(self.datos)} fallas")
        
    def generar_datos_ejemplo(self, n_muestras=50, forma=2.5, escala=1000):
        """
        Genera datos de ejemplo con distribución Weibull
        
        Args:
            n_muestras: número de muestras
            forma: parámetro de forma (beta)
            escala: parámetro de escala (eta)
        """
        np.random.seed(42)
        self.datos = np.random.weibull(forma, n_muestras) * escala
        print(f"Datos de ejemplo generados: {n_muestras} fallas")
        print(f"Parámetros reales: forma={forma}, escala={escala}")
        return self.datos
    
    def ajustar_weibull(self):
        """
        Ajusta distribución Weibull de 2 parámetros a los datos
        """
        if self.datos is None:
            print("Error: No hay datos cargados")
            return None
            
        # Ajustar Weibull usando scipy
        forma, loc, escala = stats.weibull_min.fit(self.datos)
        
        # Para Weibull de 2 parámetros, loc debería ser 0
        if abs(loc) > 0.01 * escala:
            print(f"Advertencia: loc = {loc:.2f}, considerando Weibull de 3 parámetros")
        
        self.parametros = {
            'forma': forma,
            'escala': escala,
            'loc': loc
        }
        
        print(f"Ajuste Weibull completado:")
        print(f"  Parámetro de forma (β): {forma:.3f}")
        print(f"  Parámetro de escala (η): {escala:.3f}")
        print(f"  Parámetro de localización: {loc:.3f}")
        
        return self.parametros
    
    def calcular_metricas_confiabilidad(self):
        """
        Calcula métricas de confiabilidad usando los parámetros Weibull
        """
        if self.parametros is None:
            print("Error: Primero ajuste la distribución Weibull")
            return None
            
        forma = self.parametros['forma']
        escala = self.parametros['escala']
        
        # Tiempo medio de vida (MTTF)
        mttf = escala * np.exp(np.log(2) / forma)
        
        # Vida característica (tiempo al 63.2% de fallas)
        vida_caracteristica = escala
        
        # Tiempo al 10%, 50% y 90% de fallas
        t10 = escala * (-np.log(0.9)) ** (1/forma)
        t50 = escala * (-np.log(0.5)) ** (1/forma)
        t90 = escala * (-np.log(0.1)) ** (1/forma)
        
        # Función de confiabilidad en diferentes tiempos
        tiempos_eval = np.linspace(0, escala * 2, 100)
        confiabilidad = np.exp(-(tiempos_eval / escala) ** forma)
        
        # Función de tasa de falla
        tasa_falla = (forma / escala) * (tiempos_eval / escala) ** (forma - 1)
        
        metricas = {
            'mttf': mttf,
            'vida_caracteristica': vida_caracteristica,
            't10': t10,
            't50': t50,
            't90': t90,
            'tiempos_eval': tiempos_eval,
            'confiabilidad': confiabilidad,
            'tasa_falla': tasa_falla
        }
        
        self.resultados['metricas'] = metricas
        
        return metricas
    
    def grafico_probabilidad_weibull(self):
        """
        Genera gráfico de probabilidad Weibull
        """
        if self.datos is None:
            print("Error: No hay datos cargados")
            return
            
        # Ordenar datos
        datos_ordenados = np.sort(self.datos)
        n = len(datos_ordenados)
        
        # Calcular probabilidades de falla (método de median rank)
        prob_falla = [(i - 0.3) / (n + 0.4) for i in range(1, n + 1)]
        
        # Transformación Weibull
        x_weibull = np.log(datos_ordenados)
        y_weibull = np.log(-np.log(1 - np.array(prob_falla)))
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de probabilidad Weibull
        ax1.scatter(x_weibull, y_weibull, color='blue', alpha=0.7, s=50, label='Datos')
        
        # Línea de ajuste si hay parámetros
        if self.parametros is not None:
            forma = self.parametros['forma']
            escala = self.parametros['escala']
            
            x_line = np.linspace(x_weibull.min(), x_weibull.max(), 100)
            y_line = forma * (x_line - np.log(escala))
            ax1.plot(x_line, y_line, 'r--', linewidth=2, 
                    label=f'Ajuste Weibull (β={forma:.2f})')
        
        ax1.set_xlabel('ln(Tiempo)')
        ax1.set_ylabel('ln(-ln(1-F(t)))')
        ax1.set_title('Gráfico de Probabilidad Weibull')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Histograma con ajuste
        ax2.hist(self.datos, bins=min(20, len(self.datos)//3), density=True, 
                alpha=0.7, color='lightblue', edgecolor='black', label='Datos')
        
        if self.parametros is not None:
            # Función de densidad Weibull
            x_teorico = np.linspace(0, self.datos.max() * 1.2, 1000)
            pdf_weibull = stats.weibull_min.pdf(x_teorico, 
                                              self.parametros['forma'],
                                              self.parametros['loc'],
                                              self.parametros['escala'])
            ax2.plot(x_teorico, pdf_weibull, 'r-', linewidth=2, label='PDF Weibull')
        
        ax2.set_xlabel('Tiempo de Falla')
        ax2.set_ylabel('Densidad de Probabilidad')
        ax2.set_title('Distribución de Tiempos de Falla')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
    
    def grafico_funciones_confiabilidad(self):
        """
        Genera gráficos de funciones de confiabilidad
        """
        if self.parametros is None:
            print("Error: Primero ajuste la distribución Weibull")
            return
            
        metricas = self.calcular_metricas_confiabilidad()
        if metricas is None:
            return
            
        tiempos = metricas['tiempos_eval']
        confiabilidad = metricas['confiabilidad']
        tasa_falla = metricas['tasa_falla']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Función de confiabilidad
        ax1.plot(tiempos, confiabilidad, 'b-', linewidth=2)
        ax1.set_xlabel('Tiempo')
        ax1.set_ylabel('Confiabilidad R(t)')
        ax1.set_title('Función de Confiabilidad')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0.632, color='r', linestyle='--', alpha=0.7, 
                   label='R(t) = 0.632')
        ax1.axvline(x=metricas['vida_caracteristica'], color='g', linestyle='--', 
                   alpha=0.7, label=f'η = {metricas["vida_caracteristica"]:.1f}')
        ax1.legend()
        
        # 2. Función de tasa de falla
        ax2.plot(tiempos, tasa_falla, 'r-', linewidth=2)
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('Tasa de Falla λ(t)')
        ax2.set_title('Función de Tasa de Falla')
        ax2.grid(True, alpha=0.3)
        
        # 3. Función de distribución acumulada
        f_t = 1 - confiabilidad
        ax3.plot(tiempos, f_t, 'g-', linewidth=2)
        ax3.set_xlabel('Tiempo')
        ax3.set_ylabel('Probabilidad de Falla F(t)')
        ax3.set_title('Función de Distribución Acumulada')
        ax3.grid(True, alpha=0.3)
        
        # 4. Comparación con datos reales
        if self.datos is not None:
            # Función de supervivencia empírica
            datos_ordenados = np.sort(self.datos)
            n = len(datos_ordenados)
            supervivencia_empirica = [(n - i) / n for i in range(n)]
            
            ax4.plot(datos_ordenados, supervivencia_empirica, 'bo', alpha=0.7, 
                    label='Datos Empíricos')
            ax4.plot(tiempos, confiabilidad, 'r-', linewidth=2, label='Weibull Ajustado')
            ax4.set_xlabel('Tiempo')
            ax4.set_ylabel('Confiabilidad')
            ax4.set_title('Comparación: Datos vs Weibull')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        plt.tight_layout()
        plt.show()
    
    def test_bondad_ajuste(self):
        """
        Realiza test de bondad de ajuste (Kolmogorov-Smirnov)
        """
        if self.parametros is None:
            print("Error: Primero ajuste la distribución Weibull")
            return None
            
        # Test Kolmogorov-Smirnov
        ks_statistic, p_value = stats.kstest(self.datos, 'weibull_min', 
                                           args=(self.parametros['forma'],
                                                 self.parametros['loc'],
                                                 self.parametros['escala']))
        
        print("\nTEST DE BONDAD DE AJUSTE (Kolmogorov-Smirnov):")
        print(f"Estadístico KS: {ks_statistic:.4f}")
        print(f"Valor p: {p_value:.4f}")
        
        if p_value > 0.05:
            print("Conclusión: No se rechaza la hipótesis de que los datos siguen distribución Weibull")
        else:
            print("Conclusión: Se rechaza la hipótesis de que los datos siguen distribución Weibull")
        
        return ks_statistic, p_value
    
    def reporte_completo(self):
        """
        Genera un reporte completo del análisis
        """
        print("=" * 60)
        print("REPORTE DE ANÁLISIS WEIBULL")
        print("=" * 60)
        
        # Información básica
        print(f"Número de fallas: {len(self.datos)}")
        print(f"Tiempo mínimo: {self.datos.min():.2f}")
        print(f"Tiempo máximo: {self.datos.max():.2f}")
        print(f"Tiempo medio: {self.datos.mean():.2f}")
        print(f"Desviación estándar: {self.datos.std():.2f}")
        
        # Parámetros Weibull
        if self.parametros is not None:
            print(f"\nPARÁMETROS WEIBULL:")
            print(f"Forma (β): {self.parametros['forma']:.3f}")
            print(f"Escala (η): {self.parametros['escala']:.3f}")
            print(f"Localización: {self.parametros['loc']:.3f}")
            
            # Interpretación del parámetro de forma
            forma = self.parametros['forma']
            if forma < 1:
                print("Interpretación: Tasa de falla decreciente (mortalidad infantil)")
            elif forma == 1:
                print("Interpretación: Tasa de falla constante (fallas aleatorias)")
            else:
                print("Interpretación: Tasa de falla creciente (desgaste)")
        
        # Métricas de confiabilidad
        metricas = self.calcular_metricas_confiabilidad()
        if metricas is not None:
            print(f"\nMÉTRICAS DE CONFIABILIDAD:")
            print(f"MTTF: {metricas['mttf']:.2f}")
            print(f"Vida característica (η): {metricas['vida_caracteristica']:.2f}")
            print(f"T10 (10% fallan antes): {metricas['t10']:.2f}")
            print(f"T50 (50% fallan antes): {metricas['t50']:.2f}")
            print(f"T90 (90% fallan antes): {metricas['t90']:.2f}")
        
        # Test de bondad de ajuste
        self.test_bondad_ajuste()
        
        print("=" * 60)

def ejemplo_uso():
    """
    Ejemplo de uso del módulo de análisis Weibull
    """
    print("EJEMPLO DE ANÁLISIS WEIBULL")
    print("-" * 40)
    
    # Crear instancia
    analizador = AnalizadorWeibull()
    
    # Generar datos de ejemplo
    datos = analizador.generar_datos_ejemplo(100, forma=2.5, escala=1000)
    
    # Ajustar Weibull
    parametros = analizador.ajustar_weibull()
    
    # Generar gráficos
    analizador.grafico_probabilidad_weibull()
    analizador.grafico_funciones_confiabilidad()
    
    # Reporte completo
    analizador.reporte_completo()
    
    return analizador

if __name__ == "__main__":
    ejemplo_uso()
