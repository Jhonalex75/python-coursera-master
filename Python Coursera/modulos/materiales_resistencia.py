# =============================================================================
# MÓDULO DE MATERIALES Y RESISTENCIA
# =============================================================================
# Propósito: Análisis de propiedades mecánicas, esfuerzos y deformaciones
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

class MaterialesResistenciaApp:
    """
    Aplicación para análisis de materiales y resistencia
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Materiales y Resistencia - Análisis Avanzado")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # Variables de datos
        self.datos_material = {}
        self.datos_esfuerzo = {}
        self.datos_fatiga = {}
        
        # Configurar interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        """Configura la interfaz principal de la aplicación"""
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_materiales()
        self.crear_pestana_esfuerzos()
        self.crear_pestana_fatiga()
        self.crear_pestana_resultados()
        
    def crear_pestana_materiales(self):
        """Crea la pestaña de propiedades de materiales"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 MATERIALES")
        
        # Frame izquierdo - Selección de material
        left_frame = ttk.LabelFrame(frame, text="SELECCIÓN DE MATERIAL", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Base de datos de materiales
        ttk.Label(left_frame, text="Material:").pack(anchor=tk.W)
        self.material_seleccionado = ttk.Combobox(left_frame, 
                                                values=["Acero AISI 1020", "Acero AISI 1045", "Aluminio 6061-T6", 
                                                       "Titanio Ti-6Al-4V", "Cobre C11000", "Personalizado"])
        self.material_seleccionado.pack(fill=tk.X, pady=(0, 10))
        self.material_seleccionado.set("Acero AISI 1020")
        self.material_seleccionado.bind('<<ComboboxSelected>>', self.cargar_propiedades_material)
        
        # Propiedades del material
        ttk.Label(left_frame, text="Propiedades Mecánicas:").pack(anchor=tk.W, pady=(10, 0))
        
        prop_frame = ttk.Frame(left_frame)
        prop_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(prop_frame, text="Módulo de Elasticidad (GPa):").grid(row=0, column=0, sticky=tk.W)
        self.E_var = tk.StringVar(value="200")
        ttk.Entry(prop_frame, textvariable=self.E_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(prop_frame, text="Módulo de Poisson:").grid(row=1, column=0, sticky=tk.W)
        self.nu_var = tk.StringVar(value="0.3")
        ttk.Entry(prop_frame, textvariable=self.nu_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(prop_frame, text="Límite de Fluencia (MPa):").grid(row=2, column=0, sticky=tk.W)
        self.Sy_var = tk.StringVar(value="250")
        ttk.Entry(prop_frame, textvariable=self.Sy_var, width=10).grid(row=2, column=1, padx=5)
        
        ttk.Label(prop_frame, text="Resistencia Última (MPa):").grid(row=3, column=0, sticky=tk.W)
        self.Su_var = tk.StringVar(value="400")
        ttk.Entry(prop_frame, textvariable=self.Su_var, width=10).grid(row=3, column=1, padx=5)
        
        ttk.Label(prop_frame, text="Densidad (kg/m³):").grid(row=4, column=0, sticky=tk.W)
        self.rho_var = tk.StringVar(value="7850")
        ttk.Entry(prop_frame, textvariable=self.rho_var, width=10).grid(row=4, column=1, padx=5)
        
        # Propiedades térmicas
        ttk.Label(left_frame, text="Propiedades Térmicas:").pack(anchor=tk.W, pady=(10, 0))
        
        term_frame = ttk.Frame(left_frame)
        term_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(term_frame, text="Coef. Expansión Térmica (1/K):").grid(row=0, column=0, sticky=tk.W)
        self.alpha_var = tk.StringVar(value="12e-6")
        ttk.Entry(term_frame, textvariable=self.alpha_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(term_frame, text="Conductividad Térmica (W/m·K):").grid(row=1, column=0, sticky=tk.W)
        self.k_thermal_var = tk.StringVar(value="50")
        ttk.Entry(term_frame, textvariable=self.k_thermal_var, width=10).grid(row=1, column=1, padx=5)
        
        # Botones de acción
        ttk.Button(left_frame, text="Analizar Material", 
                  command=self.analizar_material).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Comparar Materiales", 
                  command=self.comparar_materiales).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Guardar Material", 
                  command=self.guardar_material).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Gráfico de propiedades
        right_frame = ttk.LabelFrame(frame, text="PROPIEDADES DEL MATERIAL", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_material, self.ax_material = plt.subplots(figsize=(8, 6))
        self.canvas_material = FigureCanvasTkAgg(self.fig_material, right_frame)
        self.canvas_material.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_esfuerzos(self):
        """Crea la pestaña de análisis de esfuerzos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 ESFUERZOS")
        
        # Frame izquierdo - Parámetros de carga
        left_frame = ttk.LabelFrame(frame, text="PARÁMETROS DE CARGA", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Tipo de carga
        ttk.Label(left_frame, text="Tipo de Carga:").pack(anchor=tk.W)
        self.tipo_carga = ttk.Combobox(left_frame, 
                                     values=["Tracción", "Compresión", "Corte", "Flexión", "Torsión", "Combinada"])
        self.tipo_carga.pack(fill=tk.X, pady=(0, 10))
        self.tipo_carga.set("Tracción")
        
        # Geometría del elemento
        ttk.Label(left_frame, text="Geometría del Elemento:").pack(anchor=tk.W, pady=(10, 0))
        
        geo_frame = ttk.Frame(left_frame)
        geo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(geo_frame, text="Área transversal (mm²):").grid(row=0, column=0, sticky=tk.W)
        self.area_var = tk.StringVar(value="100")
        ttk.Entry(geo_frame, textvariable=self.area_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(geo_frame, text="Longitud (mm):").grid(row=1, column=0, sticky=tk.W)
        self.longitud_var = tk.StringVar(value="1000")
        ttk.Entry(geo_frame, textvariable=self.longitud_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(geo_frame, text="Momento de inercia (mm⁴):").grid(row=2, column=0, sticky=tk.W)
        self.I_var = tk.StringVar(value="10000")
        ttk.Entry(geo_frame, textvariable=self.I_var, width=10).grid(row=2, column=1, padx=5)
        
        # Cargas aplicadas
        ttk.Label(left_frame, text="Cargas Aplicadas:").pack(anchor=tk.W, pady=(10, 0))
        
        carga_frame = ttk.Frame(left_frame)
        carga_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(carga_frame, text="Fuerza axial (N):").grid(row=0, column=0, sticky=tk.W)
        self.F_axial_var = tk.StringVar(value="10000")
        ttk.Entry(carga_frame, textvariable=self.F_axial_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(carga_frame, text="Momento flector (N·m):").grid(row=1, column=0, sticky=tk.W)
        self.M_flexion_var = tk.StringVar(value="1000")
        ttk.Entry(carga_frame, textvariable=self.M_flexion_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(carga_frame, text="Momento torsor (N·m):").grid(row=2, column=0, sticky=tk.W)
        self.M_torsion_var = tk.StringVar(value="500")
        ttk.Entry(carga_frame, textvariable=self.M_torsion_var, width=10).grid(row=2, column=1, padx=5)
        
        # Botones de análisis
        ttk.Button(left_frame, text="Calcular Esfuerzos", 
                  command=self.calcular_esfuerzos).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Análisis de Deformación", 
                  command=self.analisis_deformacion).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Verificar Resistencia", 
                  command=self.verificar_resistencia).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Diagrama de esfuerzos
        right_frame = ttk.LabelFrame(frame, text="DIAGRAMA DE ESFUERZOS", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_esfuerzos, self.ax_esfuerzos = plt.subplots(figsize=(8, 6))
        self.canvas_esfuerzos = FigureCanvasTkAgg(self.fig_esfuerzos, right_frame)
        self.canvas_esfuerzos.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def crear_pestana_fatiga(self):
        """Crea la pestaña de análisis de fatiga"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔄 FATIGA")
        
        # Frame izquierdo - Parámetros de fatiga
        left_frame = ttk.LabelFrame(frame, text="PARÁMETROS DE FATIGA", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Propiedades de fatiga
        ttk.Label(left_frame, text="Propiedades de Fatiga:").pack(anchor=tk.W, pady=(0, 5))
        
        fatiga_frame = ttk.Frame(left_frame)
        fatiga_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fatiga_frame, text="Límite de fatiga (MPa):").grid(row=0, column=0, sticky=tk.W)
        self.Sf_var = tk.StringVar(value="200")
        ttk.Entry(fatiga_frame, textvariable=self.Sf_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(fatiga_frame, text="Esfuerzo máximo (MPa):").grid(row=1, column=0, sticky=tk.W)
        self.Smax_var = tk.StringVar(value="300")
        ttk.Entry(fatiga_frame, textvariable=self.Smax_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(fatiga_frame, text="Esfuerzo mínimo (MPa):").grid(row=2, column=0, sticky=tk.W)
        self.Smin_var = tk.StringVar(value="50")
        ttk.Entry(fatiga_frame, textvariable=self.Smin_var, width=10).grid(row=2, column=1, padx=5)
        
        ttk.Label(fatiga_frame, text="Número de ciclos:").grid(row=3, column=0, sticky=tk.W)
        self.N_ciclos_var = tk.StringVar(value="1000000")
        ttk.Entry(fatiga_frame, textvariable=self.N_ciclos_var, width=10).grid(row=3, column=1, padx=5)
        
        # Factores de corrección
        ttk.Label(left_frame, text="Factores de Corrección:").pack(anchor=tk.W, pady=(10, 0))
        
        fact_frame = ttk.Frame(left_frame)
        fact_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fact_frame, text="Factor de superficie:").grid(row=0, column=0, sticky=tk.W)
        self.ka_var = tk.StringVar(value="0.9")
        ttk.Entry(fact_frame, textvariable=self.ka_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(fact_frame, text="Factor de tamaño:").grid(row=1, column=0, sticky=tk.W)
        self.kb_var = tk.StringVar(value="0.85")
        ttk.Entry(fact_frame, textvariable=self.kb_var, width=10).grid(row=1, column=1, padx=5)
        
        ttk.Label(fact_frame, text="Factor de carga:").grid(row=2, column=0, sticky=tk.W)
        self.kc_var = tk.StringVar(value="0.9")
        ttk.Entry(fact_frame, textvariable=self.kc_var, width=10).grid(row=2, column=1, padx=5)
        
        # Botones de análisis
        ttk.Button(left_frame, text="Análisis de Fatiga", 
                  command=self.analisis_fatiga).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Curva S-N", 
                  command=self.curva_sn).pack(fill=tk.X, pady=5)
        
        ttk.Button(left_frame, text="Vida a Fatiga", 
                  command=self.vida_fatiga).pack(fill=tk.X, pady=5)
        
        # Frame derecho - Curva S-N
        right_frame = ttk.LabelFrame(frame, text="CURVA S-N", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de gráfico
        self.fig_fatiga, self.ax_fatiga = plt.subplots(figsize=(8, 6))
        self.canvas_fatiga = FigureCanvasTkAgg(self.fig_fatiga, right_frame)
        self.canvas_fatiga.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
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
    
    # Métodos de análisis de materiales
    def cargar_propiedades_material(self, event=None):
        """Carga las propiedades del material seleccionado"""
        material = self.material_seleccionado.get()
        
        # Base de datos de materiales
        materiales_db = {
            "Acero AISI 1020": {
                "E": 200, "nu": 0.3, "Sy": 250, "Su": 400, "rho": 7850,
                "alpha": 12e-6, "k_thermal": 50
            },
            "Acero AISI 1045": {
                "E": 200, "nu": 0.3, "Sy": 450, "Su": 600, "rho": 7850,
                "alpha": 12e-6, "k_thermal": 50
            },
            "Aluminio 6061-T6": {
                "E": 69, "nu": 0.33, "Sy": 240, "Su": 310, "rho": 2700,
                "alpha": 23e-6, "k_thermal": 167
            },
            "Titanio Ti-6Al-4V": {
                "E": 114, "nu": 0.34, "Sy": 825, "Su": 950, "rho": 4430,
                "alpha": 8.6e-6, "k_thermal": 7
            },
            "Cobre C11000": {
                "E": 110, "nu": 0.34, "Sy": 70, "Su": 220, "rho": 8960,
                "alpha": 17e-6, "k_thermal": 401
            }
        }
        
        if material in materiales_db:
            props = materiales_db[material]
            self.E_var.set(str(props["E"]))
            self.nu_var.set(str(props["nu"]))
            self.Sy_var.set(str(props["Sy"]))
            self.Su_var.set(str(props["Su"]))
            self.rho_var.set(str(props["rho"]))
            self.alpha_var.set(str(props["alpha"]))
            self.k_thermal_var.set(str(props["k_thermal"]))
    
    def analizar_material(self):
        """Analiza las propiedades del material"""
        try:
            # Obtener propiedades
            E = float(self.E_var.get()) * 1e9  # Convertir a Pa
            nu = float(self.nu_var.get())
            Sy = float(self.Sy_var.get()) * 1e6  # Convertir a Pa
            Su = float(self.Su_var.get()) * 1e6  # Convertir a Pa
            rho = float(self.rho_var.get())
            alpha = float(self.alpha_var.get())
            k_thermal = float(self.k_thermal_var.get())
            
            # Calcular propiedades derivadas
            G = E / (2 * (1 + nu))  # Módulo de corte
            K = E / (3 * (1 - 2*nu))  # Módulo volumétrico
            ratio_poisson = nu
            ductilidad = (Su - Sy) / Sy * 100  # Porcentaje
            
            # Guardar resultados
            self.datos_material = {
                'E': E, 'nu': nu, 'Sy': Sy, 'Su': Su, 'rho': rho,
                'G': G, 'K': K, 'ductilidad': ductilidad,
                'alpha': alpha, 'k_thermal': k_thermal
            }
            
            # Visualizar propiedades
            self.visualizar_propiedades_material()
            
            # Mostrar resultados
            self.mostrar_resultados_material()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis del material: {str(e)}")
    
    def visualizar_propiedades_material(self):
        """Visualiza las propiedades del material"""
        if not self.datos_material:
            return
            
        self.ax_material.clear()
        
        # Crear gráfico de barras con propiedades principales
        propiedades = ['E (GPa)', 'Sy (MPa)', 'Su (MPa)', 'G (GPa)']
        valores = [self.datos_material['E']/1e9, 
                  self.datos_material['Sy']/1e6,
                  self.datos_material['Su']/1e6,
                  self.datos_material['G']/1e9]
        
        bars = self.ax_material.bar(propiedades, valores, color=['blue', 'green', 'red', 'orange'])
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            self.ax_material.text(bar.get_x() + bar.get_width()/2., height,
                                f'{valor:.1f}', ha='center', va='bottom')
        
        self.ax_material.set_ylabel('Valor')
        self.ax_material.set_title('Propiedades Mecánicas del Material')
        self.ax_material.grid(True, axis='y')
        
        self.canvas_material.draw()
    
    def mostrar_resultados_material(self):
        """Muestra los resultados del análisis del material"""
        if not self.datos_material:
            return
            
        resultados = f"""
=== ANÁLISIS DE MATERIAL ===
Material: {self.material_seleccionado.get()}

Propiedades Mecánicas:
- Módulo de Elasticidad: {self.datos_material['E']/1e9:.1f} GPa
- Módulo de Poisson: {self.datos_material['nu']:.3f}
- Límite de Fluencia: {self.datos_material['Sy']/1e6:.1f} MPa
- Resistencia Última: {self.datos_material['Su']/1e6:.1f} MPa
- Módulo de Corte: {self.datos_material['G']/1e9:.1f} GPa
- Módulo Volumétrico: {self.datos_material['K']/1e9:.1f} GPa

Propiedades Físicas:
- Densidad: {self.datos_material['rho']} kg/m³
- Coef. Expansión Térmica: {self.datos_material['alpha']:.2e} 1/K
- Conductividad Térmica: {self.datos_material['k_thermal']} W/m·K

Características:
- Ductilidad: {self.datos_material['ductilidad']:.1f}%

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos de análisis de esfuerzos
    def calcular_esfuerzos(self):
        """Calcula los esfuerzos en el elemento"""
        try:
            # Obtener parámetros
            tipo = self.tipo_carga.get()
            A = float(self.area_var.get()) * 1e-6  # Convertir a m²
            L = float(self.longitud_var.get()) * 1e-3  # Convertir a m
            I = float(self.I_var.get()) * 1e-12  # Convertir a m⁴
            F_axial = float(self.F_axial_var.get())
            M_flexion = float(self.M_flexion_var.get())
            M_torsion = float(self.M_torsion_var.get())
            
            # Obtener propiedades del material
            E = float(self.E_var.get()) * 1e9
            Sy = float(self.Sy_var.get()) * 1e6
            
            # Calcular esfuerzos según el tipo de carga
            if tipo == "Tracción":
                sigma_axial = F_axial / A
                sigma_flexion = 0
                tau_torsion = 0
                
            elif tipo == "Flexión":
                sigma_axial = 0
                c = 0.01  # Distancia al eje neutro (m)
                sigma_flexion = M_flexion * c / I
                tau_torsion = 0
                
            elif tipo == "Torsión":
                sigma_axial = 0
                sigma_flexion = 0
                J = 2 * I  # Momento polar de inercia (aproximación)
                r = 0.01  # Radio (m)
                tau_torsion = M_torsion * r / J
                
            else:  # Combinada
                sigma_axial = F_axial / A
                c = 0.01
                sigma_flexion = M_flexion * c / I
                J = 2 * I
                r = 0.01
                tau_torsion = M_torsion * r / J
            
            # Esfuerzo normal total
            sigma_total = sigma_axial + sigma_flexion
            
            # Esfuerzo de von Mises (para materiales dúctiles)
            sigma_vm = np.sqrt(sigma_total**2 + 3*tau_torsion**2)
            
            # Factor de seguridad
            FS = Sy / sigma_vm if sigma_vm > 0 else float('inf')
            
            # Deformación
            epsilon = sigma_total / E
            delta_L = epsilon * L
            
            # Guardar resultados
            self.datos_esfuerzo = {
                'tipo': tipo,
                'sigma_axial': sigma_axial,
                'sigma_flexion': sigma_flexion,
                'tau_torsion': tau_torsion,
                'sigma_total': sigma_total,
                'sigma_vm': sigma_vm,
                'FS': FS,
                'epsilon': epsilon,
                'delta_L': delta_L
            }
            
            # Visualizar esfuerzos
            self.visualizar_esfuerzos()
            
            # Mostrar resultados
            self.mostrar_resultados_esfuerzos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo de esfuerzos: {str(e)}")
    
    def visualizar_esfuerzos(self):
        """Visualiza los esfuerzos calculados"""
        if not self.datos_esfuerzo:
            return
            
        self.ax_esfuerzos.clear()
        
        # Crear gráfico de barras con los esfuerzos
        esfuerzos = ['Axial', 'Flexión', 'Torsión', 'Total', 'Von Mises']
        valores = [self.datos_esfuerzo['sigma_axial']/1e6,
                  self.datos_esfuerzo['sigma_flexion']/1e6,
                  self.datos_esfuerzo['tau_torsion']/1e6,
                  self.datos_esfuerzo['sigma_total']/1e6,
                  self.datos_esfuerzo['sigma_vm']/1e6]
        
        bars = self.ax_esfuerzos.bar(esfuerzos, valores, color=['blue', 'green', 'red', 'orange', 'purple'])
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            self.ax_esfuerzos.text(bar.get_x() + bar.get_width()/2., height,
                                 f'{valor:.1f}', ha='center', va='bottom')
        
        self.ax_esfuerzos.set_ylabel('Esfuerzo (MPa)')
        self.ax_esfuerzos.set_title(f'Esfuerzos - Carga {self.datos_esfuerzo["tipo"]}')
        self.ax_esfuerzos.grid(True, axis='y')
        
        self.canvas_esfuerzos.draw()
    
    def mostrar_resultados_esfuerzos(self):
        """Muestra los resultados del análisis de esfuerzos"""
        if not self.datos_esfuerzo:
            return
            
        resultados = f"""
=== ANÁLISIS DE ESFUERZOS ===
Tipo de carga: {self.datos_esfuerzo['tipo']}

Esfuerzos calculados:
- Esfuerzo axial: {self.datos_esfuerzo['sigma_axial']/1e6:.1f} MPa
- Esfuerzo por flexión: {self.datos_esfuerzo['sigma_flexion']/1e6:.1f} MPa
- Esfuerzo cortante por torsión: {self.datos_esfuerzo['tau_torsion']/1e6:.1f} MPa
- Esfuerzo normal total: {self.datos_esfuerzo['sigma_total']/1e6:.1f} MPa
- Esfuerzo de von Mises: {self.datos_esfuerzo['sigma_vm']/1e6:.1f} MPa

Análisis de resistencia:
- Factor de seguridad: {self.datos_esfuerzo['FS']:.2f}
- Estado: {'Seguro' if self.datos_esfuerzo['FS'] > 1 else 'Crítico'}

Deformación:
- Deformación unitaria: {self.datos_esfuerzo['epsilon']:.6f}
- Deformación total: {self.datos_esfuerzo['delta_L']*1e3:.3f} mm

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos de análisis de fatiga
    def analisis_fatiga(self):
        """Realiza el análisis de fatiga"""
        try:
            # Obtener parámetros
            Sf = float(self.Sf_var.get())
            Smax = float(self.Smax_var.get())
            Smin = float(self.Smin_var.get())
            N = float(self.N_ciclos_var.get())
            ka = float(self.ka_var.get())
            kb = float(self.kb_var.get())
            kc = float(self.kc_var.get())
            
            # Calcular parámetros de fatiga
            Sm = (Smax + Smin) / 2  # Esfuerzo medio
            Sa = (Smax - Smin) / 2  # Amplitud de esfuerzo
            R = Smin / Smax  # Relación de esfuerzos
            
            # Límite de fatiga corregido
            Se = Sf * ka * kb * kc
            
            # Criterio de Goodman
            if Sa/Se + Sm/float(self.Su_var.get()) < 1:
                estado = "Seguro"
                margen = 1 - (Sa/Se + Sm/float(self.Su_var.get()))
            else:
                estado = "Crítico"
                margen = 0
            
            # Guardar resultados
            self.datos_fatiga = {
                'Sf': Sf, 'Smax': Smax, 'Smin': Smin, 'N': N,
                'Sm': Sm, 'Sa': Sa, 'R': R, 'Se': Se,
                'estado': estado, 'margen': margen
            }
            
            # Visualizar curva S-N
            self.visualizar_curva_sn()
            
            # Mostrar resultados
            self.mostrar_resultados_fatiga()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el análisis de fatiga: {str(e)}")
    
    def visualizar_curva_sn(self):
        """Visualiza la curva S-N"""
        if not self.datos_fatiga:
            return
            
        self.ax_fatiga.clear()
        
        # Generar curva S-N
        N = np.logspace(3, 7, 100)
        
        # Curva S-N simplificada (ley de Basquin)
        b = -0.1  # Exponente de fatiga
        Se = self.datos_fatiga['Se']
        Su = float(self.Su_var.get())
        
        # Para N < 10^3, usar resistencia última
        S = np.where(N < 1e3, Su, Se * (N/1e6)**b)
        
        self.ax_fatiga.loglog(N, S, 'b-', linewidth=2, label='Curva S-N')
        
        # Marcar punto de operación
        self.ax_fatiga.loglog(self.datos_fatiga['N'], self.datos_fatiga['Sa'], 'ro', 
                            markersize=8, label='Punto de operación')
        
        self.ax_fatiga.set_xlabel('Número de ciclos')
        self.ax_fatiga.set_ylabel('Amplitud de esfuerzo (MPa)')
        self.ax_fatiga.set_title('Curva S-N - Análisis de Fatiga')
        self.ax_fatiga.legend()
        self.ax_fatiga.grid(True)
        
        self.canvas_fatiga.draw()
    
    def mostrar_resultados_fatiga(self):
        """Muestra los resultados del análisis de fatiga"""
        if not self.datos_fatiga:
            return
            
        resultados = f"""
=== ANÁLISIS DE FATIGA ===
Parámetros de carga:
- Esfuerzo máximo: {self.datos_fatiga['Smax']} MPa
- Esfuerzo mínimo: {self.datos_fatiga['Smin']} MPa
- Esfuerzo medio: {self.datos_fatiga['Sm']:.1f} MPa
- Amplitud de esfuerzo: {self.datos_fatiga['Sa']:.1f} MPa
- Relación de esfuerzos: {self.datos_fatiga['R']:.3f}

Propiedades de fatiga:
- Límite de fatiga: {self.datos_fatiga['Sf']} MPa
- Límite de fatiga corregido: {self.datos_fatiga['Se']:.1f} MPa
- Número de ciclos: {self.datos_fatiga['N']:.0f}

Análisis de resistencia:
- Estado: {self.datos_fatiga['estado']}
- Margen de seguridad: {self.datos_fatiga['margen']:.3f}

Análisis completado exitosamente.
"""
        
        self.texto_resultados.insert(tk.END, resultados)
        self.texto_resultados.see(tk.END)
    
    # Métodos adicionales (placeholder)
    def comparar_materiales(self):
        messagebox.showinfo("En Desarrollo", "Comparación de materiales en desarrollo")
    
    def guardar_material(self):
        messagebox.showinfo("En Desarrollo", "Guardado de material en desarrollo")
    
    def analisis_deformacion(self):
        messagebox.showinfo("En Desarrollo", "Análisis de deformación en desarrollo")
    
    def verificar_resistencia(self):
        messagebox.showinfo("En Desarrollo", "Verificación de resistencia en desarrollo")
    
    def curva_sn(self):
        messagebox.showinfo("En Desarrollo", "Curva S-N en desarrollo")
    
    def vida_fatiga(self):
        messagebox.showinfo("En Desarrollo", "Vida a fatiga en desarrollo")
    
    def generar_reporte(self):
        """Genera un reporte completo de los análisis"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_materiales_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DE ANÁLISIS - MATERIALES Y RESISTENCIA\n")
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
    app = MaterialesResistenciaApp()
    app.ejecutar()

if __name__ == "__main__":
    main() 