# -----------------------------------------------------------------------------
# Purpose: Interactive GUI application to simulate and visualize pump curves (head, efficiency, flow) for centrifugal pumps.
# Application: Pump selection, hydraulic engineering, teaching.
# Dependencies: tkinter, numpy, matplotlib
# Usage: Run the script; a window will open for parameter input and visualization.
# -----------------------------------------------------------------------------
# Script de ingeniería de fluidos y bombas
# Especialidad: Ingeniería Mecánica

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches

class SimuladorCurvaBomba:
    """
    Simulador interactivo de curvas de bomba centrífuga
    Permite visualizar curvas de altura, eficiencia y potencia
    """
    
    def __init__(self):
        """Inicializa la aplicación GUI."""
        self.root = tk.Tk()
        self.root.title("Simulador de Curvas de Bomba Centrífuga")
        self.root.geometry("1200x800")
        
        # Variables de control
        self.altura_nominal = tk.DoubleVar(value=50.0)  # metros
        self.caudal_nominal = tk.DoubleVar(value=100.0)  # L/min
        self.eficiencia_max = tk.DoubleVar(value=85.0)  # %
        self.potencia_nominal = tk.DoubleVar(value=15.0)  # kW
        self.densidad_fluido = tk.DoubleVar(value=1000.0)  # kg/m³
        
        self.crear_interfaz()
        self.actualizar_curvas()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel de controles (izquierda)
        control_frame = ttk.LabelFrame(main_frame, text="Parámetros de la Bomba", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Controles de entrada
        ttk.Label(control_frame, text="Altura Nominal (m):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.altura_nominal, width=10).grid(row=0, column=1, pady=2)
        
        ttk.Label(control_frame, text="Caudal Nominal (L/min):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.caudal_nominal, width=10).grid(row=1, column=1, pady=2)
        
        ttk.Label(control_frame, text="Eficiencia Máxima (%):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.eficiencia_max, width=10).grid(row=2, column=1, pady=2)
        
        ttk.Label(control_frame, text="Potencia Nominal (kW):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.potencia_nominal, width=10).grid(row=3, column=1, pady=2)
        
        ttk.Label(control_frame, text="Densidad del Fluido (kg/m³):").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.densidad_fluido, width=10).grid(row=4, column=1, pady=2)
        
        # Botones
        ttk.Button(control_frame, text="Actualizar Curvas", 
                  command=self.actualizar_curvas).grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(control_frame, text="Punto de Operación", 
                  command=self.mostrar_punto_operacion).grid(row=6, column=0, columnspan=2, pady=5)
        
        ttk.Button(control_frame, text="Análisis de Eficiencia", 
                  command=self.analisis_eficiencia).grid(row=7, column=0, columnspan=2, pady=5)
        
        # Panel de gráficos (derecha)
        graph_frame = ttk.LabelFrame(main_frame, text="Curvas de la Bomba", padding="10")
        graph_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Información adicional
        info_frame = ttk.LabelFrame(main_frame, text="Información Técnica", padding="5")
        info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=4, width=80)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar eventos
        for var in [self.altura_nominal, self.caudal_nominal, self.eficiencia_max, 
                   self.potencia_nominal, self.densidad_fluido]:
            var.trace('w', lambda *args: self.actualizar_curvas())
    
    def calcular_curvas(self):
        """Calcula las curvas de la bomba basadas en los parámetros."""
        # Rango de caudales (0 a 150% del caudal nominal)
        caudal_max = self.caudal_nominal.get() * 1.5
        Q = np.linspace(0, caudal_max, 100)  # L/min
        
        # Curva de altura (H-Q)
        Q_nom = self.caudal_nominal.get()
        H_nom = self.altura_nominal.get()
        
        # Ecuación parabólica: H = H_nom * (1 - (Q/Q_nom)^2)
        H = H_nom * (1 - (Q/Q_nom)**2)
        H[Q > Q_nom] = 0  # Altura cero para caudales mayores al nominal
        
        # Curva de eficiencia (η-Q)
        eta_max = self.eficiencia_max.get() / 100.0
        
        # Eficiencia parabólica centrada en el caudal nominal
        eta = eta_max * (1 - ((Q - Q_nom) / Q_nom)**2)
        eta[eta < 0] = 0  # Eficiencia no puede ser negativa
        
        # Curva de potencia (P-Q)
        g = 9.81  # m/s²
        Q_m3s = Q / 60000  # Convertir L/min a m³/s
        H_m = H  # Ya está en metros
        
        # Potencia hidráulica: P_h = ρ * g * Q * H
        P_hidraulica = self.densidad_fluido.get() * g * Q_m3s * H_m / 1000  # kW
        
        # Potencia al eje: P_eje = P_hidraulica / η
        P_eje = np.where(eta > 0.01, P_hidraulica / eta, 0)
        
        return Q, H, eta * 100, P_eje, P_hidraulica
    
    def actualizar_curvas(self):
        """Actualiza las curvas en el gráfico."""
        try:
            Q, H, eta, P_eje, P_hidraulica = self.calcular_curvas()
            
            # Limpiar figura
            self.fig.clear()
            
            # Crear subplots
            gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
            
            # Curva de altura
            ax1 = self.fig.add_subplot(gs[0, 0])
            ax1.plot(Q, H, 'b-', linewidth=2, label='Altura (H)')
            ax1.set_xlabel('Caudal (L/min)')
            ax1.set_ylabel('Altura (m)')
            ax1.set_title('Curva Altura-Caudal')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Curva de eficiencia
            ax2 = self.fig.add_subplot(gs[0, 1])
            ax2.plot(Q, eta, 'g-', linewidth=2, label='Eficiencia (η)')
            ax2.set_xlabel('Caudal (L/min)')
            ax2.set_ylabel('Eficiencia (%)')
            ax2.set_title('Curva Eficiencia-Caudal')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            # Curva de potencia
            ax3 = self.fig.add_subplot(gs[1, 0])
            ax3.plot(Q, P_eje, 'r-', linewidth=2, label='Potencia al Eje')
            ax3.plot(Q, P_hidraulica, 'orange', linewidth=2, label='Potencia Hidráulica')
            ax3.set_xlabel('Caudal (L/min)')
            ax3.set_ylabel('Potencia (kW)')
            ax3.set_title('Curva Potencia-Caudal')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
            
            # Curva combinada
            ax4 = self.fig.add_subplot(gs[1, 1])
            ax4_twin = ax4.twinx()
            
            line1 = ax4.plot(Q, H, 'b-', linewidth=2, label='Altura')
            line2 = ax4_twin.plot(Q, eta, 'g-', linewidth=2, label='Eficiencia')
            
            ax4.set_xlabel('Caudal (L/min)')
            ax4.set_ylabel('Altura (m)', color='b')
            ax4_twin.set_ylabel('Eficiencia (%)', color='g')
            ax4.set_title('Curvas Combinadas')
            ax4.grid(True, alpha=0.3)
            
            # Leyendas combinadas
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax4.legend(lines, labels, loc='upper right')
            
            self.canvas.draw()
            
            # Actualizar información
            self.actualizar_informacion(Q, H, eta, P_eje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular las curvas: {str(e)}")
    
    def actualizar_informacion(self, Q, H, eta, P_eje):
        """Actualiza la información técnica mostrada."""
        Q_nom = self.caudal_nominal.get()
        H_nom = self.altura_nominal.get()
        
        # Encontrar valores en el punto nominal
        idx_nom = np.argmin(np.abs(Q - Q_nom))
        
        info = f"""
        PUNTO NOMINAL DE OPERACIÓN:
        • Caudal: {Q_nom:.1f} L/min
        • Altura: {H_nom:.1f} m
        • Eficiencia: {eta[idx_nom]:.1f}%
        • Potencia al eje: {P_eje[idx_nom]:.2f} kW
        
        CARACTERÍSTICAS DE LA BOMBA:
        • Altura máxima (Q=0): {H[0]:.1f} m
        • Eficiencia máxima: {np.max(eta):.1f}% a {Q[np.argmax(eta)]:.1f} L/min
        • Potencia máxima: {np.max(P_eje):.2f} kW
        • Rango de operación: 0 - {Q[-1]:.1f} L/min
        """
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def mostrar_punto_operacion(self):
        """Muestra el punto de operación en las curvas."""
        try:
            # Crear ventana de diálogo para punto de operación
            dialog = tk.Toplevel(self.root)
            dialog.title("Punto de Operación")
            dialog.geometry("400x200")
            
            ttk.Label(dialog, text="Ingrese el caudal de operación (L/min):").pack(pady=10)
            
            caudal_op = tk.DoubleVar(value=self.caudal_nominal.get())
            entry = ttk.Entry(dialog, textvariable=caudal_op, width=10)
            entry.pack(pady=5)
            
            def calcular_punto():
                Q_op = caudal_op.get()
                Q, H, eta, P_eje, P_hidraulica = self.calcular_curvas()
                
                # Encontrar valores en el punto de operación
                idx_op = np.argmin(np.abs(Q - Q_op))
                
                if Q_op <= Q[-1]:
                    H_op = H[idx_op]
                    eta_op = eta[idx_op]
                    P_op = P_eje[idx_op]
                    
                    resultado = f"""
                    PUNTO DE OPERACIÓN:
                    • Caudal: {Q_op:.1f} L/min
                    • Altura: {H_op:.1f} m
                    • Eficiencia: {eta_op:.1f}%
                    • Potencia requerida: {P_op:.2f} kW
                    """
                else:
                    resultado = "El caudal está fuera del rango de operación de la bomba."
                
                messagebox.showinfo("Resultado", resultado)
                dialog.destroy()
            
            ttk.Button(dialog, text="Calcular", command=calcular_punto).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def analisis_eficiencia(self):
        """Realiza análisis de eficiencia de la bomba."""
        try:
            Q, H, eta, P_eje, P_hidraulica = self.calcular_curvas()
            
            # Encontrar rango de eficiencia óptima (>80% de la máxima)
            eta_max = np.max(eta)
            eta_umbral = eta_max * 0.8
            
            # Encontrar caudales donde la eficiencia es mayor al umbral
            idx_optimo = eta >= eta_umbral
            Q_optimo = Q[idx_optimo]
            
            if len(Q_optimo) > 0:
                Q_min_optimo = np.min(Q_optimo)
                Q_max_optimo = np.max(Q_optimo)
                
                analisis = f"""
                ANÁLISIS DE EFICIENCIA:
                
                • Eficiencia máxima: {eta_max:.1f}%
                • Rango de eficiencia óptima (>80% del máximo):
                  - Caudal mínimo: {Q_min_optimo:.1f} L/min
                  - Caudal máximo: {Q_max_optimo:.1f} L/min
                  - Rango recomendado: {Q_max_optimo - Q_min_optimo:.1f} L/min
                
                • Recomendaciones:
                  - Operar la bomba entre {Q_min_optimo:.1f} y {Q_max_optimo:.1f} L/min
                  - Evitar operación a caudales muy bajos (<{Q_min_optimo:.1f} L/min)
                  - La eficiencia cae significativamente fuera del rango óptimo
                """
            else:
                analisis = "No se encontró un rango de eficiencia óptima."
            
            messagebox.showinfo("Análisis de Eficiencia", analisis)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis: {str(e)}")
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()

def main():
    """Función principal para ejecutar el simulador."""
    app = SimuladorCurvaBomba()
    app.ejecutar()

if __name__ == "__main__":
    main()
