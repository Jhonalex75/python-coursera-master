# =============================================================================
# CALCULADORA AVANZADA PARA INGENIERÍA MECÁNICA
# =============================================================================
# Propósito: Calculadora especializada con funciones de ingeniería
# Incluye: Conversiones, fórmulas, constantes físicas
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np

class CalculadoraAvanzada:
    """
    Calculadora avanzada para ingeniería mecánica
    """
    
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("Calculadora Avanzada - Ingeniería Mecánica")
        self.root.geometry("800x600")
        
        # Constantes físicas
        self.constantes = {
            'g': 9.81,  # m/s²
            'pi': math.pi,
            'e': math.e,
            'c': 299792458,  # m/s
            'R': 8.314,  # J/(mol·K)
            'k': 1.380649e-23,  # J/K
            'h': 6.62607015e-34,  # J·s
            'G': 6.67430e-11,  # m³/(kg·s²)
        }
        
        # Configurar interfaz
        self.configurar_interfaz()
        
    def configurar_interfaz(self):
        """Configura la interfaz de la calculadora"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Calculadora básica
        self.crear_pestana_basica()
        
        # Pestaña 2: Conversiones
        self.crear_pestana_conversiones()
        
        # Pestaña 3: Fórmulas de ingeniería
        self.crear_pestana_formulas()
        
        # Pestaña 4: Constantes físicas
        self.crear_pestana_constantes()
        
    def crear_pestana_basica(self):
        """Crea la pestaña de calculadora básica"""
        frame_basica = ttk.Frame(self.notebook)
        self.notebook.add(frame_basica, text="Calculadora Básica")
        
        # Display
        self.display = tk.Entry(frame_basica, font=('Arial', 20), justify='right')
        self.display.pack(fill=tk.X, padx=10, pady=10)
        
        # Frame para botones
        botones_frame = ttk.Frame(frame_basica)
        botones_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de la calculadora
        botones = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C', 'CE', '(', ')'],
            ['sin', 'cos', 'tan', 'log'],
            ['exp', 'sqrt', 'x²', 'x³'],
            ['π', 'e', 'g', 'R']
        ]
        
        for i, fila in enumerate(botones):
            for j, texto in enumerate(fila):
                btn = tk.Button(botones_frame, text=texto, font=('Arial', 12),
                              command=lambda t=texto: self.boton_presionado(t))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
        
        # Configurar grid
        for i in range(8):
            botones_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            botones_frame.grid_columnconfigure(j, weight=1)
    
    def crear_pestana_conversiones(self):
        """Crea la pestaña de conversiones"""
        frame_conv = ttk.Frame(self.notebook)
        self.notebook.add(frame_conv, text="Conversiones")
        
        # Tipos de conversión
        tipos_conversion = [
            "Longitud",
            "Área", 
            "Volumen",
            "Masa",
            "Fuerza",
            "Presión",
            "Energía",
            "Potencia",
            "Temperatura",
            "Velocidad"
        ]
        
        # Selector de tipo
        ttk.Label(frame_conv, text="Tipo de Conversión:").pack(pady=5)
        self.tipo_conv = ttk.Combobox(frame_conv, values=tipos_conversion, state="readonly")
        self.tipo_conv.pack(pady=5)
        self.tipo_conv.bind('<<ComboboxSelected>>', self.actualizar_conversiones)
        
        # Frame para conversiones
        self.frame_conv = ttk.Frame(frame_conv)
        self.frame_conv.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def crear_pestana_formulas(self):
        """Crea la pestaña de fórmulas de ingeniería"""
        frame_form = ttk.Frame(self.notebook)
        self.notebook.add(frame_form, text="Fórmulas")
        
        # Lista de fórmulas
        formulas = [
            "F = m·a (Segunda Ley de Newton)",
            "E = m·c² (Energía relativista)",
            "P = F/A (Presión)",
            "τ = F·r (Torque)",
            "I = m·r² (Momento de inercia)",
            "ω = 2π·f (Velocidad angular)",
            "v = ω·r (Velocidad tangencial)",
            "a = v²/r (Aceleración centrípeta)",
            "F = k·x (Ley de Hooke)",
            "E = ½·k·x² (Energía elástica)",
            "P = m·g·h (Energía potencial)",
            "K = ½·m·v² (Energía cinética)",
            "Q = m·c·ΔT (Calor sensible)",
            "P = V·I (Potencia eléctrica)",
            "R = ρ·L/A (Resistencia eléctrica)"
        ]
        
        # Listbox para fórmulas
        ttk.Label(frame_form, text="Fórmulas de Ingeniería:").pack(pady=5)
        self.lista_formulas = tk.Listbox(frame_form, height=15)
        self.lista_formulas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for formula in formulas:
            self.lista_formulas.insert(tk.END, formula)
        
        # Botón para calcular
        ttk.Button(frame_form, text="Calcular Fórmula Seleccionada", 
                  command=self.calcular_formula).pack(pady=10)
        
    def crear_pestana_constantes(self):
        """Crea la pestaña de constantes físicas"""
        frame_const = ttk.Frame(self.notebook)
        self.notebook.add(frame_const, text="Constantes")
        
        # Mostrar constantes
        ttk.Label(frame_const, text="Constantes Físicas:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        for nombre, valor in self.constantes.items():
            frame_constante = ttk.Frame(frame_const)
            frame_constante.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Label(frame_constante, text=f"{nombre} = {valor:.6e}", 
                     font=('Courier', 10)).pack(side=tk.LEFT)
            
            ttk.Button(frame_constante, text="Copiar", 
                      command=lambda v=valor: self.copiar_constante(v)).pack(side=tk.RIGHT)
    
    def boton_presionado(self, texto):
        """Maneja los botones presionados"""
        if texto == '=':
            try:
                resultado = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Expresión inválida")
        elif texto == 'C':
            self.display.delete(0, tk.END)
        elif texto == 'CE':
            self.display.delete(0, tk.END)
        elif texto == 'sin':
            try:
                valor = float(self.display.get())
                resultado = math.sin(math.radians(valor))
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'cos':
            try:
                valor = float(self.display.get())
                resultado = math.cos(math.radians(valor))
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'tan':
            try:
                valor = float(self.display.get())
                resultado = math.tan(math.radians(valor))
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'log':
            try:
                valor = float(self.display.get())
                resultado = math.log10(valor)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'exp':
            try:
                valor = float(self.display.get())
                resultado = math.exp(valor)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'sqrt':
            try:
                valor = float(self.display.get())
                resultado = math.sqrt(valor)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'x²':
            try:
                valor = float(self.display.get())
                resultado = valor ** 2
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'x³':
            try:
                valor = float(self.display.get())
                resultado = valor ** 3
                self.display.delete(0, tk.END)
                self.display.insert(0, str(resultado))
            except:
                messagebox.showerror("Error", "Valor inválido")
        elif texto == 'π':
            self.display.insert(tk.END, str(math.pi))
        elif texto == 'e':
            self.display.insert(tk.END, str(math.e))
        elif texto == 'g':
            self.display.insert(tk.END, str(self.constantes['g']))
        elif texto == 'R':
            self.display.insert(tk.END, str(self.constantes['R']))
        else:
            self.display.insert(tk.END, texto)
    
    def actualizar_conversiones(self, event=None):
        """Actualiza las opciones de conversión según el tipo seleccionado"""
        # Limpiar frame de conversiones
        for widget in self.frame_conv.winfo_children():
            widget.destroy()
        
        tipo = self.tipo_conv.get()
        
        if tipo == "Longitud":
            unidades = ["metros", "centímetros", "milímetros", "kilómetros", "pulgadas", "pies", "yardas", "millas"]
        elif tipo == "Área":
            unidades = ["m²", "cm²", "mm²", "km²", "pulgadas²", "pies²", "yardas²", "acres"]
        elif tipo == "Volumen":
            unidades = ["m³", "cm³", "mm³", "litros", "galones", "pulgadas³", "pies³"]
        elif tipo == "Masa":
            unidades = ["kg", "g", "mg", "toneladas", "libras", "onzas"]
        elif tipo == "Fuerza":
            unidades = ["N", "kN", "lbf", "kgf", "dyn"]
        elif tipo == "Presión":
            unidades = ["Pa", "kPa", "MPa", "bar", "atm", "psi", "mmHg"]
        elif tipo == "Energía":
            unidades = ["J", "kJ", "cal", "kcal", "BTU", "kWh", "eV"]
        elif tipo == "Potencia":
            unidades = ["W", "kW", "HP", "BTU/h", "cal/s"]
        elif tipo == "Temperatura":
            unidades = ["°C", "°F", "K", "°R"]
        elif tipo == "Velocidad":
            unidades = ["m/s", "km/h", "mph", "nudos", "ft/s"]
        else:
            unidades = []
        
        if unidades:
            # Crear entradas para conversión
            ttk.Label(self.frame_conv, text=f"Conversión de {tipo}").pack(pady=5)
            
            # Entrada de valor
            ttk.Label(self.frame_conv, text="Valor:").pack()
            self.valor_entrada = ttk.Entry(self.frame_conv)
            self.valor_entrada.pack(pady=5)
            
            # Unidad origen
            ttk.Label(self.frame_conv, text="De:").pack()
            self.unidad_origen = ttk.Combobox(self.frame_conv, values=unidades, state="readonly")
            self.unidad_origen.pack(pady=5)
            
            # Unidad destino
            ttk.Label(self.frame_conv, text="A:").pack()
            self.unidad_destino = ttk.Combobox(self.frame_conv, values=unidades, state="readonly")
            self.unidad_destino.pack(pady=5)
            
            # Botón convertir
            ttk.Button(self.frame_conv, text="Convertir", 
                      command=self.realizar_conversion).pack(pady=10)
            
            # Resultado
            self.resultado_conversion = ttk.Label(self.frame_conv, text="")
            self.resultado_conversion.pack(pady=10)
    
    def realizar_conversion(self):
        """Realiza la conversión de unidades"""
        try:
            valor = float(self.valor_entrada.get())
            origen = self.unidad_origen.get()
            destino = self.unidad_destino.get()
            
            # Factor de conversión (simplificado)
            factor = 1.0  # Aquí se implementarían las conversiones específicas
            
            resultado = valor * factor
            self.resultado_conversion.config(text=f"Resultado: {resultado:.6f} {destino}")
            
        except ValueError:
            messagebox.showerror("Error", "Valor inválido")
    
    def calcular_formula(self):
        """Calcula la fórmula seleccionada"""
        try:
            seleccion = self.lista_formulas.curselection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione una fórmula")
                return
            
            formula = self.lista_formulas.get(seleccion[0])
            messagebox.showinfo("Fórmula", f"Fórmula seleccionada: {formula}\n\nImplementación en desarrollo")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular: {str(e)}")
    
    def copiar_constante(self, valor):
        """Copia una constante al portapapeles"""
        self.root.clipboard_clear()
        self.root.clipboard_append(str(valor))
        messagebox.showinfo("Copiado", f"Constante copiada: {valor}")

def main():
    """Función principal"""
    app = CalculadoraAvanzada()
    app.root.mainloop()

if __name__ == "__main__":
    main() 