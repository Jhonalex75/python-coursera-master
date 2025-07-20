# -----------------------------------------------------------------------------
# Purpose: Setup script for the engineering project.
# Application: Engineering project.
# Dependencies: Python 3.8 or higher, pip, pytest, pytest-cov, pandas, numpy, matplotlib, seaborn, jupyter, ipykernel, black, flake8, mypy.
# Usage: Run the script; it will install dependencies, create directories, and verify the environment.
# -----------------------------------------------------------------------------
#!/usr/bin/env python3
"""
Script de Configuración - Proyecto de Ingeniería Mecánica
========================================================

Este script facilita la instalación y configuración del proyecto,
incluyendo la instalación de dependencias, creación de directorios
y verificación del entorno.

Autor: Ing. Jhon A. Valencia
Fecha: 2024
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_python():
    """Verifica la versión de Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True

def instalar_dependencias():
    """Instala las dependencias del proyecto."""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Verificar si pip está disponible
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # Instalar dependencias desde requirements.txt
        if os.path.exists("requirements.txt"):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True)
            print("✅ Dependencias instaladas correctamente")
            return True
        else:
            print("⚠️ Archivo requirements.txt no encontrado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: pip no está disponible")
        return False

def crear_estructura_directorios():
    """Crea la estructura de directorios necesaria."""
    print("\n📁 Creando estructura de directorios...")
    
    directorios = [
        "outputs",
        "logs",
        "data",
        "docs/ejemplos",
        "docs/manuales",
        "tests",
        "src/ingenieria/bombas_y_flujos",
        "src/ingenieria/metodos_numericos",
        "src/ingenieria/visualizacion",
        "src/mantenimiento",
        "src/analisis/financiero_operativo",
        "src/estadistica/analisis_datos",
        "src/gui/simuladores",
        "src/web",
        "src/scripts/conversiones",
        "src/scripts_utilidad"
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directorio}")
    
    print("✅ Estructura de directorios creada")

def crear_archivos_iniciales():
    """Crea archivos iniciales necesarios."""
    print("\n📄 Creando archivos iniciales...")
    
    # Archivo __init__.py para hacer src un paquete
    init_content = '''"""
Paquete principal del proyecto de Ingeniería Mecánica
===================================================

Este paquete contiene todas las herramientas y módulos
para análisis y diseño en ingeniería mecánica.

Autor: Ing. Jhon A. Valencia
Fecha: 2024
"""

__version__ = "1.0.0"
__author__ = "Ing. Jhon A. Valencia"
__email__ = "jhon.valencia@ejemplo.com"
'''
    
    with open("src/__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)
    
    # Archivo __init__.py para subpaquetes
    subpaquetes = [
        "src/ingenieria",
        "src/mantenimiento", 
        "src/analisis",
        "src/estadistica",
        "src/gui",
        "src/web",
        "src/scripts"
    ]
    
    for subpaquete in subpaquetes:
        init_file = os.path.join(subpaquete, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w", encoding="utf-8") as f:
                f.write('"""Módulo de ' + subpaquete.split('/')[-1] + '"""\n')
    
    print("✅ Archivos iniciales creados")

def verificar_instalacion():
    """Verifica que la instalación sea correcta."""
    print("\n🔍 Verificando instalación...")
    
    # Verificar módulos principales
    modulos_principales = [
        "numpy",
        "matplotlib", 
        "pandas",
        "scipy",
        "seaborn"
    ]
    
    for modulo in modulos_principales:
        try:
            __import__(modulo)
            print(f"   ✅ {modulo}")
        except ImportError:
            print(f"   ❌ {modulo} - No disponible")
            return False
    
    # Verificar estructura de archivos
    archivos_importantes = [
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/ingenieria/CURVA_BOMBA.py",
        "src/ingenieria/RUNGE_KUTTA.py",
        "src/mantenimiento/gestion_mtto.py"
    ]
    
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ⚠️ {archivo} - No encontrado")
    
    return True

def crear_script_ejecucion():
    """Crea un script de ejecución rápida."""
    print("\n🚀 Creando script de ejecución...")
    
    script_content = '''#!/usr/bin/env python3
"""
Script de Ejecución Rápida - Proyecto de Ingeniería Mecánica
============================================================

Ejecuta el ejemplo completo del proyecto con un solo comando.

Uso: python ejecutar_proyecto.py
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ejemplo_uso_completo import main
    print("🏭 Iniciando proyecto de Ingeniería Mecánica...")
    main()
except ImportError as e:
    print(f"❌ Error: {e}")
    print("💡 Ejecuta primero: python setup.py")
except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")
'''
    
    with open("ejecutar_proyecto.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # Hacer el script ejecutable en sistemas Unix
    try:
        os.chmod("ejecutar_proyecto.py", 0o755)
    except:
        pass
    
    print("✅ Script de ejecución creado")

def mostrar_instrucciones():
    """Muestra instrucciones de uso."""
    print("\n" + "="*60)
    print("🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print()
    print("📖 PRÓXIMOS PASOS:")
    print("1. Ejecutar el proyecto completo:")
    print("   python ejecutar_proyecto.py")
    print()
    print("2. O ejecutar ejemplos individuales:")
    print("   python src/ingenieria/CURVA_BOMBA.py")
    print("   python src/ingenieria/RUNGE_KUTTA.py")
    print("   python src/mantenimiento/gestion_mtto.py")
    print()
    print("3. Consultar la documentación:")
    print("   README.md - Guía general del proyecto")
    print("   docs/ - Manuales y ejemplos")
    print()
    print("4. Para desarrollo:")
    print("   pip install -r requirements.txt")
    print("   python -m pytest tests/")
    print()
    print("🔧 ESTRUCTURA DEL PROYECTO:")
    print("   src/ingenieria/     - Herramientas de ingeniería")
    print("   src/mantenimiento/  - Gestión de mantenimiento")
    print("   src/analisis/       - Análisis financiero")
    print("   src/estadistica/    - Análisis estadístico")
    print("   src/gui/           - Interfaces gráficas")
    print("   src/web/           - Aplicaciones web")
    print("   outputs/           - Resultados generados")
    print()
    print("📞 SOPORTE:")
    print("   - Revisar README.md para documentación")
    print("   - Consultar ejemplos en docs/")
    print("   - Crear issue en GitHub para problemas")
    print()
    print("⭐ ¡Disfruta usando las herramientas de ingeniería mecánica!")

def main():
    """Función principal de configuración."""
    print("🏭 CONFIGURACIÓN DEL PROYECTO DE INGENIERÍA MECÁNICA")
    print("=" * 60)
    print("Este script configurará el entorno para usar todas las herramientas")
    print("del proyecto de ingeniería mecánica.")
    print()
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Crear estructura de directorios
    crear_estructura_directorios()
    
    # Crear archivos iniciales
    crear_archivos_iniciales()
    
    # Instalar dependencias
    if not instalar_dependencias():
        print("⚠️ Algunas dependencias no se pudieron instalar")
        print("   Puedes instalarlas manualmente con: pip install -r requirements.txt")
    
    # Verificar instalación
    if not verificar_instalacion():
        print("⚠️ Algunos componentes no están disponibles")
    
    # Crear script de ejecución
    crear_script_ejecucion()
    
    # Mostrar instrucciones
    mostrar_instrucciones()

if __name__ == "__main__":
    main() 