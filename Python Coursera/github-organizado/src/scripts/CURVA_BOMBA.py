# -----------------------------------------------------------------------------
# Script: CURVA_BOMBA.py
# Propósito: Script para análisis de curvas de bomba
# Especialidad: Ingeniería Hidráulica / Bombas
# Dependencias: numpy, matplotlib, pandas
# Uso: Importar funciones para análisis de bombas
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

def calcular_curva_bomba(caudal_nominal, altura_nominal, potencia_nominal, eficiencia_max):
    """
    Calcula las curvas características de una bomba centrífuga
    
    Args:
        caudal_nominal: Caudal nominal (m³/h)
        altura_nominal: Altura nominal (m)
        potencia_nominal: Potencia nominal (kW)
        eficiencia_max: Eficiencia máxima (%)
    
    Returns:
        Diccionario con curvas calculadas
    """
    # Rango de caudales (0% a 140% del caudal nominal)
    caudal_max = caudal_nominal * 1.4
    caudal_min = 0
    caudales = np.linspace(caudal_min, caudal_max, 50)
    
    # Curva de altura (aproximación parabólica)
    # H = H_nominal * (1 - a*(Q/Q_nominal)^2)
    a = 0.3  # Factor de forma de la curva
    alturas = altura_nominal * (1 - a * (caudales / caudal_nominal) ** 2)
    alturas = np.maximum(alturas, 0)  # No puede ser negativa
    
    # Curva de eficiencia (aproximación parabólica)
    # η = η_max * (4*(Q/Q_nominal) - 4*(Q/Q_nominal)^2)
    eficiencias = eficiencia_max * (4 * (caudales / caudal_nominal) - 
                                  4 * (caudales / caudal_nominal) ** 2)
    eficiencias = np.maximum(eficiencias, 0)  # No puede ser negativa
    eficiencias = np.minimum(eficiencias, eficiencia_max)  # No puede superar el máximo
    
    # Curva de potencia al eje
    # P = (Q * H * ρ * g) / (η * 1000) [kW]
    rho = 1000  # Densidad del agua (kg/m³)
    g = 9.81    # Aceleración de gravedad (m/s²)
    
    potencias = (caudales * alturas * rho * g) / (eficiencias * 1000 * 100)
    potencias = np.where(eficiencias > 0, potencias, 0)
    
    return {
        'caudales': caudales,
        'alturas': alturas,
        'eficiencias': eficiencias,
        'potencias': potencias
    }

def calcular_punto_operacion(curva_bomba, curva_sistema):
    """
    Calcula el punto de operación de la bomba
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        curva_sistema: Diccionario con curva del sistema
    
    Returns:
        Punto de operación (caudal, altura)
    """
    caudales_bomba = curva_bomba['caudales']
    alturas_bomba = curva_bomba['alturas']
    caudales_sistema = curva_sistema['caudales']
    alturas_sistema = curva_sistema['alturas']
    
    # Interpolación para encontrar intersección
    from scipy.interpolate import interp1d
    
    # Interpolar curva del sistema a los caudales de la bomba
    f_sistema = interp1d(caudales_sistema, alturas_sistema, bounds_error=False, fill_value='extrapolate')
    alturas_sistema_interp = f_sistema(caudales_bomba)
    
    # Encontrar punto de intersección
    diferencia = np.abs(alturas_bomba - alturas_sistema_interp)
    idx_intersection = np.argmin(diferencia)
    
    caudal_op = caudales_bomba[idx_intersection]
    altura_op = alturas_bomba[idx_intersection]
    
    return caudal_op, altura_op

def calcular_curva_sistema(altura_estatica, factor_friccion, caudales):
    """
    Calcula la curva del sistema
    
    Args:
        altura_estatica: Altura estática (m)
        factor_friccion: Factor de fricción
        caudales: Array de caudales (m³/h)
    
    Returns:
        Array con alturas del sistema
    """
    # Curva del sistema: H = H_estatica + f * Q²
    alturas = altura_estatica + factor_friccion * (caudales / 100) ** 2
    return alturas

def graficar_curvas_bomba(curva_bomba, curva_sistema=None, punto_operacion=None):
    """
    Grafica las curvas de la bomba y del sistema
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        curva_sistema: Diccionario con curva del sistema (opcional)
        punto_operacion: Tupla (caudal, altura) del punto de operación (opcional)
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    caudales = curva_bomba['caudales']
    alturas = curva_bomba['alturas']
    eficiencias = curva_bomba['eficiencias']
    potencias = curva_bomba['potencias']
    
    # 1. Curva de altura
    ax1.plot(caudales, alturas, 'b-', linewidth=2, label='Curva de la Bomba')
    
    if curva_sistema is not None:
        ax1.plot(curva_sistema['caudales'], curva_sistema['alturas'], 
                'r-', linewidth=2, label='Curva del Sistema')
    
    if punto_operacion is not None:
        ax1.plot(punto_operacion[0], punto_operacion[1], 'ko', markersize=8, 
                label='Punto de Operación')
    
    ax1.set_xlabel('Caudal (m³/h)')
    ax1.set_ylabel('Altura (m)')
    ax1.set_title('Curva de Altura')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Curva de eficiencia
    ax2.plot(caudales, eficiencias, 'g-', linewidth=2)
    ax2.set_xlabel('Caudal (m³/h)')
    ax2.set_ylabel('Eficiencia (%)')
    ax2.set_title('Curva de Eficiencia')
    ax2.grid(True, alpha=0.3)
    
    # 3. Curva de potencia
    ax3.plot(caudales, potencias, 'r-', linewidth=2)
    ax3.set_xlabel('Caudal (m³/h)')
    ax3.set_ylabel('Potencia (kW)')
    ax3.set_title('Curva de Potencia')
    ax3.grid(True, alpha=0.3)
    
    # 4. Curvas combinadas
    ax4_twin = ax4.twinx()
    
    line1 = ax4.plot(caudales, alturas, 'b-', linewidth=2, label='Altura')
    ax4.set_xlabel('Caudal (m³/h)')
    ax4.set_ylabel('Altura (m)', color='b')
    ax4.tick_params(axis='y', labelcolor='b')
    
    line2 = ax4_twin.plot(caudales, eficiencias, 'g-', linewidth=2, label='Eficiencia')
    ax4_twin.set_ylabel('Eficiencia (%)', color='g')
    ax4_twin.tick_params(axis='y', labelcolor='g')
    
    ax4.set_title('Curvas Combinadas')
    ax4.grid(True, alpha=0.3)
    
    # Leyenda combinada
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='upper right')
    
    plt.tight_layout()
    plt.show()

def analizar_eficiencia_bomba(curva_bomba, caudal_operacion):
    """
    Analiza la eficiencia de la bomba en el punto de operación
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        caudal_operacion: Caudal de operación
    
    Returns:
        Diccionario con análisis de eficiencia
    """
    caudales = curva_bomba['caudales']
    eficiencias = curva_bomba['eficiencias']
    
    # Interpolar eficiencia en el punto de operación
    from scipy.interpolate import interp1d
    f_eficiencia = interp1d(caudales, eficiencias, bounds_error=False, fill_value='extrapolate')
    eficiencia_op = f_eficiencia(caudal_operacion)
    
    # Encontrar eficiencia máxima
    eficiencia_max = np.max(eficiencias)
    caudal_max_eficiencia = caudales[np.argmax(eficiencias)]
    
    # Calcular rango de eficiencia aceptable (>80% del máximo)
    eficiencia_min_aceptable = eficiencia_max * 0.8
    indices_aceptables = eficiencias >= eficiencia_min_aceptable
    rango_caudal_aceptable = (caudales[indices_aceptables].min(), caudales[indices_aceptables].max())
    
    return {
        'eficiencia_operacion': eficiencia_op,
        'eficiencia_maxima': eficiencia_max,
        'caudal_max_eficiencia': caudal_max_eficiencia,
        'rango_caudal_aceptable': rango_caudal_aceptable,
        'eficiencia_min_aceptable': eficiencia_min_aceptable
    }

def calcular_ahorro_energetico(curva_bomba, caudal_actual, caudal_optimizado):
    """
    Calcula el ahorro energético al optimizar el punto de operación
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        caudal_actual: Caudal actual de operación
        caudal_optimizado: Caudal optimizado
    
    Returns:
        Diccionario con ahorros calculados
    """
    caudales = curva_bomba['caudales']
    potencias = curva_bomba['potencias']
    
    # Interpolar potencias
    from scipy.interpolate import interp1d
    f_potencia = interp1d(caudales, potencias, bounds_error=False, fill_value='extrapolate')
    
    potencia_actual = f_potencia(caudal_actual)
    potencia_optimizada = f_potencia(caudal_optimizado)
    
    ahorro_potencia = potencia_actual - potencia_optimizada
    porcentaje_ahorro = (ahorro_potencia / potencia_actual) * 100 if potencia_actual > 0 else 0
    
    # Ahorro anual (asumiendo 8000 horas de operación)
    horas_anuales = 8000
    ahorro_energia_anual = ahorro_potencia * horas_anuales  # kWh
    
    return {
        'potencia_actual': potencia_actual,
        'potencia_optimizada': potencia_optimizada,
        'ahorro_potencia': ahorro_potencia,
        'porcentaje_ahorro': porcentaje_ahorro,
        'ahorro_energia_anual': ahorro_energia_anual
    }

def generar_reporte_bomba(curva_bomba, curva_sistema, punto_operacion):
    """
    Genera un reporte completo del análisis de la bomba
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        curva_sistema: Diccionario con curva del sistema
        punto_operacion: Tupla (caudal, altura) del punto de operación
    """
    caudal_op, altura_op = punto_operacion
    
    # Análisis de eficiencia
    analisis_eficiencia = analizar_eficiencia_bomba(curva_bomba, caudal_op)
    
    # Calcular potencia en el punto de operación
    caudales = curva_bomba['caudales']
    potencias = curva_bomba['potencias']
    from scipy.interpolate import interp1d
    f_potencia = interp1d(caudales, potencias, bounds_error=False, fill_value='extrapolate')
    potencia_op = f_potencia(caudal_op)
    
    print("=" * 60)
    print("REPORTE DE ANÁLISIS DE BOMBA")
    print("=" * 60)
    
    print(f"PUNTO DE OPERACIÓN:")
    print(f"Caudal: {caudal_op:.2f} m³/h")
    print(f"Altura: {altura_op:.2f} m")
    print(f"Potencia: {potencia_op:.2f} kW")
    
    print(f"\nANÁLISIS DE EFICIENCIA:")
    print(f"Eficiencia en punto de operación: {analisis_eficiencia['eficiencia_operacion']:.1f}%")
    print(f"Eficiencia máxima: {analisis_eficiencia['eficiencia_maxima']:.1f}%")
    print(f"Caudal de máxima eficiencia: {analisis_eficiencia['caudal_max_eficiencia']:.2f} m³/h")
    print(f"Rango de caudal eficiente: {analisis_eficiencia['rango_caudal_aceptable'][0]:.2f} - {analisis_eficiencia['rango_caudal_aceptable'][1]:.2f} m³/h")
    
    # Recomendaciones
    print(f"\nRECOMENDACIONES:")
    if analisis_eficiencia['eficiencia_operacion'] < analisis_eficiencia['eficiencia_min_aceptable']:
        print("- La bomba opera fuera del rango de eficiencia óptima")
        print("- Considerar ajustar el punto de operación")
    else:
        print("- La bomba opera en un rango de eficiencia aceptable")
    
    if caudal_op < analisis_eficiencia['rango_caudal_aceptable'][0]:
        print("- El caudal es menor al rango óptimo")
    elif caudal_op > analisis_eficiencia['rango_caudal_aceptable'][1]:
        print("- El caudal es mayor al rango óptimo")
    
    print("=" * 60)

def ejemplo_analisis_bomba():
    """
    Ejemplo completo de análisis de bomba
    """
    print("ANÁLISIS DE BOMBA CENTRÍFUGA")
    print("-" * 40)
    
    # Parámetros de la bomba
    caudal_nominal = 100  # m³/h
    altura_nominal = 50   # m
    potencia_nominal = 20 # kW
    eficiencia_max = 85   # %
    
    # Calcular curvas de la bomba
    curva_bomba = calcular_curva_bomba(caudal_nominal, altura_nominal, potencia_nominal, eficiencia_max)
    
    # Parámetros del sistema
    altura_estatica = 20  # m
    factor_friccion = 0.02
    
    # Calcular curva del sistema
    caudales_sistema = curva_bomba['caudales']
    alturas_sistema = calcular_curva_sistema(altura_estatica, factor_friccion, caudales_sistema)
    curva_sistema = {
        'caudales': caudales_sistema,
        'alturas': alturas_sistema
    }
    
    # Calcular punto de operación
    punto_operacion = calcular_punto_operacion(curva_bomba, curva_sistema)
    
    print(f"Punto de operación: {punto_operacion[0]:.2f} m³/h, {punto_operacion[1]:.2f} m")
    
    # Generar gráficos
    graficar_curvas_bomba(curva_bomba, curva_sistema, punto_operacion)
    
    # Generar reporte
    generar_reporte_bomba(curva_bomba, curva_sistema, punto_operacion)
    
    return curva_bomba, curva_sistema, punto_operacion

if __name__ == "__main__":
    ejemplo_analisis_bomba()
