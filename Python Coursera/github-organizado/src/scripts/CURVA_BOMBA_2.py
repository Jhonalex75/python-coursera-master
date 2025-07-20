# -----------------------------------------------------------------------------
# Script: CURVA_BOMBA_2.py
# Propósito: Script para análisis avanzado de curvas de bomba
# Especialidad: Ingeniería Hidráulica / Bombas
# Dependencias: numpy, matplotlib, pandas, scipy
# Uso: Importar funciones para análisis avanzado de bombas
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

def ajustar_curva_bomba_datos(caudales_medidos, alturas_medidas, eficiencias_medidas=None):
    """
    Ajusta curvas de bomba a datos medidos
    
    Args:
        caudales_medidos: Array de caudales medidos (m³/h)
        alturas_medidas: Array de alturas medidas (m)
        eficiencias_medidas: Array de eficiencias medidas (%) (opcional)
    
    Returns:
        Diccionario con parámetros ajustados
    """
    # Ajustar curva de altura (polinomio de segundo grado)
    def curva_altura(Q, a, b, c):
        return a * Q**2 + b * Q + c
    
    # Ajustar curva de eficiencia (polinomio de segundo grado)
    def curva_eficiencia(Q, a, b, c):
        return a * Q**2 + b * Q + c
    
    # Ajustar altura
    popt_altura, pcov_altura = curve_fit(curva_altura, caudales_medidos, alturas_medidas)
    
    # Ajustar eficiencia si hay datos
    popt_eficiencia = None
    if eficiencias_medidas is not None:
        popt_eficiencia, pcov_eficiencia = curve_fit(curva_eficiencia, caudales_medidos, eficiencias_medidas)
    
    return {
        'parametros_altura': popt_altura,
        'parametros_eficiencia': popt_eficiencia,
        'funcion_altura': lambda Q: curva_altura(Q, *popt_altura),
        'funcion_eficiencia': lambda Q: curva_eficiencia(Q, *popt_eficiencia) if popt_eficiencia is not None else None
    }

def calcular_curva_bomba_ajustada(parametros, caudales):
    """
    Calcula curvas de bomba usando parámetros ajustados
    
    Args:
        parametros: Diccionario con parámetros ajustados
        caudales: Array de caudales
    
    Returns:
        Diccionario con curvas calculadas
    """
    alturas = parametros['funcion_altura'](caudales)
    
    eficiencias = None
    if parametros['funcion_eficiencia'] is not None:
        eficiencias = parametros['funcion_eficiencia'](caudales)
        eficiencias = np.maximum(eficiencias, 0)  # No puede ser negativa
    
    # Calcular potencias
    potencias = None
    if eficiencias is not None:
        rho = 1000  # kg/m³
        g = 9.81    # m/s²
        potencias = (caudales * alturas * rho * g) / (eficiencias * 1000 * 100)
        potencias = np.where(eficiencias > 0, potencias, 0)
    
    return {
        'caudales': caudales,
        'alturas': alturas,
        'eficiencias': eficiencias,
        'potencias': potencias
    }

def analizar_estabilidad_bomba(curva_bomba, curva_sistema):
    """
    Analiza la estabilidad del punto de operación
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        curva_sistema: Diccionario con curva del sistema
    
    Returns:
        Diccionario con análisis de estabilidad
    """
    caudales = curva_bomba['caudales']
    alturas_bomba = curva_bomba['alturas']
    alturas_sistema = curva_sistema['alturas']
    
    # Encontrar puntos de intersección
    diferencias = alturas_bomba - alturas_sistema
    cambios_signo = np.diff(np.sign(diferencias))
    puntos_interseccion = np.where(cambios_signo != 0)[0]
    
    # Analizar estabilidad en cada punto
    estabilidad = []
    for idx in puntos_interseccion:
        if idx < len(caudales) - 1:
            # Calcular pendientes
            pendiente_bomba = (alturas_bomba[idx+1] - alturas_bomba[idx]) / (caudales[idx+1] - caudales[idx])
            pendiente_sistema = (alturas_sistema[idx+1] - alturas_sistema[idx]) / (caudales[idx+1] - caudales[idx])
            
            # Criterio de estabilidad: pendiente_bomba < pendiente_sistema
            es_estable = pendiente_bomba < pendiente_sistema
            
            estabilidad.append({
                'caudal': caudales[idx],
                'altura': alturas_bomba[idx],
                'es_estable': es_estable,
                'pendiente_bomba': pendiente_bomba,
                'pendiente_sistema': pendiente_sistema
            })
    
    return estabilidad

def calcular_cavitation_npsh(caudal, velocidad_rotacion, diametro_impulsor):
    """
    Calcula el NPSH requerido para evitar cavitación
    
    Args:
        caudal: Caudal de operación (m³/h)
        velocidad_rotacion: Velocidad de rotación (RPM)
        diametro_impulsor: Diámetro del impulsor (m)
    
    Returns:
        NPSH requerido (m)
    """
    # Fórmula simplificada para NPSH
    # NPSH = K * (Q/N)^(2/3) * (N*D)^(4/3)
    K = 0.001  # Factor específico de la bomba
    
    caudal_m3s = caudal / 3600  # Convertir a m³/s
    velocidad_rads = velocidad_rotacion * 2 * np.pi / 60  # Convertir a rad/s
    
    npsh = K * (caudal_m3s / velocidad_rads)**(2/3) * (velocidad_rads * diametro_impulsor)**(4/3)
    
    return npsh

def analizar_curva_caracteristica_avanzada(curva_bomba, parametros_bomba):
    """
    Análisis avanzado de la curva característica
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        parametros_bomba: Diccionario con parámetros de la bomba
    
    Returns:
        Diccionario con análisis avanzado
    """
    caudales = curva_bomba['caudales']
    alturas = curva_bomba['alturas']
    eficiencias = curva_bomba['eficiencias']
    
    # Encontrar punto de máxima eficiencia
    if eficiencias is not None:
        idx_max_eficiencia = np.argmax(eficiencias)
        caudal_bep = caudales[idx_max_eficiencia]  # Best Efficiency Point
        eficiencia_max = eficiencias[idx_max_eficiencia]
        altura_bep = alturas[idx_max_eficiencia]
    else:
        caudal_bep = None
        eficiencia_max = None
        altura_bep = None
    
    # Calcular rango de operación recomendado (±10% del BEP)
    if caudal_bep is not None:
        rango_recomendado = (caudal_bep * 0.9, caudal_bep * 1.1)
    else:
        rango_recomendado = None
    
    # Calcular pendiente de la curva de altura
    pendientes = np.gradient(alturas, caudales)
    
    # Encontrar región de estabilidad (pendiente negativa)
    region_estable = pendientes < 0
    
    return {
        'caudal_bep': caudal_bep,
        'eficiencia_max': eficiencia_max,
        'altura_bep': altura_bep,
        'rango_recomendado': rango_recomendado,
        'pendientes': pendientes,
        'region_estable': region_estable
    }

def graficar_analisis_avanzado(curva_bomba, curva_sistema, analisis_avanzado, punto_operacion=None):
    """
    Grafica análisis avanzado de la bomba
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        curva_sistema: Diccionario con curva del sistema
        analisis_avanzado: Diccionario con análisis avanzado
        punto_operacion: Tupla (caudal, altura) del punto de operación
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    caudales = curva_bomba['caudales']
    alturas = curva_bomba['alturas']
    eficiencias = curva_bomba['eficiencias']
    
    # 1. Curvas con regiones de estabilidad
    ax1.plot(caudales, alturas, 'b-', linewidth=2, label='Curva de la Bomba')
    ax1.plot(curva_sistema['caudales'], curva_sistema['alturas'], 
            'r-', linewidth=2, label='Curva del Sistema')
    
    # Marcar región estable
    if analisis_avanzado['region_estable'] is not None:
        caudales_estable = caudales[analisis_avanzado['region_estable']]
        alturas_estable = alturas[analisis_avanzado['region_estable']]
        ax1.plot(caudales_estable, alturas_estable, 'g-', linewidth=4, alpha=0.7, label='Región Estable')
    
    if punto_operacion is not None:
        ax1.plot(punto_operacion[0], punto_operacion[1], 'ko', markersize=8, label='Punto de Operación')
    
    ax1.set_xlabel('Caudal (m³/h)')
    ax1.set_ylabel('Altura (m)')
    ax1.set_title('Análisis de Estabilidad')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Curva de eficiencia con BEP
    if eficiencias is not None:
        ax2.plot(caudales, eficiencias, 'g-', linewidth=2)
        
        if analisis_avanzado['caudal_bep'] is not None:
            ax2.axvline(x=analisis_avanzado['caudal_bep'], color='r', linestyle='--', 
                       label=f'BEP: {analisis_avanzado["caudal_bep"]:.1f} m³/h')
            
            # Marcar rango recomendado
            if analisis_avanzado['rango_recomendado'] is not None:
                ax2.axvspan(analisis_avanzado['rango_recomendado'][0], 
                           analisis_avanzado['rango_recomendado'][1], 
                           alpha=0.3, color='yellow', label='Rango Recomendado')
        
        ax2.set_xlabel('Caudal (m³/h)')
        ax2.set_ylabel('Eficiencia (%)')
        ax2.set_title('Punto de Máxima Eficiencia (BEP)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
    
    # 3. Pendiente de la curva de altura
    if analisis_avanzado['pendientes'] is not None:
        ax3.plot(caudales, analisis_avanzado['pendientes'], 'purple', linewidth=2)
        ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Caudal (m³/h)')
        ax3.set_ylabel('Pendiente (m/(m³/h))')
        ax3.set_title('Pendiente de la Curva de Altura')
        ax3.grid(True, alpha=0.3)
    
    # 4. Análisis de cavitación
    velocidad_rotacion = 1750  # RPM típica
    diametro_impulsor = 0.3    # m
    npsh_requerido = calcular_cavitation_npsh(caudales, velocidad_rotacion, diametro_impulsor)
    
    ax4.plot(caudales, npsh_requerido, 'orange', linewidth=2)
    ax4.set_xlabel('Caudal (m³/h)')
    ax4.set_ylabel('NPSH Requerido (m)')
    ax4.set_title('Análisis de Cavitación')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def generar_reporte_avanzado(curva_bomba, curva_sistema, analisis_avanzado, punto_operacion):
    """
    Genera un reporte avanzado del análisis de la bomba
    
    Args:
        curva_bomba: Diccionario con curvas de la bomba
        curva_sistema: Diccionario con curva del sistema
        analisis_avanzado: Diccionario con análisis avanzado
        punto_operacion: Tupla (caudal, altura) del punto de operación
    """
    caudal_op, altura_op = punto_operacion
    
    print("=" * 70)
    print("REPORTE AVANZADO DE ANÁLISIS DE BOMBA")
    print("=" * 70)
    
    print(f"PUNTO DE OPERACIÓN:")
    print(f"Caudal: {caudal_op:.2f} m³/h")
    print(f"Altura: {altura_op:.2f} m")
    
    print(f"\nANÁLISIS DE EFICIENCIA:")
    if analisis_avanzado['caudal_bep'] is not None:
        print(f"Punto de máxima eficiencia (BEP): {analisis_avanzado['caudal_bep']:.2f} m³/h")
        print(f"Eficiencia máxima: {analisis_avanzado['eficiencia_max']:.1f}%")
        print(f"Altura en BEP: {analisis_avanzado['altura_bep']:.2f} m")
        
        # Evaluar posición relativa al BEP
        desviacion_bep = abs(caudal_op - analisis_avanzado['caudal_bep']) / analisis_avanzado['caudal_bep'] * 100
        print(f"Desviación del BEP: {desviacion_bep:.1f}%")
        
        if desviacion_bep > 20:
            print("ADVERTENCIA: Operación significativamente alejada del BEP")
        elif desviacion_bep > 10:
            print("PRECAUCIÓN: Operación moderadamente alejada del BEP")
        else:
            print("OPERACIÓN ÓPTIMA: Cerca del punto de máxima eficiencia")
    
    print(f"\nANÁLISIS DE ESTABILIDAD:")
    # Verificar si el punto de operación está en región estable
    if analisis_avanzado['region_estable'] is not None:
        idx_op = np.argmin(np.abs(curva_bomba['caudales'] - caudal_op))
        if idx_op < len(analisis_avanzado['region_estable']):
            es_estable = analisis_avanzado['region_estable'][idx_op]
            if es_estable:
                print("✓ Punto de operación en región estable")
            else:
                print("⚠ Punto de operación en región inestable")
    
    print(f"\nANÁLISIS DE CAVITACIÓN:")
    velocidad_rotacion = 1750  # RPM
    diametro_impulsor = 0.3    # m
    npsh_requerido = calcular_cavitation_npsh(caudal_op, velocidad_rotacion, diametro_impulsor)
    print(f"NPSH requerido: {npsh_requerido:.2f} m")
    
    # Recomendaciones
    print(f"\nRECOMENDACIONES:")
    if analisis_avanzado['rango_recomendado'] is not None:
        if caudal_op < analisis_avanzado['rango_recomendado'][0]:
            print("- Considerar aumentar el caudal de operación")
        elif caudal_op > analisis_avanzado['rango_recomendado'][1]:
            print("- Considerar reducir el caudal de operación")
        else:
            print("- El caudal está en el rango recomendado")
    
    print("- Monitorear vibraciones y ruidos para detectar cavitación")
    print("- Verificar que el NPSH disponible sea mayor al requerido")
    print("- Realizar mantenimiento preventivo según recomendaciones del fabricante")
    
    print("=" * 70)

def ejemplo_analisis_avanzado():
    """
    Ejemplo completo de análisis avanzado de bomba
    """
    print("ANÁLISIS AVANZADO DE BOMBA CENTRÍFUGA")
    print("-" * 50)
    
    # Datos de ejemplo (mediciones reales)
    caudales_medidos = np.array([0, 20, 40, 60, 80, 100, 120, 140])
    alturas_medidas = np.array([55, 54, 52, 49, 45, 40, 34, 27])
    eficiencias_medidas = np.array([0, 45, 70, 85, 82, 75, 60, 40])
    
    # Ajustar curvas a datos medidos
    parametros_ajustados = ajustar_curva_bomba_datos(caudales_medidos, alturas_medidas, eficiencias_medidas)
    
    # Generar curvas ajustadas
    caudales = np.linspace(0, 150, 100)
    curva_bomba = calcular_curva_bomba_ajustada(parametros_ajustados, caudales)
    
    # Curva del sistema
    altura_estatica = 20
    factor_friccion = 0.02
    alturas_sistema = altura_estatica + factor_friccion * (caudales / 100) ** 2
    curva_sistema = {
        'caudales': caudales,
        'alturas': alturas_sistema
    }
    
    # Punto de operación
    from scipy.interpolate import interp1d
    f_bomba = interp1d(curva_bomba['caudales'], curva_bomba['alturas'])
    f_sistema = interp1d(curva_sistema['caudales'], curva_sistema['alturas'])
    
    # Encontrar intersección
    diferencias = f_bomba(caudales) - f_sistema(caudales)
    idx_intersection = np.argmin(np.abs(diferencias))
    punto_operacion = (caudales[idx_intersection], curva_bomba['alturas'][idx_intersection])
    
    # Análisis avanzado
    analisis_avanzado = analizar_curva_caracteristica_avanzada(curva_bomba, {})
    
    print(f"Punto de operación: {punto_operacion[0]:.2f} m³/h, {punto_operacion[1]:.2f} m")
    
    # Generar gráficos
    graficar_analisis_avanzado(curva_bomba, curva_sistema, analisis_avanzado, punto_operacion)
    
    # Generar reporte
    generar_reporte_avanzado(curva_bomba, curva_sistema, analisis_avanzado, punto_operacion)
    
    return curva_bomba, curva_sistema, analisis_avanzado, punto_operacion

if __name__ == "__main__":
    ejemplo_analisis_avanzado()
