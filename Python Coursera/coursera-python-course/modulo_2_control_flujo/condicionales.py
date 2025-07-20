#!/usr/bin/env python3
"""
Módulo 2: Control de Flujo - Declaraciones Condicionales
========================================================

Este módulo cubre las estructuras de control de flujo en Python:
- Declaraciones if, elif, else
- Operadores de comparación
- Operadores lógicos
- Anidamiento de condiciones
- Ejercicios prácticos

Autor: Ing. Jhon A. Valencia
Curso: Python de Coursera
"""

# ============================================================================
# 1. OPERADORES DE COMPARACIÓN
# ============================================================================

def ejemplo_operadores_comparacion():
    """Demuestra los operadores de comparación en Python."""
    print("=" * 60)
    print("1. OPERADORES DE COMPARACIÓN")
    print("=" * 60)
    
    a = 10
    b = 5
    
    print(f"a = {a}, b = {b}")
    print(f"a == b (igual): {a == b}")
    print(f"a != b (diferente): {a != b}")
    print(f"a > b (mayor que): {a > b}")
    print(f"a < b (menor que): {a < b}")
    print(f"a >= b (mayor o igual): {a >= b}")
    print(f"a <= b (menor o igual): {a <= b}")
    
    # Comparaciones con strings
    print(f"\nComparaciones con strings:")
    nombre1 = "Ana"
    nombre2 = "ana"
    print(f"'{nombre1}' == '{nombre2}': {nombre1 == nombre2}")
    print(f"'{nombre1}' != '{nombre2}': {nombre1 != nombre2}")
    print(f"'{nombre1}' < '{nombre2}': {nombre1 < nombre2}")  # Orden alfabético
    
    # Comparaciones con booleanos
    print(f"\nComparaciones con booleanos:")
    verdadero = True
    falso = False
    print(f"True == True: {verdadero == True}")
    print(f"True != False: {verdadero != falso}")

# ============================================================================
# 2. OPERADORES LÓGICOS
# ============================================================================

def ejemplo_operadores_logicos():
    """Demuestra los operadores lógicos en Python."""
    print("\n" + "=" * 60)
    print("2. OPERADORES LÓGICOS")
    print("=" * 60)
    
    # Operador AND
    print("Operador AND (and):")
    print(f"True and True = {True and True}")
    print(f"True and False = {True and False}")
    print(f"False and True = {False and True}")
    print(f"False and False = {False and False}")
    
    # Operador OR
    print(f"\nOperador OR (or):")
    print(f"True or True = {True or True}")
    print(f"True or False = {True or False}")
    print(f"False or True = {False or True}")
    print(f"False or False = {False or False}")
    
    # Operador NOT
    print(f"\nOperador NOT (not):")
    print(f"not True = {not True}")
    print(f"not False = {not False}")
    
    # Ejemplos prácticos
    print(f"\nEjemplos prácticos:")
    edad = 25
    tiene_licencia = True
    
    puede_conducir = edad >= 18 and tiene_licencia
    print(f"Edad: {edad}, Tiene licencia: {tiene_licencia}")
    print(f"¿Puede conducir?: {puede_conducir}")
    
    # Precedencia de operadores
    print(f"\nPrecedencia de operadores:")
    resultado = not (edad >= 18 and tiene_licencia)
    print(f"not (edad >= 18 and tiene_licencia) = {resultado}")

# ============================================================================
# 3. DECLARACIÓN IF BÁSICA
# ============================================================================

def ejemplo_if_basico():
    """Demuestra el uso básico de la declaración if."""
    print("\n" + "=" * 60)
    print("3. DECLARACIÓN IF BÁSICA")
    print("=" * 60)
    
    # Ejemplo 1: Verificar si un número es positivo
    numero = 15
    print(f"Número: {numero}")
    
    if numero > 0:
        print("El número es positivo")
    
    # Ejemplo 2: Verificar edad para conducir
    edad = 20
    print(f"\nEdad: {edad}")
    
    if edad >= 18:
        print("Eres mayor de edad")
        print("Puedes obtener una licencia de conducir")
    
    # Ejemplo 3: Verificar contraseña
    contraseña = "python123"
    contraseña_ingresada = "python123"
    
    print(f"\nVerificando contraseña...")
    if contraseña == contraseña_ingresada:
        print("¡Contraseña correcta!")
        print("Acceso permitido")

# ============================================================================
# 4. DECLARACIÓN IF-ELSE
# ============================================================================

def ejemplo_if_else():
    """Demuestra el uso de if-else."""
    print("\n" + "=" * 60)
    print("4. DECLARACIÓN IF-ELSE")
    print("=" * 60)
    
    # Ejemplo 1: Verificar si un número es par o impar
    numero = 7
    print(f"Número: {numero}")
    
    if numero % 2 == 0:
        print("El número es par")
    else:
        print("El número es impar")
    
    # Ejemplo 2: Sistema de calificaciones
    calificacion = 85
    print(f"\nCalificación: {calificacion}")
    
    if calificacion >= 90:
        print("Calificación: A (Excelente)")
    else:
        print("Calificación: B o menor (Necesita mejorar)")
    
    # Ejemplo 3: Verificar temperatura
    temperatura = 25
    print(f"\nTemperatura: {temperatura}°C")
    
    if temperatura > 30:
        print("¡Hace mucho calor!")
    else:
        print("La temperatura está agradable")

# ============================================================================
# 5. DECLARACIÓN IF-ELIF-ELSE
# ============================================================================

def ejemplo_if_elif_else():
    """Demuestra el uso de if-elif-else para múltiples condiciones."""
    print("\n" + "=" * 60)
    print("5. DECLARACIÓN IF-ELIF-ELSE")
    print("=" * 60)
    
    # Ejemplo 1: Sistema de calificaciones completo
    calificacion = 87
    print(f"Calificación: {calificacion}")
    
    if calificacion >= 90:
        print("Calificación: A (Excelente)")
    elif calificacion >= 80:
        print("Calificación: B (Bueno)")
    elif calificacion >= 70:
        print("Calificación: C (Satisfactorio)")
    elif calificacion >= 60:
        print("Calificación: D (Necesita mejorar)")
    else:
        print("Calificación: F (Reprobado)")
    
    # Ejemplo 2: Categorización de edad
    edad = 25
    print(f"\nEdad: {edad}")
    
    if edad < 13:
        print("Categoría: Niño")
    elif edad < 20:
        print("Categoría: Adolescente")
    elif edad < 65:
        print("Categoría: Adulto")
    else:
        print("Categoría: Adulto mayor")
    
    # Ejemplo 3: Sistema de descuentos
    compra = 150
    print(f"\nMonto de compra: ${compra}")
    
    if compra >= 200:
        descuento = 0.20
        print("Descuento: 20%")
    elif compra >= 100:
        descuento = 0.10
        print("Descuento: 10%")
    elif compra >= 50:
        descuento = 0.05
        print("Descuento: 5%")
    else:
        descuento = 0
        print("Sin descuento")
    
    monto_final = compra * (1 - descuento)
    print(f"Monto final: ${monto_final:.2f}")

# ============================================================================
# 6. ANIDAMIENTO DE CONDICIONES
# ============================================================================

def ejemplo_anidamiento():
    """Demuestra el anidamiento de condiciones."""
    print("\n" + "=" * 60)
    print("6. ANIDAMIENTO DE CONDICIONES")
    print("=" * 60)
    
    # Ejemplo 1: Sistema de acceso con múltiples verificaciones
    edad = 25
    tiene_identificacion = True
    es_miembro = False
    
    print(f"Edad: {edad}")
    print(f"Tiene identificación: {tiene_identificacion}")
    print(f"Es miembro: {es_miembro}")
    
    if edad >= 18:
        if tiene_identificacion:
            if es_miembro:
                print("Acceso completo permitido")
            else:
                print("Acceso básico permitido")
        else:
            print("Se requiere identificación")
    else:
        print("Acceso denegado - Menor de edad")
    
    # Ejemplo 2: Sistema de calificaciones con comentarios
    calificacion = 85
    asistencia = 0.95
    
    print(f"\nCalificación: {calificacion}")
    print(f"Asistencia: {asistencia*100}%")
    
    if calificacion >= 80:
        if asistencia >= 0.90:
            print("¡Excelente trabajo! Mantén el buen rendimiento.")
        else:
            print("Buen trabajo, pero mejora la asistencia.")
    else:
        if asistencia >= 0.90:
            print("Buena asistencia, pero necesitas mejorar las calificaciones.")
        else:
            print("Necesitas mejorar tanto calificaciones como asistencia.")

# ============================================================================
# 7. CONDICIONES CON OPERADORES IN Y NOT IN
# ============================================================================

def ejemplo_operadores_in():
    """Demuestra el uso de los operadores in y not in."""
    print("\n" + "=" * 60)
    print("7. OPERADORES IN Y NOT IN")
    print("=" * 60)
    
    # Verificar si un elemento está en una lista
    frutas = ["manzana", "banana", "naranja", "uva"]
    fruta_buscar = "banana"
    
    print(f"Lista de frutas: {frutas}")
    print(f"Buscando: {fruta_buscar}")
    
    if fruta_buscar in frutas:
        print(f"'{fruta_buscar}' está en la lista")
    else:
        print(f"'{fruta_buscar}' no está en la lista")
    
    # Verificar si un carácter está en una cadena
    texto = "Python es genial"
    letra = "a"
    
    print(f"\nTexto: '{texto}'")
    print(f"Buscando letra: '{letra}'")
    
    if letra in texto:
        print(f"La letra '{letra}' está en el texto")
    else:
        print(f"La letra '{letra}' no está en el texto")
    
    # Verificar si una clave está en un diccionario
    usuario = {"nombre": "Ana", "edad": 25, "ciudad": "Madrid"}
    clave = "email"
    
    print(f"\nDiccionario: {usuario}")
    print(f"Buscando clave: '{clave}'")
    
    if clave not in usuario:
        print(f"La clave '{clave}' no está en el diccionario")
        print("Agregando email...")
        usuario[clave] = "ana@ejemplo.com"
        print(f"Diccionario actualizado: {usuario}")

# ============================================================================
# 8. EJERCICIOS PRÁCTICOS
# ============================================================================

def ejercicios_practicos():
    """Ejercicios prácticos para reforzar conceptos."""
    print("\n" + "=" * 60)
    print("8. EJERCICIOS PRÁCTICOS")
    print("=" * 60)
    
    # Ejercicio 1: Calculadora de IMC
    print("Ejercicio 1: Calculadora de IMC")
    peso = 70  # kg
    altura = 1.75  # metros
    imc = peso / (altura ** 2)
    
    print(f"Peso: {peso} kg")
    print(f"Altura: {altura} m")
    print(f"IMC: {imc:.1f}")
    
    if imc < 18.5:
        categoria = "Bajo peso"
    elif imc < 25:
        categoria = "Peso normal"
    elif imc < 30:
        categoria = "Sobrepeso"
    else:
        categoria = "Obesidad"
    
    print(f"Categoría: {categoria}")
    
    # Ejercicio 2: Sistema de descuentos mejorado
    print(f"\nEjercicio 2: Sistema de descuentos")
    compra = 250
    es_cliente_vip = True
    es_primera_compra = False
    
    print(f"Monto de compra: ${compra}")
    print(f"Cliente VIP: {es_cliente_vip}")
    print(f"Primera compra: {es_primera_compra}")
    
    # Calcular descuento base
    if compra >= 200:
        descuento_base = 0.15
    elif compra >= 100:
        descuento_base = 0.10
    else:
        descuento_base = 0.05
    
    # Descuentos adicionales
    descuento_vip = 0.05 if es_cliente_vip else 0
    descuento_primera = 0.10 if es_primera_compra else 0
    
    descuento_total = descuento_base + descuento_vip + descuento_primera
    monto_final = compra * (1 - descuento_total)
    
    print(f"Descuento base: {descuento_base*100}%")
    print(f"Descuento VIP: {descuento_vip*100}%")
    print(f"Descuento primera compra: {descuento_primera*100}%")
    print(f"Descuento total: {descuento_total*100}%")
    print(f"Monto final: ${monto_final:.2f}")
    
    # Ejercicio 3: Validación de contraseña
    print(f"\nEjercicio 3: Validación de contraseña")
    contraseña = "Python123!"
    
    print(f"Contraseña: {contraseña}")
    
    # Verificar longitud
    if len(contraseña) >= 8:
        longitud_ok = True
    else:
        longitud_ok = False
    
    # Verificar si tiene mayúsculas
    tiene_mayuscula = any(c.isupper() for c in contraseña)
    
    # Verificar si tiene números
    tiene_numero = any(c.isdigit() for c in contraseña)
    
    # Verificar si tiene caracteres especiales
    caracteres_especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    tiene_especial = any(c in caracteres_especiales for c in contraseña)
    
    print(f"Longitud >= 8: {longitud_ok}")
    print(f"Tiene mayúscula: {tiene_mayuscula}")
    print(f"Tiene número: {tiene_numero}")
    print(f"Tiene carácter especial: {tiene_especial}")
    
    if longitud_ok and tiene_mayuscula and tiene_numero and tiene_especial:
        print("✅ Contraseña válida")
    else:
        print("❌ Contraseña inválida")
        if not longitud_ok:
            print("  - Debe tener al menos 8 caracteres")
        if not tiene_mayuscula:
            print("  - Debe tener al menos una mayúscula")
        if not tiene_numero:
            print("  - Debe tener al menos un número")
        if not tiene_especial:
            print("  - Debe tener al menos un carácter especial")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todos los ejemplos."""
    print("🐍 MÓDULO 2: CONTROL DE FLUJO")
    print("Declaraciones Condicionales")
    print("=" * 60)
    
    # Ejecutar todos los ejemplos
    ejemplo_operadores_comparacion()
    ejemplo_operadores_logicos()
    ejemplo_if_basico()
    ejemplo_if_else()
    ejemplo_if_elif_else()
    ejemplo_anidamiento()
    ejemplo_operadores_in()
    ejercicios_practicos()
    
    print("\n" + "=" * 60)
    print("✅ MÓDULO 2 COMPLETADO")
    print("=" * 60)
    print("Conceptos cubiertos:")
    print("• Operadores de comparación")
    print("• Operadores lógicos (and, or, not)")
    print("• Declaraciones if, elif, else")
    print("• Anidamiento de condiciones")
    print("• Operadores in y not in")
    print("• Ejercicios prácticos de aplicación")

if __name__ == "__main__":
    main() 