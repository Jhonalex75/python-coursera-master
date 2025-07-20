# -----------------------------------------------------------------------------
# Script: from_kivy.py
# Propósito: Script para aplicaciones móviles con Kivy
# Especialidad: Desarrollo Móvil / Interfaces de Usuario
# Dependencias: kivy, numpy, matplotlib
# Uso: Importar para crear aplicaciones móviles con Kivy
# -----------------------------------------------------------------------------

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

class CalculadoraIngenieriaApp(App):
    """
    Aplicación móvil de calculadora de ingeniería
    """
    
    def build(self):
        """
        Construye la interfaz de la aplicación
        """
        # Configurar ventana
        Window.size = (400, 600)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='Calculadora de Ingeniería',
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # Selector de cálculo
        self.calculo_spinner = Spinner(
            text='Seleccionar cálculo',
            values=('Área de tubería', 'Momento flector', 'Esfuerzo normal', 'Potencia hidráulica'),
            size_hint_y=None,
            height=40
        )
        self.calculo_spinner.bind(text=self.on_calculo_select)
        main_layout.add_widget(self.calculo_spinner)
        
        # Contenedor de inputs
        self.inputs_layout = BoxLayout(orientation='vertical', spacing=5)
        main_layout.add_widget(self.inputs_layout)
        
        # Botón de cálculo
        self.calcular_btn = Button(
            text='Calcular',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.calcular_btn.bind(on_press=self.calcular)
        main_layout.add_widget(self.calcular_btn)
        
        # Resultado
        self.resultado_label = Label(
            text='Resultado aparecerá aquí',
            size_hint_y=None,
            height=100,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        main_layout.add_widget(self.resultado_label)
        
        # Gráfico
        self.grafico_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.grafico_layout)
        
        return main_layout
    
    def on_calculo_select(self, spinner, text):
        """
        Maneja la selección del tipo de cálculo
        """
        # Limpiar inputs anteriores
        self.inputs_layout.clear_widgets()
        
        if text == 'Área de tubería':
            self.crear_inputs_tuberia()
        elif text == 'Momento flector':
            self.crear_inputs_momento()
        elif text == 'Esfuerzo normal':
            self.crear_inputs_esfuerzo()
        elif text == 'Potencia hidráulica':
            self.crear_inputs_potencia()
    
    def crear_inputs_tuberia(self):
        """
        Crea inputs para cálculo de área de tubería
        """
        # Diámetro
        diametro_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        diametro_layout.add_widget(Label(text='Diámetro (m):', size_hint_x=0.5))
        self.diametro_input = TextInput(text='0.1', multiline=False, size_hint_x=0.5)
        diametro_layout.add_widget(self.diametro_input)
        self.inputs_layout.add_widget(diametro_layout)
    
    def crear_inputs_momento(self):
        """
        Crea inputs para cálculo de momento flector
        """
        # Fuerza
        fuerza_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        fuerza_layout.add_widget(Label(text='Fuerza (N):', size_hint_x=0.5))
        self.fuerza_input = TextInput(text='1000', multiline=False, size_hint_x=0.5)
        fuerza_layout.add_widget(self.fuerza_input)
        self.inputs_layout.add_widget(fuerza_layout)
        
        # Distancia
        distancia_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        distancia_layout.add_widget(Label(text='Distancia (m):', size_hint_x=0.5))
        self.distancia_input = TextInput(text='2.5', multiline=False, size_hint_x=0.5)
        distancia_layout.add_widget(self.distancia_input)
        self.inputs_layout.add_widget(distancia_layout)
    
    def crear_inputs_esfuerzo(self):
        """
        Crea inputs para cálculo de esfuerzo normal
        """
        # Fuerza
        fuerza_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        fuerza_layout.add_widget(Label(text='Fuerza (N):', size_hint_x=0.5))
        self.fuerza_esf_input = TextInput(text='5000', multiline=False, size_hint_x=0.5)
        fuerza_layout.add_widget(self.fuerza_esf_input)
        self.inputs_layout.add_widget(fuerza_layout)
        
        # Área
        area_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        area_layout.add_widget(Label(text='Área (m²):', size_hint_x=0.5))
        self.area_input = TextInput(text='0.01', multiline=False, size_hint_x=0.5)
        area_layout.add_widget(self.area_input)
        self.inputs_layout.add_widget(area_layout)
    
    def crear_inputs_potencia(self):
        """
        Crea inputs para cálculo de potencia hidráulica
        """
        # Caudal
        caudal_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        caudal_layout.add_widget(Label(text='Caudal (m³/s):', size_hint_x=0.5))
        self.caudal_input = TextInput(text='0.1', multiline=False, size_hint_x=0.5)
        caudal_layout.add_widget(self.caudal_input)
        self.inputs_layout.add_widget(caudal_layout)
        
        # Altura
        altura_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        altura_layout.add_widget(Label(text='Altura (m):', size_hint_x=0.5))
        self.altura_input = TextInput(text='10', multiline=False, size_hint_x=0.5)
        altura_layout.add_widget(self.altura_input)
        self.inputs_layout.add_widget(altura_layout)
        
        # Densidad
        densidad_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        densidad_layout.add_widget(Label(text='Densidad (kg/m³):', size_hint_x=0.5))
        self.densidad_input = TextInput(text='1000', multiline=False, size_hint_x=0.5)
        densidad_layout.add_widget(self.densidad_input)
        self.inputs_layout.add_widget(densidad_layout)
    
    def calcular(self, instance):
        """
        Realiza el cálculo seleccionado
        """
        try:
            calculo = self.calculo_spinner.text
            
            if calculo == 'Área de tubería':
                self.calcular_area_tuberia()
            elif calculo == 'Momento flector':
                self.calcular_momento_flector()
            elif calculo == 'Esfuerzo normal':
                self.calcular_esfuerzo_normal()
            elif calculo == 'Potencia hidráulica':
                self.calcular_potencia_hidraulica()
                
        except ValueError as e:
            self.mostrar_error("Error en los datos de entrada")
        except Exception as e:
            self.mostrar_error(f"Error en el cálculo: {str(e)}")
    
    def calcular_area_tuberia(self):
        """
        Calcula el área de una tubería circular
        """
        diametro = float(self.diametro_input.text)
        area = np.pi * (diametro / 2) ** 2
        
        resultado = f"Área de la tubería:\n{area:.6f} m²"
        self.resultado_label.text = resultado
        
        # Crear gráfico
        self.crear_grafico_tuberia(diametro, area)
    
    def calcular_momento_flector(self):
        """
        Calcula el momento flector
        """
        fuerza = float(self.fuerza_input.text)
        distancia = float(self.distancia_input.text)
        momento = fuerza * distancia
        
        resultado = f"Momento flector:\n{momento:.2f} N·m"
        self.resultado_label.text = resultado
        
        # Crear gráfico
        self.crear_grafico_momento(fuerza, distancia, momento)
    
    def calcular_esfuerzo_normal(self):
        """
        Calcula el esfuerzo normal
        """
        fuerza = float(self.fuerza_esf_input.text)
        area = float(self.area_input.text)
        esfuerzo = fuerza / area
        
        resultado = f"Esfuerzo normal:\n{esfuerzo:.2f} Pa"
        self.resultado_label.text = resultado
        
        # Crear gráfico
        self.crear_grafico_esfuerzo(fuerza, area, esfuerzo)
    
    def calcular_potencia_hidraulica(self):
        """
        Calcula la potencia hidráulica
        """
        caudal = float(self.caudal_input.text)
        altura = float(self.altura_input.text)
        densidad = float(self.densidad_input.text)
        g = 9.81  # Aceleración de gravedad
        
        potencia = caudal * altura * densidad * g
        
        resultado = f"Potencia hidráulica:\n{potencia:.2f} W"
        self.resultado_label.text = resultado
        
        # Crear gráfico
        self.crear_grafico_potencia(caudal, altura, potencia)
    
    def crear_grafico_tuberia(self, diametro, area):
        """
        Crea gráfico para área de tubería
        """
        self.grafico_layout.clear_widgets()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Dibujar círculo
        circle = plt.Circle((0, 0), diametro/2, fill=False, linewidth=2)
        ax.add_patch(circle)
        
        ax.set_xlim(-diametro/2 - 0.1, diametro/2 + 0.1)
        ax.set_ylim(-diametro/2 - 0.1, diametro/2 + 0.1)
        ax.set_aspect('equal')
        ax.set_title(f'Área: {area:.6f} m²')
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasKivyAgg(fig)
        self.grafico_layout.add_widget(canvas)
    
    def crear_grafico_momento(self, fuerza, distancia, momento):
        """
        Crea gráfico para momento flector
        """
        self.grafico_layout.clear_widgets()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Dibujar viga y fuerza
        x = np.linspace(0, distancia * 1.2, 100)
        y = np.zeros_like(x)
        
        ax.plot(x, y, 'k-', linewidth=3, label='Viga')
        ax.arrow(distancia, 0, 0, -fuerza/1000, head_width=0.1, head_length=0.1, 
                fc='red', ec='red', label=f'Fuerza: {fuerza} N')
        
        ax.set_xlim(-0.5, distancia * 1.5)
        ax.set_ylim(-fuerza/500, fuerza/500)
        ax.set_title(f'Momento: {momento:.2f} N·m')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasKivyAgg(fig)
        self.grafico_layout.add_widget(canvas)
    
    def crear_grafico_esfuerzo(self, fuerza, area, esfuerzo):
        """
        Crea gráfico para esfuerzo normal
        """
        self.grafico_layout.clear_widgets()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Dibujar sección
        lado = np.sqrt(area)
        rect = plt.Rectangle((-lado/2, -lado/2), lado, lado, fill=False, linewidth=2)
        ax.add_patch(rect)
        
        # Dibujar fuerza
        ax.arrow(0, lado/2 + 0.1, 0, -fuerza/1000, head_width=0.05, head_length=0.05,
                fc='red', ec='red', label=f'Fuerza: {fuerza} N')
        
        ax.set_xlim(-lado/2 - 0.1, lado/2 + 0.1)
        ax.set_ylim(-lado/2 - 0.1, lado/2 + 0.2)
        ax.set_aspect('equal')
        ax.set_title(f'Esfuerzo: {esfuerzo:.2f} Pa')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasKivyAgg(fig)
        self.grafico_layout.add_widget(canvas)
    
    def crear_grafico_potencia(self, caudal, altura, potencia):
        """
        Crea gráfico para potencia hidráulica
        """
        self.grafico_layout.clear_widgets()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Dibujar sistema hidráulico
        x = np.linspace(0, 2, 100)
        y_bomba = np.zeros_like(x)
        y_tuberia = altura * np.ones_like(x)
        
        ax.plot(x, y_bomba, 'b-', linewidth=3, label='Bomba')
        ax.plot(x, y_tuberia, 'g-', linewidth=3, label='Altura')
        ax.fill_between(x, y_bomba, y_tuberia, alpha=0.3, color='blue')
        
        ax.set_xlim(-0.1, 2.1)
        ax.set_ylim(-0.5, altura + 0.5)
        ax.set_title(f'Potencia: {potencia:.2f} W')
        ax.set_ylabel('Altura (m)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasKivyAgg(fig)
        self.grafico_layout.add_widget(canvas)
    
    def mostrar_error(self, mensaje):
        """
        Muestra un popup de error
        """
        popup = Popup(
            title='Error',
            content=Label(text=mensaje),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

def main():
    """
    Función principal para ejecutar la aplicación
    """
    CalculadoraIngenieriaApp().run()

if __name__ == '__main__':
    main()
