#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalación - PYTHON COURSERA MASTER
===============================================
Instalador automático para el paquete educativo de ingeniería mecánica
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Imprime el banner de bienvenida"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    PYTHON COURSERA MASTER                    ║
║              Paquete Educativo de Ingeniería Mecánica        ║
║                                                              ║
║  🚀 Instalador Automático v1.0                              ║
║  📅 Versión: 2024                                           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Verifica la versión de Python"""
    print("🔍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_pip():
    """Verifica si pip está disponible"""
    print("🔍 Verificando pip...")
    
    try:
        import pip
        print("✅ pip está disponible")
        return True
    except ImportError:
        print("❌ Error: pip no está disponible")
        print("   Instale pip antes de continuar")
        return False

def create_virtual_environment():
    """Crea un entorno virtual"""
    print("🔧 Creando entorno virtual...")
    
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"⚠️  El entorno virtual '{venv_name}' ya existe")
        response = input("¿Desea recrearlo? (s/n): ").lower()
        if response == 's':
            import shutil
            shutil.rmtree(venv_name)
        else:
            print("✅ Usando entorno virtual existente")
            return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print("✅ Entorno virtual creado exitosamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al crear el entorno virtual")
        return False

def get_activation_command():
    """Obtiene el comando de activación según el sistema operativo"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print("⚠️  Archivo requirements.txt no encontrado")
        print("   Creando archivo de dependencias básicas...")
        create_basic_requirements()
    
    try:
        # Determinar el comando de pip según el sistema
        if platform.system().lower() == "windows":
            pip_cmd = "venv\\Scripts\\pip"
        else:
            pip_cmd = "venv/bin/pip"
        
        subprocess.run([pip_cmd, "install", "-r", requirements_file], check=True)
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def create_basic_requirements():
    """Crea un archivo requirements.txt básico"""
    requirements = """# Dependencias básicas para PYTHON COURSERA MASTER
numpy>=1.21.0
matplotlib>=3.5.0
pandas>=1.3.0
scipy>=1.7.0
tkinter
pillow>=8.3.0
openpyxl>=3.0.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print("✅ Archivo requirements.txt creado")

def verify_installation():
    """Verifica que la instalación sea correcta"""
    print("🔍 Verificando instalación...")
    
    # Verificar módulos principales
    modules_to_check = [
        "numpy",
        "matplotlib", 
        "pandas",
        "scipy",
        "tkinter"
    ]
    
    missing_modules = []
    
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - Faltante")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Módulos faltantes: {', '.join(missing_modules)}")
        return False
    
    print("✅ Todos los módulos están disponibles")
    return True

def create_launcher_scripts():
    """Crea scripts de lanzamiento"""
    print("🚀 Creando scripts de lanzamiento...")
    
    # Script para Windows
    if platform.system().lower() == "windows":
        launcher_content = """@echo off
echo Iniciando PYTHON COURSERA MASTER...
call venv\\Scripts\\activate
python PYTHON_COURSERA_MASTER.py
pause
"""
        with open("ejecutar.bat", "w") as f:
            f.write(launcher_content)
        print("✅ Script ejecutar.bat creado")
    
    # Script para Unix/Linux/macOS
    launcher_content = """#!/bin/bash
echo "Iniciando PYTHON COURSERA MASTER..."
source venv/bin/activate
python PYTHON_COURSERA_MASTER.py
"""
    with open("ejecutar.sh", "w") as f:
        f.write(launcher_content)
    
    # Hacer ejecutable en Unix
    if platform.system().lower() != "windows":
        os.chmod("ejecutar.sh", 0o755)
    
    print("✅ Script ejecutar.sh creado")

def show_usage_instructions():
    """Muestra las instrucciones de uso"""
    instructions = """
🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!

📋 INSTRUCCIONES DE USO:

1. ACTIVAR EL ENTORNO VIRTUAL:
   """
    
    if platform.system().lower() == "windows":
        instructions += """
   Windows:
   venv\\Scripts\\activate
        """
    else:
        instructions += """
   macOS/Linux:
   source venv/bin/activate
        """
    
    instructions += """

2. EJECUTAR LA APLICACIÓN:
   
   Opción A - Usando Python directamente:
   python PYTHON_COURSERA_MASTER.py
   
   Opción B - Usando los scripts de lanzamiento:
   """
    
    if platform.system().lower() == "windows":
        instructions += """
   Windows: ejecutar.bat
        """
    else:
        instructions += """
   macOS/Linux: ./ejecutar.sh
        """
    
    instructions += """

3. MÓDULOS DISPONIBLES:
   ✅ Análisis Estructural
   ✅ Dinámica de Máquinas
   ✅ Termodinámica y Fluidos
   ✅ Materiales y Resistencia
   ✅ Calculadora Avanzada
   ✅ Mantenimiento y Confiabilidad
   ✅ Gestión de Proyectos

4. DOCUMENTACIÓN:
   📖 README.md - Guía completa del sistema
   📁 modulos/ - Código fuente de los módulos
   📁 herramientas/ - Herramientas adicionales

🚀 ¡Disfrute usando PYTHON COURSERA MASTER!
    """
    
    print(instructions)

def main():
    """Función principal del instalador"""
    print_banner()
    
    print("🚀 Iniciando proceso de instalación...\n")
    
    # Verificaciones previas
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Proceso de instalación
    if not create_virtual_environment():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not verify_installation():
        print("\n⚠️  Algunos módulos no se instalaron correctamente")
        print("   Intente ejecutar manualmente: pip install -r requirements.txt")
    
    # Crear scripts de lanzamiento
    create_launcher_scripts()
    
    # Mostrar instrucciones finales
    show_usage_instructions()
    
    print("\n" + "="*60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("="*60)

if __name__ == "__main__":
    main() 