#!/usr/bin/env python3
"""
Script Principal para Ejecutar el Paquete GitHub-Organizado
==========================================================

Este script permite ejecutar todos los módulos del paquete de ingeniería
de manera organizada y proporciona un menú interactivo para seleccionar
qué módulo ejecutar.

Autor: Ingeniería Mecánica
Versión: 1.0
"""

import os
import sys
import subprocess
import importlib.util
from typing import Dict, List, Optional
import time


class EjecutorPaquete:
    """
    Clase para ejecutar los módulos del paquete de ingeniería
    """
    
    def __init__(self):
        self.modulos = {
            "1": {
                "nombre": "Análisis Financiero",
                "archivo": "src/analisis/Analisis.py",
                "descripcion": "Análisis de OPEX, proyecciones financieras y rentabilidad"
            },
            "2": {
                "nombre": "Gestión de Mantenimiento",
                "archivo": "src/mantenimiento/gestion_mtto.py",
                "descripcion": "Sistema de gestión de mantenimiento industrial"
            },
            "3": {
                "nombre": "Análisis Estadístico",
                "archivo": "src/estadistica/ESTADISTICA.py",
                "descripcion": "Análisis estadístico completo para ingeniería"
            },
            "4": {
                "nombre": "Análisis de Vigas (SFD/BMD)",
                "archivo": "src/ingenieria/sfd1.py",
                "descripcion": "Diagramas de fuerza cortante y momento flector"
            },
            "5": {
                "nombre": "Sistema de Graficación",
                "archivo": "src/ingenieria/Graph_durant.py",
                "descripcion": "Sistema avanzado de visualización para ingeniería"
            },
            "6": {
                "nombre": "Curvas de Bombas",
                "archivo": "src/ingenieria/CURVA_BOMBA.py",
                "descripcion": "Análisis de curvas de bombas y sistemas de flujo"
            },
            "7": {
                "nombre": "Métodos Numéricos",
                "archivo": "src/ingenieria/RUNGE_KUTTA.py",
                "descripcion": "Implementación de métodos numéricos"
            },
            "8": {
                "nombre": "Curvas de Mantenimiento",
                "archivo": "src/ingenieria/curva_mtto.py",
                "descripcion": "Análisis de curvas de mantenimiento"
            }
        }
        
        self.herramientas = {
            "setup": {
                "nombre": "Configuración del Paquete",
                "archivo": "setup.py",
                "descripcion": "Configurar entorno del paquete"
            },
            "ejemplo": {
                "nombre": "Ejemplo de Uso Completo",
                "archivo": "ejemplo_uso_completo.py",
                "descripcion": "Ejemplo integrado de todas las funcionalidades"
            }
        }
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal del paquete"""
        print("\n" + "=" * 70)
        print("           PAQUETE GITHUB-ORGANIZADO - INGENIERÍA")
        print("=" * 70)
        print("\n📚 Módulos de Ingeniería Disponibles:")
        print("-" * 50)
        
        for clave, modulo in self.modulos.items():
            print(f"{clave}. {modulo['nombre']}")
            print(f"   📁 {modulo['archivo']}")
            print(f"   📝 {modulo['descripcion']}")
            print()
        
        print("🛠️ Herramientas de Sistema:")
        print("-" * 50)
        for clave, herramienta in self.herramientas.items():
            print(f"{clave}. {herramienta['nombre']}")
            print(f"   📁 {herramienta['archivo']}")
            print(f"   📝 {herramienta['descripcion']}")
            print()
        
        print("📋 Comandos Especiales:")
        print("-" * 50)
        print("todos    - Ejecutar todos los módulos en secuencia")
        print("test     - Ejecutar tests del paquete")
        print("info     - Mostrar información del paquete")
        print("setup    - Configurar entorno del paquete")
        print("salir    - Salir del programa")
        print()
    
    def verificar_archivo(self, archivo: str) -> bool:
        """
        Verificar si un archivo existe
        
        Args:
            archivo: Ruta del archivo
            
        Returns:
            bool: True si el archivo existe
        """
        return os.path.exists(archivo)
    
    def ejecutar_modulo(self, clave: str) -> bool:
        """
        Ejecutar un módulo específico
        
        Args:
            clave: Clave del módulo a ejecutar
            
        Returns:
            bool: True si se ejecutó correctamente
        """
        if clave in self.modulos:
            modulo = self.modulos[clave]
            archivo = modulo['archivo']
            
            if not self.verificar_archivo(archivo):
                print(f"❌ Error: Archivo '{archivo}' no encontrado")
                return False
            
            print(f"\n{'='*70}")
            print(f"🚀 EJECUTANDO: {modulo['nombre']}")
            print(f"{'='*70}")
            print(f"📁 Archivo: {archivo}")
            print(f"📝 Descripción: {modulo['descripcion']}")
            print(f"{'='*70}\n")
            
            return self._ejecutar_archivo(archivo)
        
        elif clave in self.herramientas:
            herramienta = self.herramientas[clave]
            archivo = herramienta['archivo']
            
            if not self.verificar_archivo(archivo):
                print(f"❌ Error: Archivo '{archivo}' no encontrado")
                return False
            
            print(f"\n{'='*70}")
            print(f"🛠️ EJECUTANDO: {herramienta['nombre']}")
            print(f"{'='*70}")
            print(f"📁 Archivo: {archivo}")
            print(f"📝 Descripción: {herramienta['descripcion']}")
            print(f"{'='*70}\n")
            
            return self._ejecutar_archivo(archivo)
        
        else:
            print(f"❌ Error: Módulo '{clave}' no encontrado")
            return False
    
    def _ejecutar_archivo(self, archivo: str) -> bool:
        """
        Ejecutar un archivo Python específico
        
        Args:
            archivo: Ruta del archivo a ejecutar
            
        Returns:
            bool: True si se ejecutó correctamente
        """
        try:
            # Verificar dependencias
            if not self._verificar_dependencias():
                print("⚠️ Algunas dependencias pueden no estar instaladas")
                print("Ejecute 'setup' para instalar dependencias")
            
            # Ejecutar el archivo
            resultado = subprocess.run([sys.executable, archivo], 
                                     capture_output=True, 
                                     text=True, 
                                     cwd=os.getcwd())
            
            # Mostrar salida
            if resultado.stdout:
                print(resultado.stdout)
            
            if resultado.stderr:
                print("⚠️ Advertencias/Errores:")
                print(resultado.stderr)
            
            if resultado.returncode == 0:
                print(f"✅ Módulo ejecutado exitosamente")
                return True
            else:
                print(f"❌ Error al ejecutar el módulo (código: {resultado.returncode})")
                return False
                
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return False
    
    def _verificar_dependencias(self) -> bool:
        """
        Verificar si las dependencias principales están instaladas
        
        Returns:
            bool: True si las dependencias están disponibles
        """
        dependencias = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy']
        disponibles = 0
        
        for dep in dependencias:
            try:
                importlib.import_module(dep)
                disponibles += 1
            except ImportError:
                pass
        
        return disponibles >= 3  # Al menos 3 de 5 dependencias principales
    
    def ejecutar_todos_modulos(self):
        """Ejecutar todos los módulos en secuencia"""
        print("\n" + "=" * 70)
        print("🚀 EJECUTANDO TODOS LOS MÓDULOS DEL PAQUETE")
        print("=" * 70)
        
        exitos = 0
        total = len(self.modulos)
        
        for clave in self.modulos.keys():
            print(f"\n{'='*50}")
            print(f"📊 Progreso: {exitos}/{total} módulos completados")
            print(f"{'='*50}")
            
            if self.ejecutar_modulo(clave):
                exitos += 1
            
            print("\n⏳ Esperando 3 segundos antes del siguiente módulo...")
            time.sleep(3)
        
        print(f"\n{'='*70}")
        print(f"📈 RESUMEN: {exitos}/{total} módulos ejecutados exitosamente")
        print(f"{'='*70}")
        
        if exitos == total:
            print("🎉 ¡Todos los módulos se ejecutaron correctamente!")
        elif exitos >= total * 0.8:
            print("✅ La mayoría de los módulos se ejecutaron correctamente")
        else:
            print("⚠️ Algunos módulos tuvieron problemas")
    
    def ejecutar_tests(self):
        """Ejecutar tests del paquete"""
        print("\n" + "=" * 70)
        print("🧪 EJECUTANDO TESTS DEL PAQUETE")
        print("=" * 70)
        
        # Verificar si existe directorio de tests
        if not os.path.exists("tests"):
            print("❌ Directorio 'tests' no encontrado")
            return
        
        try:
            # Ejecutar tests con pytest si está disponible
            resultado = subprocess.run([sys.executable, "-m", "pytest", "tests", "-v"], 
                                     capture_output=True, text=True)
            
            if resultado.stdout:
                print(resultado.stdout)
            
            if resultado.stderr:
                print("⚠️ Advertencias:")
                print(resultado.stderr)
            
            if resultado.returncode == 0:
                print("✅ Tests ejecutados exitosamente")
            else:
                print("❌ Algunos tests fallaron")
                
        except Exception as e:
            print(f"❌ Error al ejecutar tests: {str(e)}")
            print("💡 Asegúrese de tener pytest instalado: pip install pytest")
    
    def mostrar_informacion_paquete(self):
        """Mostrar información detallada del paquete"""
        print("\n" + "=" * 70)
        print("📚 INFORMACIÓN DEL PAQUETE GITHUB-ORGANIZADO")
        print("=" * 70)
        
        print("\n🎯 Propósito del Paquete:")
        print("-" * 30)
        print("Este paquete contiene herramientas completas de ingeniería")
        print("organizadas por disciplinas y especialidades técnicas.")
        print("Diseñado para análisis, cálculos y visualizaciones profesionales.")
        
        print("\n📁 Estructura del Paquete:")
        print("-" * 30)
        print("github-organizado/")
        print("├── src/")
        print("│   ├── analisis/          - Análisis financiero y operativo")
        print("│   ├── mantenimiento/     - Gestión de mantenimiento")
        print("│   ├── estadistica/       - Análisis estadístico")
        print("│   ├── ingenieria/        - Herramientas de ingeniería")
        print("│   ├── gui/              - Interfaces gráficas")
        print("│   └── web/              - Aplicaciones web")
        print("├── tests/                - Tests unitarios")
        print("├── docs/                 - Documentación")
        print("├── data/                 - Datos de ejemplo")
        print("└── assets/               - Recursos multimedia")
        
        print("\n🔧 Módulos Principales:")
        print("-" * 30)
        for clave, modulo in self.modulos.items():
            print(f"• {modulo['nombre']}: {modulo['descripcion']}")
        
        print("\n📦 Dependencias Principales:")
        print("-" * 30)
        dependencias = [
            "pandas - Análisis de datos",
            "numpy - Cálculos numéricos",
            "matplotlib - Visualizaciones",
            "seaborn - Gráficos estadísticos",
            "scipy - Funciones científicas",
            "plotly - Gráficos interactivos",
            "streamlit - Aplicaciones web"
        ]
        for dep in dependencias:
            print(f"• {dep}")
        
        print("\n🚀 Cómo Usar:")
        print("-" * 30)
        print("1. Ejecute 'setup' para configurar el entorno")
        print("2. Seleccione un módulo específico (1-8)")
        print("3. Ejecute 'todos' para probar todos los módulos")
        print("4. Use 'ejemplo' para ver un caso de uso completo")
        
        print("\n📋 Archivos Importantes:")
        print("-" * 30)
        archivos_importantes = [
            "setup.py - Configuración del paquete",
            "requirements.txt - Dependencias",
            "README.md - Documentación principal",
            "ejemplo_uso_completo.py - Ejemplo integrado"
        ]
        for archivo in archivos_importantes:
            print(f"• {archivo}")
    
    def ejecutar_comando_especial(self, comando: str) -> bool:
        """
        Ejecutar comandos especiales
        
        Args:
            comando: Comando a ejecutar
            
        Returns:
            bool: True si el comando se ejecutó correctamente
        """
        if comando.lower() == "todos":
            self.ejecutar_todos_modulos()
            return True
        
        elif comando.lower() in ["test", "tests"]:
            self.ejecutar_tests()
            return True
        
        elif comando.lower() == "setup":
            return self.ejecutar_modulo("setup")
        
        elif comando.lower() == "info":
            self.mostrar_informacion_paquete()
            return True
        
        elif comando.lower() in ["salir", "exit", "quit"]:
            print("\n👋 ¡Gracias por usar el Paquete GitHub-Organizado!")
            print("¡Esperamos que las herramientas de ingeniería sean útiles!")
            sys.exit(0)
        
        else:
            print(f"❌ Comando '{comando}' no reconocido")
            return False
    
    def ejecutar_interactivo(self):
        """Ejecutar el paquete en modo interactivo"""
        print("🔧 Bienvenido al Paquete GitHub-Organizado de Ingeniería")
        print("Ejecutando en modo interactivo...")
        
        while True:
            try:
                self.mostrar_menu_principal()
                
                # Obtener entrada del usuario
                entrada = input("Selecciona un módulo o comando: ").strip()
                
                if not entrada:
                    continue
                
                # Ejecutar módulo o comando
                if entrada in self.modulos or entrada in self.herramientas:
                    self.ejecutar_modulo(entrada)
                else:
                    self.ejecutar_comando_especial(entrada)
                
                print("\n⏳ Presiona Enter para continuar...")
                input()
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error inesperado: {str(e)}")
                print("Continuando...")


def main():
    """Función principal"""
    ejecutor = EjecutorPaquete()
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando in ejecutor.modulos or comando in ejecutor.herramientas:
            ejecutor.ejecutar_modulo(comando)
        else:
            ejecutor.ejecutar_comando_especial(comando)
    else:
        # Modo interactivo
        ejecutor.ejecutar_interactivo()


if __name__ == "__main__":
    main() 