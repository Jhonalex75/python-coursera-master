# =============================================================================
# MÓDULO DE DINÁMICA DE MÁQUINAS
# =============================================================================
# Propósito: Análisis de mecanismos, vibraciones, balanceo y cinemática
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
import os

class DinamicaMaquinasApp:
    """
    Aplicación para análisis de dinámica de máquinas
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dinámica de Máquinas - Análisis Avanzado")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Variables de datos
        self.datos_mecanismo = {}
        self.datos_vibracion = {}
        self.resultados = {}
        
        # Configurar interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        """Configura la interfaz principal de la aplicación"""
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_mecanismos()
        self.crear_pestana_vibraciones()
        self.crear_pestana_balanceo()
        self.crear_pestana_cinematica()
        self.crear_pestana_resultados()
        
    def crear_pestana_mecanismos(self):
        """Crea la pestaña de análisis de mecanismos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 MECANISMOS")
        
        # Frame izquierdo - Entrada de datos
        left_frame = ttk.LabelFrame(frame, text="DATOS DEL MECANISMO", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Tipo de mecanismo
        ttk.Label(left_frame, text="Tipo de Mecanismo:").pack(anchor=tk.W)
        self.tipo_mecanismo = ttk.Combobox(left_frame, 
                                         values=["4 Barras", "Manivela-Biela", "Leva-Seguidor", "Engranajes"])
        self.tipo_mecanismo.pack(fill=tk.X, pady=(0, 10))
        self.tipo_mecanismo.set("4 Barras")
        
        # Dimensiones
        ttk.Label(left_frame, text="Dimensiones (mm):").pack(anchor=tk.W, pady=(10, 0))
        
        # Frame para dimensiones
        dim_frame = ttk.Frame(left_frame)
        dim_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dim_frame, text="L1 (Manivela):").grid(row=0, column=0, sticky=tk.W)
        self.l1_var = tk.StringVar(value="100")
        ttk.Entry(dim_frame, textvariable=self.l1_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(dim_frame, text="L2 (Biela):").grid(row=1, column=0, sticky=tk.W)
        self.l2_var = tk.StringVar(value="200")
        ttk.Entry(dim_frame, textvariable=self.l2_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(dim_frame, text="L3 (Balancín):").grid(row=2, column=0, sticky=tk.W)
        self.l3_var = tk.StringVar(value="150")
        ttk.Entry(dim_frame, textvariable=self.l3_var, width=10).grid(row=2, column=1, padx=5)
        
        ttk.Label(dim_frame, text="L4 (Base):").grid(row=3, column=0, sticky=tk.W)
        self.l4_var = tk.StringVar(value="250")
        ttk.Entry(dim_frame, textvariable=self.l4_var, width=10).grid(row=3, column=1, padx=5)
        
        # Velocidad angular
        ttk.Label(left_frame, text="Velocidad Angular (rad/s):").pack(anchor=tk.W, pady=(10, 0))
        self.velocidad_var = tk.StringVar(value="10")
        ttk.Entry(left_frame, textvariable=self.velocidad_var).pack(fill=tk.X, pady=(0, 10))
        
        # Botones de acción
        ttk.Button(left_frame, text="Analizar Mecanismo", 
                  command=self.analizar_mecanismo).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Simular Movimiento", 
                  command=self.simular_movimiento).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Visualización
        right_frame = ttk.LabelFrame(frame, text="VISUALIZACIÓN", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_mecanismo, self.ax_mecanismo = plt.subplots(figsize=(8, 6))
        self.canvas_mecanismo = FigureCanvasTkAgg(self.fig_mecanismo, right_frame)
        self.canvas_mecanismo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_vibraciones(self):
        """Crea la pestaña de análisis de vibraciones"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 VIBRACIONES")
        
        # Frame izquierdo - Parámetros
        left_frame = ttk.LabelFrame(frame, text="PARÁMETROS DE VIBRACIÓN", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Sistema masa-resorte-amortiguador
        ttk.Label(left_frame, text="Sistema Masa-Resorte-Amortiguador:").pack(anchor=tk.W, pady=(0, 5))
        
        param_frame = ttk.Frame(left_frame)
        param_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(param_frame, text="Masa (kg):").grid(row=0, column=0, sticky=tk.W)
        self.masa_var = tk.StringVar(value="10")
        ttk.Entry(param_frame, textvariable=self.masa_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="Rigidez (N/m):").grid(row=1, column=0, sticky=tk.W)
        self.rigidez_var = tk.StringVar(value="1000")
        ttk.Entry(param_frame, textvariable=self.rigidez_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(param_frame, text="Amortiguamiento (Ns/m):").grid(row=2, column=0, sticky=tk.W)
        self.amortiguamiento_var = tk.StringVar(value="50")
        ttk.Entry(param_frame, textvariable=self.amortiguamiento_var, width=10).grid(row=2, column=1, padx=5)
        
        # Condiciones iniciales
        ttk.Label(left_frame, text="Condiciones Iniciales:").pack(anchor=tk.W, pady=(10, 0))
        
        cond_frame = ttk.Frame(left_frame)
        cond_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cond_frame, text="Desplazamiento inicial (m):").grid(row=0, column=0, sticky=tk.W)
        self.x0_var = tk.StringVar(value="0.1")
        ttk.Entry(cond_frame, textvariable=self.x0_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(cond_frame, text="Velocidad inicial (m/s):").grid(row=1, column=0, sticky=tk.W)
        self.v0_var = tk.StringVar(value="0")
        ttk.Entry(cond_frame, textvariable=self.v0_var, width=10).grid(row=1, column=1, padx=5)
        
        # Tiempo de simulación
        ttk.Label(left_frame, text="Tiempo de simulación (s):").pack(anchor=tk.W, pady=(10, 0))
        self.tiempo_sim_var = tk.StringVar(value="10")
        ttk.Entry(left_frame, textvariable=self.tiempo_sim_var).pack(fill=tk.X, pady=(0, 10))
        
        # Botones
        ttk.Button(left_frame, text="Analizar Vibración Libre", 
                  command=self.analizar_vibracion_libre).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Analizar Respuesta Forzada", 
                  command=self.analizar_respuesta_forzada).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Análisis de Frecuencias", 
                  command=self.analisis_frecuencias).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Gráficos
        right_frame = ttk.LabelFrame(frame, text="RESULTADOS", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráficos
        self.fig_vibracion, (self.ax_desplazamiento, self.ax_velocidad) = plt.subplots(2, 1, figsize=(8, 8))
        self.canvas_vibracion = FigureCanvasTkAgg(self.fig_vibracion, right_frame)
        self.canvas_vibracion.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_balanceo(self):
        """Crea la pestaña de balanceo de rotores"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚖️ BALANCEO")
        
        # Frame izquierdo - Datos del rotor
        left_frame = ttk.LabelFrame(frame, text="DATOS DEL ROTOR", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Parámetros del rotor
        ttk.Label(left_frame, text="Parámetros del Rotor:").pack(anchor=tk.W, pady=(0, 5))
        
        rotor_frame = ttk.Frame(left_frame)
        rotor_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(rotor_frame, text="Masa total (kg):").grid(row=0, column=0, sticky=tk.W)
        self.masa_rotor_var = tk.StringVar(value="100")
        ttk.Entry(rotor_frame, textvariable=self.masa_rotor_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(rotor_frame, text="Velocidad (rpm):").grid(row=1, column=0, sticky=tk.W)
        self.velocidad_rotor_var = tk.StringVar(value="3000")
        ttk.Entry(rotor_frame, textvariable=self.velocidad_rotor_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(rotor_frame, text="Radio del rotor (m):").grid(row=2, column=0, sticky=tk.W)
        self.radio_rotor_var = tk.StringVar(value="0.5")
        ttk.Entry(rotor_frame, textvariable=self.radio_rotor_var, width=10).grid(row=2, column=1, padx=5)
        
        # Desbalance
        ttk.Label(left_frame, text="Desbalance:").pack(anchor=tk.W, pady=(10, 0))
        
        desb_frame = ttk.Frame(left_frame)
        desb_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(desb_frame, text="Masa desbalanceada (kg):").grid(row=0, column=0, sticky=tk.W)
        self.masa_desb_var = tk.StringVar(value="0.1")
        ttk.Entry(desb_frame, textvariable=self.masa_desb_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(desb_frame, text="Radio de desbalance (m):").grid(row=1, column=0, sticky=tk.W)
        self.radio_desb_var = tk.StringVar(value="0.3")
        ttk.Entry(desb_frame, textvariable=self.radio_desb_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(desb_frame, text="Ángulo de desbalance (grados):").grid(row=2, column=0, sticky=tk.W)
        self.angulo_desb_var = tk.StringVar(value="45")
        ttk.Entry(desb_frame, textvariable=self.angulo_desb_var, width=10).grid(row=2, column=1, padx=5)
        
        # Botones
        ttk.Button(left_frame, text="Calcular Desbalance", 
                  command=self.calcular_desbalance).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Proponer Corrección", 
                  command=self.proponer_correccion).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Análisis de Velocidades Críticas", 
                  command=self.analisis_velocidades_criticas).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Resultados
        right_frame = ttk.LabelFrame(frame, text="RESULTADOS DEL BALANCEO", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de texto para resultados
        self.texto_balanceo = tk.Text(right_frame, height=20, width=50)
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.texto_balanceo.yview)
        self.texto_balanceo.configure(yscrollcommand=scrollbar.set)
        
        self.texto_balanceo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def crear_pestana_cinematica(self):
        """Crea la pestaña de análisis cinemático"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎯 CINEMÁTICA")
        
        # Frame izquierdo - Análisis cinemático
        left_frame = ttk.LabelFrame(frame, text="ANÁLISIS CINEMÁTICO", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Tipo de análisis
        ttk.Label(left_frame, text="Tipo de Análisis:").pack(anchor=tk.W)
        self.tipo_cinematica = ttk.Combobox(left_frame, 
                                          values=["Posición", "Velocidad", "Aceleración", "Completo"])
        self.tipo_cinematica.pack(fill=tk.X, pady=(0, 10))
        self.tipo_cinematica.set("Completo")
        
        # Parámetros de tiempo
        ttk.Label(left_frame, text="Parámetros de Tiempo:").pack(anchor=tk.W, pady=(10, 0))
        
        tiempo_frame = ttk.Frame(left_frame)
        tiempo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(tiempo_frame, text="Tiempo inicial (s):").grid(row=0, column=0, sticky=tk.W)
        self.ti_var = tk.StringVar(value="0")
        ttk.Entry(tiempo_frame, textvariable=self.ti_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(tiempo_frame, text="Tiempo final (s):").grid(row=1, column=0, sticky=tk.W)
        self.tf_var = tk.StringVar(value="10")
        ttk.Entry(tiempo_frame, textvariable=self.tf_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(tiempo_frame, text="Pasos:").grid(row=2, column=0, sticky=tk.W)
        self.pasos_var = tk.StringVar(value="100")
        ttk.Entry(tiempo_frame, textvariable=self.pasos_var, width=10).grid(row=2, column=1, padx=5)
        
        # Botones
        ttk.Button(left_frame, text="Análisis Cinemático", 
                  command=self.analisis_cinematico).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Generar Animación", 
                  command=self.generar_animacion).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Exportar Datos", 
                  command=self.exportar_datos_cinematica).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Gráficos cinemáticos
        right_frame = ttk.LabelFrame(frame, text="GRÁFICOS CINEMÁTICOS", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráficos
        self.fig_cinematica, ((self.ax_pos, self.ax_vel), (self.ax_acel, self.ax_trayectoria)) = plt.subplots(2, 2, figsize=(10, 8))
        self.canvas_cinematica = FigureCanvasTkAgg(self.fig_cinematica, right_frame)
        self.canvas_cinematica.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
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
    
    # Métodos de análisis de mecanismos
    def analizar_mecanismo(self):
        """Analiza el mecanismo de 4 barras"""
        try:
            # Obtener datos
            l1 = float(self.l1_var.get())
            l2 = float(self.l2_var.get())
            l3 = float(self.l3_var.get())
            l4 = float(self.l4_var.get())
            omega = float(self.velocidad_var.get())
            
            # Verificar condición de Grashof
            longitudes = sorted([l1, l2, l3, l4])
            s = longitudes[0]  # Más corta
            l = longitudes[3]  # Más larga
            p = longitudes[1]  # Intermedia 1
            q = longitudes[2]  # Intermedia 2
            
            if s + l <= p + q:
                tipo = "Mecanismo de Grashof"
            else:
                tipo = "Mecanismo no-Grashof"
            
            # Calcular ángulos para una revolución completa
            theta2 = np.linspace(0, 2*np.pi, 100)
            theta3 = []
            theta4 = []
            
            for t2 in theta2:
                # Análisis de posición usando ecuaciones de cierre
                A = 2*l3*l4 - 2*l1*l3*np.cos(t2)
                B = -2*l1*l3*np.sin(t2)
                C = l1**2 + l3**2 + l4**2 - l2**2 - 2*l1*l4*np.cos(t2)
                
                # Resolver para theta4
                cos_theta4 = (-B*np.sqrt(B**2 - A**2 + C**2) + A*C) / (A**2 + B**2)
                theta4.append(np.arccos(cos_theta4))
                
                # Calcular theta3
                cos_theta3 = (l1*np.cos(t2) + l4*np.cos(theta4[-1]) - l2) / l3
                theta3.append(np.arccos(cos_theta3))
            
            # Guardar resultados
            self.datos_mecanismo = {
                'tipo': tipo,
                'l1': l1, 'l2': l2, 'l3': l3, 'l4': l4,
                'omega': omega,
                'theta2': theta2,
                'theta3': theta3,
                'theta4': theta4
            }
            
            # Visualizar
            self.visualizar_mecanismo()
            
            # Mostrar resultados
            self.mostrar_resultados_mecanismo()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis: {str(e)}")
    
    def visualizar_mecanismo(self):
        """Visualiza el mecanismo"""
        if not self.datos_mecanismo:
            return
            
        self.ax_mecanismo.clear()
        
        # Dibujar el mecanismo en una posición específica
        theta2 = self.datos_mecanismo['theta2'][0]
        theta3 = self.datos_mecanismo['theta3'][0]
        theta4 = self.datos_mecanismo['theta4'][0]
        
        l1, l2, l3, l4 = (self.datos_mecanismo['l1'], self.datos_mecanismo['l2'],
                         self.datos_mecanismo['l3'], self.datos_mecanismo['l4'])
        
        # Calcular posiciones de los puntos
        A = [0, 0]  # Punto fijo 1
        B = [l1*np.cos(theta2), l1*np.sin(theta2)]  # Manivela
        C = [l1*np.cos(theta2) + l2*np.cos(theta3), 
             l1*np.sin(theta2) + l2*np.sin(theta3)]  # Biela
        D = [l4, 0]  # Punto fijo 2
        
        # Dibujar barras
        self.ax_mecanismo.plot([A[0], B[0]], [A[1], B[1]], 'b-', linewidth=3, label='Manivela')
        self.ax_mecanismo.plot([B[0], C[0]], [B[1], C[1]], 'r-', linewidth=3, label='Biela')
        self.ax_mecanismo.plot([C[0], D[0]], [C[1], D[1]], 'g-', linewidth=3, label='Balancín')
        self.ax_mecanismo.plot([D[0], A[0]], [D[1], A[1]], 'k-', linewidth=2, label='Base')
        
        # Dibujar puntos
        self.ax_mecanismo.plot(A[0], A[1], 'ko', markersize=8, label='A (Fijo)')
        self.ax_mecanismo.plot(B[0], B[1], 'bo', markersize=6, label='B')
        self.ax_mecanismo.plot(C[0], C[1], 'ro', markersize=6, label='C')
        self.ax_mecanismo.plot(D[0], D[1], 'ko', markersize=8, label='D (Fijo)')
        
        # Configurar gráfico
        self.ax_mecanismo.set_xlabel('X (mm)')
        self.ax_mecanismo.set_ylabel('Y (mm)')
        self.ax_mecanismo.set_title('Mecanismo de 4 Barras')
        self.ax_mecanismo.legend()
        self.ax_mecanismo.grid(True)
        self.ax_mecanismo.axis('equal')
        
        self.canvas_mecanismo.draw()
    
    def mostrar_resultados_mecanismo(self):
        """Muestra los resultados del análisis del mecanismo"""
        if not self.datos_mecanismo:
            return
            
        resultados = f"""
=== ANÁLISIS DE MECANISMO ===
Tipo: {self.datos_mecanismo['tipo']}

Dimensiones:
- Manivela (L1): {self.datos_mecanismo['l1']} mm
- Biela (L2): {self.datos_mecanismo['l2']} mm  
- Balancín (L3): {self.datos_mecanismo['l3']} mm
- Base (L4): {self.datos_mecanismo['l4']} mm

Velocidad angular: {self.datos_mecanismo['omega']} rad/s

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos de análisis de vibraciones
    def analizar_vibracion_libre(self):
        """Analiza la vibración libre del sistema"""
        try:
            # Obtener parámetros
            m = float(self.masa_var.get())
            k = float(self.rigidez_var.get())
            c = float(self.amortiguamiento_var.get())
            x0 = float(self.x0_var.get())
            v0 = float(self.v0_var.get())
            t_final = float(self.tiempo_sim_var.get())
            
            # Calcular parámetros del sistema
            wn = np.sqrt(k/m)  # Frecuencia natural
            zeta = c/(2*np.sqrt(m*k))  # Factor de amortiguamiento
            
            # Generar vector de tiempo
            t = np.linspace(0, t_final, 1000)
            
            if zeta < 1:  # Sistema subamortiguado
                wd = wn*np.sqrt(1-zeta**2)  # Frecuencia amortiguada
                A = np.sqrt(x0**2 + ((v0 + zeta*wn*x0)/wd)**2)
                phi = np.arctan2(wd*x0, v0 + zeta*wn*x0)
                
                x = A*np.exp(-zeta*wn*t)*np.cos(wd*t - phi)
                v = -A*np.exp(-zeta*wn*t)*(zeta*wn*np.cos(wd*t - phi) + wd*np.sin(wd*t - phi))
                
            elif zeta == 1:  # Sistema críticamente amortiguado
                A1 = x0
                A2 = v0 + wn*x0
                x = (A1 + A2*t)*np.exp(-wn*t)
                v = (A2 - wn*(A1 + A2*t))*np.exp(-wn*t)
                
            else:  # Sistema sobreamortiguado
                wd = wn*np.sqrt(zeta**2 - 1)
                A1 = (v0 + (zeta + np.sqrt(zeta**2 - 1))*wn*x0)/(2*wd)
                A2 = (v0 + (zeta - np.sqrt(zeta**2 - 1))*wn*x0)/(-2*wd)
                x = A1*np.exp((-zeta + np.sqrt(zeta**2 - 1))*wn*t) + A2*np.exp((-zeta - np.sqrt(zeta**2 - 1))*wn*t)
                v = A1*(-zeta + np.sqrt(zeta**2 - 1))*wn*np.exp((-zeta + np.sqrt(zeta**2 - 1))*wn*t) + \
                    A2*(-zeta - np.sqrt(zeta**2 - 1))*wn*np.exp((-zeta - np.sqrt(zeta**2 - 1))*wn*t)
            
            # Guardar resultados
            self.datos_vibracion = {
                'tipo': 'libre',
                't': t, 'x': x, 'v': v,
                'wn': wn, 'zeta': zeta,
                'm': m, 'k': k, 'c': c
            }
            
            # Visualizar resultados
            self.visualizar_vibracion()
            
            # Mostrar resultados
            self.mostrar_resultados_vibracion()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis de vibración: {str(e)}")
    
    def visualizar_vibracion(self):
        """Visualiza los resultados de vibración"""
        if not self.datos_vibracion:
            return
            
        # Limpiar gráficos
        self.ax_desplazamiento.clear()
        self.ax_velocidad.clear()
        
        # Gráfico de desplazamiento
        self.ax_desplazamiento.plot(self.datos_vibracion['t'], self.datos_vibracion['x'], 'b-', linewidth=2)
        self.ax_desplazamiento.set_xlabel('Tiempo (s)')
        self.ax_desplazamiento.set_ylabel('Desplazamiento (m)')
        self.ax_desplazamiento.set_title('Respuesta de Desplazamiento')
        self.ax_desplazamiento.grid(True)
        
        # Gráfico de velocidad
        self.ax_velocidad.plot(self.datos_vibracion['t'], self.datos_vibracion['v'], 'r-', linewidth=2)
        self.ax_velocidad.set_xlabel('Tiempo (s)')
        self.ax_velocidad.set_ylabel('Velocidad (m/s)')
        self.ax_velocidad.set_title('Respuesta de Velocidad')
        self.ax_velocidad.grid(True)
        
        self.fig_vibracion.tight_layout()
        self.canvas_vibracion.draw()
    
    def mostrar_resultados_vibracion(self):
        """Muestra los resultados del análisis de vibración"""
        if not self.datos_vibracion:
            return
            
        resultados = f"""
=== ANÁLISIS DE VIBRACIÓN LIBRE ===
Parámetros del sistema:
- Masa: {self.datos_vibracion['m']} kg
- Rigidez: {self.datos_vibracion['k']} N/m
- Amortiguamiento: {self.datos_vibracion['c']} Ns/m

Características del sistema:
- Frecuencia natural: {self.datos_vibracion['wn']:.2f} rad/s
- Factor de amortiguamiento: {self.datos_vibracion['zeta']:.3f}

Tipo de respuesta: {'Subamortiguada' if self.datos_vibracion['zeta'] < 1 else 'Críticamente amortiguada' if self.datos_vibracion['zeta'] == 1 else 'Sobreamortiguada'}

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos de balanceo
    def calcular_desbalance(self):
        """Calcula el desbalance del rotor"""
        try:
            # Obtener datos
            m_rotor = float(self.masa_rotor_var.get())
            omega = float(self.velocidad_rotor_var.get()) * 2*np.pi/60  # Convertir a rad/s
            r_rotor = float(self.radio_rotor_var.get())
            m_desb = float(self.masa_desb_var.get())
            r_desb = float(self.radio_desb_var.get())
            angulo_desb = float(self.angulo_desb_var.get()) * np.pi/180  # Convertir a rad
            
            # Calcular desbalance
            U = m_desb * r_desb  # Desbalance estático
            F_desb = U * omega**2  # Fuerza de desbalance
            
            # Calcular momento de inercia
            I = 0.5 * m_rotor * r_rotor**2
            
            # Calcular velocidad crítica
            omega_critica = np.sqrt(1e6 / m_rotor)  # Asumiendo rigidez de 1e6 N/m
            
            # Guardar resultados
            self.resultados_balanceo = {
                'U': U,
                'F_desb': F_desb,
                'omega_critica': omega_critica,
                'I': I,
                'm_rotor': m_rotor,
                'omega': omega
            }
            
            # Mostrar resultados
            self.mostrar_resultados_balanceo()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo de desbalance: {str(e)}")
    
    def mostrar_resultados_balanceo(self):
        """Muestra los resultados del balanceo"""
        if not hasattr(self, 'resultados_balanceo'):
            return
            
        resultados = f"""
=== ANÁLISIS DE BALANCEO ===
Parámetros del rotor:
- Masa del rotor: {self.resultados_balanceo['m_rotor']} kg
- Velocidad: {self.resultados_balanceo['omega']*60/(2*np.pi):.1f} rpm
- Momento de inercia: {self.resultados_balanceo['I']:.2f} kg·m²

Resultados del desbalance:
- Desbalance estático: {self.resultados_balanceo['U']:.4f} kg·m
- Fuerza de desbalance: {self.resultados_balanceo['F_desb']:.1f} N
- Velocidad crítica: {self.resultados_balanceo['omega_critica']*60/(2*np.pi):.1f} rpm

Recomendaciones:
- {'El rotor está operando cerca de su velocidad crítica. Considerar reducción de velocidad.' if abs(self.resultados_balanceo['omega'] - self.resultados_balanceo['omega_critica']) < 0.1*self.resultados_balanceo['omega_critica'] else 'El rotor opera lejos de su velocidad crítica.'}
- {'Se requiere balanceo para reducir vibraciones.' if self.resultados_balanceo['F_desb'] > 100 else 'El desbalance es aceptable.'}

Análisis completado exitosamente.
"""
        
        self.texto_balanceo.delete(1.0, tk.END)
        self.texto_balanceo.insert(tk.END, resultados)
    
    # Métodos adicionales (placeholder)
    def simular_movimiento(self):
        messagebox.showinfo("En Desarrollo", "Simulación de movimiento en desarrollo")
    
    def analizar_respuesta_forzada(self):
        messagebox.showinfo("En Desarrollo", "Análisis de respuesta forzada en desarrollo")
    
    def analisis_frecuencias(self):
        messagebox.showinfo("En Desarrollo", "Análisis de frecuencias en desarrollo")
    
    def proponer_correccion(self):
        messagebox.showinfo("En Desarrollo", "Propuesta de corrección en desarrollo")
    
    def analisis_velocidades_criticas(self):
        messagebox.showinfo("En Desarrollo", "Análisis de velocidades críticas en desarrollo")
    
    def analisis_cinematico(self):
        messagebox.showinfo("En Desarrollo", "Análisis cinemático en desarrollo")
    
    def generar_animacion(self):
        messagebox.showinfo("En Desarrollo", "Generación de animación en desarrollo")
    
    def exportar_datos_cinematica(self):
        messagebox.showinfo("En Desarrollo", "Exportación de datos en desarrollo")
    
    def generar_reporte(self):
        """Genera un reporte completo de los análisis"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_dinamica_maquinas_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE ANÁLISIS - DINÁMICA DE MÁQUINAS\n")
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
    app = DinamicaMaquinasApp()
    app.ejecutar()

if __name__ == "__main__":
    main() 