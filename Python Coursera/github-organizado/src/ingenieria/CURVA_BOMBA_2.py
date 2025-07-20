# -----------------------------------------------------------------------------
# Módulo: CURVA_BOMBA_2.py
# Propósito: Aplicación GUI interactiva para simular y visualizar curvas de bomba centrífuga
# Aplicación: Selección de bombas, ingeniería hidráulica, enseñanza
# Dependencias: tkinter, numpy, matplotlib
# Uso: Ejecutar el script; se abrirá una ventana para entrada de parámetros y visualización
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

class SimuladorBombaGUI:
    """
    Aplicación GUI para simulación de curvas de bomba centrífuga
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Curvas de Bomba Centrífuga")
        self.root.geometry("1200x800")
        
        # Variables de control
        self.velocidad = tk.DoubleVar(value=1750)
        self.diametro_impulsor = tk.DoubleVar(value=12)
        self.potencia_nominal = tk.DoubleVar(value=50)
        self.eficiencia_max = tk.DoubleVar(value=85)
        self.caudal_nominal = tk.DoubleVar(value=100)
        self.altura_nominal = tk.DoubleVar(value=50)
        
        # Configurar interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        """
        Configura la interfaz gráfica
        """
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
        self.crear_controles(control_frame)
        
        # Panel de gráficos (derecha)
        graph_frame = ttk.LabelFrame(main_frame, text="Curvas de la Bomba", padding="10")
        graph_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Calcular Curvas", 
                  command=self.calcular_curvas).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exportar Datos", 
                  command=self.exportar_datos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Punto de Operación", 
                  command=self.analizar_punto_operacion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.limpiar_graficos).pack(side=tk.LEFT, padx=5)
        
        # Generar curvas iniciales
        self.calcular_curvas()
        
    def crear_controles(self, parent):
        """
        Crea los controles de entrada de parámetros
        """
        # Velocidad de rotación
        ttk.Label(parent, text="Velocidad (RPM):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.velocidad, width=15).grid(row=0, column=1, pady=2)
        
        # Diámetro del impulsor
        ttk.Label(parent, text="Diámetro Impulsor (in):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.diametro_impulsor, width=15).grid(row=1, column=1, pady=2)
        
        # Potencia nominal
        ttk.Label(parent, text="Potencia Nominal (HP):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.potencia_nominal, width=15).grid(row=2, column=1, pady=2)
        
        # Eficiencia máxima
        ttk.Label(parent, text="Eficiencia Máxima (%):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.eficiencia_max, width=15).grid(row=3, column=1, pady=2)
        
        # Caudal nominal
        ttk.Label(parent, text="Caudal Nominal (GPM):").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.caudal_nominal, width=15).grid(row=4, column=1, pady=2)
        
        # Altura nominal
        ttk.Label(parent, text="Altura Nominal (ft):").grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Entry(parent, textvariable=self.altura_nominal, width=15).grid(row=5, column=1, pady=2)
        
        # Separador
        ttk.Separator(parent, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Información adicional
        info_frame = ttk.LabelFrame(parent, text="Información", padding="5")
        info_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(info_frame, text="• Las curvas se calculan usando\n  leyes de similitud").pack(anchor=tk.W)
        ttk.Label(info_frame, text="• La eficiencia varía con el caudal").pack(anchor=tk.W)
        ttk.Label(info_frame, text="• Se incluyen curvas de potencia").pack(anchor=tk.W)
        
    def calcular_curvas_bomba(self, caudal_nominal, altura_nominal, potencia_nominal, 
                            eficiencia_max, velocidad, diametro_impulsor):
        """
        Calcula las curvas características de la bomba
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
        # P = (Q * H * ρ * g) / (η * 550) [HP]
        rho = 62.4  # Densidad del agua (lb/ft³)
        g = 32.2    # Aceleración de gravedad (ft/s²)
        
        potencias = (caudales * alturas * rho * g) / (eficiencias * 550 * 100)
        potencias = np.where(eficiencias > 0, potencias, 0)
        
        # Potencia al freno (asumiendo eficiencia mecánica del 95%)
        eficiencia_mecanica = 0.95
        potencias_freno = potencias / eficiencia_mecanica
        
        return caudales, alturas, eficiencias, potencias, potencias_freno
    
    def calcular_curvas(self):
        """
        Calcula y muestra las curvas de la bomba
        """
        try:
            # Obtener parámetros
            caudal_nominal = self.caudal_nominal.get()
            altura_nominal = self.altura_nominal.get()
            potencia_nominal = self.potencia_nominal.get()
            eficiencia_max = self.eficiencia_max.get()
            velocidad = self.velocidad.get()
            diametro_impulsor = self.diametro_impulsor.get()
            
            # Calcular curvas
            caudales, alturas, eficiencias, potencias, potencias_freno = \
                self.calcular_curvas_bomba(caudal_nominal, altura_nominal, potencia_nominal,
                                         eficiencia_max, velocidad, diametro_impulsor)
            
            # Limpiar figura
            self.fig.clear()
            
            # Crear subplots
            gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
            
            # 1. Curva de altura
            ax1 = self.fig.add_subplot(gs[0, 0])
            ax1.plot(caudales, alturas, 'b-', linewidth=2, label='Altura')
            ax1.set_xlabel('Caudal (GPM)')
            ax1.set_ylabel('Altura (ft)')
            ax1.set_title('Curva de Altura')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # 2. Curva de eficiencia
            ax2 = self.fig.add_subplot(gs[0, 1])
            ax2.plot(caudales, eficiencias, 'g-', linewidth=2, label='Eficiencia')
            ax2.set_xlabel('Caudal (GPM)')
            ax2.set_ylabel('Eficiencia (%)')
            ax2.set_title('Curva de Eficiencia')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            # 3. Curva de potencia
            ax3 = self.fig.add_subplot(gs[1, 0])
            ax3.plot(caudales, potencias, 'r-', linewidth=2, label='Potencia Hidráulica')
            ax3.plot(caudales, potencias_freno, 'r--', linewidth=2, label='Potencia al Freno')
            ax3.axhline(y=potencia_nominal, color='k', linestyle=':', alpha=0.7, label='Potencia Nominal')
            ax3.set_xlabel('Caudal (GPM)')
            ax3.set_ylabel('Potencia (HP)')
            ax3.set_title('Curva de Potencia')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
            
            # 4. Curvas combinadas
            ax4 = self.fig.add_subplot(gs[1, 1])
            ax4_twin = ax4.twinx()
            
            # Altura en eje izquierdo
            line1 = ax4.plot(caudales, alturas, 'b-', linewidth=2, label='Altura')
            ax4.set_xlabel('Caudal (GPM)')
            ax4.set_ylabel('Altura (ft)', color='b')
            ax4.tick_params(axis='y', labelcolor='b')
            
            # Eficiencia en eje derecho
            line2 = ax4_twin.plot(caudales, eficiencias, 'g-', linewidth=2, label='Eficiencia')
            ax4_twin.set_ylabel('Eficiencia (%)', color='g')
            ax4_twin.tick_params(axis='y', labelcolor='g')
            
            ax4.set_title('Curvas Combinadas')
            ax4.grid(True, alpha=0.3)
            
            # Leyenda combinada
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax4.legend(lines, labels, loc='upper right')
            
            # Actualizar canvas
            self.canvas.draw()
            
            # Guardar datos para exportación
            self.datos_curvas = {
                'caudal': caudales,
                'altura': alturas,
                'eficiencia': eficiencias,
                'potencia_hidraulica': potencias,
                'potencia_freno': potencias_freno
            }
            
            messagebox.showinfo("Éxito", "Curvas calculadas correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular curvas: {str(e)}")
    
    def analizar_punto_operacion(self):
        """
        Analiza el punto de operación de la bomba
        """
        if not hasattr(self, 'datos_curvas'):
            messagebox.showwarning("Advertencia", "Primero calcule las curvas de la bomba")
            return
        
        # Crear ventana de análisis
        analisis_window = tk.Toplevel(self.root)
        analisis_window.title("Análisis de Punto de Operación")
        analisis_window.geometry("600x400")
        
        # Frame principal
        main_frame = ttk.Frame(analisis_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles para curva del sistema
        ttk.Label(main_frame, text="CURVA DEL SISTEMA", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Parámetros del sistema
        param_frame = ttk.Frame(main_frame)
        param_frame.pack(fill=tk.X, pady=10)
        
        altura_estatica = tk.DoubleVar(value=20)
        factor_friccion = tk.DoubleVar(value=0.02)
        
        ttk.Label(param_frame, text="Altura Estática (ft):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(param_frame, textvariable=altura_estatica, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="Factor de Fricción:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(param_frame, textvariable=factor_friccion, width=15).grid(row=1, column=1, padx=5)
        
        def calcular_punto_operacion():
            try:
                # Obtener parámetros
                h_estatica = altura_estatica.get()
                f = factor_friccion.get()
                
                # Calcular curva del sistema
                caudales = self.datos_curvas['caudal']
                alturas_sistema = h_estatica + f * (caudales / 100) ** 2
                
                # Encontrar punto de intersección
                alturas_bomba = self.datos_curvas['altura']
                diferencia = np.abs(alturas_bomba - alturas_sistema)
                idx_intersection = np.argmin(diferencia)
                
                caudal_op = caudales[idx_intersection]
                altura_op = alturas_bomba[idx_intersection]
                eficiencia_op = self.datos_curvas['eficiencia'][idx_intersection]
                potencia_op = self.datos_curvas['potencia_freno'][idx_intersection]
                
                # Mostrar resultados
                resultado_text = f"""
PUNTO DE OPERACIÓN:
Caudal: {caudal_op:.1f} GPM
Altura: {altura_op:.1f} ft
Eficiencia: {eficiencia_op:.1f}%
Potencia: {potencia_op:.1f} HP
                """
                
                # Crear gráfico
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(caudales, alturas_bomba, 'b-', linewidth=2, label='Curva de la Bomba')
                ax.plot(caudales, alturas_sistema, 'r-', linewidth=2, label='Curva del Sistema')
                ax.plot(caudal_op, altura_op, 'ko', markersize=8, label='Punto de Operación')
                ax.set_xlabel('Caudal (GPM)')
                ax.set_ylabel('Altura (ft)')
                ax.set_title('Punto de Operación')
                ax.grid(True, alpha=0.3)
                ax.legend()
                plt.tight_layout()
                plt.show()
                
                # Mostrar resultados en ventana
                resultado_label = ttk.Label(main_frame, text=resultado_text, 
                                          font=('Courier', 10), justify=tk.LEFT)
                resultado_label.pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("Error", f"Error en análisis: {str(e)}")
        
        ttk.Button(main_frame, text="Calcular Punto de Operación", 
                  command=calcular_punto_operacion).pack(pady=10)
    
    def exportar_datos(self):
        """
        Exporta los datos de las curvas a un archivo CSV
        """
        if not hasattr(self, 'datos_curvas'):
            messagebox.showwarning("Advertencia", "Primero calcule las curvas de la bomba")
            return
        
        try:
            # Crear DataFrame
            df = pd.DataFrame(self.datos_curvas)
            
            # Agregar información de la bomba
            df['velocidad_rpm'] = self.velocidad.get()
            df['diametro_impulsor_in'] = self.diametro_impulsor.get()
            df['potencia_nominal_hp'] = self.potencia_nominal.get()
            
            # Guardar archivo
            filename = f"curvas_bomba_{int(self.velocidad.get())}rpm.csv"
            df.to_csv(filename, index=False)
            
            messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def limpiar_graficos(self):
        """
        Limpia los gráficos
        """
        self.fig.clear()
        self.canvas.draw()
        messagebox.showinfo("Info", "Gráficos limpiados")

def main():
    """
    Función principal para ejecutar la aplicación
    """
    root = tk.Tk()
    app = SimuladorBombaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
