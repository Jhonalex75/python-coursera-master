# -----------------------------------------------------------------------------
# Módulo: MODELO_GRUA.py
# Propósito: Aplicación GUI para estudio y simulación de planes de izaje seguro con grúas
# Aplicación: Ingeniería Mecánica / Seguridad Industrial
# Dependencias: tkinter, numpy, matplotlib
# Uso: Ejecutar el script para abrir la aplicación de simulación de grúas
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime

class SimuladorGrua:
    """
    Aplicación GUI para simulación de operaciones de grúa
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Operaciones de Grúa - Seguridad Industrial")
        self.root.geometry("1400x900")
        
        # Variables de control
        self.capacidad_grua = tk.DoubleVar(value=50)  # toneladas
        self.peso_carga = tk.DoubleVar(value=30)      # toneladas
        self.radio_izaje = tk.DoubleVar(value=20)     # metros
        self.altura_izaje = tk.DoubleVar(value=15)    # metros
        self.angulo_pluma = tk.DoubleVar(value=45)    # grados
        self.factor_seguridad = tk.DoubleVar(value=1.25)
        
        # Variables de condiciones
        self.velocidad_viento = tk.DoubleVar(value=10)  # km/h
        self.condicion_terreno = tk.StringVar(value="Firme")
        self.tipo_carga = tk.StringVar(value="Estática")
        self.visibilidad = tk.StringVar(value="Buena")
        
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
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Crear secciones de controles
        self.crear_controles_grua(control_frame)
        self.crear_controles_carga(control_frame)
        self.crear_controles_condiciones(control_frame)
        
        # Panel de visualización (derecha)
        viz_frame = ttk.LabelFrame(main_frame, text="Visualización y Análisis", padding="10")
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Panel de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados del Análisis", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.crear_panel_resultados(results_frame)
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Analizar Operación", 
                  command=self.analizar_operacion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generar Reporte", 
                  command=self.generar_reporte).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Simular Secuencia", 
                  command=self.simular_secuencia).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.limpiar_analisis).pack(side=tk.LEFT, padx=5)
        
        # Análisis inicial
        self.analizar_operacion()
        
    def crear_controles_grua(self, parent):
        """
        Crea controles para parámetros de la grúa
        """
        grua_frame = ttk.LabelFrame(parent, text="Especificaciones de la Grúa", padding="10")
        grua_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Capacidad de la grúa
        ttk.Label(grua_frame, text="Capacidad Máxima (ton):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grua_frame, textvariable=self.capacidad_grua, width=15).grid(row=0, column=1, pady=2)
        
        # Radio de izaje
        ttk.Label(grua_frame, text="Radio de Izaje (m):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grua_frame, textvariable=self.radio_izaje, width=15).grid(row=1, column=1, pady=2)
        
        # Altura de izaje
        ttk.Label(grua_frame, text="Altura de Izaje (m):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grua_frame, textvariable=self.altura_izaje, width=15).grid(row=2, column=1, pady=2)
        
        # Ángulo de la pluma
        ttk.Label(grua_frame, text="Ángulo de Pluma (°):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(grua_frame, textvariable=self.angulo_pluma, width=15).grid(row=3, column=1, pady=2)
        
    def crear_controles_carga(self, parent):
        """
        Crea controles para parámetros de la carga
        """
        carga_frame = ttk.LabelFrame(parent, text="Especificaciones de la Carga", padding="10")
        carga_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Peso de la carga
        ttk.Label(carga_frame, text="Peso de la Carga (ton):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(carga_frame, textvariable=self.peso_carga, width=15).grid(row=0, column=1, pady=2)
        
        # Factor de seguridad
        ttk.Label(carga_frame, text="Factor de Seguridad:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(carga_frame, textvariable=self.factor_seguridad, width=15).grid(row=1, column=1, pady=2)
        
        # Tipo de carga
        ttk.Label(carga_frame, text="Tipo de Carga:").grid(row=2, column=0, sticky=tk.W, pady=2)
        tipo_combo = ttk.Combobox(carga_frame, textvariable=self.tipo_carga, 
                                 values=["Estática", "Dinámica", "Impacto"], width=12)
        tipo_combo.grid(row=2, column=1, pady=2)
        
    def crear_controles_condiciones(self, parent):
        """
        Crea controles para condiciones ambientales
        """
        cond_frame = ttk.LabelFrame(parent, text="Condiciones Ambientales", padding="10")
        cond_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Velocidad del viento
        ttk.Label(cond_frame, text="Velocidad del Viento (km/h):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(cond_frame, textvariable=self.velocidad_viento, width=15).grid(row=0, column=1, pady=2)
        
        # Condición del terreno
        ttk.Label(cond_frame, text="Condición del Terreno:").grid(row=1, column=0, sticky=tk.W, pady=2)
        terreno_combo = ttk.Combobox(cond_frame, textvariable=self.condicion_terreno,
                                   values=["Firme", "Blando", "Inestable"], width=12)
        terreno_combo.grid(row=1, column=1, pady=2)
        
        # Visibilidad
        ttk.Label(cond_frame, text="Visibilidad:").grid(row=2, column=0, sticky=tk.W, pady=2)
        vis_combo = ttk.Combobox(cond_frame, textvariable=self.visibilidad,
                               values=["Excelente", "Buena", "Regular", "Mala"], width=12)
        vis_combo.grid(row=2, column=1, pady=2)
        
        # Información de seguridad
        info_frame = ttk.LabelFrame(parent, text="Información de Seguridad", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="• Verificar capacidad vs carga").pack(anchor=tk.W)
        ttk.Label(info_frame, text="• Considerar factores ambientales").pack(anchor=tk.W)
        ttk.Label(info_frame, text="• Mantener factor de seguridad").pack(anchor=tk.W)
        ttk.Label(info_frame, text="• Revisar estabilidad del terreno").pack(anchor=tk.W)
        
    def crear_panel_resultados(self, parent):
        """
        Crea el panel de resultados
        """
        # Frame para resultados
        results_inner = ttk.Frame(parent)
        results_inner.pack(fill=tk.X)
        
        # Variables para mostrar resultados
        self.resultado_capacidad = tk.StringVar(value="")
        self.resultado_seguridad = tk.StringVar(value="")
        self.resultado_recomendaciones = tk.StringVar(value="")
        
        # Etiquetas de resultados
        ttk.Label(results_inner, text="Estado de Capacidad:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Label(results_inner, textvariable=self.resultado_capacidad, font=('Arial', 10)).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(results_inner, text="Factor de Seguridad:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        ttk.Label(results_inner, textvariable=self.resultado_seguridad, font=('Arial', 10)).grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(results_inner, text="Recomendaciones:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        ttk.Label(results_inner, textvariable=self.resultado_recomendaciones, font=('Arial', 9), 
                 wraplength=800).grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=(5, 0))
        
    def calcular_capacidad_efectiva(self):
        """
        Calcula la capacidad efectiva de la grúa según el radio
        """
        capacidad_max = self.capacidad_grua.get()
        radio = self.radio_izaje.get()
        
        # Curva de capacidad típica (simplificada)
        # Capacidad disminuye con el radio
        radio_max = 30  # Radio máximo típico
        factor_radio = max(0.3, 1 - (radio / radio_max) ** 1.5)
        
        capacidad_efectiva = capacidad_max * factor_radio
        
        return capacidad_efectiva
    
    def calcular_factores_ambientales(self):
        """
        Calcula factores de reducción por condiciones ambientales
        """
        viento = self.velocidad_viento.get()
        terreno = self.condicion_terreno.get()
        visibilidad = self.visibilidad.get()
        
        # Factor por viento
        if viento <= 10:
            factor_viento = 1.0
        elif viento <= 20:
            factor_viento = 0.9
        elif viento <= 30:
            factor_viento = 0.7
        else:
            factor_viento = 0.5
        
        # Factor por terreno
        factores_terreno = {
            "Firme": 1.0,
            "Blando": 0.8,
            "Inestable": 0.6
        }
        factor_terreno = factores_terreno.get(terreno, 1.0)
        
        # Factor por visibilidad
        factores_vis = {
            "Excelente": 1.0,
            "Buena": 0.95,
            "Regular": 0.8,
            "Mala": 0.6
        }
        factor_vis = factores_vis.get(visibilidad, 1.0)
        
        return factor_viento * factor_terreno * factor_vis
    
    def analizar_operacion(self):
        """
        Analiza la operación de izaje
        """
        try:
            # Obtener parámetros
            peso_carga = self.peso_carga.get()
            capacidad_efectiva = self.calcular_capacidad_efectiva()
            factor_ambiental = self.calcular_factores_ambientales()
            factor_seguridad = self.factor_seguridad.get()
            
            # Capacidad disponible considerando factores
            capacidad_disponible = capacidad_efectiva * factor_ambiental / factor_seguridad
            
            # Análisis de seguridad
            margen_seguridad = capacidad_disponible - peso_carga
            porcentaje_uso = (peso_carga / capacidad_disponible) * 100
            
            # Actualizar resultados
            if margen_seguridad > 0:
                self.resultado_capacidad.set(f"SEGURO - Margen: {margen_seguridad:.1f} ton")
            else:
                self.resultado_capacidad.set(f"INSEGURO - Exceso: {abs(margen_seguridad):.1f} ton")
            
            self.resultado_seguridad.set(f"{porcentaje_uso:.1f}% de capacidad")
            
            # Generar recomendaciones
            recomendaciones = []
            if porcentaje_uso > 90:
                recomendaciones.append("ALERTA: Operación en límite de capacidad")
            if porcentaje_uso > 80:
                recomendaciones.append("Precaución: Alta utilización de capacidad")
            if self.velocidad_viento.get() > 20:
                recomendaciones.append("Reducir operaciones por viento fuerte")
            if self.condicion_terreno.get() != "Firme":
                recomendaciones.append("Verificar estabilidad del terreno")
            if self.visibilidad.get() in ["Regular", "Mala"]:
                recomendaciones.append("Mejorar condiciones de visibilidad")
            
            if not recomendaciones:
                recomendaciones.append("Operación dentro de parámetros seguros")
            
            self.resultado_recomendaciones.set(" | ".join(recomendaciones))
            
            # Generar visualización
            self.generar_visualizacion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en análisis: {str(e)}")
    
    def generar_visualizacion(self):
        """
        Genera la visualización de la operación
        """
        # Limpiar figura
        self.fig.clear()
        
        # Crear subplots
        gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Diagrama de la grúa
        ax1 = self.fig.add_subplot(gs[0, 0])
        self.dibujar_grua(ax1)
        
        # 2. Curva de capacidad
        ax2 = self.fig.add_subplot(gs[0, 1])
        self.dibujar_curva_capacidad(ax2)
        
        # 3. Análisis de factores
        ax3 = self.fig.add_subplot(gs[1, 0])
        self.dibujar_analisis_factores(ax3)
        
        # 4. Indicadores de seguridad
        ax4 = self.fig.add_subplot(gs[1, 1])
        self.dibujar_indicadores_seguridad(ax4)
        
        plt.tight_layout()
        self.canvas.draw()
    
    def dibujar_grua(self, ax):
        """
        Dibuja el diagrama esquemático de la grúa
        """
        # Coordenadas de la grúa
        x_grua = [0, 0, 5, 8]
        y_grua = [0, 10, 15, 12]
        
        # Dibujar grúa
        ax.plot(x_grua, y_grua, 'k-', linewidth=3, label='Pluma')
        ax.plot([0, 0], [0, 2], 'k-', linewidth=5, label='Base')
        
        # Dibujar carga
        radio = self.radio_izaje.get()
        altura = self.altura_izaje.get()
        ax.plot([radio], [altura], 'ro', markersize=15, label='Carga')
        
        # Dibujar cable
        ax.plot([0, radio], [10, altura], 'b--', linewidth=2, label='Cable')
        
        # Configurar gráfico
        ax.set_xlim(-2, radio + 5)
        ax.set_ylim(0, altura + 5)
        ax.set_xlabel('Distancia (m)')
        ax.set_ylabel('Altura (m)')
        ax.set_title('Diagrama de la Operación')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_aspect('equal')
    
    def dibujar_curva_capacidad(self, ax):
        """
        Dibuja la curva de capacidad de la grúa
        """
        radios = np.linspace(5, 35, 50)
        capacidad_max = self.capacidad_grua.get()
        
        # Curva de capacidad
        capacidades = capacidad_max * np.maximum(0.3, 1 - (radios / 30) ** 1.5)
        
        ax.plot(radios, capacidades, 'b-', linewidth=2, label='Capacidad Máxima')
        
        # Punto de operación actual
        radio_actual = self.radio_izaje.get()
        capacidad_actual = self.calcular_capacidad_efectiva()
        ax.plot(radio_actual, capacidad_actual, 'ro', markersize=10, label='Punto Actual')
        
        # Línea de carga
        peso_carga = self.peso_carga.get()
        ax.axhline(y=peso_carga, color='g', linestyle='--', alpha=0.7, label=f'Carga: {peso_carga} ton')
        
        ax.set_xlabel('Radio (m)')
        ax.set_ylabel('Capacidad (ton)')
        ax.set_title('Curva de Capacidad')
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    def dibujar_analisis_factores(self, ax):
        """
        Dibuja el análisis de factores ambientales
        """
        factores = ['Viento', 'Terreno', 'Visibilidad', 'Seguridad']
        valores = [
            self.calcular_factores_ambientales() * 100,
            80 if self.condicion_terreno.get() == "Firme" else 60,
            90 if self.visibilidad.get() == "Buena" else 70,
            self.factor_seguridad.get() * 100
        ]
        
        colores = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
        bars = ax.bar(factores, valores, color=colores, alpha=0.7)
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{valor:.0f}%', ha='center', va='bottom')
        
        ax.set_ylabel('Factor (%)')
        ax.set_title('Análisis de Factores')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')
    
    def dibujar_indicadores_seguridad(self, ax):
        """
        Dibuja indicadores de seguridad
        """
        peso_carga = self.peso_carga.get()
        capacidad_disponible = self.calcular_capacidad_efectiva() * self.calcular_factores_ambientales() / self.factor_seguridad.get()
        
        # Crear gráfico de dona
        sizes = [peso_carga, capacidad_disponible - peso_carga]
        labels = ['Carga', 'Margen']
        colors = ['red' if peso_carga > capacidad_disponible else 'green', 'lightgray']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90)
        
        ax.set_title('Utilización de Capacidad')
        
        # Agregar texto de estado
        if peso_carga > capacidad_disponible:
            ax.text(0, -1.5, 'INSEGURO', ha='center', va='center', 
                   fontsize=14, fontweight='bold', color='red')
        else:
            ax.text(0, -1.5, 'SEGURO', ha='center', va='center', 
                   fontsize=14, fontweight='bold', color='green')
    
    def simular_secuencia(self):
        """
        Simula una secuencia de operación
        """
        # Crear ventana de simulación
        sim_window = tk.Toplevel(self.root)
        sim_window.title("Simulación de Secuencia de Operación")
        sim_window.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(sim_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de pasos
        pasos = [
            "1. Verificación previa de la grúa",
            "2. Inspección del terreno",
            "3. Verificación de la carga",
            "4. Posicionamiento de la grúa",
            "5. Izaje de la carga",
            "6. Transporte de la carga",
            "7. Descenso de la carga",
            "8. Finalización de la operación"
        ]
        
        ttk.Label(main_frame, text="SECUENCIA DE OPERACIÓN", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        for paso in pasos:
            ttk.Label(main_frame, text=paso, font=('Arial', 11)).pack(anchor=tk.W, pady=2)
        
        # Botón para cerrar
        ttk.Button(main_frame, text="Cerrar", 
                  command=sim_window.destroy).pack(pady=20)
    
    def generar_reporte(self):
        """
        Genera un reporte de la operación
        """
        try:
            # Crear contenido del reporte
            reporte = f"""
REPORTE DE OPERACIÓN DE GRÚA
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ESPECIFICACIONES DE LA GRÚA:
- Capacidad máxima: {self.capacidad_grua.get()} ton
- Radio de izaje: {self.radio_izaje.get()} m
- Altura de izaje: {self.altura_izaje.get()} m
- Ángulo de pluma: {self.angulo_pluma.get()}°

ESPECIFICACIONES DE LA CARGA:
- Peso de la carga: {self.peso_carga.get()} ton
- Tipo de carga: {self.tipo_carga.get()}
- Factor de seguridad: {self.factor_seguridad.get()}

CONDICIONES AMBIENTALES:
- Velocidad del viento: {self.velocidad_viento.get()} km/h
- Condición del terreno: {self.condicion_terreno.get()}
- Visibilidad: {self.visibilidad.get()}

ANÁLISIS DE SEGURIDAD:
- Capacidad efectiva: {self.calcular_capacidad_efectiva():.1f} ton
- Factor ambiental: {self.calcular_factores_ambientales():.2f}
- Capacidad disponible: {self.calcular_capacidad_efectiva() * self.calcular_factores_ambientales() / self.factor_seguridad.get():.1f} ton
- Estado: {self.resultado_capacidad.get()}

RECOMENDACIONES:
{self.resultado_recomendaciones.get()}
            """
            
            # Guardar archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Guardar Reporte"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(reporte)
                messagebox.showinfo("Éxito", f"Reporte guardado en {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def limpiar_analisis(self):
        """
        Limpia el análisis actual
        """
        self.resultado_capacidad.set("")
        self.resultado_seguridad.set("")
        self.resultado_recomendaciones.set("")
        self.fig.clear()
        self.canvas.draw()
        messagebox.showinfo("Info", "Análisis limpiado")

def main():
    """
    Función principal para ejecutar la aplicación
    """
    root = tk.Tk()
    app = SimuladorGrua(root)
    root.mainloop()

if __name__ == "__main__":
    main()
