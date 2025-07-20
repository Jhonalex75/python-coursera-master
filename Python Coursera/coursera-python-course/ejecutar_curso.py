#!/usr/bin/env python3
"""
Script Principal para Ejecutar el Curso de Python de Coursera
============================================================

Este script permite ejecutar todos los módulos del curso de manera organizada.
Proporciona un menú interactivo para seleccionar qué módulo ejecutar.

Autor: Curso Python Coursera
Versión: 1.0
"""

import os
import sys
import subprocess
import importlib.util
from typing import Dict, List, Optional


class EjecutorCurso:
    """
    Clase para ejecutar los módulos del curso de manera organizada
    """
    
    def __init__(self):
        self.modulos = {
            "1": {
                "nombre": "Fundamentos de Python",
                "archivo": "modulo_1_fundamentos/variables_tipos.py",
                "descripcion": "Variables, tipos de datos, operaciones básicas"
            },
            "2": {
                "nombre": "Control de Flujo",
                "archivo": "modulo_2_control_flujo/condicionales.py",
                "descripcion": "Condicionales, bucles, estructuras de control"
            },
            "3": {
                "nombre": "Ordenamiento y Manejo de Errores",
                "archivo": "modulo_3_ordenamiento_errores/ordenamiento_errores.py",
                "descripcion": "Algoritmos de ordenamiento, excepciones, validación"
            },
            "4": {
                "nombre": "Control de Versiones con Git",
                "archivo": "modulo_4_control_versiones/git_basico.py",
                "descripcion": "Git básico, comandos, flujo de trabajo"
            },
            "5": {
                "nombre": "Testing con pytest",
                "archivo": "modulo_5_testing/testing_pytest.py",
                "descripcion": "Tests unitarios, fixtures, parametrización"
            },
            "6": {
                "nombre": "Manejo de Errores Avanzado",
                "archivo": "modulo_6_manejo_errores/debugging.py",
                "descripcion": "Debugging avanzado, logging, assertions"
            }
        }
        
        self.herramientas = {
            "debug": {
                "nombre": "Kit de Debugging",
                "archivo": "herramientas_utilidad/debugging_toolkit.py",
                "descripcion": "Herramientas avanzadas de debugging"
            },
            "setup": {
                "nombre": "Configuración del Curso",
                "archivo": "setup_coursera.py",
                "descripcion": "Configurar entorno del curso"
            }
        }
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal del curso"""
        print("\n" + "=" * 60)
        print("           CURSO DE PYTHON - COURSERA")
        print("=" * 60)
        print("\nMódulos disponibles:")
        print("-" * 40)
        
        for clave, modulo in self.modulos.items():
            print(f"{clave}. {modulo['nombre']}")
            print(f"   {modulo['descripcion']}")
            print()
        
        print("Herramientas:")
        print("-" * 40)
        for clave, herramienta in self.herramientas.items():
            print(f"{clave}. {herramienta['nombre']}")
            print(f"   {herramienta['descripcion']}")
            print()
        
        print("Comandos especiales:")
        print("-" * 40)
        print("todos    - Ejecutar todos los módulos en secuencia")
        print("tests    - Ejecutar tests del módulo 5")
        print("setup    - Configurar entorno del curso")
        print("info     - Mostrar información del curso")
        print("salir    - Salir del programa")
        print()
    
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
            
            print(f"\n{'='*60}")
            print(f"EJECUTANDO: {modulo['nombre']}")
            print(f"{'='*60}")
            print(f"Archivo: {archivo}")
            print(f"Descripción: {modulo['descripcion']}")
            print(f"{'='*60}\n")
            
            return self._ejecutar_archivo(archivo)
        
        elif clave in self.herramientas:
            herramienta = self.herramientas[clave]
            archivo = herramienta['archivo']
            
            print(f"\n{'='*60}")
            print(f"EJECUTANDO: {herramienta['nombre']}")
            print(f"{'='*60}")
            print(f"Archivo: {archivo}")
            print(f"Descripción: {herramienta['descripcion']}")
            print(f"{'='*60}\n")
            
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
            if not os.path.exists(archivo):
                print(f"❌ Error: Archivo '{archivo}' no encontrado")
                return False
            
            # Ejecutar el archivo
            resultado = subprocess.run([sys.executable, archivo], 
                                     capture_output=True, 
                                     text=True, 
                                     cwd=os.getcwd())
            
            # Mostrar salida
            if resultado.stdout:
                print(resultado.stdout)
            
            if resultado.stderr:
                print("⚠️  Advertencias/Errores:")
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
    
    def ejecutar_todos_modulos(self):
        """Ejecutar todos los módulos en secuencia"""
        print("\n" + "=" * 60)
        print("EJECUTANDO TODOS LOS MÓDULOS")
        print("=" * 60)
        
        exitos = 0
        total = len(self.modulos)
        
        for clave in self.modulos.keys():
            print(f"\n{'='*40}")
            print(f"Progreso: {exitos}/{total} módulos completados")
            print(f"{'='*40}")
            
            if self.ejecutar_modulo(clave):
                exitos += 1
            
            print("\nPresiona Enter para continuar con el siguiente módulo...")
            input()
        
        print(f"\n{'='*60}")
        print(f"RESUMEN: {exitos}/{total} módulos ejecutados exitosamente")
        print(f"{'='*60}")
    
    def ejecutar_tests(self):
        """Ejecutar tests del módulo 5"""
        print("\n" + "=" * 60)
        print("EJECUTANDO TESTS DEL MÓDULO 5")
        print("=" * 60)
        
        archivo_test = "modulo_5_testing/test_funciones.py"
        
        if not os.path.exists(archivo_test):
            print(f"❌ Error: Archivo de tests '{archivo_test}' no encontrado")
            return
        
        try:
            # Verificar si pytest está instalado
            resultado = subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                                     capture_output=True, text=True)
            
            if resultado.returncode != 0:
                print("❌ Error: pytest no está instalado")
                print("Instala pytest con: pip install pytest")
                return
            
            # Ejecutar tests
            print("Ejecutando tests con pytest...")
            resultado = subprocess.run([sys.executable, "-m", "pytest", archivo_test, "-v"], 
                                     capture_output=True, text=True)
            
            if resultado.stdout:
                print(resultado.stdout)
            
            if resultado.stderr:
                print("⚠️  Advertencias:")
                print(resultado.stderr)
            
            if resultado.returncode == 0:
                print("✅ Todos los tests pasaron exitosamente")
            else:
                print("❌ Algunos tests fallaron")
                
        except Exception as e:
            print(f"❌ Error al ejecutar tests: {str(e)}")
    
    def mostrar_informacion_curso(self):
        """Mostrar información detallada del curso"""
        print("\n" + "=" * 60)
        print("INFORMACIÓN DEL CURSO DE PYTHON - COURSERA")
        print("=" * 60)
        
        print("\n📚 Estructura del Curso:")
        print("-" * 30)
        for clave, modulo in self.modulos.items():
            print(f"Módulo {clave}: {modulo['nombre']}")
            print(f"  📁 {modulo['archivo']}")
            print(f"  📝 {modulo['descripcion']}")
            print()
        
        print("\n🛠️  Herramientas Disponibles:")
        print("-" * 30)
        for clave, herramienta in self.herramientas.items():
            print(f"{clave}: {herramienta['nombre']}")
            print(f"  📁 {herramienta['archivo']}")
            print(f"  📝 {herramienta['descripcion']}")
            print()
        
        print("\n📋 Comandos Disponibles:")
        print("-" * 30)
        print("• Número del módulo (1-6): Ejecutar módulo específico")
        print("• 'todos': Ejecutar todos los módulos")
        print("• 'tests': Ejecutar tests del módulo 5")
        print("• 'setup': Configurar entorno")
        print("• 'info': Mostrar esta información")
        print("• 'salir': Salir del programa")
        
        print("\n📖 Archivos Importantes:")
        print("-" * 30)
        archivos_importantes = [
            "README.md - Documentación principal",
            "requirements.txt - Dependencias del curso",
            "setup_coursera.py - Configuración del entorno",
            "pytest.ini - Configuración de tests"
        ]
        
        for archivo in archivos_importantes:
            print(f"• {archivo}")
        
        print("\n🚀 Para comenzar:")
        print("-" * 30)
        print("1. Ejecuta 'setup' para configurar el entorno")
        print("2. Comienza con el módulo 1: '1'")
        print("3. Sigue la secuencia de módulos")
        print("4. Ejecuta 'tests' para verificar tu aprendizaje")
    
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
        
        elif comando.lower() == "tests":
            self.ejecutar_tests()
            return True
        
        elif comando.lower() == "setup":
            return self.ejecutar_modulo("setup")
        
        elif comando.lower() == "info":
            self.mostrar_informacion_curso()
            return True
        
        elif comando.lower() in ["salir", "exit", "quit"]:
            print("\n👋 ¡Gracias por usar el curso de Python de Coursera!")
            print("¡Esperamos que hayas aprendido mucho!")
            sys.exit(0)
        
        else:
            print(f"❌ Comando '{comando}' no reconocido")
            return False
    
    def ejecutar_interactivo(self):
        """Ejecutar el curso en modo interactivo"""
        print("🎓 Bienvenido al Curso de Python de Coursera")
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
                
                print("\nPresiona Enter para continuar...")
                input()
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error inesperado: {str(e)}")
                print("Continuando...")


def main():
    """Función principal"""
    ejecutor = EjecutorCurso()
    
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