#!/usr/bin/env python3
"""
Script de Configuración - Curso de Python de Coursera
====================================================

Este script facilita la instalación y configuración del curso de Python de Coursera,
incluyendo la instalación de dependencias, creación de directorios y verificación
del entorno de aprendizaje.

Autor: Ing. Jhon A. Valencia
Curso: Python de Coursera
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN DE COLORES PARA SALIDA
# ============================================================================

class Colors:
    """Colores para la salida en terminal."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_color(mensaje: str, color: str = Colors.ENDC):
    """Imprime un mensaje con color."""
    print(f"{color}{mensaje}{Colors.ENDC}")

# ============================================================================
# VERIFICACIÓN DEL ENTORNO
# ============================================================================

def verificar_python():
    """Verifica la versión de Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_color("❌ Error: Se requiere Python 3.8 o superior", Colors.FAIL)
        print_color(f"   Versión actual: {version.major}.{version.minor}.{version.micro}", Colors.FAIL)
        return False
    else:
        print_color(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK", Colors.OKGREEN)
        return True

def verificar_pip():
    """Verifica si pip está disponible."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print_color("✅ pip disponible - OK", Colors.OKGREEN)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_color("❌ Error: pip no está disponible", Colors.FAIL)
        return False

# ============================================================================
# INSTALACIÓN DE DEPENDENCIAS
# ============================================================================

def crear_requirements_coursera():
    """Crea el archivo requirements.txt específico para el curso."""
    requirements_content = """# Dependencias para el Curso de Python de Coursera
# Versión mínima requerida para cada paquete

# Dependencias básicas para el curso
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.5.0

# Para ejercicios y proyectos
requests>=2.25.0
beautifulsoup4>=4.9.0

# Para testing (Módulo 8)
pytest>=6.0.0
pytest-cov>=2.12.0

# Para debugging (Módulo 6)
# (logging viene incluido con Python)

# Para visualización de datos
seaborn>=0.11.0

# Para desarrollo
black>=21.0.0
flake8>=3.9.0

# Utilidades
tqdm>=4.62.0
python-dotenv>=0.19.0
"""
    
    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    
    print_color("✅ Archivo requirements.txt creado", Colors.OKGREEN)

def instalar_dependencias():
    """Instala las dependencias del curso."""
    print_color("\n📦 Instalando dependencias del curso...", Colors.OKBLUE)
    
    try:
        if os.path.exists("requirements.txt"):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True)
            print_color("✅ Dependencias instaladas correctamente", Colors.OKGREEN)
            return True
        else:
            print_color("⚠️ Archivo requirements.txt no encontrado", Colors.WARNING)
            return False
            
    except subprocess.CalledProcessError as e:
        print_color(f"❌ Error al instalar dependencias: {e}", Colors.FAIL)
        return False

# ============================================================================
# CREACIÓN DE ESTRUCTURA DE DIRECTORIOS
# ============================================================================

def crear_estructura_coursera():
    """Crea la estructura de directorios para el curso."""
    print_color("\n📁 Creando estructura de directorios del curso...", Colors.OKBLUE)
    
    directorios = [
        # Módulos del curso
        "modulo_1_fundamentos",
        "modulo_1_fundamentos/ejercicios",
        "modulo_2_control_flujo",
        "modulo_2_control_flujo/ejercicios",
        "modulo_3_bucles",
        "modulo_3_bucles/ejercicios",
        "modulo_4_estructuras_datos",
        "modulo_4_estructuras_datos/ejercicios",
        "modulo_5_funciones",
        "modulo_5_funciones/ejercicios",
        "modulo_6_manejo_errores",
        "modulo_6_manejo_errores/ejercicios",
        "modulo_7_control_versiones",
        "modulo_7_control_versiones/ejercicios",
        "modulo_8_testing",
        "modulo_8_testing/ejercicios",
        
        # Proyectos integrados
        "proyectos_integrados",
        "proyectos_integrados/calculadora",
        "proyectos_integrados/gestor_contactos",
        "proyectos_integrados/analizador_datos",
        "proyectos_integrados/juego_adivinanza",
        
        # Herramientas de utilidad
        "herramientas_utilidad",
        
        # Recursos
        "recursos",
        "recursos/datos_ejemplo",
        "recursos/plantillas",
        "recursos/documentacion",
        
        # Salida y logs
        "outputs",
        "logs",
        
        # Tests
        "tests",
        "tests/modulo_1",
        "tests/modulo_2",
        "tests/modulo_3",
        "tests/modulo_4",
        "tests/modulo_5",
        "tests/modulo_6",
        "tests/modulo_7",
        "tests/modulo_8"
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(parents=True, exist_ok=True)
        print_color(f"   ✅ {directorio}", Colors.OKGREEN)
    
    print_color("✅ Estructura de directorios creada", Colors.OKGREEN)

# ============================================================================
# CREACIÓN DE ARCHIVOS INICIALES
# ============================================================================

def crear_archivos_iniciales():
    """Crea archivos iniciales necesarios."""
    print_color("\n📄 Creando archivos iniciales...", Colors.OKBLUE)
    
    # Archivo __init__.py para cada módulo
    modulos = [
        "modulo_1_fundamentos",
        "modulo_2_control_flujo", 
        "modulo_3_bucles",
        "modulo_4_estructuras_datos",
        "modulo_5_funciones",
        "modulo_6_manejo_errores",
        "modulo_7_control_versiones",
        "modulo_8_testing",
        "proyectos_integrados",
        "herramientas_utilidad"
    ]
    
    for modulo in modulos:
        init_file = os.path.join(modulo, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(f'"""Módulo {modulo.replace("_", " ").title()}"""\n')
    
    # Archivo de configuración del curso
    config_content = '''# Configuración del Curso de Python de Coursera
# ================================================

# Información del curso
CURSO_NOMBRE = "Python for Everybody"
PLATAFORMA = "Coursera"
INSTRUCTOR = "Dr. Charles Severance"
AUTOR_MATERIALES = "Ing. Jhon A. Valencia"

# Configuración de módulos
MODULOS = [
    "Fundamentos de Python",
    "Control de Flujo",
    "Bucles y Repetición", 
    "Estructuras de Datos",
    "Funciones y Modularización",
    "Manejo de Errores",
    "Control de Versiones",
    "Testing"
]

# Configuración de debugging
DEBUG_MODE = True
LOG_LEVEL = "INFO"
LOG_FILE = "logs/coursera_python.log"

# Configuración de testing
TEST_COVERAGE_MIN = 80
TEST_TIMEOUT = 30

# Configuración de proyectos
PROYECTOS_DISPONIBLES = [
    "calculadora",
    "gestor_contactos", 
    "analizador_datos",
    "juego_adivinanza"
]
'''
    
    with open("config_coursera.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print_color("✅ Archivos iniciales creados", Colors.OKGREEN)

# ============================================================================
# CREACIÓN DE DATOS DE EJEMPLO
# ============================================================================

def crear_datos_ejemplo():
    """Crea archivos de datos de ejemplo para el curso."""
    print_color("\n📊 Creando datos de ejemplo...", Colors.OKBLUE)
    
    # Datos de estudiantes
    estudiantes_data = '''nombre,edad,calificacion,asistencia
Juan Pérez,20,85,0.95
María García,22,92,0.88
Carlos López,19,78,0.75
Ana Martínez,21,96,0.98
Luis Rodríguez,23,82,0.90
'''
    
    with open("recursos/datos_ejemplo/estudiantes.csv", "w", encoding="utf-8") as f:
        f.write(estudiantes_data)
    
    # Datos de ventas
    ventas_data = '''fecha,producto,cantidad,precio,total
2024-01-15,Laptop,2,1200.00,2400.00
2024-01-15,Mouse,5,25.00,125.00
2024-01-16,Teclado,3,50.00,150.00
2024-01-16,Monitor,1,300.00,300.00
2024-01-17,Auriculares,4,75.00,300.00
'''
    
    with open("recursos/datos_ejemplo/ventas.csv", "w", encoding="utf-8") as f:
        f.write(ventas_data)
    
    # Datos de contactos
    contactos_data = '''nombre,email,telefono,ciudad
Juan Pérez,juan@ejemplo.com,123-456-7890,Madrid
María García,maria@ejemplo.com,098-765-4321,Barcelona
Carlos López,carlos@ejemplo.com,555-123-4567,Valencia
Ana Martínez,ana@ejemplo.com,777-888-9999,Sevilla
'''
    
    with open("recursos/datos_ejemplo/contactos.csv", "w", encoding="utf-8") as f:
        f.write(contactos_data)
    
    print_color("✅ Datos de ejemplo creados", Colors.OKGREEN)

# ============================================================================
# VERIFICACIÓN DE INSTALACIÓN
# ============================================================================

def verificar_instalacion():
    """Verifica que la instalación sea correcta."""
    print_color("\n🔍 Verificando instalación...", Colors.OKBLUE)
    
    # Verificar módulos principales
    modulos_principales = [
        "numpy",
        "pandas", 
        "matplotlib",
        "pytest"
    ]
    
    for modulo in modulos_principales:
        try:
            __import__(modulo)
            print_color(f"   ✅ {modulo}", Colors.OKGREEN)
        except ImportError:
            print_color(f"   ❌ {modulo} - No disponible", Colors.FAIL)
            return False
    
    # Verificar estructura de archivos
    archivos_importantes = [
        "requirements.txt",
        "README.md",
        "config_coursera.py",
        "modulo_1_fundamentos/variables_tipos.py",
        "modulo_2_control_flujo/condicionales.py",
        "modulo_6_manejo_errores/debugging.py"
    ]
    
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            print_color(f"   ✅ {archivo}", Colors.OKGREEN)
        else:
            print_color(f"   ⚠️ {archivo} - No encontrado", Colors.WARNING)
    
    return True

# ============================================================================
# CREACIÓN DE SCRIPT DE EJECUCIÓN
# ============================================================================

def crear_script_ejecucion():
    """Crea un script de ejecución rápida para el curso."""
    print_color("\n🚀 Creando script de ejecución...", Colors.OKBLUE)
    
    script_content = '''#!/usr/bin/env python3
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
        print(f"\\n--- MÓDULO {i} ---")
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
'''
    
    with open("ejecutar_curso.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # Hacer el script ejecutable en sistemas Unix
    try:
        os.chmod("ejecutar_curso.py", 0o755)
    except:
        pass
    
    print_color("✅ Script de ejecución creado", Colors.OKGREEN)

# ============================================================================
# MOSTRAR INSTRUCCIONES
# ============================================================================

def mostrar_instrucciones():
    """Muestra instrucciones de uso del curso."""
    print_color("\n" + "="*60, Colors.HEADER)
    print_color("🎉 INSTALACIÓN DEL CURSO COMPLETADA EXITOSAMENTE", Colors.HEADER)
    print_color("="*60, Colors.HEADER)
    print()
    print_color("📖 PRÓXIMOS PASOS:", Colors.BOLD)
    print_color("1. Ejecutar el curso completo:", Colors.OKBLUE)
    print_color("   python ejecutar_curso.py todos", Colors.OKCYAN)
    print()
    print_color("2. Ejecutar módulos individuales:", Colors.OKBLUE)
    print_color("   python ejecutar_curso.py modulo_1", Colors.OKCYAN)
    print_color("   python ejecutar_curso.py modulo_2", Colors.OKCYAN)
    print_color("   python ejecutar_curso.py modulo_3", Colors.OKCYAN)
    print()
    print_color("3. Ejecutar ejemplos específicos:", Colors.OKBLUE)
    print_color("   python ejecutar_curso.py modulo_1 variables_tipos", Colors.OKCYAN)
    print_color("   python ejecutar_curso.py modulo_2 condicionales", Colors.OKCYAN)
    print()
    print_color("4. Ejecutar proyectos:", Colors.OKBLUE)
    print_color("   python ejecutar_curso.py proyecto calculadora", Colors.OKCYAN)
    print_color("   python ejecutar_curso.py proyecto gestor_contactos", Colors.OKCYAN)
    print()
    print_color("5. Consultar la documentación:", Colors.OKBLUE)
    print_color("   README.md - Guía general del curso", Colors.OKCYAN)
    print_color("   recursos/documentacion/ - Manuales específicos", Colors.OKCYAN)
    print()
    print_color("🔧 ESTRUCTURA DEL CURSO:", Colors.BOLD)
    print_color("   modulo_1_fundamentos/     - Variables y tipos de datos", Colors.OKGREEN)
    print_color("   modulo_2_control_flujo/   - Condicionales y decisiones", Colors.OKGREEN)
    print_color("   modulo_3_bucles/          - Bucles y repetición", Colors.OKGREEN)
    print_color("   modulo_4_estructuras_datos/ - Listas, diccionarios, etc.", Colors.OKGREEN)
    print_color("   modulo_5_funciones/       - Funciones y modularización", Colors.OKGREEN)
    print_color("   modulo_6_manejo_errores/  - Excepciones y debugging", Colors.OKGREEN)
    print_color("   modulo_7_control_versiones/ - Git básico", Colors.OKGREEN)
    print_color("   modulo_8_testing/         - Pruebas unitarias", Colors.OKGREEN)
    print_color("   proyectos_integrados/     - Proyectos completos", Colors.OKGREEN)
    print_color("   herramientas_utilidad/    - Herramientas de apoyo", Colors.OKGREEN)
    print_color("   recursos/                 - Datos y documentación", Colors.OKGREEN)
    print()
    print_color("📞 SOPORTE:", Colors.BOLD)
    print_color("   - Revisar README.md para documentación completa", Colors.OKCYAN)
    print_color("   - Consultar ejemplos en cada módulo", Colors.OKCYAN)
    print_color("   - Ver logs en carpeta logs/", Colors.OKCYAN)
    print()
    print_color("⭐ ¡Disfruta aprendiendo Python con este curso organizado!", Colors.HEADER)

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal de configuración."""
    print_color("🐍 CONFIGURACIÓN DEL CURSO DE PYTHON DE COURSERA", Colors.HEADER)
    print_color("=" * 60, Colors.HEADER)
    print_color("Este script configurará el entorno para el curso de Python", Colors.OKBLUE)
    print_color("de Coursera, incluyendo todos los módulos y herramientas.", Colors.OKBLUE)
    print()
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Verificar pip
    if not verificar_pip():
        print_color("⚠️ Continuando sin pip...", Colors.WARNING)
    
    # Crear estructura de directorios
    crear_estructura_coursera()
    
    # Crear archivos iniciales
    crear_archivos_iniciales()
    
    # Crear requirements.txt
    crear_requirements_coursera()
    
    # Instalar dependencias
    if not instalar_dependencias():
        print_color("⚠️ Algunas dependencias no se pudieron instalar", Colors.WARNING)
        print_color("   Puedes instalarlas manualmente con: pip install -r requirements.txt", Colors.WARNING)
    
    # Crear datos de ejemplo
    crear_datos_ejemplo()
    
    # Verificar instalación
    if not verificar_instalacion():
        print_color("⚠️ Algunos componentes no están disponibles", Colors.WARNING)
    
    # Crear script de ejecución
    crear_script_ejecucion()
    
    # Mostrar instrucciones
    mostrar_instrucciones()

if __name__ == "__main__":
    main() 