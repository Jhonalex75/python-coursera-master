import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# --- Lógica Principal de la Simulación (Portado de JS) ---

class LeachingSimulator:
    """
    Encapsula toda la lógica para la simulación de lixiviación.
    """
    def __init__(self, params):
        self.params = params

    def get_derivatives(self, state, input_concentrations):
        """
        Calcula las derivadas del sistema de EDOs en un punto (t, state).
        Esta función es la implementación directa del sistema de ecuaciones diferenciales.
        """
        h, r_no3, r_mg, c_no3, c_mg = state
        c_no3_in, c_mg_in = input_concentrations
        p = self.params

        # --- Ecuación 1: Cambio en el Radio de la Partícula (dr/dt) ---
        dr_no3_dt = (-p['species']['NO3']['k'] / p['species']['NO3']['rho']) * \
                    np.power(max(0, p['species']['NO3']['C_s'] - c_no3), p['n_order'])
        dr_mg_dt = (-p['species']['Mg']['k'] / p['species']['Mg']['rho']) * \
                   np.power(max(0, p['species']['Mg']['C_s'] - c_mg), p['n_order'])

        # --- Ecuación 2: Cambio en la Altura del Lecho (dh/dt) ---
        sum_term_h = (p['N_NO3'] * r_no3**2 * dr_no3_dt) + (p['N_Mg'] * r_mg**2 * dr_mg_dt)
        dh_dt = ((4 * np.pi) / (p['A'] * (1 - p['xi']))) * sum_term_h

        # --- Ecuación 3: Cambio en la Concentración (dC/dt) ---
        V = p['xi'] * p['A'] * h  # Volumen actual de la solución en la sección
        if V <= 0:
            return 0, 0, 0, 0, 0

        # Término de reacción para NO3
        reaction_term_no3 = 4 * np.pi * p['N_NO3'] * p['species']['NO3']['k'] * r_no3**2 * \
                            np.power(max(0, p['species']['NO3']['C_s'] - c_no3), p['n_order'])
        dC_no3_dt = (1 / V) * (p['q'] * (c_no3_in - c_no3) + reaction_term_no3 - (p['xi'] * p['A'] * c_no3 * dh_dt))

        # Término de reacción para Mg
        reaction_term_mg = 4 * np.pi * p['N_Mg'] * p['species']['Mg']['k'] * r_mg**2 * \
                           np.power(max(0, p['species']['Mg']['C_s'] - c_mg), p['n_order'])
        dC_mg_dt = (1 / V) * (p['q'] * (c_mg_in - c_mg) + reaction_term_mg - (p['xi'] * p['A'] * c_mg * dh_dt))

        return dh_dt, dr_no3_dt, dr_mg_dt, dC_no3_dt, dC_mg_dt

    def rk4_step(self, state, dt, input_concentrations):
        """
        Realiza un paso de integración usando el método Runge-Kutta de 4º orden (RK4).
        """
        k1 = self.get_derivatives(state, input_concentrations)
        
        state2 = [s + 0.5 * dt * k for s, k in zip(state, k1)]
        k2 = self.get_derivatives(state2, input_concentrations)

        state3 = [s + 0.5 * dt * k for s, k in zip(state, k2)]
        k3 = self.get_derivatives(state3, input_concentrations)

        state4 = [s + dt * k for s, k in zip(state, k3)]
        k4 = self.get_derivatives(state4, input_concentrations)

        new_state = [s + (dt / 6.0) * (k1_i + 2*k2_i + 2*k3_i + k4_i) for s, k1_i, k2_i, k3_i, k4_i in zip(state, k1, k2, k3, k4)]
        
        # Asegurar que los valores no sean negativos
        new_state[1] = max(0, new_state[1]) # r_NO3
        new_state[2] = max(0, new_state[2]) # r_Mg
        new_state[0] = max(0, new_state[0]) # h
        new_state[3] = max(0, new_state[3]) # C_NO3
        new_state[4] = max(0, new_state[4]) # C_Mg

        return new_state

    def run_simulation(self):
        """
        Ejecuta la simulación completa.
        """
        p = self.params
        H = p['H']
        R = p['R']
        
        # Calcular número de partículas N a partir de las fracciones másicas
        V_total_solid = p['A'] * H * (1 - p['xi'])
        mass_total_solid = V_total_solid / (
            (p['species']['NO3']['initial_mass_fraction'] / p['species']['NO3']['rho']) +
            (p['species']['Mg']['initial_mass_fraction'] / p['species']['Mg']['rho']) +
            ((1 - p['species']['NO3']['initial_mass_fraction'] - p['species']['Mg']['initial_mass_fraction']) / p['rho_insoluble'])
        )
        
        V_particle_NO3 = (4/3) * np.pi * R**3
        mass_particle_NO3 = V_particle_NO3 * p['species']['NO3']['rho']
        p['N_NO3'] = (mass_total_solid * p['species']['NO3']['initial_mass_fraction']) / mass_particle_NO3

        V_particle_Mg = (4/3) * np.pi * R**3
        mass_particle_Mg = V_particle_Mg * p['species']['Mg']['rho']
        p['N_Mg'] = (mass_total_solid * p['species']['Mg']['initial_mass_fraction']) / mass_particle_Mg

        # Condiciones iniciales para las 3 alturas
        states = [
            [H, R, R, p['species']['NO3']['C_s'], p['species']['Mg']['C_s']],
            [H, R, R, p['species']['NO3']['C_s'], p['species']['Mg']['C_s']],
            [H, R, R, p['species']['NO3']['C_s'], p['species']['Mg']['C_s']]
        ]

        results = {
            'time': [],
            'C_NO3_h1': [], 'C_Mg_h1': [],
            'C_NO3_h2': [], 'C_Mg_h2': [],
            'C_NO3_h3': [], 'C_Mg_h3': [],
        }

        t_max = 450
        dt = 0.5

        for t in np.arange(0, t_max + dt, dt):
            results['time'].append(t)
            input_concentrations = (0, 0) # Agua pura para la primera altura

            for i in range(len(states)):
                states[i] = self.rk4_step(states[i], dt, input_concentrations)
                
                results[f'C_NO3_h{i+1}'].append(states[i][3])
                results[f'C_Mg_h{i+1}'].append(states[i][4])

                input_concentrations = (states[i][3], states[i][4])
        
        return results

# --- Interfaz Gráfica con Tkinter ---

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Interactivo de Lixiviación de Caliche")
        self.geometry("1200x700")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.thread = None

        # --- Estilo ---
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))

        # --- Layout Principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        controls_frame = ttk.Frame(main_frame, padding="10")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        plot_frame = ttk.Frame(main_frame)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Controles ---
        ttk.Label(controls_frame, text="Panel de Control", style='Header.TLabel').pack(pady=(0, 15))

        self.entries = {}
        params = [
            ("Caudal de Riego (q, m³/h)", "flowRate", 0.000154),
            ("Altura Inicial del Lecho (H, m)", "initialHeight", 0.91),
            ("Constante Disolución NO₃ (k)", "k_no3", 0.2),
            ("Constante Disolución Mg (k)", "k_mg", 0.01),
            ("Radio de Partícula Inicial (R, m)", "particleRadius", 0.00635)
        ]

        for text, key, value in params:
            frame = ttk.Frame(controls_frame)
            ttk.Label(frame, text=text).pack(fill=tk.X)
            var = tk.DoubleVar(value=value)
            entry = ttk.Entry(frame, textvariable=var, width=20)
            entry.pack(fill=tk.X, pady=(2, 8))
            self.entries[key] = var
            frame.pack(fill=tk.X)

        self.run_button = ttk.Button(controls_frame, text="Ejecutar Simulación", command=self.start_simulation_thread)
        self.run_button.pack(fill=tk.X, ipady=5, pady=(20, 10))
        
        self.progress_bar = ttk.Progressbar(controls_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)

        # --- Gráfico Matplotlib ---
        self.fig = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.draw_initial_plot()

    def draw_initial_plot(self):
        self.ax.clear()
        self.ax.set_title("Curvas de Concentración vs. Tiempo")
        self.ax.set_xlabel("Tiempo de Riego (horas)")
        self.ax.set_ylabel("Concentración (gramos por litro)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.fig.tight_layout()
        self.canvas.draw()

    def update_plot(self, results):
        self.ax.clear()
        self.ax.plot(results['time'], results['C_NO3_h1'], label='NO₃ - Altura 1', color='blue')
        self.ax.plot(results['time'], results['C_NO3_h2'], label='NO₃ - Altura 2', color='red')
        self.ax.plot(results['time'], results['C_NO3_h3'], label='NO₃ - Altura 3', color='green')
        
        self.ax.plot(results['time'], results['C_Mg_h1'], label='Mg - Altura 1', color='blue', linestyle='--')
        self.ax.plot(results['time'], results['C_Mg_h2'], label='Mg - Altura 2', color='red', linestyle='--')
        self.ax.plot(results['time'], results['C_Mg_h3'], label='Mg - Altura 3', color='green', linestyle='--')
        
        self.ax.set_title("Curvas de Concentración vs. Tiempo")
        self.ax.set_xlabel("Tiempo de Riego (horas)")
        self.ax.set_ylabel("Concentración (gramos por litro)")
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Habilitar botón y detener barra de progreso
        self.run_button.config(state=tk.NORMAL)
        self.progress_bar.stop()

    def start_simulation_thread(self):
        self.run_button.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        
        self.thread = threading.Thread(target=self.run_simulation_task)
        self.thread.daemon = True # Permite cerrar la app aunque el hilo esté corriendo
        self.thread.start()

    def run_simulation_task(self):
        # Parámetros y constantes del modelo
        params = {
            'q': self.entries['flowRate'].get(),
            'H': self.entries['initialHeight'].get(),
            'R': self.entries['particleRadius'].get(),
            'A': np.pi * (0.2 / 2)**2,
            'xi': 0.2,
            'n_order': 0.6,
            'rho_insoluble': 2650,
            'species': {
                'NO3': {
                    'k': self.entries['k_no3'].get(),
                    'C_s': 250, 'rho': 2260, 'initial_mass_fraction': 0.1015
                },
                'Mg': {
                    'k': self.entries['k_mg'].get(),
                    'C_s': 20, 'rho': 2320, 'initial_mass_fraction': 0.0078
                }
            }
        }
        
        simulator = LeachingSimulator(params)
        results = simulator.run_simulation()
        
        # Programar la actualización del gráfico en el hilo principal de Tkinter
        self.after(0, self.update_plot, results)

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()