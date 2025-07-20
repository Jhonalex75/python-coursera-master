#!/usr/bin/env python3
"""
Módulo 6: Manejo de Errores y Debugging
=======================================

Este módulo cubre técnicas avanzadas de debugging y manejo de errores:
- Técnicas de debugging con print
- Logging avanzado
- Manejo de excepciones
- Herramientas de diagnóstico
- Casos de estudio reales

Autor: Ing. Jhon A. Valencia
Curso: Python de Coursera
Basado en: debugging_toolkit_examples.py
"""

import logging
import time
import sys
import traceback
from datetime import datetime
from typing import List, Dict, Any, Optional

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

def configurar_logging():
    """Configura el sistema de logging para debugging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        handlers=[
            logging.FileHandler('debug_toolkit.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

# ============================================================================
# 1. DEBUGGING CON PRINT STATEMENTS
# ============================================================================

def ejemplo_print_statements():
    """Demuestra técnicas de debugging con print statements."""
    print("=" * 60)
    print("1. DEBUGGING CON PRINT STATEMENTS")
    print("=" * 60)
    
    def calcular_promedio_basico(numeros):
        """Función básica sin debugging."""
        total = sum(numeros)
        count = len(numeros)
        return total / count
    
    def calcular_promedio_con_debug(numeros):
        """Misma función con print statements para debugging."""
        print(f"DEBUG: Entrada - numeros = {numeros}")
        print(f"DEBUG: Tipo de numeros = {type(numeros)}")
        
        total = sum(numeros)
        print(f"DEBUG: Total calculado = {total}")
        
        count = len(numeros)
        print(f"DEBUG: Cantidad de elementos = {count}")
        
        if count == 0:
            print("DEBUG: ¡ADVERTENCIA! Lista vacía detectada")
            return 0
        
        promedio = total / count
        print(f"DEBUG: Promedio calculado = {promedio}")
        
        return promedio
    
    # Test con datos normales
    print("Test con datos normales:")
    datos_normales = [10, 20, 30, 40, 50]
    resultado1 = calcular_promedio_basico(datos_normales)
    print(f"Resultado básico: {resultado1}")
    
    print("\nTest con debugging:")
    resultado2 = calcular_promedio_con_debug(datos_normales)
    print(f"Resultado con debug: {resultado2}")
    
    # Test con datos problemáticos
    print("\nTest con lista vacía:")
    try:
        resultado3 = calcular_promedio_con_debug([])
        print(f"Resultado con lista vacía: {resultado3}")
    except ZeroDivisionError as e:
        print(f"Error capturado: {e}")
        print("Los print statements nos ayudaron a identificar el problema!")

# ============================================================================
# 2. LOGGING AVANZADO
# ============================================================================

def ejemplo_logging_avanzado():
    """Demuestra logging avanzado para debugging."""
    print("\n" + "=" * 60)
    print("2. LOGGING AVANZADO")
    print("=" * 60)
    
    def procesar_datos_usuario(datos_usuario: Dict[str, Any]) -> bool:
        """Procesa datos de usuario con logging detallado."""
        logging.info(f"Iniciando procesamiento para usuario: {datos_usuario.get('nombre', 'Desconocido')}")
        
        try:
            # Validar estructura de datos
            logging.debug("Validando estructura de datos de usuario")
            campos_requeridos = ['nombre', 'edad', 'email']
            
            for campo in campos_requeridos:
                if campo not in datos_usuario:
                    logging.warning(f"Campo requerido faltante: {campo}")
                    return False
            
            # Procesar edad
            edad = datos_usuario['edad']
            logging.debug(f"Procesando edad: {edad}")
            
            if not isinstance(edad, int):
                logging.error(f"Edad debe ser entero, recibido: {type(edad)}")
                return False
            
            if edad < 0 or edad > 120:
                logging.error(f"Edad inválida: {edad}")
                return False
            
            # Procesar email
            email = datos_usuario['email']
            logging.debug(f"Procesando email: {email}")
            
            if '@' not in email or '.' not in email:
                logging.error(f"Formato de email inválido: {email}")
                return False
            
            logging.info("Datos de usuario procesados exitosamente")
            return True
            
        except Exception as e:
            logging.error(f"Error inesperado procesando datos: {e}")
            logging.debug(f"Traceback completo: {traceback.format_exc()}")
            return False
    
    # Casos de prueba
    casos_prueba = [
        {'nombre': 'Ana', 'edad': 25, 'email': 'ana@ejemplo.com'},
        {'nombre': 'Bob', 'edad': -5, 'email': 'bob@ejemplo.com'},
        {'nombre': 'Carlos', 'edad': 30, 'email': 'email-invalido'},
        {'nombre': 'Diana', 'edad': 35},  # Falta email
        {'nombre': 'Eva', 'edad': 'treinta', 'email': 'eva@ejemplo.com'}  # Edad como string
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\nProcesando caso {i}: {caso.get('nombre', 'Desconocido')}")
        exito = procesar_datos_usuario(caso)
        print(f"Resultado: {'ÉXITO' if exito else 'FALLÓ'}")

# ============================================================================
# 3. MANEJO DE EXCEPCIONES ESPECÍFICAS
# ============================================================================

def ejemplo_manejo_excepciones():
    """Demuestra manejo específico de diferentes tipos de excepciones."""
    print("\n" + "=" * 60)
    print("3. MANEJO DE EXCEPCIONES ESPECÍFICAS")
    print("=" * 60)
    
    def procesar_archivo_seguro(nombre_archivo: str) -> Optional[str]:
        """Procesa un archivo con manejo robusto de errores."""
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                logging.info(f"Archivo {nombre_archivo} leído exitosamente")
                return contenido
                
        except FileNotFoundError:
            logging.error(f"Archivo no encontrado: {nombre_archivo}")
            print(f"Error: El archivo '{nombre_archivo}' no existe")
            return None
            
        except PermissionError:
            logging.error(f"Permiso denegado para archivo: {nombre_archivo}")
            print(f"Error: No tienes permisos para leer '{nombre_archivo}'")
            return None
            
        except UnicodeDecodeError as e:
            logging.error(f"Error de codificación en archivo {nombre_archivo}: {e}")
            print(f"Error: El archivo '{nombre_archivo}' tiene codificación inválida")
            return None
            
        except Exception as e:
            logging.error(f"Error inesperado procesando archivo {nombre_archivo}: {e}")
            print(f"Error inesperado: {e}")
            return None
    
    def dividir_numeros_seguro(a: Any, b: Any) -> Optional[float]:
        """Divide dos números con manejo de errores."""
        try:
            # Convertir a float si es necesario
            num_a = float(a)
            num_b = float(b)
            
            resultado = num_a / num_b
            logging.info(f"División exitosa: {num_a} / {num_b} = {resultado}")
            return resultado
            
        except ValueError as e:
            logging.error(f"Error de conversión: {e}")
            print(f"Error: Los valores deben ser numéricos")
            return None
            
        except ZeroDivisionError:
            logging.error("División por cero")
            print("Error: No se puede dividir por cero")
            return None
            
        except Exception as e:
            logging.error(f"Error inesperado en división: {e}")
            print(f"Error inesperado: {e}")
            return None
    
    # Pruebas de manejo de archivos
    print("Pruebas de manejo de archivos:")
    archivos_prueba = [
        "archivo_inexistente.txt",
        "archivo_sin_permisos.txt",
        "archivo_valido.txt"
    ]
    
    for archivo in archivos_prueba:
        resultado = procesar_archivo_seguro(archivo)
        if resultado:
            print(f"Contenido de {archivo}: {len(resultado)} caracteres")
    
    # Pruebas de división
    print(f"\nPruebas de división:")
    casos_division = [
        (10, 2),
        (10, 0),
        ("10", "2"),
        ("abc", "def"),
        (10, "0")
    ]
    
    for a, b in casos_division:
        resultado = dividir_numeros_seguro(a, b)
        if resultado is not None:
            print(f"{a} / {b} = {resultado}")
        else:
            print(f"No se pudo calcular {a} / {b}")

# ============================================================================
# 4. ASSERTIONS PARA VALIDACIÓN
# ============================================================================

def ejemplo_assertions():
    """Demuestra el uso de assertions para validación."""
    print("\n" + "=" * 60)
    print("4. ASSERTIONS PARA VALIDACIÓN")
    print("=" * 60)
    
    def calcular_area_rectangulo(largo: float, ancho: float) -> float:
        """Calcula el área de un rectángulo con assertions."""
        assert largo > 0, f"El largo debe ser positivo, recibido: {largo}"
        assert ancho > 0, f"El ancho debe ser positivo, recibido: {ancho}"
        assert isinstance(largo, (int, float)), f"El largo debe ser numérico, recibido: {type(largo)}"
        assert isinstance(ancho, (int, float)), f"El ancho debe ser numérico, recibido: {type(ancho)}"
        
        area = largo * ancho
        assert area > 0, f"El área calculada debe ser positiva, calculada: {area}"
        
        return area
    
    def calcular_porcentaje(total: float, parte: float) -> float:
        """Calcula porcentaje con assertions."""
        assert total > 0, f"El total debe ser positivo, recibido: {total}"
        assert parte >= 0, f"La parte debe ser no negativa, recibido: {parte}"
        assert parte <= total, f"La parte ({parte}) no puede ser mayor que el total ({total})"
        
        porcentaje = (parte / total) * 100
        assert 0 <= porcentaje <= 100, f"El porcentaje debe estar entre 0-100, calculado: {porcentaje}"
        
        return porcentaje
    
    # Test casos válidos
    print("Test casos válidos:")
    try:
        area1 = calcular_area_rectangulo(5, 3)
        print(f"Área del rectángulo: {area1}")
        
        porcentaje1 = calcular_porcentaje(100, 25)
        print(f"Porcentaje: {porcentaje1}%")
    except AssertionError as e:
        print(f"Assertion falló: {e}")
    
    # Test casos inválidos
    print(f"\nTest casos inválidos:")
    casos_invalidos = [
        ("Largo negativo", lambda: calcular_area_rectangulo(-5, 3)),
        ("Ancho cero", lambda: calcular_area_rectangulo(5, 0)),
        ("Entrada string", lambda: calcular_area_rectangulo("5", 3)),
        ("Porcentaje inválido", lambda: calcular_porcentaje(100, 150))
    ]
    
    for descripcion, test_func in casos_invalidos:
        try:
            test_func()
            print(f"❌ {descripcion}: No se detectó el error")
        except AssertionError as e:
            print(f"✅ {descripcion}: {e}")

# ============================================================================
# 5. DEBUGGER INTERACTIVO
# ============================================================================

def ejemplo_debugger():
    """Demuestra el uso del debugger de Python."""
    print("\n" + "=" * 60)
    print("5. DEBUGGER INTERACTIVO")
    print("=" * 60)
    
    def funcion_compleja_datos(datos: List[int]) -> Dict[str, Any]:
        """Función compleja para demostrar debugging."""
        resultado = {
            'suma': 0,
            'promedio': 0,
            'maximo': None,
            'minimo': None,
            'cantidad': 0
        }
        
        # Punto de debugging (comentado para evitar interacción)
        # import pdb; pdb.set_trace()
        
        if not datos:
            logging.warning("Lista de datos vacía")
            return resultado
        
        resultado['cantidad'] = len(datos)
        resultado['suma'] = sum(datos)
        resultado['promedio'] = resultado['suma'] / resultado['cantidad']
        resultado['maximo'] = max(datos)
        resultado['minimo'] = min(datos)
        
        return resultado
    
    # Simulación de debugging
    print("Simulación de debugging:")
    datos_prueba = [10, 20, 30, 40, 50]
    print(f"Datos de entrada: {datos_prueba}")
    
    # Simular pasos del debugger
    print("Paso 1: Verificando si la lista no está vacía")
    print("Paso 2: Calculando cantidad de elementos")
    print("Paso 3: Calculando suma")
    print("Paso 4: Calculando promedio")
    print("Paso 5: Encontrando máximo y mínimo")
    
    resultado = funcion_compleja_datos(datos_prueba)
    print(f"Resultado final: {resultado}")

# ============================================================================
# 6. CASO DE ESTUDIO: PROCESAMIENTO DE DATOS
# ============================================================================

def caso_estudio_procesamiento():
    """Caso de estudio real de debugging en procesamiento de datos."""
    print("\n" + "=" * 60)
    print("6. CASO DE ESTUDIO: PROCESAMIENTO DE DATOS")
    print("=" * 60)
    
    def procesar_ventas_datos(datos_ventas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Procesa datos de ventas con debugging completo."""
        logging.info(f"Iniciando procesamiento de {len(datos_ventas)} registros de ventas")
        
        resultado = {
            'total_ventas': 0,
            'cantidad_transacciones': 0,
            'promedio_venta': 0,
            'productos_vendidos': set(),
            'errores_encontrados': []
        }
        
        for i, venta in enumerate(datos_ventas):
            try:
                logging.debug(f"Procesando venta {i+1}: {venta}")
                
                # Validar estructura de venta
                if 'monto' not in venta:
                    error_msg = f"Venta {i+1}: Falta campo 'monto'"
                    logging.error(error_msg)
                    resultado['errores_encontrados'].append(error_msg)
                    continue
                
                if 'producto' not in venta:
                    error_msg = f"Venta {i+1}: Falta campo 'producto'"
                    logging.error(error_msg)
                    resultado['errores_encontrados'].append(error_msg)
                    continue
                
                # Procesar monto
                monto = venta['monto']
                if not isinstance(monto, (int, float)):
                    error_msg = f"Venta {i+1}: Monto debe ser numérico, recibido {type(monto)}"
                    logging.error(error_msg)
                    resultado['errores_encontrados'].append(error_msg)
                    continue
                
                if monto < 0:
                    error_msg = f"Venta {i+1}: Monto negativo: {monto}"
                    logging.warning(error_msg)
                    resultado['errores_encontrados'].append(error_msg)
                    continue
                
                # Actualizar estadísticas
                resultado['total_ventas'] += monto
                resultado['cantidad_transacciones'] += 1
                resultado['productos_vendidos'].add(venta['producto'])
                
                logging.debug(f"Venta {i+1} procesada exitosamente: ${monto}")
                
            except Exception as e:
                error_msg = f"Venta {i+1}: Error inesperado - {e}"
                logging.error(error_msg)
                resultado['errores_encontrados'].append(error_msg)
        
        # Calcular promedio
        if resultado['cantidad_transacciones'] > 0:
            resultado['promedio_venta'] = resultado['total_ventas'] / resultado['cantidad_transacciones']
        
        # Convertir set a lista para serialización
        resultado['productos_vendidos'] = list(resultado['productos_vendidos'])
        
        logging.info(f"Procesamiento completado. Transacciones válidas: {resultado['cantidad_transacciones']}")
        return resultado
    
    # Datos de prueba con errores
    datos_ventas_prueba = [
        {'monto': 100, 'producto': 'Laptop'},
        {'monto': 50, 'producto': 'Mouse'},
        {'monto': -25, 'producto': 'Teclado'},  # Monto negativo
        {'monto': 'abc', 'producto': 'Monitor'},  # Monto inválido
        {'producto': 'Auriculares'},  # Falta monto
        {'monto': 75},  # Falta producto
        {'monto': 200, 'producto': 'Laptop'},
        {'monto': 150, 'producto': 'Tablet'}
    ]
    
    print("Procesando datos de ventas con errores...")
    resultado = procesar_ventas_datos(datos_ventas_prueba)
    
    print(f"\nResultados del procesamiento:")
    print(f"Total de ventas: ${resultado['total_ventas']}")
    print(f"Transacciones válidas: {resultado['cantidad_transacciones']}")
    print(f"Promedio por venta: ${resultado['promedio_venta']:.2f}")
    print(f"Productos vendidos: {resultado['productos_vendidos']}")
    print(f"Errores encontrados: {len(resultado['errores_encontrados'])}")
    
    if resultado['errores_encontrados']:
        print(f"\nDetalle de errores:")
        for error in resultado['errores_encontrados']:
            print(f"  - {error}")

# ============================================================================
# 7. EJERCICIOS PRÁCTICOS
# ============================================================================

def ejercicios_practicos():
    """Ejercicios prácticos de debugging."""
    print("\n" + "=" * 60)
    print("7. EJERCICIOS PRÁCTICOS")
    print("=" * 60)
    
    # Ejercicio 1: Debugging de función de cálculo
    print("Ejercicio 1: Debugging de función de cálculo")
    
    def funcion_con_bug(numeros):
        """Función con bug para debugging."""
        total = 0
        for i in range(len(numeros)):
            total += numeros[i]  # Bug: debería ser numeros[i]
        return total / len(numeros)
    
    def funcion_debuggeada(numeros):
        """Versión debuggeada de la función."""
        print(f"DEBUG: Entrada - numeros = {numeros}")
        print(f"DEBUG: Tipo de numeros = {type(numeros)}")
        
        if not numeros:
            print("DEBUG: Lista vacía detectada")
            return 0
        
        total = 0
        print(f"DEBUG: Iniciando suma de {len(numeros)} elementos")
        
        for i in range(len(numeros)):
            valor = numeros[i]
            total += valor
            print(f"DEBUG: Elemento {i} = {valor}, Total acumulado = {total}")
        
        promedio = total / len(numeros)
        print(f"DEBUG: Promedio calculado = {promedio}")
        return promedio
    
    datos = [10, 20, 30, 40]
    print(f"Datos: {datos}")
    
    try:
        resultado_bug = funcion_con_bug(datos)
        print(f"Resultado con bug: {resultado_bug}")
    except Exception as e:
        print(f"Error en función con bug: {e}")
    
    resultado_debug = funcion_debuggeada(datos)
    print(f"Resultado debuggeado: {resultado_debug}")
    
    # Ejercicio 2: Validación de datos con logging
    print(f"\nEjercicio 2: Validación de datos con logging")
    
    def validar_usuario_datos(nombre, edad, email):
        """Valida datos de usuario con logging detallado."""
        logging.info(f"Validando datos para usuario: {nombre}")
        
        errores = []
        
        # Validar nombre
        if not nombre or not isinstance(nombre, str):
            logging.error(f"Nombre inválido: {nombre}")
            errores.append("Nombre debe ser una cadena no vacía")
        
        # Validar edad
        if not isinstance(edad, int):
            logging.error(f"Edad debe ser entero, recibido: {type(edad)}")
            errores.append("Edad debe ser un número entero")
        elif edad < 0 or edad > 120:
            logging.error(f"Edad fuera de rango: {edad}")
            errores.append("Edad debe estar entre 0 y 120")
        
        # Validar email
        if not email or '@' not in email:
            logging.error(f"Email inválido: {email}")
            errores.append("Email debe contener '@'")
        
        if errores:
            logging.warning(f"Usuario {nombre} tiene {len(errores)} errores de validación")
            return False, errores
        else:
            logging.info(f"Usuario {nombre} validado exitosamente")
            return True, []
    
    casos_validacion = [
        ("Ana", 25, "ana@ejemplo.com"),
        ("", 30, "bob@ejemplo.com"),
        ("Carlos", "treinta", "carlos@ejemplo.com"),
        ("Diana", 150, "diana@ejemplo.com"),
        ("Eva", 35, "email-invalido")
    ]
    
    for nombre, edad, email in casos_validacion:
        print(f"\nValidando: {nombre}, {edad}, {email}")
        valido, errores = validar_usuario_datos(nombre, edad, email)
        if valido:
            print("✅ Datos válidos")
        else:
            print("❌ Datos inválidos:")
            for error in errores:
                print(f"  - {error}")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🐍 MÓDULO 6: MANEJO DE ERRORES Y DEBUGGING")
    print("Técnicas Avanzadas de Debugging")
    print("=" * 60)
    
    # Configurar logging
    configurar_logging()
    
    # Ejecutar todos los ejemplos
    ejemplo_print_statements()
    ejemplo_logging_avanzado()
    ejemplo_manejo_excepciones()
    ejemplo_assertions()
    ejemplo_debugger()
    caso_estudio_procesamiento()
    ejercicios_practicos()
    
    print("\n" + "=" * 60)
    print("✅ MÓDULO 6 COMPLETADO")
    print("=" * 60)
    print("Conceptos cubiertos:")
    print("• Debugging con print statements")
    print("• Logging avanzado y configuración")
    print("• Manejo específico de excepciones")
    print("• Uso de assertions para validación")
    print("• Debugger interactivo")
    print("• Casos de estudio reales")
    print("• Ejercicios prácticos de debugging")

if __name__ == "__main__":
    main() 