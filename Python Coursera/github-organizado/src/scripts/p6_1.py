# -----------------------------------------------------------------------------
# Script: p6_1.py
# Propósito: Script para análisis de proyectos y programación
# Especialidad: Gestión de Proyectos / Programación
# Dependencias: numpy, matplotlib, pandas
# Uso: Importar funciones para análisis de proyectos
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

def calcular_ruta_critica(actividades, duraciones, dependencias):
    """
    Calcula la ruta crítica de un proyecto
    
    Args:
        actividades: Lista de nombres de actividades
        duraciones: Lista de duraciones en días
        dependencias: Lista de tuplas (actividad_predecesora, actividad_sucesora)
    
    Returns:
        Ruta crítica y duración total
    """
    # Crear matriz de adyacencia
    n = len(actividades)
    matriz = np.zeros((n, n))
    
    # Llenar matriz con dependencias
    for pred, succ in dependencias:
        i = actividades.index(pred)
        j = actividades.index(succ)
        matriz[i][j] = duraciones[i]
    
    # Calcular tiempos tempranos
    tiempos_early = np.zeros(n)
    for i in range(n):
        max_early = 0
        for j in range(n):
            if matriz[j][i] > 0:
                max_early = max(max_early, tiempos_early[j] + matriz[j][i])
        tiempos_early[i] = max_early
    
    # Calcular tiempos tardíos
    tiempos_late = np.full(n, tiempos_early[-1])
    for i in range(n-1, -1, -1):
        min_late = tiempos_late[-1]
        for j in range(n):
            if matriz[i][j] > 0:
                min_late = min(min_late, tiempos_late[j] - matriz[i][j])
        tiempos_late[i] = min_late
    
    # Identificar ruta crítica
    ruta_critica = []
    for i in range(n):
        if abs(tiempos_early[i] - tiempos_late[i]) < 0.001:
            ruta_critica.append(actividades[i])
    
    return ruta_critica, tiempos_early[-1]

def calcular_indices_rendimiento(planificado, real, costo_planificado, costo_real):
    """
    Calcula índices de rendimiento del proyecto
    
    Args:
        planificado: Valor planificado (PV)
        real: Valor ganado (EV)
        costo_planificado: Costo planificado (PV)
        costo_real: Costo real (AC)
    
    Returns:
        Diccionario con índices de rendimiento
    """
    # Índices de rendimiento
    spi = real / planificado if planificado > 0 else 0  # Schedule Performance Index
    cpi = real / costo_real if costo_real > 0 else 0    # Cost Performance Index
    
    # Variaciones
    sv = real - planificado  # Schedule Variance
    cv = real - costo_real   # Cost Variance
    
    # Estimaciones
    eac = costo_real + (planificado - real) / cpi if cpi > 0 else float('inf')  # Estimate at Completion
    etc = eac - costo_real  # Estimate to Complete
    
    return {
        'SPI': spi,
        'CPI': cpi,
        'SV': sv,
        'CV': cv,
        'EAC': eac,
        'ETC': etc
    }

def graficar_gantt(actividades, duraciones, dependencias):
    """
    Genera un diagrama de Gantt
    
    Args:
        actividades: Lista de nombres de actividades
        duraciones: Lista de duraciones
        dependencias: Lista de dependencias
    """
    # Calcular tiempos de inicio
    ruta_critica, duracion_total = calcular_ruta_critica(actividades, duraciones, dependencias)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Posiciones de las barras
    y_pos = np.arange(len(actividades))
    
    # Calcular tiempos de inicio (simplificado)
    tiempos_inicio = np.zeros(len(actividades))
    for i, actividad in enumerate(actividades):
        # Buscar predecesores
        for pred, succ in dependencias:
            if succ == actividad:
                pred_idx = actividades.index(pred)
                tiempos_inicio[i] = max(tiempos_inicio[i], 
                                      tiempos_inicio[pred_idx] + duraciones[pred_idx])
    
    # Dibujar barras
    colores = ['red' if act in ruta_critica else 'blue' for act in actividades]
    ax.barh(y_pos, duraciones, left=tiempos_inicio, color=colores, alpha=0.7)
    
    # Configurar gráfico
    ax.set_yticks(y_pos)
    ax.set_yticklabels(actividades)
    ax.set_xlabel('Tiempo (días)')
    ax.set_title('Diagrama de Gantt')
    ax.grid(True, alpha=0.3)
    
    # Agregar leyenda
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', alpha=0.7, label='Ruta Crítica'),
                      Patch(facecolor='blue', alpha=0.7, label='Actividades')]
    ax.legend(handles=legend_elements)
    
    plt.tight_layout()
    plt.show()

def analizar_riesgos(riesgos, probabilidades, impactos):
    """
    Analiza riesgos del proyecto
    
    Args:
        riesgos: Lista de descripciones de riesgos
        probabilidades: Lista de probabilidades (0-1)
        impactos: Lista de impactos (1-5)
    
    Returns:
        DataFrame con análisis de riesgos
    """
    # Calcular exposición al riesgo
    exposiciones = [prob * impacto for prob, impacto in zip(probabilidades, impactos)]
    
    # Crear DataFrame
    df = pd.DataFrame({
        'Riesgo': riesgos,
        'Probabilidad': probabilidades,
        'Impacto': impactos,
        'Exposición': exposiciones
    })
    
    # Ordenar por exposición
    df = df.sort_values('Exposición', ascending=False)
    
    # Categorizar riesgos
    df['Categoría'] = df['Exposición'].apply(lambda x: 
        'Alto' if x > 3 else 'Medio' if x > 1.5 else 'Bajo')
    
    return df

def graficar_curva_s(planificado, real, fechas):
    """
    Grafica curva S del proyecto
    
    Args:
        planificado: Valores planificados acumulados
        real: Valores reales acumulados
        fechas: Lista de fechas
    """
    plt.figure(figsize=(12, 6))
    
    # Convertir fechas a datetime si es necesario
    if isinstance(fechas[0], str):
        fechas = [datetime.strptime(f, '%Y-%m-%d') for f in fechas]
    
    # Graficar curvas
    plt.plot(fechas, planificado, 'b-', linewidth=2, label='Planificado (PV)')
    plt.plot(fechas, real, 'r-', linewidth=2, label='Real (EV)')
    
    # Configurar gráfico
    plt.xlabel('Fecha')
    plt.ylabel('Valor Acumulado')
    plt.title('Curva S del Proyecto')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

def ejemplo_analisis_proyecto():
    """
    Ejemplo de análisis completo de un proyecto
    """
    print("ANÁLISIS DE PROYECTO")
    print("-" * 40)
    
    # Datos del proyecto
    actividades = ['Inicio', 'Planificación', 'Diseño', 'Desarrollo', 'Pruebas', 'Implementación', 'Cierre']
    duraciones = [0, 5, 10, 15, 8, 5, 2]
    dependencias = [
        ('Inicio', 'Planificación'),
        ('Planificación', 'Diseño'),
        ('Diseño', 'Desarrollo'),
        ('Desarrollo', 'Pruebas'),
        ('Pruebas', 'Implementación'),
        ('Implementación', 'Cierre')
    ]
    
    # Calcular ruta crítica
    ruta_critica, duracion_total = calcular_ruta_critica(actividades, duraciones, dependencias)
    print(f"Ruta crítica: {' -> '.join(ruta_critica)}")
    print(f"Duración total: {duracion_total} días")
    
    # Análisis de rendimiento
    pv = 100000  # Valor planificado
    ev = 85000   # Valor ganado
    ac = 95000   # Costo real
    
    indices = calcular_indices_rendimiento(pv, ev, pv, ac)
    print(f"\nÍndices de Rendimiento:")
    print(f"SPI: {indices['SPI']:.2f}")
    print(f"CPI: {indices['CPI']:.2f}")
    print(f"Variación de cronograma: {indices['SV']:.0f}")
    print(f"Variación de costo: {indices['CV']:.0f}")
    
    # Análisis de riesgos
    riesgos = ['Retraso en desarrollo', 'Cambios de requerimientos', 'Problemas técnicos']
    probabilidades = [0.3, 0.2, 0.4]
    impactos = [4, 3, 5]
    
    df_riesgos = analizar_riesgos(riesgos, probabilidades, impactos)
    print(f"\nAnálisis de Riesgos:")
    print(df_riesgos)
    
    # Generar gráficos
    graficar_gantt(actividades, duraciones, dependencias)
    
    # Curva S
    fechas = ['2024-01-01', '2024-01-15', '2024-02-01', '2024-02-15', '2024-03-01']
    pv_acum = [0, 20000, 45000, 75000, 100000]
    ev_acum = [0, 18000, 40000, 65000, 85000]
    
    graficar_curva_s(pv_acum, ev_acum, fechas)

if __name__ == "__main__":
    ejemplo_analisis_proyecto()
