#!/usr/bin/env python3
"""
Ejemplo de Uso Completo - Proyecto de Ingeniería Mecánica
========================================================

Este script demuestra el uso de todas las herramientas principales del proyecto
de ingeniería mecánica, incluyendo análisis de bombas, métodos numéricos,
gestión de mantenimiento y visualización de datos.

Autor: Ing. Jhon A. Valencia
Fecha: 2024
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🏭 PROYECTO DE INGENIERÍA MECÁNICA")
    print("=" * 50)
    print("Ejemplo de uso completo de todas las herramientas")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Ejemplo 1: Análisis de Curvas de Bomba
        print("1️⃣ ANÁLISIS DE CURVAS DE BOMBA")
        print("-" * 30)
        ejemplo_curvas_bomba()
        
        # Ejemplo 2: Métodos Numéricos
        print("\n2️⃣ MÉTODOS NUMÉRICOS - RUNGE-KUTTA")
        print("-" * 30)
        ejemplo_metodos_numericos()
        
        # Ejemplo 3: Gestión de Mantenimiento
        print("\n3️⃣ GESTIÓN DE MANTENIMIENTO")
        print("-" * 30)
        ejemplo_gestion_mantenimiento()
        
        # Ejemplo 4: Análisis de Confiabilidad
        print("\n4️⃣ ANÁLISIS DE CONFIABILIDAD")
        print("-" * 30)
        ejemplo_analisis_confiabilidad()
        
        # Ejemplo 5: Visualización de Datos
        print("\n5️⃣ VISUALIZACIÓN DE DATOS")
        print("-" * 30)
        ejemplo_visualizacion()
        
        print("\n✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("📊 Los gráficos se han generado y guardado")
        print("📁 Revisa la carpeta 'outputs' para ver los resultados")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de tener todas las dependencias instaladas:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        print("💡 Revisa los logs para más detalles")

def ejemplo_curvas_bomba():
    """Ejemplo de análisis de curvas de bomba."""
    try:
        from ingenieria.CURVA_BOMBA import SimuladorCurvaBomba
        
        print("📊 Generando curvas de bomba centrífuga...")
        
        # Crear datos de ejemplo
        caudal = np.linspace(0, 120, 100)  # L/min
        altura_nominal = 50  # m
        caudal_nominal = 80  # L/min
        
        # Curva de altura (H-Q)
        altura = altura_nominal * (1 - (caudal/caudal_nominal)**2)
        altura[caudal > caudal_nominal] = 0
        
        # Curva de eficiencia
        eficiencia_max = 85  # %
        eficiencia = eficiencia_max * (1 - ((caudal - caudal_nominal) / caudal_nominal)**2)
        eficiencia[eficiencia < 0] = 0
        
        # Visualizar
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.plot(caudal, altura, 'b-', linewidth=2, label='Altura')
        ax1.set_xlabel('Caudal (L/min)')
        ax1.set_ylabel('Altura (m)')
        ax1.set_title('Curva Altura-Caudal')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.plot(caudal, eficiencia, 'g-', linewidth=2, label='Eficiencia')
        ax2.set_xlabel('Caudal (L/min)')
        ax2.set_ylabel('Eficiencia (%)')
        ax2.set_title('Curva Eficiencia-Caudal')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig('outputs/curvas_bomba.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Curvas de bomba generadas y guardadas")
        
        # Análisis del punto de operación
        punto_op = (60, 28)  # Caudal y altura de operación
        print(f"📍 Punto de operación: {punto_op[0]} L/min, {punto_op[1]} m")
        
    except ImportError:
        print("⚠️ Módulo de curvas de bomba no disponible")

def ejemplo_metodos_numericos():
    """Ejemplo de métodos numéricos con Runge-Kutta."""
    try:
        from ingenieria.RUNGE_KUTTA import MetodoRungeKutta
        
        print("🔢 Resolviendo EDO con método de Runge-Kutta...")
        
        # Definir EDO: dy/dt = -y (decaimiento exponencial)
        def f(t, y):
            return -y
        
        # Solución analítica para comparación
        def y_analitica(t):
            return np.exp(-t)
        
        # Resolver con RK4
        rk = MetodoRungeKutta()
        t, y = rk.runge_kutta_4(f, y0=1.0, t0=0.0, tf=5.0, h=0.1)
        
        # Comparar con solución analítica
        y_exacta = y_analitica(t)
        error = np.abs(y - y_exacta)
        
        # Visualizar resultados
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.plot(t, y, 'b-', linewidth=2, label='RK4')
        ax1.plot(t, y_exacta, 'r--', linewidth=2, label='Analítica')
        ax1.set_xlabel('Tiempo')
        ax1.set_ylabel('y(t)')
        ax1.set_title('Solución EDO: dy/dt = -y')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.semilogy(t, error, 'g-', linewidth=2)
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('Error Absoluto')
        ax2.set_title('Error del Método RK4')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/metodo_runge_kutta.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ EDO resuelta. Error máximo: {np.max(error):.6f}")
        
    except ImportError:
        print("⚠️ Módulo de métodos numéricos no disponible")

def ejemplo_gestion_mantenimiento():
    """Ejemplo de gestión de mantenimiento."""
    try:
        from mantenimiento.gestion_mtto import GestionMantenimiento
        
        print("🔧 Analizando sistema de mantenimiento...")
        
        # Crear sistema de gestión
        gestion = GestionMantenimiento()
        
        # Analizar costos
        resultados_costos = gestion.analizar_costos_mtto()
        
        # Calcular indicadores
        indicadores = gestion.calcular_indicadores_mtto()
        
        print("📊 Resultados del análisis de mantenimiento:")
        print(f"   • Total de equipos: {len(gestion.equipos)}")
        print(f"   • Órdenes de trabajo: {len(gestion.historial_mtto)}")
        
        if isinstance(indicadores, str):
            print(f"   • Indicadores: {indicadores}")
        else:
            print("   • Indicadores calculados exitosamente")
        
        # Obtener historial de un equipo específico
        equipo_id = "BOM-001"
        historial = gestion.obtener_historial_equipo(equipo_id)
        
        if isinstance(historial, str):
            print(f"   • Historial {equipo_id}: {historial}")
        else:
            print(f"   • Historial {equipo_id}: {len(historial)} registros")
        
        print("✅ Análisis de mantenimiento completado")
        
    except ImportError:
        print("⚠️ Módulo de gestión de mantenimiento no disponible")

def ejemplo_analisis_confiabilidad():
    """Ejemplo de análisis de confiabilidad."""
    try:
        from ingenieria.curva_mtto import AnalizadorConfiabilidad
        
        print("📈 Generando curva de bañera...")
        
        # Crear analizador
        analizador = AnalizadorConfiabilidad()
        
        # Generar curva de bañera
        tiempo, tasa_falla = analizador.curva_banera(
            tiempo_max=100,
            tasa_falla_inicial=0.15,
            tasa_falla_estable=0.02,
            tasa_falla_desgaste=0.20
        )
        
        # Visualizar curva
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(tiempo, tasa_falla, 'b-', linewidth=3, label='Tasa de Falla')
        
        # Identificar fases
        idx_min = np.argmin(tasa_falla)
        
        # Fase 1: Mortalidad infantil
        ax.fill_between(tiempo[:idx_min], 0, tasa_falla[:idx_min], 
                       alpha=0.3, color='red', label='Mortalidad Infantil')
        
        # Fase 2: Vida útil
        ax.fill_between(tiempo[idx_min:], 0, tasa_falla[idx_min:], 
                       alpha=0.3, color='green', label='Vida Útil')
        
        ax.set_xlabel('Tiempo (unidades)', fontweight='bold')
        ax.set_ylabel('Tasa de Falla λ(t)', fontweight='bold')
        ax.set_title('Curva de Bañera - Análisis de Confiabilidad', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        plt.savefig('outputs/curva_banera.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Curva de bañera generada")
        
        # Análisis de mantenimiento preventivo
        analisis = analizador.calcular_mantenimiento_preventivo(
            tiempo_operacion=1000,
            tasa_falla_critica=0.001,
            costo_mtto_preventivo=5000,
            costo_mtto_correctivo=25000
        )
        
        print(f"💡 Recomendación: {analisis['recomendacion']}")
        print(f"💰 Ahorro esperado: ${analisis['ahorro_esperado']:.2f}")
        
    except ImportError:
        print("⚠️ Módulo de análisis de confiabilidad no disponible")

def ejemplo_visualizacion():
    """Ejemplo de visualización de datos."""
    try:
        from ingenieria.Grafica_Duran import VisualizadorIngenieria
        
        print("📊 Creando visualizaciones profesionales...")
        
        # Crear visualizador
        vis = VisualizadorIngenieria(estilo="ingenieria")
        
        # Datos de ejemplo
        x = np.linspace(0, 10, 100)
        y1 = 50 * np.exp(-x/5)
        y2 = 40 * np.exp(-x/3)
        y3 = 60 * np.exp(-x/7)
        
        # Gráfico comparativo
        datos = {
            'Sistema A': (x, y1),
            'Sistema B': (x, y2),
            'Sistema C': (x, y3)
        }
        
        fig = vis.grafico_comparativo_multiples(
            datos,
            titulo="Comparación de Sistemas",
            xlabel="Tiempo (horas)",
            ylabel="Eficiencia (%)"
        )
        
        plt.savefig('outputs/comparacion_sistemas.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Histograma estadístico
        datos_estadisticos = np.random.normal(100, 15, 1000)
        fig = vis.grafico_histograma_estadistico(
            datos_estadisticos,
            titulo="Distribución de Eficiencias",
            xlabel="Eficiencia (%)",
            ylabel="Frecuencia"
        )
        
        plt.savefig('outputs/distribucion_eficiencias.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Visualizaciones generadas y guardadas")
        
    except ImportError:
        print("⚠️ Módulo de visualización no disponible")

def crear_directorio_outputs():
    """Crea el directorio de salida si no existe."""
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        print("📁 Directorio 'outputs' creado")

if __name__ == "__main__":
    # Crear directorio de salida
    crear_directorio_outputs()
    
    # Ejecutar ejemplos
    main() 