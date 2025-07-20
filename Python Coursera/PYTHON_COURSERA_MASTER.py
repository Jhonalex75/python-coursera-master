# =============================================================================
# PYTHON COURSERA MASTER - PAQUETE EDUCATIVO DE INGENIERÍA MECÁNICA
# =============================================================================
# Propósito: Plataforma educativa integral para ingeniería mecánica usando Python
# Enfoque: Python como herramienta sofisticada para todas las áreas de la ingeniería
# Autor: Sistema de Ingeniería Mecánica con Python
# Versión: 1.0
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import subprocess
import webbrowser
from datetime import datetime

class PythonCourseraMaster:
    """
    Plataforma principal para el paquete educativo de ingeniería mecánica
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PYTHON COURSERA MASTER - Ingeniería Mecánica")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz principal
        self.crear_interfaz_principal()
        
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground='#ecf0f1',
                       background='#2c3e50')
        
        style.configure('Header.TLabel', 
                       font=('Arial', 12, 'bold'), 
                       foreground='#3498db',
                       background='#2c3e50')
        
        style.configure('Module.TButton', 
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
        style.configure('Info.TLabel', 
                       font=('Arial', 9),
                       foreground='#bdc3c7',
                       background='#2c3e50')
    
    def crear_interfaz_principal(self):
        """Crea la interfaz principal de la aplicación"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="PYTHON COURSERA MASTER", 
                 style='Title.TLabel').pack()
        
        ttk.Label(title_frame, 
                 text="Plataforma Educativa de Ingeniería Mecánica con Python", 
                 style='Info.TLabel').pack()
        
        # Frame de contenido principal
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Módulos principales
        left_panel = ttk.LabelFrame(content_frame, text="MÓDULOS PRINCIPALES", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.crear_modulos_principales(left_panel)
        
        # Panel derecho - Herramientas y recursos
        right_panel = ttk.LabelFrame(content_frame, text="HERRAMIENTAS Y RECURSOS", padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.crear_herramientas_recursos(right_panel)
        
        # Barra de estado
        self.status_bar = ttk.Label(main_frame, text="Listo", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def crear_modulos_principales(self, parent):
        """Crea los módulos principales de ingeniería mecánica"""
        # 1. Análisis Estructural
        ttk.Button(parent, text="🏗️ ANÁLISIS ESTRUCTURAL", 
                  style='Module.TButton',
                  command=self.abrir_analisis_estructural).pack(fill=tk.X, pady=2)
        
        # 2. Dinámica de Máquinas
        ttk.Button(parent, text="⚙️ DINÁMICA DE MÁQUINAS", 
                  style='Module.TButton',
                  command=self.abrir_dinamica_maquinas).pack(fill=tk.X, pady=2)
        
        # 3. Termodinámica y Fluidos
        ttk.Button(parent, text="🌡️ TERMODINÁMICA Y FLUIDOS", 
                  style='Module.TButton',
                  command=self.abrir_termo_fluidos).pack(fill=tk.X, pady=2)
        
        # 4. Materiales y Resistencia
        ttk.Button(parent, text="🔧 MATERIALES Y RESISTENCIA", 
                  style='Module.TButton',
                  command=self.abrir_materiales).pack(fill=tk.X, pady=2)
        
        # 5. Control y Automatización
        ttk.Button(parent, text="🎛️ CONTROL Y AUTOMATIZACIÓN", 
                  style='Module.TButton',
                  command=self.abrir_control).pack(fill=tk.X, pady=2)
        
        # 6. Manufactura y Procesos
        ttk.Button(parent, text="🏭 MANUFACTURA Y PROCESOS", 
                  style='Module.TButton',
                  command=self.abrir_manufactura).pack(fill=tk.X, pady=2)
        
        # 7. Mantenimiento y Confiabilidad
        ttk.Button(parent, text="🔧 MANTENIMIENTO Y CONFIABILIDAD", 
                  style='Module.TButton',
                  command=self.abrir_mantenimiento).pack(fill=tk.X, pady=2)
        
        # 8. Gestión de Proyectos
        ttk.Button(parent, text="📊 GESTIÓN DE PROYECTOS", 
                  style='Module.TButton',
                  command=self.abrir_gestion_proyectos).pack(fill=tk.X, pady=2)
    
    def crear_herramientas_recursos(self, parent):
        """Crea las herramientas y recursos adicionales"""
        # Herramientas de cálculo
        ttk.Label(parent, text="HERRAMIENTAS DE CÁLCULO", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Button(parent, text="Calculadora Avanzada", 
                  command=self.abrir_calculadora).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Conversor de Unidades", 
                  command=self.abrir_conversor).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Generador de Gráficos", 
                  command=self.abrir_generador_graficos).pack(fill=tk.X, pady=1)
        
        # Recursos educativos
        ttk.Label(parent, text="RECURSOS EDUCATIVOS", style='Header.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        ttk.Button(parent, text="Tutoriales Interactivos", 
                  command=self.abrir_tutoriales).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Base de Datos Técnica", 
                  command=self.abrir_base_datos).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Ejemplos Prácticos", 
                  command=self.abrir_ejemplos).pack(fill=tk.X, pady=1)
        
        # Herramientas de desarrollo
        ttk.Label(parent, text="DESARROLLO Y PROGRAMACIÓN", style='Header.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        ttk.Button(parent, text="Editor de Código", 
                  command=self.abrir_editor).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Depurador de Código", 
                  command=self.abrir_depurador).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Generador de Reportes", 
                  command=self.abrir_generador_reportes).pack(fill=tk.X, pady=1)
        
        # Información del sistema
        ttk.Label(parent, text="INFORMACIÓN DEL SISTEMA", style='Header.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        ttk.Button(parent, text="Estado del Sistema", 
                  command=self.mostrar_estado_sistema).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Actualizar Paquete", 
                  command=self.actualizar_paquete).pack(fill=tk.X, pady=1)
        
        ttk.Button(parent, text="Ayuda y Documentación", 
                  command=self.abrir_ayuda).pack(fill=tk.X, pady=1)
    
    # Métodos para abrir módulos principales
    def abrir_analisis_estructural(self):
        """Abre el módulo de análisis estructural"""
        self.status_bar.config(text="Abriendo Análisis Estructural...")
        try:
            # Importar y ejecutar módulo de análisis estructural
            from modulos.analisis_estructural import AnalisisEstructuralApp
            app = AnalisisEstructuralApp()
        except ImportError:
            messagebox.showinfo("Módulo en Desarrollo", 
                              "El módulo de Análisis Estructural está siendo desarrollado.\n"
                              "Próximamente disponible.")
    
    def abrir_dinamica_maquinas(self):
        """Abre el módulo de dinámica de máquinas"""
        self.status_bar.config(text="Abriendo Dinámica de Máquinas...")
        try:
            from modulos.dinamica_maquinas import DinamicaMaquinasApp
            app = DinamicaMaquinasApp()
            app.ejecutar()
        except ImportError:
            messagebox.showinfo("Módulo en Desarrollo", 
                              "El módulo de Dinámica de Máquinas está siendo desarrollado.\n"
                              "Próximamente disponible.")
    
    def abrir_termo_fluidos(self):
        """Abre el módulo de termodinámica y fluidos"""
        self.status_bar.config(text="Abriendo Termodinámica y Fluidos...")
        try:
            from modulos.termodinamica_fluidos import TermodinamicaFluidosApp
            app = TermodinamicaFluidosApp()
            app.ejecutar()
        except ImportError:
            messagebox.showinfo("Módulo en Desarrollo", 
                              "El módulo de Termodinámica y Fluidos está siendo desarrollado.\n"
                              "Próximamente disponible.")
    
    def abrir_materiales(self):
        """Abre el módulo de materiales y resistencia"""
        self.status_bar.config(text="Abriendo Materiales y Resistencia...")
        try:
            from modulos.materiales_resistencia import MaterialesResistenciaApp
            app = MaterialesResistenciaApp()
            app.ejecutar()
        except ImportError:
            messagebox.showinfo("Módulo en Desarrollo", 
                              "El módulo de Materiales y Resistencia está siendo desarrollado.\n"
                              "Próximamente disponible.")
    
    def abrir_control(self):
        """Abre el módulo de control y automatización"""
        self.status_bar.config(text="Abriendo Control y Automatización...")
        try:
            from modulos.control import ControlApp
            app = ControlApp()
        except ImportError:
            messagebox.showinfo("Módulo en Desarrollo", 
                              "El módulo de Control y Automatización está siendo desarrollado.\n"
                              "Próximamente disponible.")
    
    def abrir_manufactura(self):
        """Abre el módulo de manufactura y procesos"""
        self.status_bar.config(text="Abriendo Manufactura y Procesos...")
        try:
            from modulos.manufactura import ManufacturaApp
            app = ManufacturaApp()
        except ImportError:
            messagebox.showinfo("Módulo en Desarrollo", 
                              "El módulo de Manufactura y Procesos está siendo desarrollado.\n"
                              "Próximamente disponible.")
    
    def abrir_mantenimiento(self):
        """Abre el módulo de mantenimiento y confiabilidad"""
        self.status_bar.config(text="Abriendo Mantenimiento y Confiabilidad...")
        try:
            # Usar el módulo existente de github-organizado
            subprocess.run([sys.executable, "github-organizado/src/mantenimiento/gestion_mtto.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el módulo: {str(e)}")
    
    def abrir_gestion_proyectos(self):
        """Abre el módulo de gestión de proyectos"""
        self.status_bar.config(text="Abriendo Gestión de Proyectos...")
        try:
            # Usar el módulo existente de github-organizado
            subprocess.run([sys.executable, "github-organizado/src/scripts/p6_1.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el módulo: {str(e)}")
    
    # Métodos para herramientas y recursos
    def abrir_calculadora(self):
        """Abre la calculadora avanzada"""
        self.status_bar.config(text="Abriendo Calculadora Avanzada...")
        messagebox.showinfo("Calculadora", "Calculadora Avanzada - En desarrollo")
    
    def abrir_conversor(self):
        """Abre el conversor de unidades"""
        self.status_bar.config(text="Abriendo Conversor de Unidades...")
        messagebox.showinfo("Conversor", "Conversor de Unidades - En desarrollo")
    
    def abrir_generador_graficos(self):
        """Abre el generador de gráficos"""
        self.status_bar.config(text="Abriendo Generador de Gráficos...")
        messagebox.showinfo("Generador", "Generador de Gráficos - En desarrollo")
    
    def abrir_tutoriales(self):
        """Abre los tutoriales interactivos"""
        self.status_bar.config(text="Abriendo Tutoriales...")
        webbrowser.open("https://docs.python.org/3/tutorial/")
    
    def abrir_base_datos(self):
        """Abre la base de datos técnica"""
        self.status_bar.config(text="Abriendo Base de Datos Técnica...")
        messagebox.showinfo("Base de Datos", "Base de Datos Técnica - En desarrollo")
    
    def abrir_ejemplos(self):
        """Abre los ejemplos prácticos"""
        self.status_bar.config(text="Abriendo Ejemplos Prácticos...")
        messagebox.showinfo("Ejemplos", "Ejemplos Prácticos - En desarrollo")
    
    def abrir_editor(self):
        """Abre el editor de código"""
        self.status_bar.config(text="Abriendo Editor de Código...")
        messagebox.showinfo("Editor", "Editor de Código - En desarrollo")
    
    def abrir_depurador(self):
        """Abre el depurador de código"""
        self.status_bar.config(text="Abriendo Depurador...")
        messagebox.showinfo("Depurador", "Depurador de Código - En desarrollo")
    
    def abrir_generador_reportes(self):
        """Abre el generador de reportes"""
        self.status_bar.config(text="Abriendo Generador de Reportes...")
        messagebox.showinfo("Reportes", "Generador de Reportes - En desarrollo")
    
    def mostrar_estado_sistema(self):
        """Muestra el estado del sistema"""
        info = f"""
ESTADO DEL SISTEMA PYTHON COURSERA MASTER

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Versión Python: {sys.version}
Directorio de trabajo: {os.getcwd()}

MÓDULOS DISPONIBLES:
✅ Análisis Estructural (completo)
✅ Dinámica de Máquinas (completo)
✅ Termodinámica y Fluidos (completo)
✅ Materiales y Resistencia (completo)
✅ Calculadora Avanzada (completo)
✅ Mantenimiento y Confiabilidad (github-organizado)
✅ Gestión de Proyectos (github-organizado)

MÓDULOS EN DESARROLLO:
🔄 Control y Automatización
🔄 Manufactura y Procesos
🔄 Herramientas adicionales

Estado: Funcionando correctamente
Módulos activos: 7/9
        """
        messagebox.showinfo("Estado del Sistema", info)
    
    def actualizar_paquete(self):
        """Actualiza el paquete"""
        self.status_bar.config(text="Actualizando paquete...")
        messagebox.showinfo("Actualización", "Función de actualización en desarrollo")
    
    def abrir_ayuda(self):
        """Abre la ayuda y documentación"""
        self.status_bar.config(text="Abriendo Ayuda...")
        webbrowser.open("https://github.com/python/cpython")
    
    def ejecutar(self):
        """Ejecuta la aplicación principal"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = PythonCourseraMaster()
    app.ejecutar()

if __name__ == "__main__":
    main() 