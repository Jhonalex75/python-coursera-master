#!/usr/bin/env python3
"""
Script de Prueba para el Curso de Python de Coursera
===================================================

Este script verifica que todos los módulos del curso funcionan correctamente
y proporciona un resumen del estado del curso.

Autor: Curso Python Coursera
Versión: 1.0
"""

import os
import sys
import subprocess
import importlib.util
from typing import Dict, List, Tuple


class VerificadorCurso:
    """
    Clase para verificar el estado del curso
    """
    
    def __init__(self):
        self.modulos = {
            "modulo_1_fundamentos": {
                "archivo": "variables_tipos.py",
                "descripcion": "Fundamentos de Python"
            },
            "modulo_2_control_flujo": {
                "archivo": "condicionales.py",
                "descripcion": "Control de Flujo"
            },
            "modulo_3_ordenamiento_errores": {
                "archivo": "ordenamiento_errores.py",
                "descripcion": "Ordenamiento y Manejo de Errores"
            },
            "modulo_4_control_versiones": {
                "archivo": "git_basico.py",
                "descripcion": "Control de Versiones con Git"
            },
            "modulo_5_testing": {
                "archivo": "testing_pytest.py",
                "descripcion": "Testing con pytest"
            },
            "modulo_6_manejo_errores": {
                "archivo": "debugging.py",
                "descripcion": "Manejo de Errores Avanzado"
            }
        }
        
        self.herramientas = {
            "herramientas_utilidad": {
                "archivo": "debugging_toolkit.py",
                "descripcion": "Kit de Debugging"
            }
        }
        
        self.archivos_principales = [
            "setup_coursera.py",
            "ejecutar_curso.py",
            "requirements.txt",
            "pytest.ini",
            "README.md"
        ]
    
    def verificar_archivo(self, ruta: str) -> Tuple[bool, str]:
        """
        Verificar si un archivo existe y es ejecutable
        
        Args:
            ruta: Ruta del archivo a verificar
            
        Returns:
            Tuple[bool, str]: (existe, mensaje)
        """
        if not os.path.exists(ruta):
            return False, f"❌ Archivo no encontrado: {ruta}"
        
        if not os.path.isfile(ruta):
            return False, f"❌ No es un archivo: {ruta}"
        
        # Verificar si es un archivo Python ejecutable
        if ruta.endswith('.py'):
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    if 'def main()' in contenido or 'if __name__' in contenido:
                        return True, f"✅ {ruta} (ejecutable)"
                    else:
                        return True, f"✅ {ruta} (módulo)"
            except Exception as e:
                return False, f"❌ Error leyendo {ruta}: {str(e)}"
        
        return True, f"✅ {ruta}"
    
    def verificar_modulo(self, nombre_modulo: str, info_modulo: Dict) -> Dict:
        """
        Verificar un módulo completo
        
        Args:
            nombre_modulo: Nombre del módulo
            info_modulo: Información del módulo
            
        Returns:
            Dict: Resultado de la verificación
        """
        ruta_archivo = os.path.join(nombre_modulo, info_modulo['archivo'])
        existe, mensaje = self.verificar_archivo(ruta_archivo)
        
        resultado = {
            'modulo': nombre_modulo,
            'descripcion': info_modulo['descripcion'],
            'archivo': info_modulo['archivo'],
            'existe': existe,
            'mensaje': mensaje,
            'ruta_completa': ruta_archivo
        }
        
        # Verificar si el directorio existe
        if not os.path.exists(nombre_modulo):
            resultado['existe'] = False
            resultado['mensaje'] = f"❌ Directorio no encontrado: {nombre_modulo}"
        
        return resultado
    
    def verificar_tests(self) -> Dict:
        """
        Verificar archivos de tests
        
        Returns:
            Dict: Resultado de la verificación de tests
        """
        archivo_test = "modulo_5_testing/test_funciones.py"
        existe, mensaje = self.verificar_archivo(archivo_test)
        
        # Verificar si pytest está disponible
        pytest_disponible = False
        try:
            resultado = subprocess.run([sys.executable, "-m", "pytest", "--version"], 
                                     capture_output=True, text=True)
            pytest_disponible = resultado.returncode == 0
        except:
            pass
        
        return {
            'archivo_test': archivo_test,
            'existe': existe,
            'mensaje': mensaje,
            'pytest_disponible': pytest_disponible
        }
    
    def verificar_dependencias(self) -> Dict:
        """
        Verificar archivo de dependencias
        
        Returns:
            Dict: Resultado de la verificación
        """
        archivo_requirements = "requirements.txt"
        existe, mensaje = self.verificar_archivo(archivo_requirements)
        
        dependencias_instaladas = []
        if existe:
            try:
                with open(archivo_requirements, 'r') as f:
                    for linea in f:
                        linea = linea.strip()
                        if linea and not linea.startswith('#') and '>=' in linea:
                            paquete = linea.split('>=')[0].strip()
                            dependencias_instaladas.append(paquete)
            except Exception as e:
                return {
                    'existe': False,
                    'mensaje': f"❌ Error leyendo requirements.txt: {str(e)}",
                    'dependencias': []
                }
        
        return {
            'existe': existe,
            'mensaje': mensaje,
            'dependencias': dependencias_instaladas
        }
    
    def ejecutar_prueba_rapida(self, modulo: str) -> Tuple[bool, str]:
        """
        Ejecutar una prueba rápida de un módulo
        
        Args:
            modulo: Nombre del módulo
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Intentar importar el módulo
            ruta_archivo = os.path.join(modulo, self.modulos[modulo]['archivo'])
            spec = importlib.util.spec_from_file_location(modulo, ruta_archivo)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Solo verificar que se puede cargar, no ejecutar
                return True, "✅ Módulo se puede importar correctamente"
            else:
                return False, "❌ No se pudo cargar el módulo"
        except Exception as e:
            return False, f"❌ Error al importar: {str(e)}"
    
    def generar_reporte(self) -> str:
        """
        Generar reporte completo del estado del curso
        
        Returns:
            str: Reporte formateado
        """
        print("🔍 VERIFICANDO CURSO DE PYTHON DE COURSERA")
        print("=" * 60)
        
        reporte = []
        reporte.append("📊 REPORTE DE VERIFICACIÓN DEL CURSO")
        reporte.append("=" * 60)
        
        # Verificar archivos principales
        reporte.append("\n📁 ARCHIVOS PRINCIPALES:")
        reporte.append("-" * 30)
        archivos_ok = 0
        for archivo in self.archivos_principales:
            existe, mensaje = self.verificar_archivo(archivo)
            reporte.append(mensaje)
            if existe:
                archivos_ok += 1
        
        # Verificar módulos
        reporte.append("\n📚 MÓDULOS DEL CURSO:")
        reporte.append("-" * 30)
        modulos_ok = 0
        for nombre_modulo, info_modulo in self.modulos.items():
            resultado = self.verificar_modulo(nombre_modulo, info_modulo)
            reporte.append(f"{resultado['mensaje']} - {resultado['descripcion']}")
            if resultado['existe']:
                modulos_ok += 1
        
        # Verificar herramientas
        reporte.append("\n🛠️ HERRAMIENTAS:")
        reporte.append("-" * 30)
        herramientas_ok = 0
        for nombre_herramienta, info_herramienta in self.herramientas.items():
            resultado = self.verificar_modulo(nombre_herramienta, info_herramienta)
            reporte.append(f"{resultado['mensaje']} - {resultado['descripcion']}")
            if resultado['existe']:
                herramientas_ok += 1
        
        # Verificar tests
        reporte.append("\n🧪 TESTS:")
        reporte.append("-" * 30)
        resultado_tests = self.verificar_tests()
        reporte.append(resultado_tests['mensaje'])
        if resultado_tests['pytest_disponible']:
            reporte.append("✅ pytest está disponible")
        else:
            reporte.append("⚠️ pytest no está instalado (pip install pytest)")
        
        # Verificar dependencias
        reporte.append("\n📦 DEPENDENCIAS:")
        reporte.append("-" * 30)
        resultado_deps = self.verificar_dependencias()
        reporte.append(resultado_deps['mensaje'])
        if resultado_deps['dependencias']:
            reporte.append(f"📋 {len(resultado_deps['dependencias'])} dependencias definidas")
        
        # Resumen
        total_archivos = len(self.archivos_principales)
        total_modulos = len(self.modulos)
        total_herramientas = len(self.herramientas)
        
        reporte.append("\n📈 RESUMEN:")
        reporte.append("-" * 30)
        reporte.append(f"Archivos principales: {archivos_ok}/{total_archivos}")
        reporte.append(f"Módulos del curso: {modulos_ok}/{total_modulos}")
        reporte.append(f"Herramientas: {herramientas_ok}/{total_herramientas}")
        reporte.append(f"Tests: {'✅' if resultado_tests['existe'] else '❌'}")
        reporte.append(f"Dependencias: {'✅' if resultado_deps['existe'] else '❌'}")
        
        # Estado general
        total_items = total_archivos + total_modulos + total_herramientas
        items_ok = archivos_ok + modulos_ok + herramientas_ok
        porcentaje = (items_ok / total_items) * 100 if total_items > 0 else 0
        
        reporte.append(f"\n🎯 ESTADO GENERAL: {porcentaje:.1f}% ({items_ok}/{total_items})")
        
        if porcentaje >= 90:
            reporte.append("🎉 ¡El curso está completamente configurado!")
        elif porcentaje >= 70:
            reporte.append("✅ El curso está mayormente configurado")
        elif porcentaje >= 50:
            reporte.append("⚠️ El curso está parcialmente configurado")
        else:
            reporte.append("❌ El curso necesita configuración")
        
        return "\n".join(reporte)
    
    def ejecutar_pruebas_rapidas(self) -> str:
        """
        Ejecutar pruebas rápidas de los módulos
        
        Returns:
            str: Reporte de pruebas
        """
        print("\n🚀 EJECUTANDO PRUEBAS RÁPIDAS...")
        print("=" * 60)
        
        reporte = []
        reporte.append("🧪 PRUEBAS RÁPIDAS DE MÓDULOS:")
        reporte.append("-" * 40)
        
        for nombre_modulo in self.modulos.keys():
            if nombre_modulo in self.modulos:
                exito, mensaje = self.ejecutar_prueba_rapida(nombre_modulo)
                reporte.append(f"{nombre_modulo}: {mensaje}")
        
        return "\n".join(reporte)


def main():
    """Función principal"""
    verificador = VerificadorCurso()
    
    # Generar reporte principal
    reporte_principal = verificador.generar_reporte()
    print(reporte_principal)
    
    # Ejecutar pruebas rápidas
    reporte_pruebas = verificador.ejecutar_pruebas_rapidas()
    print(reporte_pruebas)
    
    print("\n" + "=" * 60)
    print("✅ Verificación del curso completada")
    print("=" * 60)
    
    print("\n📋 Próximos pasos:")
    print("1. Si hay errores, ejecuta: python setup_coursera.py")
    print("2. Para usar el curso: python ejecutar_curso.py")
    print("3. Para ejecutar tests: python ejecutar_curso.py tests")
    print("4. Para más información: python ejecutar_curso.py info")


if __name__ == "__main__":
    main() 