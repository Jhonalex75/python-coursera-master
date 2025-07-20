# -----------------------------------------------------------------------------
# Script: curva_mtto.py
# Propósito: Script para análisis de curvas de mantenimiento
# Especialidad: Mantenimiento Industrial
# Dependencias: numpy, matplotlib, pandas
# Uso: Importar funciones para análisis de mantenimiento
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

def generar_curva_bañera(tiempo, fallas_infantiles=0.1, fallas_aleatorias=0.05, fallas_desgaste=0.2):
    """
    Genera una curva de bañera (bathtub curve) para análisis de confiabilidad
    
    Args:
        tiempo: Array de tiempos
        fallas_infantiles: Tasa de fallas infantiles
        fallas_aleatorias: Tasa de fallas aleatorias
        fallas_desgaste: Tasa de fallas por desgaste
    
    Returns:
        Array con tasas de falla
    """
    # Componentes de la curva de bañera
    # Fase 1: Mortalidad infantil (decreciente)
    mortalidad_infantil = fallas_infantiles * np.exp(-tiempo / 100)
    
    # Fase 2: Fallas aleatorias (constante)
    fallas_constantes = np.full_like(tiempo, fallas_aleatorias)
    
    # Fase 3: Desgaste (creciente)
    desgaste = fallas_desgaste * (tiempo / 1000) ** 2
    
    # Curva total
    tasa_falla = mortalidad_infantil + fallas_constantes + desgaste
    
    return tasa_falla

def calcular_mtbf(tiempos_falla):
    """
    Calcula el tiempo medio entre fallas (MTBF)
    
    Args:
        tiempos_falla: Lista de tiempos entre fallas
    
    Returns:
        MTBF
    """
    return np.mean(tiempos_falla)

def calcular_mttr(tiempos_reparacion):
    """
    Calcula el tiempo medio de reparación (MTTR)
    
    Args:
        tiempos_reparacion: Lista de tiempos de reparación
    
    Returns:
        MTTR
    """
    return np.mean(tiempos_reparacion)

def calcular_disponibilidad(mtbf, mttr):
    """
    Calcula la disponibilidad del equipo
    
    Args:
        mtbf: Tiempo medio entre fallas
        mttr: Tiempo medio de reparación
    
    Returns:
        Disponibilidad (0-1)
    """
    return mtbf / (mtbf + mttr)

def analizar_tendencias_mantenimiento(datos_mtto):
    """
    Analiza tendencias en datos de mantenimiento
    
    Args:
        datos_mtto: DataFrame con datos de mantenimiento
    
    Returns:
        Análisis de tendencias
    """
    # Calcular estadísticas por mes
    datos_mtto['fecha'] = pd.to_datetime(datos_mtto['fecha'])
    datos_mtto['mes'] = datos_mtto['fecha'].dt.to_period('M')
    
    # Agrupar por mes
    resumen_mensual = datos_mtto.groupby('mes').agg({
        'costo': 'sum',
        'tiempo_reparacion': 'mean',
        'tipo_mtto': 'count'
    }).reset_index()
    
    # Calcular tendencias
    tendencia_costo = np.polyfit(range(len(resumen_mensual)), resumen_mensual['costo'], 1)
    tendencia_tiempo = np.polyfit(range(len(resumen_mensual)), resumen_mensual['tiempo_reparacion'], 1)
    
    return {
        'resumen_mensual': resumen_mensual,
        'tendencia_costo': tendencia_costo,
        'tendencia_tiempo': tendencia_tiempo
    }

def graficar_curva_mantenimiento(tiempo, tasa_falla, mtbf=None, mttr=None):
    """
    Grafica la curva de mantenimiento y métricas
    
    Args:
        tiempo: Array de tiempos
        tasa_falla: Array de tasas de falla
        mtbf: Tiempo medio entre fallas
        mttr: Tiempo medio de reparación
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Curva de bañera
    ax1.plot(tiempo, tasa_falla, 'b-', linewidth=2)
    ax1.set_xlabel('Tiempo (horas)')
    ax1.set_ylabel('Tasa de Falla')
    ax1.set_title('Curva de Bañera - Tasa de Falla')
    ax1.grid(True, alpha=0.3)
    
    # Agregar líneas de referencia si hay datos
    if mtbf is not None:
        ax1.axvline(x=mtbf, color='r', linestyle='--', alpha=0.7, label=f'MTBF: {mtbf:.1f}')
        ax1.legend()
    
    # 2. Función de confiabilidad
    confiabilidad = np.exp(-np.cumsum(tasa_falla) * np.diff(tiempo, prepend=0))
    ax2.plot(tiempo, confiabilidad, 'g-', linewidth=2)
    ax2.set_xlabel('Tiempo (horas)')
    ax2.set_ylabel('Confiabilidad R(t)')
    ax2.set_title('Función de Confiabilidad')
    ax2.grid(True, alpha=0.3)
    
    # 3. Función de disponibilidad
    if mtbf is not None and mttr is not None:
        disponibilidad = calcular_disponibilidad(mtbf, mttr)
        ax3.bar(['Disponibilidad'], [disponibilidad], color='orange', alpha=0.7)
        ax3.set_ylabel('Disponibilidad')
        ax3.set_title(f'Disponibilidad: {disponibilidad:.3f}')
        ax3.set_ylim(0, 1)
        ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Comparación MTBF vs MTTR
    if mtbf is not None and mttr is not None:
        metricas = ['MTBF', 'MTTR']
        valores = [mtbf, mttr]
        colores = ['green', 'red']
        
        bars = ax4.bar(metricas, valores, color=colores, alpha=0.7)
        ax4.set_ylabel('Tiempo (horas)')
        ax4.set_title('Comparación MTBF vs MTTR')
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{valor:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def generar_datos_mantenimiento_ejemplo(n_registros=100):
    """
    Genera datos de ejemplo para análisis de mantenimiento
    
    Args:
        n_registros: Número de registros a generar
    
    Returns:
        DataFrame con datos de mantenimiento
    """
    np.random.seed(42)
    
    # Generar fechas
    fechas = pd.date_range(start='2023-01-01', periods=n_registros, freq='D')
    
    # Generar tipos de mantenimiento
    tipos = np.random.choice(['Preventivo', 'Correctivo', 'Predictivo'], n_registros, p=[0.6, 0.3, 0.1])
    
    # Generar costos
    costos = np.random.exponential(1000, n_registros)
    
    # Generar tiempos de reparación
    tiempos_reparacion = np.random.exponential(4, n_registros)
    
    # Generar equipos
    equipos = np.random.choice(['Bomba A', 'Motor B', 'Compresor C', 'Ventilador D'], n_registros)
    
    # Crear DataFrame
    datos = pd.DataFrame({
        'fecha': fechas,
        'equipo': equipos,
        'tipo_mtto': tipos,
        'costo': costos,
        'tiempo_reparacion': tiempos_reparacion
    })
    
    return datos

def analizar_costo_mantenimiento(datos_mtto):
    """
    Analiza costos de mantenimiento
    
    Args:
        datos_mtto: DataFrame con datos de mantenimiento
    
    Returns:
        Análisis de costos
    """
    # Análisis por tipo de mantenimiento
    costo_por_tipo = datos_mtto.groupby('tipo_mtto')['costo'].agg(['sum', 'mean', 'count'])
    
    # Análisis por equipo
    costo_por_equipo = datos_mtto.groupby('equipo')['costo'].agg(['sum', 'mean', 'count'])
    
    # Análisis temporal
    datos_mtto['mes'] = datos_mtto['fecha'].dt.to_period('M')
    costo_mensual = datos_mtto.groupby('mes')['costo'].sum()
    
    return {
        'costo_por_tipo': costo_por_tipo,
        'costo_por_equipo': costo_por_equipo,
        'costo_mensual': costo_mensual
    }

def graficar_analisis_costos(analisis_costos):
    """
    Grafica análisis de costos de mantenimiento
    
    Args:
        analisis_costos: Resultado de analizar_costo_mantenimiento
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Costo total por tipo de mantenimiento
    costo_por_tipo = analisis_costos['costo_por_tipo']
    ax1.bar(costo_por_tipo.index, costo_por_tipo['sum'], alpha=0.7)
    ax1.set_title('Costo Total por Tipo de Mantenimiento')
    ax1.set_ylabel('Costo Total')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Costo promedio por tipo
    ax2.bar(costo_por_tipo.index, costo_por_tipo['mean'], alpha=0.7, color='orange')
    ax2.set_title('Costo Promedio por Tipo de Mantenimiento')
    ax2.set_ylabel('Costo Promedio')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Costo por equipo
    costo_por_equipo = analisis_costos['costo_por_equipo']
    ax3.bar(costo_por_equipo.index, costo_por_equipo['sum'], alpha=0.7, color='green')
    ax3.set_title('Costo Total por Equipo')
    ax3.set_ylabel('Costo Total')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Evolución temporal
    costo_mensual = analisis_costos['costo_mensual']
    ax4.plot(costo_mensual.index.astype(str), costo_mensual.values, 'b-o', linewidth=2)
    ax4.set_title('Evolución de Costos Mensuales')
    ax4.set_ylabel('Costo Mensual')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def ejemplo_analisis_mantenimiento():
    """
    Ejemplo completo de análisis de mantenimiento
    """
    print("ANÁLISIS DE MANTENIMIENTO")
    print("-" * 40)
    
    # Generar datos de ejemplo
    datos_mtto = generar_datos_mantenimiento_ejemplo(200)
    print(f"Datos generados: {len(datos_mtto)} registros")
    
    # Calcular métricas básicas
    mtbf = calcular_mtbf(np.random.exponential(100, 50))
    mttr = calcular_mttr(np.random.exponential(4, 50))
    disponibilidad = calcular_disponibilidad(mtbf, mttr)
    
    print(f"MTBF: {mtbf:.1f} horas")
    print(f"MTTR: {mttr:.1f} horas")
    print(f"Disponibilidad: {disponibilidad:.3f}")
    
    # Generar curva de bañera
    tiempo = np.linspace(0, 1000, 1000)
    tasa_falla = generar_curva_bañera(tiempo)
    
    # Graficar curva de mantenimiento
    graficar_curva_mantenimiento(tiempo, tasa_falla, mtbf, mttr)
    
    # Análisis de costos
    analisis_costos = analizar_costo_mantenimiento(datos_mtto)
    print(f"\nAnálisis de Costos por Tipo:")
    print(analisis_costos['costo_por_tipo'])
    
    # Graficar análisis de costos
    graficar_analisis_costos(analisis_costos)
    
    # Análisis de tendencias
    tendencias = analizar_tendencias_mantenimiento(datos_mtto)
    print(f"\nTendencia de costos: {tendencias['tendencia_costo'][0]:.2f} por mes")
    print(f"Tendencia de tiempo: {tendencias['tendencia_tiempo'][0]:.2f} por mes")

if __name__ == "__main__":
    ejemplo_analisis_mantenimiento()
