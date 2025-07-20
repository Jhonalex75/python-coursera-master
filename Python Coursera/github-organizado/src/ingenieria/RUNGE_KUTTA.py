# Script de métodos numéricos
# Especialidad: Ingeniería / Métodos Numéricos
# Implementación del método de Runge-Kutta de 4to orden para resolver EDOs

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

class MetodoRungeKutta:
    """
    Clase para implementar el método de Runge-Kutta de 4to orden
    para resolver ecuaciones diferenciales ordinarias (EDOs)
    """
    
    def __init__(self):
        """Inicializa el método de Runge-Kutta."""
        self.historial_soluciones = []
        self.historial_tiempos = []
    
    def runge_kutta_4(self, f: Callable, y0: float, t0: float, tf: float, h: float) -> tuple:
        """
        Implementa el método de Runge-Kutta de 4to orden.
        
        Args:
            f: Función que define la EDO dy/dt = f(t, y)
            y0: Condición inicial y(t0)
            t0: Tiempo inicial
            tf: Tiempo final
            h: Paso de integración
            
        Returns:
            tuple: (tiempos, soluciones)
        """
        # Inicializar arrays
        n_steps = int((tf - t0) / h) + 1
        t = np.linspace(t0, tf, n_steps)
        y = np.zeros(n_steps)
        y[0] = y0
        
        # Método de Runge-Kutta de 4to orden
        for i in range(n_steps - 1):
            k1 = f(t[i], y[i])
            k2 = f(t[i] + h/2, y[i] + h*k1/2)
            k3 = f(t[i] + h/2, y[i] + h*k2/2)
            k4 = f(t[i] + h, y[i] + h*k3)
            
            y[i+1] = y[i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        
        self.historial_tiempos = t
        self.historial_soluciones = y
        return t, y
    
    def resolver_sistema_edos(self, f_sistema: Callable, y0: np.ndarray, t0: float, 
                            tf: float, h: float) -> tuple:
        """
        Resuelve un sistema de EDOs usando Runge-Kutta de 4to orden.
        
        Args:
            f_sistema: Función que define el sistema de EDOs
            y0: Vector de condiciones iniciales
            t0: Tiempo inicial
            tf: Tiempo final
            h: Paso de integración
            
        Returns:
            tuple: (tiempos, soluciones)
        """
        n_steps = int((tf - t0) / h) + 1
        t = np.linspace(t0, tf, n_steps)
        n_variables = len(y0)
        y = np.zeros((n_steps, n_variables))
        y[0] = y0
        
        for i in range(n_steps - 1):
            k1 = f_sistema(t[i], y[i])
            k2 = f_sistema(t[i] + h/2, y[i] + h*k1/2)
            k3 = f_sistema(t[i] + h/2, y[i] + h*k2/2)
            k4 = f_sistema(t[i] + h, y[i] + h*k3)
            
            y[i+1] = y[i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        
        return t, y
    
    def visualizar_solucion(self, titulo: str = "Solución EDO - Método Runge-Kutta"):
        """
        Visualiza la solución obtenida.
        
        Args:
            titulo: Título del gráfico
        """
        if len(self.historial_tiempos) == 0:
            print("No hay solución para visualizar. Ejecute primero el método.")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.historial_tiempos, self.historial_soluciones, 'b-', linewidth=2, label='Solución RK4')
        plt.xlabel('Tiempo')
        plt.ylabel('y(t)')
        plt.title(titulo)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def comparar_con_analitica(self, solucion_analitica: Callable, titulo: str = "Comparación RK4 vs Analítica"):
        """
        Compara la solución numérica con la solución analítica.
        
        Args:
            solucion_analitica: Función que proporciona la solución analítica
            titulo: Título del gráfico
        """
        if len(self.historial_tiempos) == 0:
            print("No hay solución numérica para comparar.")
            return
        
        y_analitica = solucion_analitica(self.historial_tiempos)
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.historial_tiempos, self.historial_soluciones, 'b-', linewidth=2, label='RK4')
        plt.plot(self.historial_tiempos, y_analitica, 'r--', linewidth=2, label='Analítica')
        plt.xlabel('Tiempo')
        plt.ylabel('y(t)')
        plt.title(titulo)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        # Calcular error
        error = np.abs(self.historial_soluciones - y_analitica)
        error_max = np.max(error)
        error_medio = np.mean(error)
        
        print(f"Error máximo: {error_max:.6f}")
        print(f"Error medio: {error_medio:.6f}")

# Ejemplos de uso
def ejemplo_edo_simple():
    """Ejemplo: Resolver dy/dt = -y con y(0) = 1"""
    print("=== Ejemplo: EDO Simple dy/dt = -y ===")
    
    # Definir la EDO
    def f(t, y):
        return -y
    
    # Solución analítica
    def y_analitica(t):
        return np.exp(-t)
    
    # Configurar parámetros
    y0 = 1.0
    t0 = 0.0
    tf = 5.0
    h = 0.1
    
    # Resolver con RK4
    rk = MetodoRungeKutta()
    t, y = rk.runge_kutta_4(f, y0, t0, tf, h)
    
    # Visualizar resultados
    rk.visualizar_solucion("Decaimiento Exponencial - RK4")
    rk.comparar_con_analitica(y_analitica, "Decaimiento Exponencial - RK4 vs Analítica")
    
    return t, y

def ejemplo_sistema_edos():
    """Ejemplo: Sistema de EDOs - Oscilador armónico"""
    print("\n=== Ejemplo: Sistema de EDOs - Oscilador Armónico ===")
    
    # Sistema: dx/dt = v, dv/dt = -ω²x
    omega = 2.0  # Frecuencia angular
    
    def sistema_oscilador(t, y):
        x, v = y
        return np.array([v, -omega**2 * x])
    
    # Condiciones iniciales: x(0) = 1, v(0) = 0
    y0 = np.array([1.0, 0.0])
    t0 = 0.0
    tf = 10.0
    h = 0.01
    
    # Resolver
    rk = MetodoRungeKutta()
    t, y = rk.resolver_sistema_edos(sistema_oscilador, y0, t0, tf, h)
    
    # Visualizar
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(t, y[:, 0], 'b-', linewidth=2, label='Posición')
    plt.xlabel('Tiempo')
    plt.ylabel('x(t)')
    plt.title('Oscilador Armónico - Posición')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(t, y[:, 1], 'r-', linewidth=2, label='Velocidad')
    plt.xlabel('Tiempo')
    plt.ylabel('v(t)')
    plt.title('Oscilador Armónico - Velocidad')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Diagrama de fase
    plt.figure(figsize=(8, 8))
    plt.plot(y[:, 0], y[:, 1], 'g-', linewidth=2)
    plt.xlabel('Posición x')
    plt.ylabel('Velocidad v')
    plt.title('Diagrama de Fase - Oscilador Armónico')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.show()
    
    return t, y

if __name__ == "__main__":
    # Ejecutar ejemplos
    ejemplo_edo_simple()
    ejemplo_sistema_edos()
