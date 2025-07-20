# =============================================================================
# MÓDULO DE TERMODINÁMICA Y FLUIDOS
# =============================================================================
# Propósito: Análisis de ciclos termodinámicos, flujo de fluidos y transferencia de calor
# Autor: Sistema de Ingeniería Mecánica con Python
# Versión: 1.0
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from datetime import datetime

class TermodinamicaFluidosApp:
    """
    Aplicación para análisis de termodinámica y fluidos
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Termodinámica y Fluidos - Análisis Avanzado")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Variables de datos
        self.datos_ciclo = {}
        self.datos_fluido = {}
        self.datos_transferencia = {}
        
        # Configurar interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        """Configura la interfaz principal de la aplicación"""
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_ciclos()
        self.crear_pestana_fluidos()
        self.crear_pestana_transferencia()
        self.crear_pestana_resultados()
        
    def crear_pestana_ciclos(self):
        """Crea la pestaña de análisis de ciclos termodinámicos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔄 CICLOS")
        
        # Frame izquierdo - Parámetros del ciclo
        left_frame = ttk.LabelFrame(frame, text="PARÁMETROS DEL CICLO", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Tipo de ciclo
        ttk.Label(left_frame, text="Tipo de Ciclo:").pack(anchor=tk.W)
        self.tipo_ciclo = ttk.Combobox(left_frame, 
                                     values=["Ciclo de Carnot", "Ciclo de Otto", "Ciclo de Diesel", "Ciclo de Brayton"])
        self.tipo_ciclo.pack(fill=tk.X, pady=(0, 10))
        self.tipo_ciclo.set("Ciclo de Otto")
        
        # Parámetros del fluido de trabajo
        ttk.Label(left_frame, text="Fluido de Trabajo:").pack(anchor=tk.W, pady=(10, 0))
        
        fluido_frame = ttk.Frame(left_frame)
        fluido_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fluido_frame, text="Temperatura alta (K):").grid(row=0, column=0, sticky=tk.W)
        self.T_alta_var = tk.StringVar(value="800")
        ttk.Entry(fluido_frame, textvariable=self.T_alta_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(fluido_frame, text="Temperatura baja (K):").grid(row=1, column=0, sticky=tk.W)
        self.T_baja_var = tk.StringVar(value="300")
        ttk.Entry(fluido_frame, textvariable=self.T_baja_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(fluido_frame, text="Presión alta (kPa):").grid(row=2, column=0, sticky=tk.W)
        self.P_alta_var = tk.StringVar(value="1000")
        ttk.Entry(fluido_frame, textvariable=self.P_alta_var, width=10).grid(row=2, column=1, padx=5)
        
        ttk.Label(fluido_frame, text="Presión baja (kPa):").grid(row=3, column=0, sticky=tk.W)
        self.P_baja_var = tk.StringVar(value="100")
        ttk.Entry(fluido_frame, textvariable=self.P_baja_var, width=10).grid(row=3, column=1, padx=5)
        
        # Relación de compresión (para ciclos Otto/Diesel)
        ttk.Label(left_frame, text="Relación de Compresión:").pack(anchor=tk.W, pady=(10, 0))
        self.r_compresion_var = tk.StringVar(value="8")
        ttk.Entry(left_frame, textvariable=self.r_compresion_var).pack(fill=tk.X, pady=(0, 10))
        
        # Botones de acción
        ttk.Button(left_frame, text="Analizar Ciclo", 
                  command=self.analizar_ciclo).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Calcular Eficiencia", 
                  command=self.calcular_eficiencia).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Optimizar Ciclo", 
                  command=self.optimizar_ciclo).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Diagrama P-V
        right_frame = ttk.LabelFrame(frame, text="DIAGRAMA P-V", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_ciclo, self.ax_ciclo = plt.subplots(figsize=(8, 6))
        self.canvas_ciclo = FigureCanvasTkAgg(self.fig_ciclo, right_frame)
        self.canvas_ciclo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_fluidos(self):
        """Crea la pestaña de análisis de flujo de fluidos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💧 FLUIDOS")
        
        # Frame izquierdo - Parámetros del flujo
        left_frame = ttk.LabelFrame(frame, text="PARÁMETROS DEL FLUJO", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Propiedades del fluido
        ttk.Label(left_frame, text="Propiedades del Fluido:").pack(anchor=tk.W, pady=(0, 5))
        
        fluido_frame = ttk.Frame(left_frame)
        fluido_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fluido_frame, text="Densidad (kg/m³):").grid(row=0, column=0, sticky=tk.W)
        self.densidad_var = tk.StringVar(value="1000")
        ttk.Entry(fluido_frame, textvariable=self.densidad_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(fluido_frame, text="Viscosidad (Pa·s):").grid(row=1, column=0, sticky=tk.W)
        self.viscosidad_var = tk.StringVar(value="0.001")
        ttk.Entry(fluido_frame, textvariable=self.viscosidad_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(fluido_frame, text="Velocidad (m/s):").grid(row=2, column=0, sticky=tk.W)
        self.velocidad_var = tk.StringVar(value="2")
        ttk.Entry(fluido_frame, textvariable=self.velocidad_var, width=10).grid(row=2, column=1, padx=5)
        
        # Geometría del conducto
        ttk.Label(left_frame, text="Geometría del Conducto:").pack(anchor=tk.W, pady=(10, 0))
        
        geo_frame = ttk.Frame(left_frame)
        geo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(geo_frame, text="Diámetro (m):").grid(row=0, column=0, sticky=tk.W)
        self.diametro_var = tk.StringVar(value="0.1")
        ttk.Entry(geo_frame, textvariable=self.diametro_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(geo_frame, text="Longitud (m):").grid(row=1, column=0, sticky=tk.W)
        self.longitud_var = tk.StringVar(value="10")
        ttk.Entry(geo_frame, textvariable=self.longitud_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(geo_frame, text="Rugosidad (m):").grid(row=2, column=0, sticky=tk.W)
        self.rugosidad_var = tk.StringVar(value="0.000045")
        ttk.Entry(geo_frame, textvariable=self.rugosidad_var, width=10).grid(row=2, column=1, padx=5)
        
        # Botones de análisis
        ttk.Button(left_frame, text="Análisis de Flujo", 
                  command=self.analizar_flujo).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Calcular Pérdidas", 
                  command=self.calcular_perdidas).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Análisis de Presión", 
                  command=self.analisis_presion).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Perfil de velocidad
        right_frame = ttk.LabelFrame(frame, text="PERFIL DE VELOCIDAD", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_fluido, self.ax_fluido = plt.subplots(figsize=(8, 6))
        self.canvas_fluido = FigureCanvasTkAgg(self.fig_fluido, right_frame)
        self.canvas_fluido.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_transferencia(self):
        """Crea la pestaña de transferencia de calor"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔥 TRANSFERENCIA")
        
        # Frame izquierdo - Parámetros de transferencia
        left_frame = ttk.LabelFrame(frame, text="PARÁMETROS DE TRANSFERENCIA", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Tipo de transferencia
        ttk.Label(left_frame, text="Tipo de Transferencia:").pack(anchor=tk.W)
        self.tipo_transferencia = ttk.Combobox(left_frame, 
                                             values=["Conducción", "Convección", "Radiación", "Combinada"])
        self.tipo_transferencia.pack(fill=tk.X, pady=(0, 10))
        self.tipo_transferencia.set("Conducción")
        
        # Propiedades del material
        ttk.Label(left_frame, text="Propiedades del Material:").pack(anchor=tk.W, pady=(10, 0))
        
        mat_frame = ttk.Frame(left_frame)
        mat_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mat_frame, text="Conductividad (W/m·K):").grid(row=0, column=0, sticky=tk.W)
        self.conductividad_var = tk.StringVar(value="50")
        ttk.Entry(mat_frame, textvariable=self.conductividad_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(mat_frame, text="Espesor (m):").grid(row=1, column=0, sticky=tk.W)
        self.espesor_var = tk.StringVar(value="0.01")
        ttk.Entry(mat_frame, textvariable=self.espesor_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(mat_frame, text="Área (m²):").grid(row=2, column=0, sticky=tk.W)
        self.area_var = tk.StringVar(value="1")
        ttk.Entry(mat_frame, textvariable=self.area_var, width=10).grid(row=2, column=1, padx=5)
        
        # Temperaturas
        ttk.Label(left_frame, text="Temperaturas:").pack(anchor=tk.W, pady=(10, 0))
        
        temp_frame = ttk.Frame(left_frame)
        temp_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(temp_frame, text="Temperatura caliente (K):").grid(row=0, column=0, sticky=tk.W)
        self.T_caliente_var = tk.StringVar(value="373")
        ttk.Entry(temp_frame, textvariable=self.T_caliente_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(temp_frame, text="Temperatura fría (K):").grid(row=1, column=0, sticky=tk.W)
        self.T_fria_var = tk.StringVar(value="293")
        ttk.Entry(temp_frame, textvariable=self.T_fria_var, width=10).grid(row=1, column=1, padx=5)
        
        # Coeficiente de convección
        ttk.Label(left_frame, text="Coeficiente de Convección (W/m²·K):").pack(anchor=tk.W, pady=(10, 0))
        self.h_conveccion_var = tk.StringVar(value="25")
        ttk.Entry(left_frame, textvariable=self.h_conveccion_var).pack(fill=tk.X, pady=(0, 10))
        
        # Botones
        ttk.Button(left_frame, text="Calcular Transferencia", 
                  command=self.calcular_transferencia).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Análisis de Resistencia", 
                  command=self.analisis_resistencia).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Optimizar Aislamiento", 
                  command=self.optimizar_aislamiento).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Distribución de temperatura
        right_frame = ttk.LabelFrame(frame, text="DISTRIBUCIÓN DE TEMPERATURA", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_transferencia, self.ax_transferencia = plt.subplots(figsize=(8, 6))
        self.canvas_transferencia = FigureCanvasTkAgg(self.fig_transferencia, right_frame)
        self.canvas_transferencia.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_resultados(self):
        """Crea la pestaña de resultados generales"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 RESULTADOS")
        
        # Frame principal
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto para resultados
        self.texto_resultados = tk.Text(main_frame, height=30, width=80)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.texto_resultados.yview)
        self.texto_resultados.configure(yscrollcommand=scrollbar.set)
        
        self.texto_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="Generar Reporte", 
                  command=self.generar_reporte).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Guardar Resultados", 
                  command=self.guardar_resultados).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Limpiar Resultados", 
                  command=self.limpiar_resultados).pack(side=tk.LEFT, padx=5)
    
    # Métodos de análisis de ciclos
    def analizar_ciclo(self):
        """Analiza el ciclo termodinámico seleccionado"""
        try:
            tipo = self.tipo_ciclo.get()
            T_alta = float(self.T_alta_var.get())
            T_baja = float(self.T_baja_var.get())
            P_alta = float(self.P_alta_var.get())
            P_baja = float(self.P_baja_var.get())
            r = float(self.r_compresion_var.get())
            
            if tipo == "Ciclo de Carnot":
                eficiencia = 1 - T_baja/T_alta
                trabajo_neto = 1000  # kJ/kg (ejemplo)
                calor_entrada = trabajo_neto / eficiencia
                
            elif tipo == "Ciclo de Otto":
                gamma = 1.4  # Para aire
                eficiencia = 1 - (1/r**(gamma-1))
                trabajo_neto = 800  # kJ/kg (ejemplo)
                calor_entrada = trabajo_neto / eficiencia
                
            elif tipo == "Ciclo de Diesel":
                gamma = 1.4
                rc = 2  # Relación de corte
                eficiencia = 1 - (1/r**(gamma-1)) * ((rc**gamma - 1)/(gamma*(rc - 1)))
                trabajo_neto = 900  # kJ/kg (ejemplo)
                calor_entrada = trabajo_neto / eficiencia
                
            else:  # Brayton
                gamma = 1.4
                eficiencia = 1 - (1/r**((gamma-1)/gamma))
                trabajo_neto = 600  # kJ/kg (ejemplo)
                calor_entrada = trabajo_neto / eficiencia
            
            # Guardar resultados
            self.datos_ciclo = {
                'tipo': tipo,
                'eficiencia': eficiencia,
                'trabajo_neto': trabajo_neto,
                'calor_entrada': calor_entrada,
                'T_alta': T_alta,
                'T_baja': T_baja,
                'P_alta': P_alta,
                'P_baja': P_baja,
                'r': r
            }
            
            # Visualizar ciclo
            self.visualizar_ciclo()
            
            # Mostrar resultados
            self.mostrar_resultados_ciclo()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis del ciclo: {str(e)}")
    
    def visualizar_ciclo(self):
        """Visualiza el ciclo termodinámico en diagrama P-V"""
        if not self.datos_ciclo:
            return
            
        self.ax_ciclo.clear()
        
        # Generar puntos para el ciclo (ejemplo simplificado)
        V = np.linspace(0.1, 2, 100)
        
        if self.datos_ciclo['tipo'] == "Ciclo de Otto":
            # Proceso 1-2: Compresión isentrópica
            V1, V2 = 2, 2/self.datos_ciclo['r']
            P1, P2 = self.datos_ciclo['P_baja'], self.datos_ciclo['P_alta']
            
            # Proceso 2-3: Adición de calor a volumen constante
            V3 = V2
            P3 = P2 * (self.datos_ciclo['T_alta'] / self.datos_ciclo['T_baja'])
            
            # Proceso 3-4: Expansión isentrópica
            V4 = V1
            P4 = P3 / (self.datos_ciclo['r']**1.4)
            
            # Proceso 4-1: Rechazo de calor a volumen constante
            V_cycle = [V1, V2, V3, V4, V1]
            P_cycle = [P1, P2, P3, P4, P1]
            
            self.ax_ciclo.plot(V_cycle, P_cycle, 'b-', linewidth=2, label='Ciclo Otto')
            self.ax_ciclo.plot(V_cycle[0], P_cycle[0], 'ro', markersize=8, label='Punto 1')
            self.ax_ciclo.plot(V_cycle[1], P_cycle[1], 'go', markersize=8, label='Punto 2')
            self.ax_ciclo.plot(V_cycle[2], P_cycle[2], 'bo', markersize=8, label='Punto 3')
            self.ax_ciclo.plot(V_cycle[3], P_cycle[3], 'mo', markersize=8, label='Punto 4')
        
        self.ax_ciclo.set_xlabel('Volumen (m³)')
        self.ax_ciclo.set_ylabel('Presión (kPa)')
        self.ax_ciclo.set_title(f'Diagrama P-V: {self.datos_ciclo["tipo"]}')
        self.ax_ciclo.legend()
        self.ax_ciclo.grid(True)
        
        self.canvas_ciclo.draw()
    
    def mostrar_resultados_ciclo(self):
        """Muestra los resultados del análisis del ciclo"""
        if not self.datos_ciclo:
            return
            
        resultados = f"""
=== ANÁLISIS DE CICLO TERMODINÁMICO ===
Tipo de ciclo: {self.datos_ciclo['tipo']}

Parámetros de operación:
- Temperatura alta: {self.datos_ciclo['T_alta']} K
- Temperatura baja: {self.datos_ciclo['T_baja']} K
- Presión alta: {self.datos_ciclo['P_alta']} kPa
- Presión baja: {self.datos_ciclo['P_baja']} kPa
- Relación de compresión: {self.datos_ciclo['r']}

Resultados del análisis:
- Eficiencia térmica: {self.datos_ciclo['eficiencia']:.3f} ({self.datos_ciclo['eficiencia']*100:.1f}%)
- Trabajo neto: {self.datos_ciclo['trabajo_neto']} kJ/kg
- Calor de entrada: {self.datos_ciclo['calor_entrada']:.1f} kJ/kg

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos de análisis de fluidos
    def analizar_flujo(self):
        """Analiza el flujo de fluidos"""
        try:
            # Obtener parámetros
            rho = float(self.densidad_var.get())
            mu = float(self.viscosidad_var.get())
            V = float(self.velocidad_var.get())
            D = float(self.diametro_var.get())
            L = float(self.longitud_var.get())
            e = float(self.rugosidad_var.get())
            
            # Calcular número de Reynolds
            Re = rho * V * D / mu
            
            # Determinar régimen de flujo
            if Re < 2300:
                regimen = "Laminar"
                f = 64 / Re
            else:
                regimen = "Turbulento"
                # Factor de fricción de Colebrook (aproximación)
                f = 0.02  # Valor típico para flujo turbulento
            
            # Calcular pérdidas por fricción
            hf = f * (L/D) * (V**2) / (2 * 9.81)
            
            # Calcular caída de presión
            delta_P = rho * 9.81 * hf
            
            # Guardar resultados
            self.datos_fluido = {
                'Re': Re,
                'regimen': regimen,
                'f': f,
                'hf': hf,
                'delta_P': delta_P,
                'V': V,
                'D': D
            }
            
            # Visualizar perfil de velocidad
            self.visualizar_perfil_velocidad()
            
            # Mostrar resultados
            self.mostrar_resultados_fluido()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis de flujo: {str(e)}")
    
    def visualizar_perfil_velocidad(self):
        """Visualiza el perfil de velocidad en el conducto"""
        if not self.datos_fluido:
            return
            
        self.ax_fluido.clear()
        
        # Generar perfil de velocidad
        r = np.linspace(0, self.datos_fluido['D']/2, 50)
        
        if self.datos_fluido['regimen'] == "Laminar":
            # Perfil parabólico para flujo laminar
            v = self.datos_fluido['V'] * (1 - (r/(self.datos_fluido['D']/2))**2)
        else:
            # Perfil de ley de potencia para flujo turbulento
            n = 7  # Exponente para flujo turbulento
            v = self.datos_fluido['V'] * (1 - (r/(self.datos_fluido['D']/2)))**(1/n)
        
        # Graficar perfil
        self.ax_fluido.plot(v, r, 'b-', linewidth=2, label='Perfil de velocidad')
        self.ax_fluido.plot(v, -r, 'b-', linewidth=2)
        
        # Dibujar conducto
        self.ax_fluido.axhline(y=self.datos_fluido['D']/2, color='k', linestyle='-', linewidth=2)
        self.ax_fluido.axhline(y=-self.datos_fluido['D']/2, color='k', linestyle='-', linewidth=2)
        
        self.ax_fluido.set_xlabel('Velocidad (m/s)')
        self.ax_fluido.set_ylabel('Radio (m)')
        self.ax_fluido.set_title(f'Perfil de Velocidad - Flujo {self.datos_fluido["regimen"]}')
        self.ax_fluido.legend()
        self.ax_fluido.grid(True)
        
        self.canvas_fluido.draw()
    
    def mostrar_resultados_fluido(self):
        """Muestra los resultados del análisis de flujo"""
        if not self.datos_fluido:
            return
            
        resultados = f"""
=== ANÁLISIS DE FLUJO DE FLUIDOS ===
Características del flujo:
- Número de Reynolds: {self.datos_fluido['Re']:.0f}
- Régimen de flujo: {self.datos_fluido['regimen']}
- Factor de fricción: {self.datos_fluido['f']:.4f}

Resultados del análisis:
- Pérdida de carga: {self.datos_fluido['hf']:.3f} m
- Caída de presión: {self.datos_fluido['delta_P']:.1f} Pa

Velocidad promedio: {self.datos_fluido['V']} m/s
Diámetro del conducto: {self.datos_fluido['D']} m

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos de transferencia de calor
    def calcular_transferencia(self):
        """Calcula la transferencia de calor"""
        try:
            # Obtener parámetros
            k = float(self.conductividad_var.get())
            L = float(self.espesor_var.get())
            A = float(self.area_var.get())
            T_hot = float(self.T_caliente_var.get())
            T_cold = float(self.T_fria_var.get())
            h = float(self.h_conveccion_var.get())
            
            tipo = self.tipo_transferencia.get()
            
            if tipo == "Conducción":
                # Transferencia por conducción
                q_cond = k * A * (T_hot - T_cold) / L
                R_cond = L / (k * A)
                
                # Distribución de temperatura
                x = np.linspace(0, L, 100)
                T = T_hot - (T_hot - T_cold) * x / L
                
                self.datos_transferencia = {
                    'tipo': tipo,
                    'q': q_cond,
                    'R': R_cond,
                    'x': x,
                    'T': T,
                    'T_hot': T_hot,
                    'T_cold': T_cold
                }
                
            elif tipo == "Convección":
                # Transferencia por convección
                q_conv = h * A * (T_hot - T_cold)
                R_conv = 1 / (h * A)
                
                self.datos_transferencia = {
                    'tipo': tipo,
                    'q': q_conv,
                    'R': R_conv,
                    'T_hot': T_hot,
                    'T_cold': T_cold
                }
                
            else:
                # Transferencia combinada
                R_total = L/(k*A) + 1/(h*A)
                q_total = (T_hot - T_cold) / R_total
                
                self.datos_transferencia = {
                    'tipo': tipo,
                    'q': q_total,
                    'R': R_total,
                    'T_hot': T_hot,
                    'T_cold': T_cold
                }
            
            # Visualizar distribución de temperatura
            self.visualizar_distribucion_temperatura()
            
            # Mostrar resultados
            self.mostrar_resultados_transferencia()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo de transferencia: {str(e)}")
    
    def visualizar_distribucion_temperatura(self):
        """Visualiza la distribución de temperatura"""
        if not self.datos_transferencia:
            return
            
        self.ax_transferencia.clear()
        
        if self.datos_transferencia['tipo'] == "Conducción":
            self.ax_transferencia.plot(self.datos_transferencia['x'], 
                                     self.datos_transferencia['T'], 'r-', linewidth=2)
            self.ax_transferencia.set_xlabel('Distancia (m)')
            self.ax_transferencia.set_ylabel('Temperatura (K)')
            self.ax_transferencia.set_title('Distribución de Temperatura - Conducción')
        else:
            # Para otros tipos, mostrar valores puntuales
            self.ax_transferencia.bar(['T_caliente', 'T_fría'], 
                                    [self.datos_transferencia['T_hot'], 
                                     self.datos_transferencia['T_cold']], 
                                    color=['red', 'blue'])
            self.ax_transferencia.set_ylabel('Temperatura (K)')
            self.ax_transferencia.set_title('Temperaturas - Transferencia de Calor')
        
        self.ax_transferencia.grid(True)
        self.canvas_transferencia.draw()
    
    def mostrar_resultados_transferencia(self):
        """Muestra los resultados de transferencia de calor"""
        if not self.datos_transferencia:
            return
            
        resultados = f"""
=== ANÁLISIS DE TRANSFERENCIA DE CALOR ===
Tipo de transferencia: {self.datos_transferencia['tipo']}

Resultados del análisis:
- Tasa de transferencia de calor: {self.datos_transferencia['q']:.1f} W
- Resistencia térmica: {self.datos_transferencia['R']:.4f} K/W

Temperaturas:
- Temperatura caliente: {self.datos_transferencia['T_hot']} K
- Temperatura fría: {self.datos_transferencia['T_cold']} K

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos adicionales (placeholder)
    def calcular_eficiencia(self):
        messagebox.showinfo("En Desarrollo", "Cálculo de eficiencia en desarrollo")
    
    def optimizar_ciclo(self):
        messagebox.showinfo("En Desarrollo", "Optimización de ciclo en desarrollo")
    
    def calcular_perdidas(self):
        messagebox.showinfo("En Desarrollo", "Cálculo de pérdidas en desarrollo")
    
    def analisis_presion(self):
        messagebox.showinfo("En Desarrollo", "Análisis de presión en desarrollo")
    
    def analisis_resistencia(self):
        messagebox.showinfo("En Desarrollo", "Análisis de resistencia en desarrollo")
    
    def optimizar_aislamiento(self):
        messagebox.showinfo("En Desarrollo", "Optimización de aislamiento en desarrollo")
    
    def generar_reporte(self):
        """Genera un reporte completo de los análisis"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_termodinamica_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE ANÁLISIS - TERMODINÁMICA Y FLUIDOS\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Agregar contenido del área de resultados
                contenido = self.texto_resultados.get(1.0, tk.END)
                f.write(contenido)
            
            messagebox.showinfo("Éxito", f"Reporte guardado como: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def guardar_resultados(self):
        """Guarda los resultados en un archivo"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    contenido = self.texto_resultados.get(1.0, tk.END)
                    f.write(contenido)
                
                messagebox.showinfo("Éxito", f"Resultados guardados en: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def limpiar_resultados(self):
        """Limpia el área de resultados"""
        self.texto_resultados.delete(1.0, tk.END)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = TermodinamicaFluidosApp()
    app.ejecutar()

if __name__ == "__main__":
    main() 