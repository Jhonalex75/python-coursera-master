"""
Análisis de Diagramas de Fuerza Cortante y Momento Flector (SFD & BMD)
=====================================================================

Este módulo calcula y visualiza los diagramas de fuerza cortante (SFD) y momento flector (BMD)
para diferentes tipos de vigas y cargas.

Aplicaciones:
- Análisis estructural
- Diseño de vigas
- Educación en ingeniería estructural
- Verificación de cálculos manuales

Autor: Ingeniería Mecánica
Versión: 2.0
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import math


class AnalizadorVigas:
    """
    Clase para análisis de vigas y generación de diagramas SFD/BMD
    """
    
    def __init__(self):
        """Inicializa el analizador de vigas."""
        self.vigas = {}
        self.resultados = {}
        
    def crear_viga_simple(self, longitud: float, carga_uniforme: float = 0) -> str:
        """
        Crea una viga simplemente apoyada con carga uniforme
        
        Args:
            longitud: Longitud de la viga en metros
            carga_uniforme: Carga uniformemente distribuida en kN/m
            
        Returns:
            str: ID de la viga creada
        """
        viga_id = f"VIGA_{len(self.vigas) + 1}"
        
        self.vigas[viga_id] = {
            "tipo": "simplemente_apoyada",
            "longitud": longitud,
            "cargas": {
                "uniforme": carga_uniforme,
                "puntuales": [],
                "momentos": []
            },
            "apoyos": [
                {"tipo": "articulado", "posicion": 0},
                {"tipo": "articulado", "posicion": longitud}
            ]
        }
        
        return viga_id
    
    def agregar_carga_puntual(self, viga_id: str, posicion: float, magnitud: float) -> bool:
        """
        Agrega una carga puntual a la viga
        
        Args:
            viga_id: ID de la viga
            posicion: Posición de la carga desde el extremo izquierdo (m)
            magnitud: Magnitud de la carga (kN, positiva hacia abajo)
            
        Returns:
            bool: True si se agregó correctamente
        """
        if viga_id not in self.vigas:
            return False
        
        self.vigas[viga_id]["cargas"]["puntuales"].append({
            "posicion": posicion,
            "magnitud": magnitud
        })
        
        return True
    
    def agregar_momento(self, viga_id: str, posicion: float, magnitud: float) -> bool:
        """
        Agrega un momento concentrado a la viga
        
        Args:
            viga_id: ID de la viga
            posicion: Posición del momento desde el extremo izquierdo (m)
            magnitud: Magnitud del momento (kN·m, positiva en sentido horario)
            
        Returns:
            bool: True si se agregó correctamente
        """
        if viga_id not in self.vigas:
            return False
        
        self.vigas[viga_id]["cargas"]["momentos"].append({
            "posicion": posicion,
            "magnitud": magnitud
        })
        
        return True
    
    def calcular_reacciones(self, viga_id: str) -> Dict:
        """
        Calcula las reacciones en los apoyos
        
        Args:
            viga_id: ID de la viga
            
        Returns:
            Dict: Reacciones calculadas
        """
        if viga_id not in self.vigas:
            return {"error": "Viga no encontrada"}
        
        viga = self.vigas[viga_id]
        L = viga["longitud"]
        
        # Carga uniforme
        w = viga["cargas"]["uniforme"]
        F_uniforme = w * L
        
        # Cargas puntuales
        F_puntuales = sum(carga["magnitud"] for carga in viga["cargas"]["puntuales"])
        momento_puntuales = sum(carga["magnitud"] * carga["posicion"] 
                               for carga in viga["cargas"]["puntuales"])
        
        # Momentos concentrados
        momento_concentrado = sum(mom["magnitud"] for mom in viga["cargas"]["momentos"])
        
        # Cálculo de reacciones (suma de momentos en A = 0)
        momento_total = F_uniforme * L/2 + momento_puntuales + momento_concentrado
        R_B = momento_total / L
        
        # Suma de fuerzas verticales = 0
        R_A = F_uniforme + F_puntuales - R_B
        
        return {
            "R_A": R_A,
            "R_B": R_B,
            "fuerza_total": F_uniforme + F_puntuales
        }
    
    def calcular_sfd_bmd(self, viga_id: str, num_puntos: int = 100) -> Dict:
        """
        Calcula los diagramas de fuerza cortante y momento flector
        
        Args:
            viga_id: ID de la viga
            num_puntos: Número de puntos para el cálculo
            
        Returns:
            Dict: Resultados del análisis
        """
        if viga_id not in self.vigas:
            return {"error": "Viga no encontrada"}
        
        viga = self.vigas[viga_id]
        L = viga["longitud"]
        reacciones = self.calcular_reacciones(viga_id)
        
        if "error" in reacciones:
            return reacciones
        
        # Crear array de posiciones
        x = np.linspace(0, L, num_puntos)
        V = np.zeros(num_puntos)  # Fuerza cortante
        M = np.zeros(num_puntos)  # Momento flector
        
        # Aplicar reacciones
        V += reacciones["R_A"]
        M += reacciones["R_A"] * x
        
        # Aplicar carga uniforme
        w = viga["cargas"]["uniforme"]
        V -= w * x
        M -= w * x**2 / 2
        
        # Aplicar cargas puntuales
        for carga in viga["cargas"]["puntuales"]:
            pos = carga["posicion"]
            mag = carga["magnitud"]
            
            # Fuerza cortante
            V[x >= pos] -= mag
            
            # Momento flector
            M[x >= pos] -= mag * (x[x >= pos] - pos)
        
        # Aplicar momentos concentrados
        for momento in viga["cargas"]["momentos"]:
            pos = momento["posicion"]
            mag = momento["magnitud"]
            
            # Momento flector (los momentos no afectan la fuerza cortante)
            M[x >= pos] += mag
        
        return {
            "posiciones": x,
            "fuerza_cortante": V,
            "momento_flector": M,
            "reacciones": reacciones,
            "longitud": L
        }
    
    def graficar_diagramas(self, viga_id: str, mostrar_valores: bool = True) -> None:
        """
        Genera y muestra los diagramas SFD y BMD
        
        Args:
            viga_id: ID de la viga
            mostrar_valores: Si mostrar valores máximos y mínimos
        """
        resultados = self.calcular_sfd_bmd(viga_id)
        
        if "error" in resultados:
            print(f"Error: {resultados['error']}")
            return
        
        x = resultados["posiciones"]
        V = resultados["fuerza_cortante"]
        M = resultados["momento_flector"]
        
        # Crear figura con subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Diagrama de Fuerza Cortante (SFD)
        ax1.plot(x, V, 'b-', linewidth=2, label='Fuerza Cortante')
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax1.fill_between(x, V, 0, alpha=0.3, color='blue')
        ax1.set_title('Diagrama de Fuerza Cortante (SFD)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Fuerza Cortante (kN)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Mostrar valores máximos y mínimos
        if mostrar_valores:
            V_max = np.max(V)
            V_min = np.min(V)
            ax1.annotate(f'V_max = {V_max:.2f} kN', 
                        xy=(x[np.argmax(V)], V_max), 
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
            ax1.annotate(f'V_min = {V_min:.2f} kN', 
                        xy=(x[np.argmin(V)], V_min), 
                        xytext=(10, -10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        # Diagrama de Momento Flector (BMD)
        ax2.plot(x, M, 'r-', linewidth=2, label='Momento Flector')
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.fill_between(x, M, 0, alpha=0.3, color='red')
        ax2.set_title('Diagrama de Momento Flector (BMD)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Posición (m)', fontsize=12)
        ax2.set_ylabel('Momento Flector (kN·m)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Mostrar valores máximos y mínimos
        if mostrar_valores:
            M_max = np.max(M)
            M_min = np.min(M)
            ax2.annotate(f'M_max = {M_max:.2f} kN·m', 
                        xy=(x[np.argmax(M)], M_max), 
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
            ax2.annotate(f'M_min = {M_min:.2f} kN·m', 
                        xy=(x[np.argmin(M)], M_min), 
                        xytext=(10, -10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        plt.tight_layout()
        plt.show()
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN DEL ANÁLISIS - Viga {viga_id}")
        print("=" * 50)
        print(f"Longitud: {resultados['longitud']:.2f} m")
        print(f"Reacción A: {resultados['reacciones']['R_A']:.2f} kN")
        print(f"Reacción B: {resultados['reacciones']['R_B']:.2f} kN")
        print(f"Fuerza cortante máxima: {np.max(V):.2f} kN")
        print(f"Fuerza cortante mínima: {np.min(V):.2f} kN")
        print(f"Momento flector máximo: {np.max(M):.2f} kN·m")
        print(f"Momento flector mínimo: {np.min(M):.2f} kN·m")
    
    def crear_viga_ejemplo(self) -> str:
        """
        Crea una viga de ejemplo para demostración
        
        Returns:
            str: ID de la viga creada
        """
        # Crear viga de 6 metros con carga uniforme
        viga_id = self.crear_viga_simple(longitud=6.0, carga_uniforme=5.0)
        
        # Agregar cargas puntuales
        self.agregar_carga_puntual(viga_id, posicion=2.0, magnitud=10.0)
        self.agregar_carga_puntual(viga_id, posicion=4.0, magnitud=15.0)
        
        # Agregar momento concentrado
        self.agregar_momento(viga_id, posicion=3.0, magnitud=20.0)
        
        return viga_id


def ejemplo_viga_simple():
    """
    Ejemplo de análisis de viga simplemente apoyada
    """
    print("🏗️ ANÁLISIS DE VIGA SIMPLEMENTE APOYADA")
    print("=" * 50)
    
    # Crear analizador
    analizador = AnalizadorVigas()
    
    # Crear viga de ejemplo
    viga_id = analizador.crear_viga_ejemplo()
    print(f"Viga creada: {viga_id}")
    
    # Mostrar propiedades de la viga
    viga = analizador.vigas[viga_id]
    print(f"\n📋 Propiedades de la viga:")
    print(f"Longitud: {viga['longitud']} m")
    print(f"Carga uniforme: {viga['cargas']['uniforme']} kN/m")
    print(f"Cargas puntuales: {len(viga['cargas']['puntuales'])}")
    print(f"Momentos concentrados: {len(viga['cargas']['momentos'])}")
    
    # Calcular y mostrar reacciones
    reacciones = analizador.calcular_reacciones(viga_id)
    print(f"\n⚖️ Reacciones calculadas:")
    print(f"R_A = {reacciones['R_A']:.2f} kN")
    print(f"R_B = {reacciones['R_B']:.2f} kN")
    
    # Generar diagramas
    print(f"\n📈 Generando diagramas SFD y BMD...")
    analizador.graficar_diagramas(viga_id)


def ejemplo_viga_cantilever():
    """
    Ejemplo de análisis de viga en voladizo
    """
    print("\n🏗️ ANÁLISIS DE VIGA EN VOLADIZO")
    print("=" * 50)
    
    # Crear analizador
    analizador = AnalizadorVigas()
    
    # Crear viga en voladizo (simulada como viga simple con reacciones especiales)
    viga_id = analizador.crear_viga_simple(longitud=4.0, carga_uniforme=3.0)
    
    # Agregar carga puntual en el extremo libre
    analizador.agregar_carga_puntual(viga_id, posicion=4.0, magnitud=8.0)
    
    # Generar diagramas
    analizador.graficar_diagramas(viga_id)


def main():
    """
    Función principal del módulo
    """
    print("🔧 ANÁLISIS DE DIAGRAMAS SFD Y BMD")
    print("=" * 60)
    
    # Ejemplo 1: Viga simplemente apoyada
    ejemplo_viga_simple()
    
    # Ejemplo 2: Viga en voladizo
    ejemplo_viga_cantilever()
    
    print("\n" + "=" * 60)
    print("✅ Análisis completado exitosamente!")
    print("\n📚 Aplicaciones:")
    print("• Diseño estructural de vigas")
    print("• Verificación de cálculos manuales")
    print("• Educación en ingeniería estructural")
    print("• Análisis de elementos estructurales")


if __name__ == "__main__":
    main()
