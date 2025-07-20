# -----------------------------------------------------------------------------
# Módulo: Grafica_duran_1.py
# Propósito: Análisis de datos de duración y confiabilidad con gráficos avanzados
# Aplicación: Ingeniería de confiabilidad, análisis de fallas, estudios de vida útil
# Dependencias: numpy, matplotlib, scipy, pandas
# Uso: Importar y usar las clases para análisis de confiabilidad
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import seaborn as sns
from datetime import datetime, timedelta

class AnalizadorConfiabilidad:
    """
    Clase para análisis de confiabilidad y datos de duración
    """
    
    def __init__(self):
        self.datos = None
        self.resultados = {}
        
    def cargar_datos(self, datos):
        """
        Carga datos de fallas o tiempos de vida
        
        Args:
            datos: DataFrame con columnas ['tiempo', 'estado', 'tipo_falla']
        """
        self.datos = datos
        print(f"Datos cargados: {len(datos)} registros")
        
    def generar_datos_ejemplo(self, n_muestras=100):
        """
        Genera datos de ejemplo para demostración
        """
        np.random.seed(42)
        
        # Simular tiempos de falla con distribución Weibull
        forma = 2.5
        escala = 1000
        tiempos_falla = np.random.weibull(forma, n_muestras) * escala
        
        # Simular datos censurados (algunos equipos no han fallado)
        censura = np.random.random(n_muestras) > 0.3
        tiempos_censurados = np.where(censura, tiempos_falla, 
                                    np.random.uniform(tiempos_falla, tiempos_falla * 1.5))
        
        # Crear DataFrame
        datos = pd.DataFrame({
            'tiempo': tiempos_censurados,
            'estado': censura.astype(int),  # 1 = falló, 0 = censurado
            'tipo_falla': np.random.choice(['mecanica', 'electrica', 'operacional'], n_muestras)
        })
        
        self.datos = datos
        return datos
    
    def analisis_supervivencia(self):
        """
        Análisis de supervivencia básico
        """
        if self.datos is None:
            print("Error: No hay datos cargados")
            return
            
        # Ordenar por tiempo
        datos_ordenados = self.datos.sort_values('tiempo')
        
        # Calcular función de supervivencia
        n_total = len(datos_ordenados)
        supervivencia = []
        tiempos = []
        
        for i, (_, fila) in enumerate(datos_ordenados.iterrows()):
            if fila['estado'] == 1:  # Falló
                supervivencia.append((n_total - i) / n_total)
                tiempos.append(fila['tiempo'])
        
        self.resultados['supervivencia'] = {
            'tiempos': tiempos,
            'probabilidad': supervivencia
        }
        
        return tiempos, supervivencia
    
    def ajuste_weibull(self):
        """
        Ajusta distribución Weibull a los datos de falla
        """
        if self.datos is None:
            print("Error: No hay datos cargados")
            return
            
        # Obtener solo datos de falla
        datos_falla = self.datos[self.datos['estado'] == 1]['tiempo'].values
        
        # Ajustar Weibull
        forma, loc, escala = stats.weibull_min.fit(datos_falla)
        
        self.resultados['weibull'] = {
            'forma': forma,
            'escala': escala,
            'loc': loc
        }
        
        return forma, escala, loc
    
    def grafico_supervivencia(self):
        """
        Gráfico de función de supervivencia
        """
        if 'supervivencia' not in self.resultados:
            self.analisis_supervivencia()
            
        tiempos, supervivencia = self.resultados['supervivencia']['tiempos'], self.resultados['supervivencia']['probabilidad']
        
        plt.figure(figsize=(12, 8))
        
        # Gráfico de supervivencia
        plt.subplot(2, 2, 1)
        plt.plot(tiempos, supervivencia, 'b-', linewidth=2, label='Función de Supervivencia')
        plt.scatter(tiempos, supervivencia, color='red', alpha=0.6)
        plt.xlabel('Tiempo (horas)')
        plt.ylabel('Probabilidad de Supervivencia')
        plt.title('Función de Supervivencia')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Gráfico de tasa de falla
        plt.subplot(2, 2, 2)
        tasa_falla = []
        for i in range(1, len(supervivencia)):
            tasa = (supervivencia[i-1] - supervivencia[i]) / (tiempos[i] - tiempos[i-1])
            tasa_falla.append(tasa)
        
        plt.plot(tiempos[1:], tasa_falla, 'g-', linewidth=2)
        plt.xlabel('Tiempo (horas)')
        plt.ylabel('Tasa de Falla')
        plt.title('Tasa de Falla vs Tiempo')
        plt.grid(True, alpha=0.3)
        
        # Histograma de tiempos de falla
        plt.subplot(2, 2, 3)
        datos_falla = self.datos[self.datos['estado'] == 1]['tiempo']
        plt.hist(datos_falla, bins=20, alpha=0.7, color='orange', edgecolor='black')
        plt.xlabel('Tiempo de Falla (horas)')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de Tiempos de Falla')
        plt.grid(True, alpha=0.3)
        
        # Gráfico de tipos de falla
        plt.subplot(2, 2, 4)
        tipos_falla = self.datos['tipo_falla'].value_counts()
        plt.pie(tipos_falla.values, labels=tipos_falla.index, autopct='%1.1f%%')
        plt.title('Distribución por Tipo de Falla')
        
        plt.tight_layout()
        plt.show()
    
    def grafico_weibull(self):
        """
        Gráfico de probabilidad Weibull
        """
        if 'weibull' not in self.resultados:
            self.ajuste_weibull()
            
        forma, escala, loc = (self.resultados['weibull']['forma'], 
                             self.resultados['weibull']['escala'],
                             self.resultados['weibull']['loc'])
        
        datos_falla = self.datos[self.datos['estado'] == 1]['tiempo'].values
        datos_falla_ordenados = np.sort(datos_falla)
        
        # Calcular probabilidades de falla
        n = len(datos_falla_ordenados)
        prob_falla = [(i - 0.3) / (n + 0.4) for i in range(1, n + 1)]
        
        # Transformación Weibull
        x_weibull = np.log(datos_falla_ordenados)
        y_weibull = np.log(-np.log(1 - np.array(prob_falla)))
        
        plt.figure(figsize=(12, 5))
        
        # Gráfico de probabilidad Weibull
        plt.subplot(1, 2, 1)
        plt.scatter(x_weibull, y_weibull, color='blue', alpha=0.7, label='Datos')
        
        # Línea de ajuste
        x_line = np.linspace(x_weibull.min(), x_weibull.max(), 100)
        y_line = forma * (x_line - np.log(escala))
        plt.plot(x_line, y_line, 'r--', linewidth=2, label=f'Ajuste Weibull (β={forma:.2f})')
        
        plt.xlabel('ln(Tiempo)')
        plt.ylabel('ln(-ln(1-F(t)))')
        plt.title('Gráfico de Probabilidad Weibull')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Función de densidad Weibull
        plt.subplot(1, 2, 2)
        x_teorico = np.linspace(0, datos_falla.max() * 1.2, 1000)
        pdf_weibull = stats.weibull_min.pdf(x_teorico, forma, loc, escala)
        
        plt.plot(x_teorico, pdf_weibull, 'r-', linewidth=2, label='PDF Weibull')
        plt.hist(datos_falla, bins=20, density=True, alpha=0.7, color='blue', 
                edgecolor='black', label='Datos')
        plt.xlabel('Tiempo (horas)')
        plt.ylabel('Densidad de Probabilidad')
        plt.title('Ajuste de Distribución Weibull')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def calcular_metricas_confiabilidad(self):
        """
        Calcula métricas clave de confiabilidad
        """
        if self.datos is None:
            print("Error: No hay datos cargados")
            return
            
        datos_falla = self.datos[self.datos['estado'] == 1]['tiempo']
        
        # Métricas básicas
        mtbf = datos_falla.mean()  # Tiempo medio entre fallas
        desv_std = datos_falla.std()
        
        # Percentiles
        p10 = np.percentile(datos_falla, 10)
        p50 = np.percentile(datos_falla, 50)  # Mediana
        p90 = np.percentile(datos_falla, 90)
        
        # Si hay ajuste Weibull
        if 'weibull' in self.resultados:
            forma, escala, loc = (self.resultados['weibull']['forma'], 
                                 self.resultados['weibull']['escala'],
                                 self.resultados['weibull']['loc'])
            
            # Vida característica (tiempo al 63.2% de fallas)
            vida_caracteristica = escala
            
            # Tiempo medio de vida
            tiempo_medio = escala * np.exp(np.log(2) / forma)
        else:
            vida_caracteristica = None
            tiempo_medio = None
        
        metricas = {
            'mtbf': mtbf,
            'desv_std': desv_std,
            'p10': p10,
            'p50': p50,
            'p90': p90,
            'vida_caracteristica': vida_caracteristica,
            'tiempo_medio': tiempo_medio
        }
        
        self.resultados['metricas'] = metricas
        
        return metricas
    
    def reporte_confiabilidad(self):
        """
        Genera un reporte completo de confiabilidad
        """
        print("=" * 60)
        print("REPORTE DE ANÁLISIS DE CONFIABILIDAD")
        print("=" * 60)
        
        # Información básica
        print(f"Total de registros: {len(self.datos)}")
        print(f"Fallas observadas: {len(self.datos[self.datos['estado'] == 1])}")
        print(f"Datos censurados: {len(self.datos[self.datos['estado'] == 0])}")
        
        # Métricas
        metricas = self.calcular_metricas_confiabilidad()
        print("\nMÉTRICAS DE CONFIABILIDAD:")
        print(f"MTBF: {metricas['mtbf']:.2f} horas")
        print(f"Desviación estándar: {metricas['desv_std']:.2f} horas")
        print(f"P10 (10% fallan antes): {metricas['p10']:.2f} horas")
        print(f"P50 (50% fallan antes): {metricas['p50']:.2f} horas")
        print(f"P90 (90% fallan antes): {metricas['p90']:.2f} horas")
        
        if metricas['vida_caracteristica']:
            print(f"Vida característica (Weibull): {metricas['vida_caracteristica']:.2f} horas")
            print(f"Tiempo medio de vida (Weibull): {metricas['tiempo_medio']:.2f} horas")
        
        # Análisis por tipo de falla
        print("\nANÁLISIS POR TIPO DE FALLA:")
        tipos_falla = self.datos['tipo_falla'].value_counts()
        for tipo, count in tipos_falla.items():
            porcentaje = (count / len(self.datos)) * 100
            print(f"  {tipo}: {count} ({porcentaje:.1f}%)")
        
        print("=" * 60)

def ejemplo_uso():
    """
    Ejemplo de uso del módulo de análisis de confiabilidad
    """
    print("EJEMPLO DE ANÁLISIS DE CONFIABILIDAD")
    print("-" * 40)
    
    # Crear instancia
    analizador = AnalizadorConfiabilidad()
    
    # Generar datos de ejemplo
    datos = analizador.generar_datos_ejemplo(150)
    print("Datos de ejemplo generados")
    
    # Análisis completo
    analizador.analisis_supervivencia()
    analizador.ajuste_weibull()
    
    # Generar gráficos
    analizador.grafico_supervivencia()
    analizador.grafico_weibull()
    
    # Reporte
    analizador.reporte_confiabilidad()
    
    return analizador

if __name__ == "__main__":
    ejemplo_uso()
