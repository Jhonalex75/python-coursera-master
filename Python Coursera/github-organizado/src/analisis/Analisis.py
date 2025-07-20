"""
Sistema de Análisis Financiero y Operativo
==========================================

Este módulo proporciona herramientas completas para análisis financiero,
operativo y de proyecciones para proyectos de ingeniería.

Funcionalidades:
- Análisis de costos operativos (OPEX)
- Proyecciones financieras
- Análisis de rentabilidad
- Indicadores de rendimiento
- Reportes automatizados

Autor: Ingeniería Financiera
Versión: 2.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class AnalizadorFinanciero:
    """
    Clase principal para análisis financiero y operativo
    """
    
    def __init__(self):
        """Inicializa el analizador financiero."""
        self.datos = {}
        self.resultados = {}
        self.proyecciones = {}
        
    def cargar_datos_opex(self, datos: Dict[str, List]) -> pd.DataFrame:
        """
        Carga datos de costos operativos
        
        Args:
            datos: Diccionario con datos de OPEX
            
        Returns:
            DataFrame con los datos cargados
        """
        df = pd.DataFrame(datos)
        df['Fecha'] = pd.to_datetime(df['Fecha']) if 'Fecha' in df.columns else None
        return df
    
    def calcular_metricas_opex(self, df: pd.DataFrame) -> Dict:
        """
        Calcula métricas completas de OPEX
        
        Args:
            df: DataFrame con datos de OPEX
            
        Returns:
            Diccionario con métricas calculadas
        """
        if 'Opex' not in df.columns:
            raise ValueError("El DataFrame debe contener una columna 'Opex'")
        
        opex_values = df['Opex']
        
        metricas = {
            'total': opex_values.sum(),
            'promedio': opex_values.mean(),
            'mediana': opex_values.median(),
            'desviacion_estandar': opex_values.std(),
            'minimo': opex_values.min(),
            'maximo': opex_values.max(),
            'varianza': opex_values.var(),
            'coeficiente_variacion': opex_values.std() / opex_values.mean() if opex_values.mean() != 0 else 0
        }
        
        # Calcular percentiles
        for p in [25, 50, 75, 90, 95]:
            metricas[f'percentil_{p}'] = opex_values.quantile(p/100)
        
        return metricas
    
    def analizar_tendencia_opex(self, df: pd.DataFrame, columna_fecha: str = 'Fecha') -> Dict:
        """
        Analiza la tendencia temporal de OPEX
        
        Args:
            df: DataFrame con datos
            columna_fecha: Nombre de la columna de fecha
            
        Returns:
            Diccionario con análisis de tendencia
        """
        if columna_fecha not in df.columns:
            raise ValueError(f"Columna de fecha '{columna_fecha}' no encontrada")
        
        # Ordenar por fecha
        df_sorted = df.sort_values(columna_fecha).copy()
        
        # Calcular tendencia lineal
        x = np.arange(len(df_sorted))
        y = df_sorted['Opex'].values
        
        # Ajuste lineal
        coeffs = np.polyfit(x, y, 1)
        tendencia_lineal = coeffs[0]  # Pendiente
        
        # Calcular crecimiento porcentual
        if len(df_sorted) > 1:
            crecimiento_total = ((df_sorted['Opex'].iloc[-1] - df_sorted['Opex'].iloc[0]) / 
                               df_sorted['Opex'].iloc[0]) * 100
        else:
            crecimiento_total = 0
        
        # Calcular volatilidad
        volatilidad = df_sorted['Opex'].std() / df_sorted['Opex'].mean() * 100
        
        return {
            'tendencia_lineal': tendencia_lineal,
            'crecimiento_total_porcentual': crecimiento_total,
            'volatilidad_porcentual': volatilidad,
            'datos_ordenados': df_sorted
        }
    
    def proyectar_opex(self, df: pd.DataFrame, periodos_futuros: int = 12, 
                      metodo: str = 'lineal') -> pd.DataFrame:
        """
        Proyecta OPEX futuro usando diferentes métodos
        
        Args:
            df: DataFrame con datos históricos
            periodos_futuros: Número de periodos a proyectar
            metodo: Método de proyección ('lineal', 'promedio', 'tendencia')
            
        Returns:
            DataFrame con proyecciones
        """
        if 'Opex' not in df.columns:
            raise ValueError("El DataFrame debe contener una columna 'Opex'")
        
        # Crear fechas futuras
        if 'Fecha' in df.columns:
            ultima_fecha = df['Fecha'].max()
            fechas_futuras = pd.date_range(start=ultima_fecha + timedelta(days=1), 
                                         periods=periodos_futuros, freq='M')
        else:
            fechas_futuras = range(len(df) + 1, len(df) + periodos_futuros + 1)
        
        proyecciones = []
        
        if metodo == 'lineal':
            # Proyección lineal usando regresión
            x = np.arange(len(df))
            y = df['Opex'].values
            coeffs = np.polyfit(x, y, 1)
            
            for i, fecha in enumerate(fechas_futuras):
                valor_proyectado = coeffs[0] * (len(df) + i) + coeffs[1]
                proyecciones.append({
                    'Fecha': fecha,
                    'Opex': max(0, valor_proyectado),  # OPEX no puede ser negativo
                    'Tipo': 'Proyección'
                })
        
        elif metodo == 'promedio':
            # Proyección usando promedio móvil
            promedio_historico = df['Opex'].mean()
            
            for fecha in fechas_futuras:
                proyecciones.append({
                    'Fecha': fecha,
                    'Opex': promedio_historico,
                    'Tipo': 'Proyección'
                })
        
        elif metodo == 'tendencia':
            # Proyección usando tendencia exponencial
            x = np.arange(len(df))
            y = df['Opex'].values
            
            # Ajuste exponencial
            log_y = np.log(y)
            coeffs = np.polyfit(x, log_y, 1)
            
            for i, fecha in enumerate(fechas_futuras):
                valor_proyectado = np.exp(coeffs[0] * (len(df) + i) + coeffs[1])
                proyecciones.append({
                    'Fecha': fecha,
                    'Opex': max(0, valor_proyectado),
                    'Tipo': 'Proyección'
                })
        
        return pd.DataFrame(proyecciones)
    
    def calcular_indicadores_rentabilidad(self, ingresos: List[float], 
                                        costos: List[float]) -> Dict:
        """
        Calcula indicadores de rentabilidad
        
        Args:
            ingresos: Lista de ingresos por periodo
            costos: Lista de costos por periodo
            
        Returns:
            Diccionario con indicadores de rentabilidad
        """
        ingresos = np.array(ingresos)
        costos = np.array(costos)
        
        # Calcular utilidades
        utilidades = ingresos - costos
        
        # Margen de utilidad
        margen_utilidad = (utilidades / ingresos * 100) if np.any(ingresos > 0) else np.zeros_like(utilidades)
        
        # ROI (Return on Investment)
        roi = (utilidades / costos * 100) if np.any(costos > 0) else np.zeros_like(utilidades)
        
        # Payback period (simplificado)
        inversion_inicial = costos[0] if len(costos) > 0 else 0
        if inversion_inicial > 0:
            utilidades_acumuladas = np.cumsum(utilidades)
            payback_period = np.where(utilidades_acumuladas >= inversion_inicial)[0]
            payback_period = payback_period[0] + 1 if len(payback_period) > 0 else float('inf')
        else:
            payback_period = 0
        
        return {
            'utilidades': utilidades.tolist(),
            'margen_utilidad_porcentual': margen_utilidad.tolist(),
            'roi_porcentual': roi.tolist(),
            'payback_period': payback_period,
            'utilidad_total': utilidades.sum(),
            'ingresos_total': ingresos.sum(),
            'costos_total': costos.sum()
        }
    
    def generar_reporte_opex(self, df: pd.DataFrame, nombre_proyecto: str = "Proyecto") -> None:
        """
        Genera un reporte completo de análisis OPEX
        
        Args:
            df: DataFrame con datos de OPEX
            nombre_proyecto: Nombre del proyecto para el reporte
        """
        print(f"📊 REPORTE DE ANÁLISIS OPEX - {nombre_proyecto}")
        print("=" * 60)
        
        # Calcular métricas
        metricas = self.calcular_metricas_opex(df)
        tendencia = self.analizar_tendencia_opex(df)
        
        # Mostrar resumen ejecutivo
        print(f"\n📈 RESUMEN EJECUTIVO:")
        print(f"OPEX Total: ${metricas['total']:,.2f}")
        print(f"OPEX Promedio: ${metricas['promedio']:,.2f}")
        print(f"OPEX Máximo: ${metricas['maximo']:,.2f}")
        print(f"OPEX Mínimo: ${metricas['minimo']:,.2f}")
        print(f"Desviación Estándar: ${metricas['desviacion_estandar']:,.2f}")
        
        # Análisis de tendencia
        print(f"\n📊 ANÁLISIS DE TENDENCIA:")
        print(f"Tendencia Lineal: {tendencia['tendencia_lineal']:+.2f} por periodo")
        print(f"Crecimiento Total: {tendencia['crecimiento_total_porcentual']:+.2f}%")
        print(f"Volatilidad: {tendencia['volatilidad_porcentual']:.2f}%")
        
        # Visualización
        self.visualizar_analisis_opex(df, metricas, tendencia)
    
    def visualizar_analisis_opex(self, df: pd.DataFrame, metricas: Dict, tendencia: Dict) -> None:
        """
        Visualiza el análisis de OPEX
        
        Args:
            df: DataFrame con datos
            metricas: Métricas calculadas
            tendencia: Análisis de tendencia
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Evolución temporal
        if 'Fecha' in df.columns:
            df_sorted = df.sort_values('Fecha')
            ax1.plot(df_sorted['Fecha'], df_sorted['Opex'], 'b-o', linewidth=2, markersize=6)
            ax1.set_title('Evolución Temporal de OPEX', fontweight='bold')
            ax1.set_xlabel('Fecha')
            ax1.set_ylabel('OPEX ($)')
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
        else:
            ax1.plot(df.index, df['Opex'], 'b-o', linewidth=2, markersize=6)
            ax1.set_title('Evolución de OPEX', fontweight='bold')
            ax1.set_xlabel('Periodo')
            ax1.set_ylabel('OPEX ($)')
            ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Distribución
        ax2.hist(df['Opex'], bins=15, alpha=0.7, color='green', edgecolor='black')
        ax2.axvline(metricas['promedio'], color='red', linestyle='--', 
                   label=f'Promedio: ${metricas["promedio"]:,.2f}')
        ax2.set_title('Distribución de OPEX', fontweight='bold')
        ax2.set_xlabel('OPEX ($)')
        ax2.set_ylabel('Frecuencia')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Gráfico 3: Box plot
        ax3.boxplot(df['Opex'], patch_artist=True, boxprops=dict(facecolor='lightblue'))
        ax3.set_title('Diagrama de Caja - OPEX', fontweight='bold')
        ax3.set_ylabel('OPEX ($)')
        ax3.grid(True, alpha=0.3)
        
        # Gráfico 4: Métricas clave
        metricas_clave = ['promedio', 'mediana', 'minimo', 'maximo']
        valores_clave = [metricas[m] for m in metricas_clave]
        colores = ['blue', 'green', 'orange', 'red']
        
        bars = ax4.bar(metricas_clave, valores_clave, color=colores, alpha=0.7)
        ax4.set_title('Métricas Clave de OPEX', fontweight='bold')
        ax4.set_ylabel('OPEX ($)')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores_clave):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'${valor:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()


def crear_datos_ejemplo() -> Dict:
    """
    Crea datos de ejemplo para demostración
    
    Returns:
        Diccionario con datos de ejemplo
    """
    fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    opex_base = 10000
    opex_variacion = np.random.normal(0, 1000, len(fechas))
    opex_tendencia = np.linspace(0, 2000, len(fechas))
    
    opex_values = opex_base + opex_variacion + opex_tendencia
    
    return {
        'Fecha': fechas,
        'Opex': opex_values,
        'Mes': [f.strftime('%B') for f in fechas]
    }


def ejemplo_analisis_completo():
    """
    Ejemplo completo de análisis financiero
    """
    print("💰 ANÁLISIS FINANCIERO COMPLETO")
    print("=" * 50)
    
    # Crear analizador
    analizador = AnalizadorFinanciero()
    
    # Crear datos de ejemplo
    datos_ejemplo = crear_datos_ejemplo()
    df = analizador.cargar_datos_opex(datos_ejemplo)
    
    print(f"Datos cargados: {len(df)} registros")
    print(f"Periodo: {df['Fecha'].min().strftime('%Y-%m')} a {df['Fecha'].max().strftime('%Y-%m')}")
    
    # Generar reporte completo
    analizador.generar_reporte_opex(df, "Proyecto de Ingeniería 2023")
    
    # Proyecciones
    print(f"\n🔮 PROYECCIONES FUTURAS")
    print("-" * 30)
    
    proyecciones_lineal = analizador.proyectar_opex(df, periodos_futuros=6, metodo='lineal')
    proyecciones_promedio = analizador.proyectar_opex(df, periodos_futuros=6, metodo='promedio')
    
    print("Proyección Lineal (próximos 6 meses):")
    print(proyecciones_lineal[['Fecha', 'Opex']].head())
    
    # Análisis de rentabilidad
    print(f"\n📈 ANÁLISIS DE RENTABILIDAD")
    print("-" * 30)
    
    ingresos_ejemplo = [15000, 16000, 17000, 18000, 19000, 20000]
    costos_ejemplo = [12000, 12500, 13000, 13500, 14000, 14500]
    
    rentabilidad = analizador.calcular_indicadores_rentabilidad(ingresos_ejemplo, costos_ejemplo)
    
    print(f"Utilidad Total: ${rentabilidad['utilidad_total']:,.2f}")
    print(f"Ingresos Total: ${rentabilidad['ingresos_total']:,.2f}")
    print(f"Costos Total: ${rentabilidad['costos_total']:,.2f}")
    print(f"Payback Period: {rentabilidad['payback_period']} periodos")


def main():
    """
    Función principal del módulo
    """
    print("📊 SISTEMA DE ANÁLISIS FINANCIERO Y OPERATIVO")
    print("=" * 60)
    
    # Ejecutar ejemplo completo
    ejemplo_analisis_completo()
    
    print("\n" + "=" * 60)
    print("✅ Análisis financiero completado exitosamente!")
    print("\n📚 Funcionalidades incluidas:")
    print("• Análisis completo de OPEX")
    print("• Proyecciones financieras")
    print("• Indicadores de rentabilidad")
    print("• Visualizaciones profesionales")
    print("• Reportes automatizados")


if __name__ == "__main__":
    main()
