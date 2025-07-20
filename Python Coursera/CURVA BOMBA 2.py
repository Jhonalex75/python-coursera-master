# -----------------------------------------------------------------------------
# Simulador avanzado de Curvas de Bomba Centrífuga con identificación de BEP
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Aplicación GUI interactiva para simular y visualizar curvas de bomba
# (carga, eficiencia, caudal) para bombas centrífugas, resaltando el BEP.
# Aplicación: Selección de bombas, ingeniería hidráulica, docencia.
#
# Dependencias: tkinter, numpy, matplotlib
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale los paquetes tkinter, numpy y matplotlib si no los tiene.
#      Ejemplo: pip install numpy matplotlib
#   3. Se abrirá una ventana para ingresar parámetros y visualizar las curvas.
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PumpCurveApp:
    def __init__(self, master):
        self.master = master
        master.title("Simulador de Curvas de Bomba")
        master.geometry("950x750") # Ajustar tamaño para mejor visualización

        # Datos base de la bomba de referencia (6 pulgadas, 1750 rpm de la imagen)
        self.Q_base_data = np.array([0, 500, 800, 1000, 1300, 1600])  # gpm
        self.H_base_data = np.array([124, 119, 112, 104, 90, 66])    # ft
        self.Eff_base_data = np.array([0, 54, 64, 68, 70, 67])       # %
        
        self.D_base_default = 6.0  # pulgadas
        self.N_base_default = 1750.0 # rpm

        # --- Sección de Parámetros ---
        param_frame = ttk.LabelFrame(master, text="Parámetros de las Bombas")
        param_frame.pack(padx=10, pady=10, fill="x")

        # Parámetros de la Bomba de Referencia
        ref_pump_frame = ttk.Frame(param_frame)
        ref_pump_frame.pack(side=tk.LEFT, padx=20, pady=10, anchor="n")

        ttk.Label(ref_pump_frame, text="Bomba de Referencia:", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(ref_pump_frame, text="Diámetro (D1, pulgadas):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.d1_entry = ttk.Entry(ref_pump_frame, width=10)
        self.d1_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.d1_entry.insert(0, str(self.D_base_default))
        self.d1_entry.config(state='readonly') # Generalmente fijo, basado en datos conocidos

        ttk.Label(ref_pump_frame, text="Velocidad (N1, RPM):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.n1_entry = ttk.Entry(ref_pump_frame, width=10)
        self.n1_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.n1_entry.insert(0, str(self.N_base_default))
        self.n1_entry.config(state='readonly') # Generalmente fijo

        # Parámetros de la Nueva Bomba
        new_pump_frame = ttk.Frame(param_frame)
        new_pump_frame.pack(side=tk.LEFT, padx=20, pady=10, anchor="n")

        ttk.Label(new_pump_frame, text="Nueva Bomba:", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(new_pump_frame, text="Diámetro (D2, pulgadas):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.d2_entry = ttk.Entry(new_pump_frame, width=10)
        self.d2_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.d2_entry.insert(0, "8.0") # Valor de ejemplo de la imagen

        ttk.Label(new_pump_frame, text="Velocidad (N2, RPM):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.n2_entry = ttk.Entry(new_pump_frame, width=10)
        self.n2_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        self.n2_entry.insert(0, "1450.0") # Valor de ejemplo de la imagen

        # Botón de cálculo
        self.calculate_button = ttk.Button(param_frame, text="Calcular y Graficar Curvas", command=self.update_plots)
        self.calculate_button.pack(side=tk.LEFT, padx=20, pady=20, ipady=10)
        
        # --- Sección de Gráficas ---
        plot_frame = ttk.LabelFrame(master, text="Curvas Características de la Bomba")
        plot_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 7)) # Ajustar figsize para más espacio
        self.fig.tight_layout(pad=4.0) # Ajustar espaciado

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        self.plot_initial_reference_curve()

    def find_bep(self, q_data, h_data, eff_data):
        """Encuentra el Caudal, Cabeza y Eficiencia en el Punto de Máxima Eficiencia (BEP).
        Devuelve (Q, H, Eff) del BEP. Si los datos están vacíos, devuelve None."""
        if len(eff_data) == 0: # Manejar caso de datos vacíos
            return None, None, None
        max_eff_idx = np.argmax(eff_data)
        q_bep = q_data[max_eff_idx]
        h_bep = h_data[max_eff_idx]
        eff_bep = eff_data[max_eff_idx]
        return q_bep, h_bep, eff_bep

    def plot_initial_reference_curve(self):
        """ Grafica solo la curva de referencia inicial e identifica su BEP. """
        self.ax1.clear()
        self.ax2.clear()

        # Curva H-Q de referencia
        self.ax1.plot(self.Q_base_data, self.H_base_data, 'bo-', label=f'Referencia: D1={self.D_base_default}", N1={self.N_base_default} RPM (H-Q)')
        
        # BEP para bomba de referencia
        q_bep_base, h_bep_base, eff_bep_base = self.find_bep(self.Q_base_data, self.H_base_data, self.Eff_base_data)
        if q_bep_base is not None:
            # Marcar y anotar el BEP en la curva H-Q
            self.ax1.plot(q_bep_base, h_bep_base, 'k*', markersize=10, label=f'BEP Ref: Q={q_bep_base:.1f}, H={h_bep_base:.1f}')
            self.ax1.annotate(f'BEP\nQ={q_bep_base:.1f} gpm\nH={h_bep_base:.1f} ft', 
                              xy=(q_bep_base, h_bep_base), xytext=(q_bep_base + 50, h_bep_base + 5),
                              arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                              bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=0.5, alpha=0.8))

        self.ax1.set_xlabel("Caudal (Q, gpm)")
        self.ax1.set_ylabel("Altura (H, ft)")
        self.ax1.set_title("Curva Carga vs. Caudal (H-Q)")
        self.ax1.legend(loc='upper right')
        self.ax1.grid(True)

        # Curva Eff-Q de referencia
        self.ax2.plot(self.Q_base_data, self.Eff_base_data, 'go-', label=f'Referencia: D1={self.D_base_default}", N1={self.N_base_default} RPM (Eff-Q)')
        if q_bep_base is not None:
            # Marcar y anotar el BEP en la curva Eff-Q
            self.ax2.plot(q_bep_base, eff_bep_base, 'k*', markersize=10, label=f'BEP Ref: Q={q_bep_base:.1f}, Eff={eff_bep_base:.1f}%')
            self.ax2.annotate(f'BEP\nQ={q_bep_base:.1f} gpm\nEff={eff_bep_base:.1f}%',
                              xy=(q_bep_base, eff_bep_base), xytext=(q_bep_base + 50, eff_bep_base - 10),
                              arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                              bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=0.5, alpha=0.8))

        self.ax2.set_xlabel("Caudal (Q, gpm)")
        self.ax2.set_ylabel("Eficiencia (Eff, %)")
        self.ax2.set_title("Curva Eficiencia vs. Caudal (Eff-Q)")
        self.ax2.legend(loc='lower right')
        self.ax2.grid(True)
        
        self.canvas.draw()

    def update_plots(self):
        """ Calcula las curvas para la nueva bomba, identifica BEPs y actualiza las gráficas. """
        try:
            d1 = float(self.d1_entry.get())
            n1 = float(self.n1_entry.get())
            d2 = float(self.d2_entry.get())
            n2 = float(self.n2_entry.get())

            if d1 <= 0 or n1 <= 0 or d2 <= 0 or n2 <= 0:
                messagebox.showerror("Error de Entrada", "Los diámetros y velocidades deben ser números positivos.")
                return

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos para diámetros y velocidades.")
            return

        # --- Leyes de afinidad para bombas centrífugas ---
        # Q2 = Q1 * (D2/D1)^3 * (N2/N1)
        # H2 = H1 * (D2/D1)^2 * (N2/N1)^2
        # Eff2 se asume igual en puntos correspondientes (misma forma de curva de eficiencia)
        q_new = self.Q_base_data * (d2 / d1)**3 * (n2 / n1)
        h_new = self.H_base_data * (d2 / d1)**2 * (n2 / n1)**2
        eff_new = self.Eff_base_data # La eficiencia en los puntos correspondientes es la misma

        self.ax1.clear()
        self.ax2.clear()

        # BEP para bomba de referencia
        q_bep_base, h_bep_base, eff_bep_base = self.find_bep(self.Q_base_data, self.H_base_data, self.Eff_base_data)
        # BEP para nueva bomba
        q_bep_new, h_bep_new, eff_bep_new = self.find_bep(q_new, h_new, eff_new)

        # Graficar Curva H-Q
        self.ax1.plot(self.Q_base_data, self.H_base_data, 'bo-', label=f'Ref: D1={d1}", N1={n1} RPM')
        self.ax1.plot(q_new, h_new, 'ro-', label=f'Nueva: D2={d2}", N2={n2} RPM')

        if q_bep_base is not None:
            # Marcar y anotar el BEP de referencia
            self.ax1.plot(q_bep_base, h_bep_base, 'k*', markersize=10, label=f'BEP Ref: Q={q_bep_base:.1f}, H={h_bep_base:.1f}')
            self.ax1.annotate(f'BEP Ref.\nQ={q_bep_base:.1f}\nH={h_bep_base:.1f}', 
                              xy=(q_bep_base, h_bep_base), xytext=(q_bep_base + 50, h_bep_base + 5),
                              arrowprops=dict(facecolor='blue', shrink=0.05, width=1, headwidth=5,connectionstyle="arc3,rad=.2"),
                              bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", ec="blue", lw=0.5, alpha=0.8))
        if q_bep_new is not None:
            # Marcar y anotar el BEP de la nueva bomba
            self.ax1.plot(q_bep_new, h_bep_new, 'ms', markersize=8, label=f'BEP Nueva: Q={q_bep_new:.1f}, H={h_bep_new:.1f}')
            self.ax1.annotate(f'BEP Nueva\nQ={q_bep_new:.1f}\nH={h_bep_new:.1f}', 
                              xy=(q_bep_new, h_bep_new), xytext=(q_bep_new - 150, h_bep_new - 15),
                              arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=5,connectionstyle="arc3,rad=-.2"),
                              bbox=dict(boxstyle="round,pad=0.3", fc="pink", ec="red", lw=0.5, alpha=0.8))

        self.ax1.set_xlabel("Caudal (Q, gpm)")
        self.ax1.set_ylabel("Altura (H, ft)")
        self.ax1.set_title("Curva Carga vs. Caudal (H-Q)")
        self.ax1.legend(loc='best')
        self.ax1.grid(True)

        # Graficar Curva Eff-Q
        self.ax2.plot(self.Q_base_data, self.Eff_base_data, 'go-', label=f'Ref: D1={d1}", N1={n1} RPM')
        self.ax2.plot(q_new, eff_new, 'co-', label=f'Nueva: D2={d2}", N2={n2} RPM')

        if q_bep_base is not None:
            # Marcar y anotar el BEP de referencia
            self.ax2.plot(q_bep_base, eff_bep_base, 'k*', markersize=10, label=f'BEP Ref: Q={q_bep_base:.1f}, Eff={eff_bep_base:.1f}%')
            self.ax2.annotate(f'BEP Ref.\nQ={q_bep_base:.1f}\nEff={eff_bep_base:.1f}%',
                              xy=(q_bep_base, eff_bep_base), xytext=(q_bep_base + 50, eff_bep_base - 10),
                              arrowprops=dict(facecolor='green', shrink=0.05, width=1, headwidth=5,connectionstyle="arc3,rad=.2"),
                              bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen", ec="green", lw=0.5, alpha=0.8))
        if q_bep_new is not None:
            # Marcar y anotar el BEP de la nueva bomba
            self.ax2.plot(q_bep_new, eff_bep_new, 'ms', markersize=8, label=f'BEP Nueva: Q={q_bep_new:.1f}, Eff={eff_bep_new:.1f}%')
            self.ax2.annotate(f'BEP Nueva\nQ={q_bep_new:.1f}\nEff={eff_bep_new:.1f}%',
                              xy=(q_bep_new, eff_bep_new), xytext=(q_bep_new - 150, eff_bep_new - 10),
                              arrowprops=dict(facecolor='magenta', shrink=0.05, width=1, headwidth=5,connectionstyle="arc3,rad=-.2"),
                              bbox=dict(boxstyle="round,pad=0.3", fc="pink", ec="magenta", lw=0.5, alpha=0.8))

        self.ax2.set_xlabel("Caudal (Q, gpm)")
        self.ax2.set_ylabel("Eficiencia (Eff, %)")
        self.ax2.set_title("Curva Eficiencia vs. Caudal (Eff-Q)")
        self.ax2.legend(loc='best')
        self.ax2.grid(True)

        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = PumpCurveApp(root)
    root.mainloop()