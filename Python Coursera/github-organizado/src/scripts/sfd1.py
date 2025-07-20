# -----------------------------------------------------------------------------
# Script: sfd1.py
# Propósito: Script de utilidad para cálculos de ingeniería estructural
# Especialidad: Ingeniería Civil / Estructural
# Dependencias: numpy, matplotlib
# Uso: Importar funciones para cálculos estructurales
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

def calcular_momento_flector(fuerza, distancia):
    """
    Calcula el momento flector
    
    Args:
        fuerza: Fuerza aplicada (N)
        distancia: Distancia al punto de aplicación (m)
    
    Returns:
        Momento flector (N·m)
    """
    return fuerza * distancia

def calcular_esfuerzo_corte(fuerza, area):
    """
    Calcula el esfuerzo cortante
    
    Args:
        fuerza: Fuerza cortante (N)
        area: Área de la sección (m²)
    
    Returns:
        Esfuerzo cortante (Pa)
    """
    return fuerza / area

def calcular_esfuerzo_normal(fuerza, area):
    """
    Calcula el esfuerzo normal
    
    Args:
        fuerza: Fuerza axial (N)
        area: Área de la sección (m²)
    
    Returns:
        Esfuerzo normal (Pa)
    """
    return fuerza / area

def calcular_deformacion_axial(esfuerzo, modulo_elasticidad):
    """
    Calcula la deformación axial
    
    Args:
        esfuerzo: Esfuerzo normal (Pa)
        modulo_elasticidad: Módulo de elasticidad (Pa)
    
    Returns:
        Deformación axial (adimensional)
    """
    return esfuerzo / modulo_elasticidad

def calcular_flecha_viga_simples(fuerza, longitud, modulo_elasticidad, momento_inercia):
    """
    Calcula la flecha máxima de una viga simplemente apoyada con carga puntual central
    
    Args:
        fuerza: Fuerza aplicada (N)
        longitud: Longitud de la viga (m)
        modulo_elasticidad: Módulo de elasticidad (Pa)
        momento_inercia: Momento de inercia (m⁴)
    
    Returns:
        Flecha máxima (m)
    """
    return (fuerza * longitud**3) / (48 * modulo_elasticidad * momento_inercia)

def calcular_momento_inercia_rectangular(base, altura):
    """
    Calcula el momento de inercia de una sección rectangular
    
    Args:
        base: Base del rectángulo (m)
        altura: Altura del rectángulo (m)
    
    Returns:
        Momento de inercia (m⁴)
    """
    return (base * altura**3) / 12

def calcular_momento_inercia_circular(diametro):
    """
    Calcula el momento de inercia de una sección circular
    
    Args:
        diametro: Diámetro de la sección (m)
    
    Returns:
        Momento de inercia (m⁴)
    """
    return (np.pi * diametro**4) / 64

def graficar_diagramas_viga(longitud, cargas, apoyos):
    """
    Grafica diagramas de momento flector y esfuerzo cortante
    
    Args:
        longitud: Longitud de la viga (m)
        cargas: Lista de tuplas (posición, magnitud) de cargas
        apoyos: Lista de posiciones de apoyos
    """
    x = np.linspace(0, longitud, 100)
    
    # Calcular reacciones (simplificado)
    fuerza_total = sum(carga[1] for carga in cargas)
    reaccion = fuerza_total / len(apoyos)
    
    # Calcular momento flector y cortante
    momento = np.zeros_like(x)
    cortante = np.zeros_like(x)
    
    for i, xi in enumerate(x):
        # Esfuerzo cortante
        cortante[i] = reaccion
        for pos, mag in cargas:
            if xi > pos:
                cortante[i] -= mag
        
        # Momento flector
        momento[i] = reaccion * xi
        for pos, mag in cargas:
            if xi > pos:
                momento[i] -= mag * (xi - pos)
    
    # Crear gráficos
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Diagrama de esfuerzo cortante
    ax1.plot(x, cortante, 'b-', linewidth=2)
    ax1.set_xlabel('Posición (m)')
    ax1.set_ylabel('Esfuerzo Cortante (N)')
    ax1.set_title('Diagrama de Esfuerzo Cortante')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Diagrama de momento flector
    ax2.plot(x, momento, 'r-', linewidth=2)
    ax2.set_xlabel('Posición (m)')
    ax2.set_ylabel('Momento Flector (N·m)')
    ax2.set_title('Diagrama de Momento Flector')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def ejemplo_calculos():
    """
    Ejemplo de uso de las funciones de cálculo estructural
    """
    print("EJEMPLO DE CÁLCULOS ESTRUCTURALES")
    print("-" * 40)
    
    # Parámetros de ejemplo
    fuerza = 10000  # N
    longitud = 5.0   # m
    base = 0.2       # m
    altura = 0.3     # m
    modulo_elasticidad = 2.1e11  # Pa (acero)
    
    # Cálculos
    momento_inercia = calcular_momento_inercia_rectangular(base, altura)
    flecha = calcular_flecha_viga_simples(fuerza, longitud, modulo_elasticidad, momento_inercia)
    esfuerzo_normal = calcular_esfuerzo_normal(fuerza, base * altura)
    
    print(f"Momento de inercia: {momento_inercia:.2e} m⁴")
    print(f"Flecha máxima: {flecha:.6f} m")
    print(f"Esfuerzo normal: {esfuerzo_normal:.2e} Pa")
    
    # Graficar diagramas
    cargas = [(longitud/2, fuerza)]  # Carga central
    apoyos = [0, longitud]  # Apoyos en extremos
    graficar_diagramas_viga(longitud, cargas, apoyos)

if __name__ == "__main__":
    ejemplo_calculos()
