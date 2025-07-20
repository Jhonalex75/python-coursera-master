#!/usr/bin/env python3
"""
Módulo 1: Fundamentos de Python - Variables y Tipos de Datos
============================================================

Este módulo cubre los conceptos básicos de Python:
- Variables y asignación
- Tipos de datos básicos
- Conversión de tipos
- Operaciones básicas

Autor: Ing. Jhon A. Valencia
Curso: Python de Coursera
"""

# ============================================================================
# 1. VARIABLES Y ASIGNACIÓN
# ============================================================================

def ejemplo_variables():
    """Demuestra la creación y uso de variables."""
    print("=" * 60)
    print("1. VARIABLES Y ASIGNACIÓN")
    print("=" * 60)
    
    # Asignación básica
    nombre = "Juan"
    edad = 25
    altura = 1.75
    es_estudiante = True
    
    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")
    print(f"Altura: {altura}")
    print(f"¿Es estudiante?: {es_estudiante}")
    
    # Múltiples asignaciones
    x, y, z = 1, 2, 3
    print(f"\nMúltiples variables: x={x}, y={y}, z={z}")
    
    # Asignación múltiple del mismo valor
    a = b = c = 10
    print(f"Mismo valor: a={a}, b={b}, c={c}")
    
    # Reasignación
    print(f"\nAntes de reasignar: edad = {edad}")
    edad = 26
    print(f"Después de reasignar: edad = {edad}")

# ============================================================================
# 2. TIPOS DE DATOS BÁSICOS
# ============================================================================

def ejemplo_tipos_datos():
    """Demuestra los tipos de datos básicos de Python."""
    print("\n" + "=" * 60)
    print("2. TIPOS DE DATOS BÁSICOS")
    print("=" * 60)
    
    # Números enteros (int)
    numero_entero = 42
    print(f"Entero: {numero_entero} (tipo: {type(numero_entero)})")
    
    # Números de punto flotante (float)
    numero_decimal = 3.14159
    print(f"Decimal: {numero_decimal} (tipo: {type(numero_decimal)})")
    
    # Cadenas de texto (str)
    texto = "Hola, Python!"
    print(f"Texto: {texto} (tipo: {type(texto)})")
    
    # Valores booleanos (bool)
    verdadero = True
    falso = False
    print(f"Booleano verdadero: {verdadero} (tipo: {type(verdadero)})")
    print(f"Booleano falso: {falso} (tipo: {type(falso)})")
    
    # Valor nulo (None)
    valor_nulo = None
    print(f"Valor nulo: {valor_nulo} (tipo: {type(valor_nulo)})")

# ============================================================================
# 3. OPERACIONES CON NÚMEROS
# ============================================================================

def ejemplo_operaciones_numericas():
    """Demuestra operaciones matemáticas básicas."""
    print("\n" + "=" * 60)
    print("3. OPERACIONES CON NÚMEROS")
    print("=" * 60)
    
    a = 10
    b = 3
    
    # Operaciones básicas
    suma = a + b
    resta = a - b
    multiplicacion = a * b
    division = a / b
    division_entera = a // b
    modulo = a % b
    potencia = a ** b
    
    print(f"a = {a}, b = {b}")
    print(f"Suma: {a} + {b} = {suma}")
    print(f"Resta: {a} - {b} = {resta}")
    print(f"Multiplicación: {a} * {b} = {multiplicacion}")
    print(f"División: {a} / {b} = {division}")
    print(f"División entera: {a} // {b} = {division_entera}")
    print(f"Módulo: {a} % {b} = {modulo}")
    print(f"Potencia: {a} ** {b} = {potencia}")
    
    # Operaciones con punto flotante
    print(f"\nOperaciones con decimales:")
    x = 5.5
    y = 2.2
    print(f"x = {x}, y = {y}")
    print(f"x + y = {x + y}")
    print(f"x * y = {x * y}")
    print(f"x / y = {x / y}")

# ============================================================================
# 4. OPERACIONES CON CADENAS
# ============================================================================

def ejemplo_operaciones_cadenas():
    """Demuestra operaciones con cadenas de texto."""
    print("\n" + "=" * 60)
    print("4. OPERACIONES CON CADENAS")
    print("=" * 60)
    
    # Concatenación
    nombre = "María"
    apellido = "García"
    nombre_completo = nombre + " " + apellido
    print(f"Concatenación: '{nombre}' + ' ' + '{apellido}' = '{nombre_completo}'")
    
    # Repetición
    linea = "-" * 20
    print(f"Repetición: '-' * 20 = '{linea}'")
    
    # Longitud de cadena
    texto = "Python es genial"
    longitud = len(texto)
    print(f"Longitud de '{texto}': {longitud} caracteres")
    
    # Acceso a caracteres
    print(f"Primer carácter: '{texto[0]}'")
    print(f"Último carácter: '{texto[-1]}'")
    print(f"Carácter en posición 7: '{texto[7]}'")
    
    # Slicing (rebanado)
    print(f"Primeros 6 caracteres: '{texto[:6]}'")
    print(f"Últimos 6 caracteres: '{texto[-6:]}'")
    print(f"Del carácter 7 al 9: '{texto[7:10]}'")

# ============================================================================
# 5. CONVERSIÓN DE TIPOS
# ============================================================================

def ejemplo_conversion_tipos():
    """Demuestra la conversión entre diferentes tipos de datos."""
    print("\n" + "=" * 60)
    print("5. CONVERSIÓN DE TIPOS")
    print("=" * 60)
    
    # Conversión a entero
    numero_texto = "42"
    numero_entero = int(numero_texto)
    print(f"Texto '{numero_texto}' convertido a entero: {numero_entero}")
    
    # Conversión a float
    decimal_texto = "3.14"
    numero_decimal = float(decimal_texto)
    print(f"Texto '{decimal_texto}' convertido a float: {numero_decimal}")
    
    # Conversión a string
    numero = 123
    texto_numero = str(numero)
    print(f"Número {numero} convertido a texto: '{texto_numero}'")
    
    # Conversión de float a int
    decimal = 3.9
    entero = int(decimal)
    print(f"Float {decimal} convertido a int: {entero}")
    
    # Conversión de booleanos
    verdadero = True
    falso = False
    print(f"True convertido a int: {int(verdadero)}")
    print(f"False convertido a int: {int(falso)}")
    print(f"True convertido a float: {float(verdadero)}")
    print(f"False convertido a float: {float(falso)}")

# ============================================================================
# 6. ENTRADA Y SALIDA BÁSICA
# ============================================================================

def ejemplo_entrada_salida():
    """Demuestra entrada y salida básica."""
    print("\n" + "=" * 60)
    print("6. ENTRADA Y SALIDA BÁSICA")
    print("=" * 60)
    
    # Salida con print
    print("Hola, mundo!")
    print("Python", "es", "genial", sep=" - ")
    print("Línea 1", end=" ")
    print("Línea 2")
    
    # Formateo de strings
    nombre = "Ana"
    edad = 30
    altura = 1.65
    
    # Formateo con f-strings (recomendado)
    print(f"Nombre: {nombre}, Edad: {edad}, Altura: {altura:.2f}m")
    
    # Formateo con .format()
    print("Nombre: {}, Edad: {}, Altura: {:.2f}m".format(nombre, edad, altura))
    
    # Formateo con %
    print("Nombre: %s, Edad: %d, Altura: %.2fm" % (nombre, edad, altura))
    
    # Entrada con input (comentado para evitar interacción)
    # nombre_usuario = input("Ingresa tu nombre: ")
    # print(f"Hola, {nombre_usuario}!")
    
    # Simulación de entrada
    print("\nSimulación de entrada:")
    nombre_simulado = "Carlos"
    print(f"Entrada simulada: {nombre_simulado}")
    print(f"Salida: Hola, {nombre_simulado}!")

# ============================================================================
# 7. EJERCICIOS PRÁCTICOS
# ============================================================================

def ejercicios_practicos():
    """Ejercicios prácticos para reforzar conceptos."""
    print("\n" + "=" * 60)
    print("7. EJERCICIOS PRÁCTICOS")
    print("=" * 60)
    
    # Ejercicio 1: Calculadora básica
    print("Ejercicio 1: Calculadora básica")
    num1 = 15
    num2 = 4
    
    suma = num1 + num2
    resta = num1 - num2
    multiplicacion = num1 * num2
    division = num1 / num2
    
    print(f"Operaciones con {num1} y {num2}:")
    print(f"  Suma: {suma}")
    print(f"  Resta: {resta}")
    print(f"  Multiplicación: {multiplicacion}")
    print(f"  División: {division:.2f}")
    
    # Ejercicio 2: Manipulación de texto
    print("\nEjercicio 2: Manipulación de texto")
    texto = "Python Programming"
    
    print(f"Texto original: '{texto}'")
    print(f"Longitud: {len(texto)} caracteres")
    print(f"En mayúsculas: '{texto.upper()}'")
    print(f"En minúsculas: '{texto.lower()}'")
    print(f"Primera palabra: '{texto[:6]}'")
    print(f"Segunda palabra: '{texto[7:]}'")
    
    # Ejercicio 3: Conversiones
    print("\nEjercicio 3: Conversiones")
    precio_texto = "29.99"
    cantidad_texto = "5"
    
    precio = float(precio_texto)
    cantidad = int(cantidad_texto)
    total = precio * cantidad
    
    print(f"Precio: ${precio}")
    print(f"Cantidad: {cantidad}")
    print(f"Total: ${total:.2f}")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🐍 MÓDULO 1: FUNDAMENTOS DE PYTHON")
    print("Variables y Tipos de Datos")
    print("=" * 60)
    
    # Ejecutar todos los ejemplos
    ejemplo_variables()
    ejemplo_tipos_datos()
    ejemplo_operaciones_numericas()
    ejemplo_operaciones_cadenas()
    ejemplo_conversion_tipos()
    ejemplo_entrada_salida()
    ejercicios_practicos()
    
    print("\n" + "=" * 60)
    print("✅ MÓDULO 1 COMPLETADO")
    print("=" * 60)
    print("Conceptos cubiertos:")
    print("• Variables y asignación")
    print("• Tipos de datos básicos")
    print("• Operaciones matemáticas")
    print("• Manipulación de cadenas")
    print("• Conversión de tipos")
    print("• Entrada y salida básica")

if __name__ == "__main__":
    main() 