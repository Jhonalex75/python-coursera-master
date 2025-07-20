#!/usr/bin/env python3
"""
Script de Ejecución Rápida - Curso de Python de Coursera
=======================================================

Ejecuta ejemplos y ejercicios del curso con un solo comando.

Uso: python ejecutar_curso.py [modulo] [ejemplo]
Ejemplos:
  python ejecutar_curso.py modulo_1
  python ejecutar_curso.py modulo_2 condicionales
  python ejecutar_curso.py proyecto calculadora
"""

import sys
import os
import subprocess
from pathlib import Path

def mostrar_ayuda():
    """Muestra la ayuda del script."""
    print("🐍 CURSO DE PYTHON DE COURSERA")
    print("=" * 50)
    print("Uso: python ejecutar_curso.py [opción]")
    print()
    print("Opciones disponibles:")
    print("  modulo_1     - Ejecutar Módulo 1: Fundamentos")
    print("  modulo_2     - Ejecutar Módulo 2: Control de Flujo")
    print("  modulo_3     - Ejecutar Módulo 3: Bucles")
    print("  modulo_4     - Ejecutar Módulo 4: Estructuras de Datos")
    print("  modulo_5     - Ejecutar Módulo 5: Funciones")
    print("  modulo_6     - Ejecutar Módulo 6: Manejo de Errores")
    print("  modulo_7     - Ejecutar Módulo 7: Control de Versiones")
    print("  modulo_8     - Ejecutar Módulo 8: Testing")
    print("  proyecto     - Ejecutar proyectos integrados")
    print("  todos        - Ejecutar todos los módulos")
    print("  ayuda        - Mostrar esta ayuda")
    print()
    print("Ejemplos:")
    print("  python ejecutar_curso.py modulo_1")
    print("  python ejecutar_curso.py modulo_2 condicionales")
    print("  python ejecutar_curso.py proyecto calculadora")

def ejecutar_modulo(modulo, ejemplo=None):
    """Ejecuta un módulo específico."""
    modulo_path = f"modulo_{modulo}"
    
    if not os.path.exists(modulo_path):
        print(f"❌ Módulo {modulo} no encontrado")
        return False
    
    if ejemplo:
        archivo = os.path.join(modulo_path, f"{ejemplo}.py")
        if os.path.exists(archivo):
            print(f"🚀 Ejecutando {archivo}...")
            subprocess.run([sys.executable, archivo])
        else:
            print(f"❌ Archivo {archivo} no encontrado")
            return False
    else:
        # Ejecutar todos los archivos del módulo
        archivos_py = list(Path(modulo_path).glob("*.py"))
        if archivos_py:
            print(f"🚀 Ejecutando módulo {modulo}...")
            for archivo in archivos_py:
                if archivo.name != "__init__.py":
                    print(f"  Ejecutando {archivo.name}...")
                    subprocess.run([sys.executable, str(archivo)])
        else:
            print(f"❌ No se encontraron archivos Python en {modulo_path}")
            return False
    
    return True

def ejecutar_proyecto(proyecto):
    """Ejecuta un proyecto específico."""
    proyecto_path = f"proyectos_integrados/{proyecto}"
    
    if not os.path.exists(proyecto_path):
        print(f"❌ Proyecto {proyecto} no encontrado")
        return False
    
    archivo_principal = os.path.join(proyecto_path, f"{proyecto}.py")
    if os.path.exists(archivo_principal):
        print(f"🚀 Ejecutando proyecto {proyecto}...")
        subprocess.run([sys.executable, archivo_principal])
    else:
        print(f"❌ Archivo principal {archivo_principal} no encontrado")
        return False
    
    return True

def ejecutar_todos():
    """Ejecuta todos los módulos."""
    print("🚀 Ejecutando todos los módulos...")
    
    for i in range(1, 9):
        print(f"\n--- MÓDULO {i} ---")
        ejecutar_modulo(i)

def main():
    """Función principal."""
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return
    
    opcion = sys.argv[1].lower()
    
    if opcion == "ayuda" or opcion == "help":
        mostrar_ayuda()
    
    elif opcion == "todos":
        ejecutar_todos()
    
    elif opcion.startswith("modulo_"):
        modulo_num = opcion.split("_")[1]
        ejemplo = sys.argv[2] if len(sys.argv) > 2 else None
        ejecutar_modulo(modulo_num, ejemplo)
    
    elif opcion == "proyecto":
        if len(sys.argv) < 3:
            print("❌ Debes especificar un proyecto")
            print("Proyectos disponibles: calculadora, gestor_contactos, analizador_datos, juego_adivinanza")
            return
        proyecto = sys.argv[2]
        ejecutar_proyecto(proyecto)
    
    else:
        print(f"❌ Opción '{opcion}' no reconocida")
        mostrar_ayuda()

if __name__ == "__main__":
    main()
