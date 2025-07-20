# -----------------------------------------------------------------------------
# Script: CURVA2.py
# Propósito: Script para análisis de curvas de confiabilidad
# Especialidad: Ingeniería de Confiabilidad / Análisis de Fallas
# Dependencias: numpy, matplotlib, pandas, scipy
# Uso: Importar funciones para análisis de confiabilidad
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit

def ajustar_distribucion_weibull(tiempos_falla):
    """
    Ajusta distribución Weibull a datos de falla
    
    Args:
        tiempos_falla: Array de tiempos de falla
    
    Returns:
        Diccionario con parámetros ajustados
    """
    # Ajustar Weibull usando scipy
    forma, loc, escala = stats.weibull_min.fit(tiempos_falla)
    
    return {
        'forma': forma,
        'escala': escala,
        'loc': loc,
        'funcion_confiabilidad': lambda t: np.exp(-((t - loc) / escala) ** forma),
        'funcion_tasa_falla': lambda t: (forma / escala) * ((t - loc) / escala) ** (forma - 1)
    }

def calcular_curva_supervivencia(tiempos, estados):
    """
    Calcula la curva de supervivencia (Kaplan-Meier)
    
    Args:
        tiempos: Array de tiempos
        estados: Array de estados (1 = falló, 0 = censurado)
    
    Returns:
        Diccionario con curva de supervivencia
    """
    # Ordenar datos
    datos = pd.DataFrame({'tiempo': tiempos, 'estado': estados})
    datos_ordenados = datos.sort_values('tiempo').reset_index(drop=True)
    
    # Calcular función de supervivencia
    n_total = len(datos_ordenados)
    supervivencia = []
    tiempos_km = []
    
    for i, (_, fila) in enumerate(datos_ordenados.iterrows()):
        if fila['estado'] == 1:  # Falló
            supervivencia.append((n_total - i) / n_total)
            tiempos_km.append(fila['tiempo'])
    
    return {
        'tiempos': tiempos_km,
        'supervivencia': supervivencia
    }

def calcular_metricas_confiabilidad(parametros_weibull):
    """
    Calcula métricas de confiabilidad usando parámetros Weibull
    
    Args:
        parametros_weibull: Diccionario con parámetros Weibull
    
    Returns:
        Diccionario con métricas
    """
    forma = parametros_weibull['forma']
    escala = parametros_weibull['escala']
    loc = parametros_weibull['loc']
    
    # Tiempo medio de vida (MTTF)
    mttf = escala * np.exp(np.log(2) / forma) + loc
    
    # Vida característica (tiempo al 63.2% de fallas)
    vida_caracteristica = escala + loc
    
    # Tiempo al 10%, 50% y 90% de fallas
    t10 = escala * (-np.log(0.9)) ** (1/forma) + loc
    t50 = escala * (-np.log(0.5)) ** (1/forma) + loc
    t90 = escala * (-np.log(0.1)) ** (1/forma) + loc
    
    return {
        'mttf': mttf,
        'vida_caracteristica': vida_caracteristica,
        't10': t10,
        't50': t50,
        't90': t90
    }

def graficar_curvas_confiabilidad(tiempos_falla, parametros_weibull=None, curva_supervivencia=None):
    """
    Grafica curvas de confiabilidad
    
    Args:
        tiempos_falla: Array de tiempos de falla
        parametros_weibull: Diccionario con parámetros Weibull (opcional)
        curva_supervivencia: Diccionario con curva de supervivencia (opcional)
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Histograma de tiempos de falla
    ax1.hist(tiempos_falla, bins=min(20, len(tiempos_falla)//3), density=True, 
            alpha=0.7, color='lightblue', edgecolor='black', label='Datos')
    
    if parametros_weibull is not None:
        # Función de densidad Weibull
        x_teorico = np.linspace(0, tiempos_falla.max() * 1.2, 1000)
        pdf_weibull = stats.weibull_min.pdf(x_teorico, 
                                          parametros_weibull['forma'],
                                          parametros_weibull['loc'],
                                          parametros_weibull['escala'])
        ax1.plot(x_teorico, pdf_weibull, 'r-', linewidth=2, label='PDF Weibull')
    
    ax1.set_xlabel('Tiempo de Falla')
    ax1.set_ylabel('Densidad de Probabilidad')
    ax1.set_title('Distribución de Tiempos de Falla')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Función de confiabilidad
    if parametros_weibull is not None:
        x_teorico = np.linspace(0, tiempos_falla.max() * 1.2, 1000)
        confiabilidad = parametros_weibull['funcion_confiabilidad'](x_teorico)
        ax2.plot(x_teorico, confiabilidad, 'b-', linewidth=2, label='Weibull')
    
    if curva_supervivencia is not None:
        ax2.plot(curva_supervivencia['tiempos'], curva_supervivencia['supervivencia'], 
                'ro', markersize=4, label='Kaplan-Meier')
    
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('Confiabilidad R(t)')
    ax2.set_title('Función de Confiabilidad')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # 3. Función de tasa de falla
    if parametros_weibull is not None:
        x_teorico = np.linspace(0, tiempos_falla.max() * 1.2, 1000)
        tasa_falla = parametros_weibull['funcion_tasa_falla'](x_teorico)
        ax3.plot(x_teorico, tasa_falla, 'g-', linewidth=2)
        ax3.set_xlabel('Tiempo')
        ax3.set_ylabel('Tasa de Falla λ(t)')
        ax3.set_title('Función de Tasa de Falla')
        ax3.grid(True, alpha=0.3)
    
    # 4. Gráfico de probabilidad Weibull
    if parametros_weibull is not None:
        # Ordenar datos
        datos_ordenados = np.sort(tiempos_falla)
        n = len(datos_ordenados)
        
        # Calcular probabilidades de falla
        prob_falla = [(i - 0.3) / (n + 0.4) for i in range(1, n + 1)]
        
        # Transformación Weibull
        x_weibull = np.log(datos_ordenados - parametros_weibull['loc'])
        y_weibull = np.log(-np.log(1 - np.array(prob_falla)))
        
        ax4.scatter(x_weibull, y_weibull, color='blue', alpha=0.7, s=50, label='Datos')
        
        # Línea de ajuste
        forma = parametros_weibull['forma']
        escala = parametros_weibull['escala']
        x_line = np.linspace(x_weibull.min(), x_weibull.max(), 100)
        y_line = forma * (x_line - np.log(escala))
        ax4.plot(x_line, y_line, 'r--', linewidth=2, label=f'Ajuste Weibull (β={forma:.2f})')
        
        ax4.set_xlabel('ln(Tiempo - γ)')
        ax4.set_ylabel('ln(-ln(1-F(t)))')
        ax4.set_title('Gráfico de Probabilidad Weibull')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
    
    plt.tight_layout()
    plt.show()

def test_bondad_ajuste(tiempos_falla, parametros_weibull):
    """
    Realiza test de bondad de ajuste
    
    Args:
        tiempos_falla: Array de tiempos de falla
        parametros_weibull: Diccionario con parámetros Weibull
    
    Returns:
        Diccionario con resultados del test
    """
    # Test Kolmogorov-Smirnov
    ks_statistic, p_value = stats.kstest(tiempos_falla, 'weibull_min', 
                                       args=(parametros_weibull['forma'],
                                             parametros_weibull['loc'],
                                             parametros_weibull['escala']))
    
    # Test Anderson-Darling
    ad_statistic, ad_critical_values, ad_significance_levels = stats.anderson(
        tiempos_falla, dist='weibull_min'
    )
    
    return {
        'ks_statistic': ks_statistic,
        'ks_p_value': p_value,
        'ad_statistic': ad_statistic,
        'ad_critical_values': ad_critical_values,
        'ad_significance_levels': ad_significance_levels
    }

def generar_datos_confiabilidad_ejemplo(n_muestras=100, forma=2.5, escala=1000, loc=0):
    """
    Genera datos de ejemplo para análisis de confiabilidad
    
    Args:
        n_muestras: Número de muestras
        forma: Parámetro de forma Weibull
        escala: Parámetro de escala Weibull
        loc: Parámetro de localización Weibull
    
    Returns:
        Array con tiempos de falla
    """
    np.random.seed(42)
    return np.random.weibull(forma, n_muestras) * escala + loc

def analizar_tendencias_falla(tiempos_falla, fechas_falla=None):
    """
    Analiza tendencias en los datos de falla
    
    Args:
        tiempos_falla: Array de tiempos de falla
        fechas_falla: Array de fechas de falla (opcional)
    
    Returns:
        Diccionario con análisis de tendencias
    """
    # Calcular estadísticas básicas
    estadisticas = {
        'media': np.mean(tiempos_falla),
        'mediana': np.median(tiempos_falla),
        'desv_std': np.std(tiempos_falla),
        'min': np.min(tiempos_falla),
        'max': np.max(tiempos_falla)
    }
    
    # Análisis de tendencias temporales si hay fechas
    tendencias = {}
    if fechas_falla is not None:
        # Convertir a DataFrame para análisis temporal
        df = pd.DataFrame({
            'fecha': pd.to_datetime(fechas_falla),
            'tiempo_falla': tiempos_falla
        })
        
        # Agrupar por mes
        df['mes'] = df['fecha'].dt.to_period('M')
        resumen_mensual = df.groupby('mes').agg({
            'tiempo_falla': ['count', 'mean', 'std']
        }).reset_index()
        
        # Calcular tendencia
        x = np.arange(len(resumen_mensual))
        y = resumen_mensual[('tiempo_falla', 'mean')].values
        tendencia = np.polyfit(x, y, 1)
        
        tendencias = {
            'resumen_mensual': resumen_mensual,
            'pendiente_tendencia': tendencia[0],
            'intercepto_tendencia': tendencia[1]
        }
    
    return {
        'estadisticas': estadisticas,
        'tendencias': tendencias
    }

def generar_reporte_confiabilidad(tiempos_falla, parametros_weibull, metricas, test_bondad):
    """
    Genera un reporte completo de análisis de confiabilidad
    
    Args:
        tiempos_falla: Array de tiempos de falla
        parametros_weibull: Diccionario con parámetros Weibull
        metricas: Diccionario con métricas de confiabilidad
        test_bondad: Diccionario con resultados del test de bondad de ajuste
    """
    print("=" * 70)
    print("REPORTE DE ANÁLISIS DE CONFIABILIDAD")
    print("=" * 70)
    
    print(f"INFORMACIÓN GENERAL:")
    print(f"Número de fallas: {len(tiempos_falla)}")
    print(f"Tiempo mínimo: {np.min(tiempos_falla):.2f}")
    print(f"Tiempo máximo: {np.max(tiempos_falla):.2f}")
    print(f"Tiempo medio: {np.mean(tiempos_falla):.2f}")
    print(f"Desviación estándar: {np.std(tiempos_falla):.2f}")
    
    print(f"\nPARÁMETROS WEIBULL:")
    print(f"Forma (β): {parametros_weibull['forma']:.3f}")
    print(f"Escala (η): {parametros_weibull['escala']:.3f}")
    print(f"Localización (γ): {parametros_weibull['loc']:.3f}")
    
    # Interpretación del parámetro de forma
    forma = parametros_weibull['forma']
    if forma < 1:
        print("Interpretación: Tasa de falla decreciente (mortalidad infantil)")
    elif forma == 1:
        print("Interpretación: Tasa de falla constante (fallas aleatorias)")
    else:
        print("Interpretación: Tasa de falla creciente (desgaste)")
    
    print(f"\nMÉTRICAS DE CONFIABILIDAD:")
    print(f"MTTF: {metricas['mttf']:.2f}")
    print(f"Vida característica (η): {metricas['vida_caracteristica']:.2f}")
    print(f"T10 (10% fallan antes): {metricas['t10']:.2f}")
    print(f"T50 (50% fallan antes): {metricas['t50']:.2f}")
    print(f"T90 (90% fallan antes): {metricas['t90']:.2f}")
    
    print(f"\nTEST DE BONDAD DE AJUSTE:")
    print(f"Kolmogorov-Smirnov:")
    print(f"  Estadístico: {test_bondad['ks_statistic']:.4f}")
    print(f"  Valor p: {test_bondad['ks_p_value']:.4f}")
    
    if test_bondad['ks_p_value'] > 0.05:
        print("  Conclusión: No se rechaza la hipótesis de distribución Weibull")
    else:
        print("  Conclusión: Se rechaza la hipótesis de distribución Weibull")
    
    print(f"Anderson-Darling:")
    print(f"  Estadístico: {test_bondad['ad_statistic']:.4f}")
    
    # Recomendaciones
    print(f"\nRECOMENDACIONES:")
    if forma < 1:
        print("- Implementar programa de rodaje para reducir fallas infantiles")
    elif forma > 3:
        print("- Implementar programa de mantenimiento preventivo más agresivo")
    
    if test_bondad['ks_p_value'] < 0.05:
        print("- Considerar otras distribuciones (Exponencial, Normal, Log-normal)")
    
    print("- Monitorear tendencias de falla para detectar cambios en el comportamiento")
    print("- Actualizar análisis periódicamente con nuevos datos")
    
    print("=" * 70)

def ejemplo_analisis_confiabilidad():
    """
    Ejemplo completo de análisis de confiabilidad
    """
    print("ANÁLISIS DE CONFIABILIDAD")
    print("-" * 40)
    
    # Generar datos de ejemplo
    tiempos_falla = generar_datos_confiabilidad_ejemplo(150, forma=2.5, escala=1000)
    print(f"Datos generados: {len(tiempos_falla)} fallas")
    
    # Ajustar distribución Weibull
    parametros_weibull = ajustar_distribucion_weibull(tiempos_falla)
    print(f"Ajuste Weibull completado")
    
    # Calcular métricas
    metricas = calcular_metricas_confiabilidad(parametros_weibull)
    
    # Test de bondad de ajuste
    test_bondad = test_bondad_ajuste(tiempos_falla, parametros_weibull)
    
    # Calcular curva de supervivencia
    estados = np.ones(len(tiempos_falla))  # Todas son fallas
    curva_supervivencia = calcular_curva_supervivencia(tiempos_falla, estados)
    
    # Generar gráficos
    graficar_curvas_confiabilidad(tiempos_falla, parametros_weibull, curva_supervivencia)
    
    # Generar reporte
    generar_reporte_confiabilidad(tiempos_falla, parametros_weibull, metricas, test_bondad)
    
    return tiempos_falla, parametros_weibull, metricas, test_bondad

if __name__ == "__main__":
    ejemplo_analisis_confiabilidad()
