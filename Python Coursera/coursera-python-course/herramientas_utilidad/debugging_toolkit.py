#!/usr/bin/env python3
"""
Debugging Toolkit: Essential Techniques for Python Developers
============================================================

This file demonstrates various debugging techniques including:
1. Print statements for quick debugging
2. Logging for detailed event tracking
3. Assertions for validation
4. Debugger usage examples
5. Real-world debugging scenarios

Autor: Ing. Jhon A. Valencia
Curso: Python de Coursera
Versión mejorada del debugging_toolkit_examples.py original
"""

import logging
import time
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
import traceback
import json
import os

# ============================================================================
# CONFIGURACIÓN DE LOGGING MEJORADA
# ============================================================================

def configurar_logging_avanzado(nivel=logging.DEBUG, archivo_log='debug_toolkit.log'):
    """Configura logging avanzado con múltiples handlers."""
    # Crear formateador personalizado
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler(archivo_log, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configurar logger raíz
    logging.basicConfig(
        level=nivel,
        handlers=[file_handler, console_handler],
        force=True
    )
    
    return logging.getLogger(__name__)

# ============================================================================
# 1. PRINT STATEMENTS MEJORADOS
# ============================================================================

class DebugPrinter:
    """Clase para debugging con print statements mejorados."""
    
    def __init__(self, habilitado=True, prefijo="DEBUG"):
        self.habilitado = habilitado
        self.prefijo = prefijo
        self.contador = 0
    
    def print(self, mensaje: str, datos: Any = None):
        """Imprime mensaje de debug con formato mejorado."""
        if not self.habilitado:
            return
        
        self.contador += 1
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"[{timestamp}] {self.prefijo} #{self.contador}: {mensaje}")
        if datos is not None:
            print(f"  Datos: {datos}")
    
    def print_variable(self, nombre: str, valor: Any):
        """Imprime el valor de una variable específica."""
        self.print(f"Variable '{nombre}'", valor)
    
    def print_function_call(self, nombre_funcion: str, args: tuple = None, kwargs: dict = None):
        """Imprime información de llamada a función."""
        call_info = f"Llamando a {nombre_funcion}"
        if args:
            call_info += f" con args: {args}"
        if kwargs:
            call_info += f" con kwargs: {kwargs}"
        self.print(call_info)
    
    def print_function_return(self, nombre_funcion: str, valor_retorno: Any):
        """Imprime el valor de retorno de una función."""
        self.print(f"Retorno de {nombre_funcion}", valor_retorno)

def ejemplo_print_statements_mejorado():
    """Demuestra print statements mejorados para debugging."""
    print("\n" + "="*60)
    print("1. PRINT STATEMENTS MEJORADOS")
    print("="*60)
    
    debug = DebugPrinter(habilitado=True, prefijo="DEBUG")
    
    def calcular_estadisticas_avanzadas(numeros: List[float]) -> Dict[str, float]:
        """Función con debugging mejorado."""
        debug.print_function_call("calcular_estadisticas_avanzadas", (numeros,))
        debug.print_variable("numeros", numeros)
        
        if not numeros:
            debug.print("Lista vacía detectada")
            debug.print_function_return("calcular_estadisticas_avanzadas", {})
            return {}
        
        # Calcular suma
        suma = sum(numeros)
        debug.print_variable("suma", suma)
        
        # Calcular promedio
        promedio = suma / len(numeros)
        debug.print_variable("promedio", promedio)
        
        # Calcular máximo y mínimo
        maximo = max(numeros)
        minimo = min(numeros)
        debug.print_variable("maximo", maximo)
        debug.print_variable("minimo", minimo)
        
        # Calcular varianza
        varianza = sum((x - promedio) ** 2 for x in numeros) / len(numeros)
        debug.print_variable("varianza", varianza)
        
        resultado = {
            'suma': suma,
            'promedio': promedio,
            'maximo': maximo,
            'minimo': minimo,
            'varianza': varianza,
            'cantidad': len(numeros)
        }
        
        debug.print_function_return("calcular_estadisticas_avanzadas", resultado)
        return resultado
    
    # Test con datos normales
    print("Test con datos normales:")
    datos = [10.5, 20.3, 15.7, 8.9, 12.1]
    resultado = calcular_estadisticas_avanzadas(datos)
    print(f"Resultado final: {resultado}")
    
    # Test con lista vacía
    print("\nTest con lista vacía:")
    resultado_vacio = calcular_estadisticas_avanzadas([])
    print(f"Resultado con lista vacía: {resultado_vacio}")

# ============================================================================
# 2. LOGGING AVANZADO CON CONTEXTO
# ============================================================================

class ContextLogger:
    """Logger con contexto para debugging avanzado."""
    
    def __init__(self, nombre: str):
        self.logger = logging.getLogger(nombre)
        self.contexto = {}
    
    def agregar_contexto(self, clave: str, valor: Any):
        """Agrega información al contexto de debugging."""
        self.contexto[clave] = valor
    
    def limpiar_contexto(self):
        """Limpia el contexto de debugging."""
        self.contexto.clear()
    
    def log_con_contexto(self, nivel: str, mensaje: str, datos: Any = None):
        """Log con contexto incluido."""
        contexto_str = f" | Contexto: {self.contexto}" if self.contexto else ""
        mensaje_completo = f"{mensaje}{contexto_str}"
        
        if datos is not None:
            mensaje_completo += f" | Datos: {datos}"
        
        if nivel.upper() == 'DEBUG':
            self.logger.debug(mensaje_completo)
        elif nivel.upper() == 'INFO':
            self.logger.info(mensaje_completo)
        elif nivel.upper() == 'WARNING':
            self.logger.warning(mensaje_completo)
        elif nivel.upper() == 'ERROR':
            self.logger.error(mensaje_completo)
        elif nivel.upper() == 'CRITICAL':
            self.logger.critical(mensaje_completo)

def ejemplo_logging_avanzado():
    """Demuestra logging avanzado con contexto."""
    print("\n" + "="*60)
    print("2. LOGGING AVANZADO CON CONTEXTO")
    print("="*60)
    
    logger = ContextLogger("ProcesamientoDatos")
    
    def procesar_archivo_complejo(nombre_archivo: str, usuario: str) -> Dict[str, Any]:
        """Procesa archivo con logging contextual."""
        logger.agregar_contexto("archivo", nombre_archivo)
        logger.agregar_contexto("usuario", usuario)
        logger.agregar_contexto("timestamp", datetime.now().isoformat())
        
        logger.log_con_contexto("INFO", "Iniciando procesamiento de archivo")
        
        resultado = {
            'archivo': nombre_archivo,
            'usuario': usuario,
            'lineas_procesadas': 0,
            'errores': [],
            'estadisticas': {}
        }
        
        try:
            # Simular procesamiento
            logger.log_con_contexto("DEBUG", "Abriendo archivo")
            
            # Simular lectura de líneas
            lineas_simuladas = ["línea1", "línea2", "línea3", "línea4", "línea5"]
            resultado['lineas_procesadas'] = len(lineas_simuladas)
            
            logger.log_con_contexto("INFO", f"Procesadas {len(lineas_simuladas)} líneas")
            
            # Simular estadísticas
            resultado['estadisticas'] = {
                'caracteres_totales': sum(len(linea) for linea in lineas_simuladas),
                'linea_mas_larga': max(lineas_simuladas, key=len),
                'promedio_caracteres': sum(len(linea) for linea in lineas_simuladas) / len(lineas_simuladas)
            }
            
            logger.log_con_contexto("INFO", "Procesamiento completado exitosamente", resultado['estadisticas'])
            
        except Exception as e:
            logger.log_con_contexto("ERROR", f"Error durante procesamiento: {e}")
            resultado['errores'].append(str(e))
        
        finally:
            logger.limpiar_contexto()
        
        return resultado
    
    # Procesar archivos de ejemplo
    archivos_ejemplo = [
        ("datos1.txt", "usuario1"),
        ("datos2.txt", "usuario2"),
        ("datos3.txt", "usuario3")
    ]
    
    for archivo, usuario in archivos_ejemplo:
        print(f"\nProcesando {archivo} para {usuario}:")
        resultado = procesar_archivo_complejo(archivo, usuario)
        print(f"Resultado: {resultado['lineas_procesadas']} líneas procesadas")

# ============================================================================
# 3. ASSERTIONS AVANZADAS
# ============================================================================

class Validator:
    """Clase para validaciones avanzadas con assertions."""
    
    @staticmethod
    def validar_tipo(valor: Any, tipo_esperado: type, nombre_variable: str = "variable"):
        """Valida el tipo de una variable."""
        assert isinstance(valor, tipo_esperado), \
            f"{nombre_variable} debe ser de tipo {tipo_esperado.__name__}, recibido {type(valor).__name__}"
    
    @staticmethod
    def validar_rango(valor: float, min_valor: float, max_valor: float, nombre_variable: str = "variable"):
        """Valida que un valor esté en un rango específico."""
        assert min_valor <= valor <= max_valor, \
            f"{nombre_variable} debe estar entre {min_valor} y {max_valor}, recibido {valor}"
    
    @staticmethod
    def validar_no_vacio(valor: Any, nombre_variable: str = "variable"):
        """Valida que una variable no esté vacía."""
        if isinstance(valor, (list, tuple, str)):
            assert len(valor) > 0, f"{nombre_variable} no puede estar vacío"
        else:
            assert valor is not None, f"{nombre_variable} no puede ser None"
    
    @staticmethod
    def validar_condicion(condicion: bool, mensaje: str):
        """Valida una condición personalizada."""
        assert condicion, mensaje

def ejemplo_assertions_avanzadas():
    """Demuestra assertions avanzadas para validación."""
    print("\n" + "="*60)
    print("3. ASSERTIONS AVANZADAS")
    print("="*60)
    
    def procesar_datos_validados(datos: List[float], factor: float) -> List[float]:
        """Procesa datos con validaciones avanzadas."""
        # Validaciones de entrada
        Validator.validar_tipo(datos, list, "datos")
        Validator.validar_no_vacio(datos, "datos")
        Validator.validar_tipo(factor, (int, float), "factor")
        Validator.validar_rango(factor, 0.1, 10.0, "factor")
        
        # Validar que todos los elementos sean numéricos
        for i, valor in enumerate(datos):
            Validator.validar_tipo(valor, (int, float), f"datos[{i}]")
            Validator.validar_rango(valor, -1000, 1000, f"datos[{i}]")
        
        # Procesar datos
        resultado = [valor * factor for valor in datos]
        
        # Validaciones de salida
        Validator.validar_tipo(resultado, list, "resultado")
        Validator.validar_condicion(len(resultado) == len(datos), 
                                  "El resultado debe tener la misma longitud que los datos de entrada")
        
        return resultado
    
    # Test casos válidos
    print("Test casos válidos:")
    try:
        datos_validos = [10, 20, 30, 40]
        factor_valido = 2.5
        resultado = procesar_datos_validados(datos_validos, factor_valido)
        print(f"Resultado: {resultado}")
    except AssertionError as e:
        print(f"Error de validación: {e}")
    
    # Test casos inválidos
    print(f"\nTest casos inválidos:")
    casos_invalidos = [
        ("Lista vacía", lambda: procesar_datos_validados([], 2.0)),
        ("Factor fuera de rango", lambda: procesar_datos_validados([1, 2, 3], 20.0)),
        ("Datos no numéricos", lambda: procesar_datos_validados([1, "abc", 3], 2.0)),
        ("Factor negativo", lambda: procesar_datos_validados([1, 2, 3], -1.0))
    ]
    
    for descripcion, test_func in casos_invalidos:
        try:
            test_func()
            print(f"❌ {descripcion}: No se detectó el error")
        except AssertionError as e:
            print(f"✅ {descripcion}: {e}")

# ============================================================================
# 4. DEBUGGER INTERACTIVO MEJORADO
# ============================================================================

class DebuggerHelper:
    """Helper para debugging interactivo."""
    
    @staticmethod
    def inspeccionar_variable(nombre: str, valor: Any):
        """Inspecciona una variable en detalle."""
        print(f"\n🔍 INSPECCIÓN DE VARIABLE: {nombre}")
        print(f"  Tipo: {type(valor).__name__}")
        print(f"  Valor: {valor}")
        print(f"  Longitud: {len(valor) if hasattr(valor, '__len__') else 'N/A'}")
        
        if isinstance(valor, (list, tuple)):
            print(f"  Elementos: {len(valor)}")
            for i, elem in enumerate(valor[:5]):  # Mostrar solo los primeros 5
                print(f"    [{i}]: {elem} ({type(elem).__name__})")
            if len(valor) > 5:
                print(f"    ... y {len(valor) - 5} elementos más")
        
        elif isinstance(valor, dict):
            print(f"  Claves: {list(valor.keys())}")
            for clave, valor_clave in list(valor.items())[:5]:
                print(f"    '{clave}': {valor_clave} ({type(valor_clave).__name__})")
            if len(valor) > 5:
                print(f"    ... y {len(valor) - 5} claves más")
    
    @staticmethod
    def comparar_variables(var1_nombre: str, var1_valor: Any, var2_nombre: str, var2_valor: Any):
        """Compara dos variables."""
        print(f"\n⚖️ COMPARACIÓN DE VARIABLES")
        print(f"  {var1_nombre}: {var1_valor} ({type(var1_valor).__name__})")
        print(f"  {var2_nombre}: {var2_valor} ({type(var2_valor).__name__})")
        print(f"  Iguales: {var1_valor == var2_valor}")
        print(f"  Mismo tipo: {type(var1_valor) == type(var2_valor)}")
    
    @staticmethod
    def punto_de_control(mensaje: str = "Punto de control alcanzado"):
        """Punto de control para debugging."""
        print(f"\n⏸️ PUNTO DE CONTROL: {mensaje}")
        print("  Presiona Enter para continuar...")
        input()

def ejemplo_debugger_mejorado():
    """Demuestra debugging interactivo mejorado."""
    print("\n" + "="*60)
    print("4. DEBUGGER INTERACTIVO MEJORADO")
    print("="*60)
    
    def funcion_compleja_debuggeada(datos_entrada: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Función compleja con debugging interactivo."""
        debug_helper = DebuggerHelper()
        
        debug_helper.inspeccionar_variable("datos_entrada", datos_entrada)
        
        # Punto de control opcional
        # debug_helper.punto_de_control("Antes de procesar datos")
        
        resultado = {
            'total_elementos': 0,
            'elementos_procesados': 0,
            'errores': [],
            'estadisticas': {}
        }
        
        resultado['total_elementos'] = len(datos_entrada)
        debug_helper.inspeccionar_variable("resultado_inicial", resultado)
        
        for i, elemento in enumerate(datos_entrada):
            try:
                debug_helper.inspeccionar_variable(f"elemento_{i}", elemento)
                
                # Procesar elemento
                if 'valor' in elemento and isinstance(elemento['valor'], (int, float)):
                    resultado['elementos_procesados'] += 1
                else:
                    resultado['errores'].append(f"Elemento {i}: valor inválido")
                
            except Exception as e:
                resultado['errores'].append(f"Elemento {i}: {e}")
        
        # Calcular estadísticas
        if resultado['elementos_procesados'] > 0:
            valores_validos = [elem['valor'] for elem in datos_entrada 
                             if 'valor' in elem and isinstance(elem['valor'], (int, float))]
            resultado['estadisticas'] = {
                'promedio': sum(valores_validos) / len(valores_validos),
                'maximo': max(valores_validos),
                'minimo': min(valores_validos)
            }
        
        debug_helper.inspeccionar_variable("resultado_final", resultado)
        return resultado
    
    # Datos de prueba
    datos_prueba = [
        {'id': 1, 'valor': 10.5, 'categoria': 'A'},
        {'id': 2, 'valor': 20.3, 'categoria': 'B'},
        {'id': 3, 'valor': 'invalido', 'categoria': 'C'},  # Valor inválido
        {'id': 4, 'categoria': 'D'},  # Falta valor
        {'id': 5, 'valor': 15.7, 'categoria': 'A'}
    ]
    
    print("Procesando datos con debugging interactivo...")
    resultado = funcion_compleja_debuggeada(datos_prueba)
    print(f"\nResultado final: {resultado}")

# ============================================================================
# 5. CASO DE ESTUDIO: SISTEMA DE PROCESAMIENTO DE PEDIDOS
# ============================================================================

def caso_estudio_sistema_pedidos():
    """Caso de estudio completo: Sistema de procesamiento de pedidos."""
    print("\n" + "="*60)
    print("5. CASO DE ESTUDIO: SISTEMA DE PROCESAMIENTO DE PEDIDOS")
    print("="*60)
    
    class SistemaPedidos:
        """Sistema de procesamiento de pedidos con debugging completo."""
        
        def __init__(self):
            self.logger = ContextLogger("SistemaPedidos")
            self.debug = DebugPrinter(habilitado=True, prefijo="PEDIDOS")
            self.pedidos_procesados = 0
            self.errores_totales = 0
        
        def validar_pedido(self, pedido: Dict[str, Any]) -> bool:
            """Valida un pedido con debugging detallado."""
            self.debug.print_function_call("validar_pedido", (pedido,))
            
            # Validaciones básicas
            campos_requeridos = ['id', 'cliente', 'productos', 'total']
            
            for campo in campos_requeridos:
                if campo not in pedido:
                    self.debug.print(f"Campo requerido faltante: {campo}")
                    return False
            
            # Validar ID
            if not isinstance(pedido['id'], int) or pedido['id'] <= 0:
                self.debug.print("ID inválido", pedido['id'])
                return False
            
            # Validar cliente
            if not isinstance(pedido['cliente'], str) or len(pedido['cliente'].strip()) == 0:
                self.debug.print("Cliente inválido", pedido['cliente'])
                return False
            
            # Validar productos
            if not isinstance(pedido['productos'], list) or len(pedido['productos']) == 0:
                self.debug.print("Lista de productos inválida", pedido['productos'])
                return False
            
            # Validar total
            if not isinstance(pedido['total'], (int, float)) or pedido['total'] <= 0:
                self.debug.print("Total inválido", pedido['total'])
                return False
            
            self.debug.print("Pedido válido")
            return True
        
        def procesar_pedido(self, pedido: Dict[str, Any]) -> Dict[str, Any]:
            """Procesa un pedido con debugging completo."""
            self.logger.agregar_contexto("pedido_id", pedido.get('id', 'desconocido'))
            self.logger.log_con_contexto("INFO", "Iniciando procesamiento de pedido")
            
            resultado = {
                'id': pedido.get('id'),
                'estado': 'pendiente',
                'errores': [],
                'tiempo_procesamiento': 0
            }
            
            inicio_tiempo = time.time()
            
            try:
                # Validar pedido
                if not self.validar_pedido(pedido):
                    resultado['estado'] = 'error'
                    resultado['errores'].append("Pedido inválido")
                    self.logger.log_con_contexto("ERROR", "Pedido inválido")
                    return resultado
                
                # Simular procesamiento
                self.debug.print("Procesando productos...")
                for i, producto in enumerate(pedido['productos']):
                    self.debug.print(f"Procesando producto {i+1}", producto)
                    time.sleep(0.1)  # Simular trabajo
                
                # Verificar stock (simulado)
                self.debug.print("Verificando stock...")
                stock_suficiente = all(len(str(p)) < 10 for p in pedido['productos'])  # Simulación
                
                if not stock_suficiente:
                    resultado['estado'] = 'error'
                    resultado['errores'].append("Stock insuficiente")
                    self.logger.log_con_contexto("WARNING", "Stock insuficiente")
                    return resultado
                
                # Calcular impuestos
                self.debug.print("Calculando impuestos...")
                impuestos = pedido['total'] * 0.16  # 16% IVA
                total_con_impuestos = pedido['total'] + impuestos
                
                self.debug.print_variable("impuestos", impuestos)
                self.debug.print_variable("total_con_impuestos", total_con_impuestos)
                
                # Actualizar resultado
                resultado.update({
                    'estado': 'completado',
                    'total_original': pedido['total'],
                    'impuestos': impuestos,
                    'total_final': total_con_impuestos,
                    'productos_procesados': len(pedido['productos'])
                })
                
                self.pedidos_procesados += 1
                self.logger.log_con_contexto("INFO", "Pedido procesado exitosamente", resultado)
                
            except Exception as e:
                resultado['estado'] = 'error'
                resultado['errores'].append(str(e))
                self.errores_totales += 1
                self.logger.log_con_contexto("ERROR", f"Error procesando pedido: {e}")
            
            finally:
                resultado['tiempo_procesamiento'] = time.time() - inicio_tiempo
                self.logger.limpiar_contexto()
            
            return resultado
        
        def obtener_estadisticas(self) -> Dict[str, Any]:
            """Obtiene estadísticas del sistema."""
            return {
                'pedidos_procesados': self.pedidos_procesados,
                'errores_totales': self.errores_totales,
                'tasa_exito': (self.pedidos_procesados - self.errores_totales) / max(self.pedidos_procesados, 1) * 100
            }
    
    # Crear sistema
    sistema = SistemaPedidos()
    
    # Pedidos de prueba
    pedidos_prueba = [
        {
            'id': 1,
            'cliente': 'Juan Pérez',
            'productos': ['Laptop', 'Mouse', 'Teclado'],
            'total': 1500.00
        },
        {
            'id': 2,
            'cliente': '',  # Cliente inválido
            'productos': ['Monitor'],
            'total': 300.00
        },
        {
            'id': 3,
            'cliente': 'María García',
            'productos': [],  # Lista vacía
            'total': 100.00
        },
        {
            'id': 4,
            'cliente': 'Carlos López',
            'productos': ['Auriculares', 'Webcam'],
            'total': -50.00  # Total negativo
        },
        {
            'id': 5,
            'cliente': 'Ana Martínez',
            'productos': ['Smartphone', 'Cargador'],
            'total': 800.00
        }
    ]
    
    # Procesar pedidos
    print("Procesando pedidos...")
    resultados = []
    
    for pedido in pedidos_prueba:
        print(f"\n--- Procesando Pedido {pedido['id']} ---")
        resultado = sistema.procesar_pedido(pedido)
        resultados.append(resultado)
        print(f"Estado: {resultado['estado']}")
        if resultado['errores']:
            print(f"Errores: {resultado['errores']}")
    
    # Mostrar estadísticas
    print(f"\n--- ESTADÍSTICAS DEL SISTEMA ---")
    stats = sistema.obtener_estadisticas()
    for clave, valor in stats.items():
        print(f"{clave}: {valor}")

# ============================================================================
# 6. EJERCICIOS PRÁCTICOS AVANZADOS
# ============================================================================

def ejercicios_practicos_avanzados():
    """Ejercicios prácticos avanzados de debugging."""
    print("\n" + "="*60)
    print("6. EJERCICIOS PRÁCTICOS AVANZADOS")
    print("="*60)
    
    # Ejercicio 1: Debugging de algoritmo de ordenamiento
    print("Ejercicio 1: Debugging de algoritmo de ordenamiento")
    
    def ordenamiento_con_debug(numeros: List[int]) -> List[int]:
        """Ordenamiento burbuja con debugging detallado."""
        debug = DebugPrinter(habilitado=True, prefijo="ORDENAMIENTO")
        debug.print_function_call("ordenamiento_con_debug", (numeros,))
        
        if not numeros:
            debug.print("Lista vacía, retornando lista vacía")
            return []
        
        resultado = numeros.copy()
        n = len(resultado)
        debug.print_variable("longitud", n)
        
        for i in range(n):
            debug.print(f"Iteración {i+1}/{n}")
            intercambios = 0
            
            for j in range(0, n - i - 1):
                debug.print(f"  Comparando posiciones {j} y {j+1}")
                debug.print_variable(f"resultado[{j}]", resultado[j])
                debug.print_variable(f"resultado[{j+1}]", resultado[j+1])
                
                if resultado[j] > resultado[j + 1]:
                    # Intercambiar
                    resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
                    intercambios += 1
                    debug.print(f"  Intercambio realizado ({intercambios} en esta iteración)")
                else:
                    debug.print("  No se necesita intercambio")
            
            debug.print(f"  Iteración {i+1} completada con {intercambios} intercambios")
            
            # Si no hay intercambios, la lista está ordenada
            if intercambios == 0:
                debug.print("  No se realizaron intercambios, lista ordenada")
                break
        
        debug.print_function_return("ordenamiento_con_debug", resultado)
        return resultado
    
    # Test del ordenamiento
    datos_desordenados = [64, 34, 25, 12, 22, 11, 90]
    print(f"Datos originales: {datos_desordenados}")
    datos_ordenados = ordenamiento_con_debug(datos_desordenados)
    print(f"Datos ordenados: {datos_ordenados}")
    
    # Ejercicio 2: Validación de datos con logging contextual
    print(f"\nEjercicio 2: Validación de datos con logging contextual")
    
    def validar_formulario_usuario(datos: Dict[str, Any]) -> Dict[str, Any]:
        """Valida formulario de usuario con logging contextual."""
        logger = ContextLogger("ValidacionFormulario")
        logger.agregar_contexto("usuario_id", datos.get('id', 'nuevo'))
        logger.log_con_contexto("INFO", "Iniciando validación de formulario")
        
        errores = []
        advertencias = []
        
        # Validar nombre
        nombre = datos.get('nombre', '')
        if not nombre or len(nombre.strip()) < 2:
            errores.append("Nombre debe tener al menos 2 caracteres")
            logger.log_con_contexto("ERROR", "Nombre inválido", nombre)
        elif len(nombre) > 50:
            advertencias.append("Nombre muy largo")
            logger.log_con_contexto("WARNING", "Nombre muy largo", nombre)
        
        # Validar email
        email = datos.get('email', '')
        if not email or '@' not in email or '.' not in email:
            errores.append("Email inválido")
            logger.log_con_contexto("ERROR", "Email inválido", email)
        
        # Validar edad
        edad = datos.get('edad')
        if edad is not None:
            if not isinstance(edad, int):
                errores.append("Edad debe ser un número entero")
                logger.log_con_contexto("ERROR", "Edad no es entero", edad)
            elif edad < 0 or edad > 120:
                errores.append("Edad debe estar entre 0 y 120")
                logger.log_con_contexto("ERROR", "Edad fuera de rango", edad)
        
        # Validar teléfono
        telefono = datos.get('telefono', '')
        if telefono and not telefono.replace('-', '').replace(' ', '').isdigit():
            advertencias.append("Formato de teléfono sospechoso")
            logger.log_con_contexto("WARNING", "Formato de teléfono sospechoso", telefono)
        
        resultado = {
            'valido': len(errores) == 0,
            'errores': errores,
            'advertencias': advertencias,
            'campos_validados': len(datos)
        }
        
        if resultado['valido']:
            logger.log_con_contexto("INFO", "Formulario válido")
        else:
            logger.log_con_contexto("ERROR", f"Formulario inválido con {len(errores)} errores")
        
        logger.limpiar_contexto()
        return resultado
    
    # Test de validación
    formularios_prueba = [
        {'id': 1, 'nombre': 'Juan', 'email': 'juan@ejemplo.com', 'edad': 25, 'telefono': '123-456-7890'},
        {'id': 2, 'nombre': 'A', 'email': 'email-invalido', 'edad': 'treinta', 'telefono': 'abc-def-ghij'},
        {'id': 3, 'nombre': 'María Isabel González Rodríguez de la Cruz', 'email': 'maria@ejemplo.com', 'edad': 150},
        {'id': 4, 'email': 'ana@ejemplo.com'}  # Falta nombre
    ]
    
    for i, formulario in enumerate(formularios_prueba, 1):
        print(f"\nValidando formulario {i}:")
        resultado = validar_formulario_usuario(formulario)
        print(f"Válido: {resultado['valido']}")
        if resultado['errores']:
            print(f"Errores: {resultado['errores']}")
        if resultado['advertencias']:
            print(f"Advertencias: {resultado['advertencias']}")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🐍 DEBUGGING TOOLKIT AVANZADO")
    print("Técnicas Esenciales para Desarrolladores Python")
    print("=" * 60)
    
    # Configurar logging
    logger = configurar_logging_avanzado()
    logger.info("Iniciando Debugging Toolkit")
    
    # Ejecutar todos los ejemplos
    ejemplo_print_statements_mejorado()
    ejemplo_logging_avanzado()
    ejemplo_assertions_avanzadas()
    ejemplo_debugger_mejorado()
    caso_estudio_sistema_pedidos()
    ejercicios_practicos_avanzados()
    
    print("\n" + "=" * 60)
    print("✅ DEBUGGING TOOLKIT COMPLETADO")
    print("=" * 60)
    print("Técnicas cubiertas:")
    print("• Print statements mejorados con contexto")
    print("• Logging avanzado con múltiples handlers")
    print("• Assertions para validación robusta")
    print("• Debugger interactivo con helpers")
    print("• Caso de estudio completo")
    print("• Ejercicios prácticos avanzados")
    print("\n📁 Logs guardados en: debug_toolkit.log")

if __name__ == "__main__":
    main() 