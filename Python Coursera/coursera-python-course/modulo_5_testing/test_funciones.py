"""
Archivo de Tests para Módulo 5 - Testing con pytest
==================================================

Este archivo contiene todos los tests para las funciones del módulo 5.
Puede ejecutarse directamente con pytest.

Uso:
    pytest test_funciones.py
    pytest test_funciones.py -v
    pytest test_funciones.py::test_calcular_area_circulo
"""

import pytest
import math
import random
from typing import List, Dict, Any


# ============================================================================
# FUNCIONES A TESTEAR (copiadas del módulo principal)
# ============================================================================

def calcular_area_circulo(radio: float) -> float:
    """Calcular el área de un círculo"""
    if radio < 0:
        raise ValueError("El radio no puede ser negativo")
    return math.pi * radio ** 2


def calcular_descuento(libros_comprados: int, umbral_descuento: int, umbral_bonus: int) -> str:
    """Calcular descuento basado en cantidad de libros"""
    if libros_comprados >= umbral_bonus:
        return "Big discount applied!"
    elif libros_comprados >= umbral_descuento:
        return "Discount applied!"
    else:
        return "No discount."


def promedio_puntajes(puntajes: List[float]) -> float:
    """Calcular promedio de puntajes"""
    if not puntajes:
        raise ValueError("La lista de puntajes no puede estar vacía")
    return sum(puntajes) / len(puntajes)


def validar_email(email: str) -> bool:
    """Validar formato de email básico"""
    if not email or '@' not in email or '.' not in email:
        return False
    
    partes = email.split('@')
    if len(partes) != 2:
        return False
    
    usuario, dominio = partes
    if not usuario or not dominio:
        return False
    
    if '.' not in dominio:
        return False
    
    return True


def ordenar_estudiantes(estudiantes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Ordenar estudiantes por puntaje de mayor a menor"""
    return sorted(estudiantes, key=lambda x: x.get('puntaje', 0), reverse=True)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def datos_estudiantes():
    """Fixture con datos de estudiantes de prueba"""
    return [
        {"nombre": "Ana", "puntaje": 85, "edad": 20},
        {"nombre": "Juan", "puntaje": 92, "edad": 22},
        {"nombre": "María", "puntaje": 78, "edad": 19},
        {"nombre": "Carlos", "puntaje": 95, "edad": 21},
        {"nombre": "Elena", "puntaje": 88, "edad": 23}
    ]


@pytest.fixture
def emails_validos():
    """Fixture con emails válidos"""
    return [
        "usuario@dominio.com",
        "test@example.org",
        "admin@empresa.co",
        "info@website.net"
    ]


@pytest.fixture
def emails_invalidos():
    """Fixture con emails inválidos"""
    return [
        "",
        "sinarroba",
        "@dominio.com",
        "usuario@",
        "usuario@dominio",
        "usuario..@dominio.com"
    ]


@pytest.fixture
def datos_puntajes():
    """Fixture con datos de puntajes"""
    return [87, 90, 75, 100, 100, 70]


# ============================================================================
# TESTS BÁSICOS
# ============================================================================

def test_calcular_area_circulo():
    """Test básico para calcular área de círculo"""
    assert calcular_area_circulo(5) == pytest.approx(78.54, abs=0.01)
    assert calcular_area_circulo(0) == 0
    assert calcular_area_circulo(1) == pytest.approx(math.pi, abs=0.01)


def test_calcular_area_circulo_negativo():
    """Test para radio negativo"""
    with pytest.raises(ValueError, match="El radio no puede ser negativo"):
        calcular_area_circulo(-2)


def test_calcular_descuento():
    """Test para función de descuento"""
    assert calcular_descuento(3, 5, 10) == "No discount."
    assert calcular_descuento(7, 5, 10) == "Discount applied!"
    assert calcular_descuento(12, 5, 10) == "Big discount applied!"


def test_promedio_puntajes():
    """Test para cálculo de promedio"""
    assert promedio_puntajes([85, 90, 95]) == 90.0
    assert promedio_puntajes([100]) == 100.0
    assert promedio_puntajes([0, 0, 0]) == 0.0


def test_promedio_puntajes_vacio():
    """Test para lista vacía"""
    with pytest.raises(ValueError, match="La lista de puntajes no puede estar vacía"):
        promedio_puntajes([])


def test_validar_email():
    """Test para validación de email"""
    # Emails válidos
    assert validar_email("usuario@dominio.com") == True
    assert validar_email("test@example.org") == True
    assert validar_email("a@b.c") == True
    
    # Emails inválidos
    assert validar_email("") == False
    assert validar_email("sinarroba") == False
    assert validar_email("@dominio.com") == False
    assert validar_email("usuario@") == False
    assert validar_email("usuario@dominio") == False


def test_ordenar_estudiantes():
    """Test para ordenamiento de estudiantes"""
    estudiantes = [
        {"nombre": "Ana", "puntaje": 85},
        {"nombre": "Juan", "puntaje": 92},
        {"nombre": "María", "puntaje": 78}
    ]
    
    resultado = ordenar_estudiantes(estudiantes)
    
    assert len(resultado) == 3
    assert resultado[0]["nombre"] == "Juan"  # Mayor puntaje
    assert resultado[1]["nombre"] == "Ana"
    assert resultado[2]["nombre"] == "María"  # Menor puntaje


# ============================================================================
# TESTS CON FIXTURES
# ============================================================================

def test_ordenar_estudiantes_con_fixture(datos_estudiantes):
    """Test usando fixture de estudiantes"""
    resultado = ordenar_estudiantes(datos_estudiantes)
    
    # Verificar que está ordenado por puntaje descendente
    puntajes = [est["puntaje"] for est in resultado]
    assert puntajes == sorted(puntajes, reverse=True)
    
    # Verificar que el primero tiene el puntaje más alto
    assert resultado[0]["puntaje"] == 95
    assert resultado[0]["nombre"] == "Carlos"


def test_validar_emails_validos(emails_validos):
    """Test para emails válidos usando fixture"""
    for email in emails_validos:
        assert validar_email(email) == True, f"Email {email} debería ser válido"


def test_validar_emails_invalidos(emails_invalidos):
    """Test para emails inválidos usando fixture"""
    for email in emails_invalidos:
        assert validar_email(email) == False, f"Email {email} debería ser inválido"


def test_promedio_puntajes_con_fixture(datos_puntajes):
    """Test de promedio usando fixture"""
    resultado = promedio_puntajes(datos_puntajes)
    assert resultado == pytest.approx(87.0, abs=0.01)


# ============================================================================
# TESTS PARAMETRIZADOS
# ============================================================================

@pytest.mark.parametrize("radio,area_esperada", [
    (0, 0),
    (1, math.pi),
    (2, 4 * math.pi),
    (5, 25 * math.pi),
    (10, 100 * math.pi)
])
def test_calcular_area_circulo_parametrizado(radio, area_esperada):
    """Test parametrizado para área de círculo"""
    assert calcular_area_circulo(radio) == pytest.approx(area_esperada, abs=0.01)


@pytest.mark.parametrize("libros,umbral,umbral_bonus,esperado", [
    (3, 5, 10, "No discount."),
    (7, 5, 10, "Discount applied!"),
    (12, 5, 10, "Big discount applied!"),
    (0, 5, 10, "No discount."),
    (15, 5, 10, "Big discount applied!"),
    (5, 5, 10, "Discount applied!")
])
def test_calcular_descuento_parametrizado(libros, umbral, umbral_bonus, esperado):
    """Test parametrizado para función de descuento"""
    assert calcular_descuento(libros, umbral, umbral_bonus) == esperado


@pytest.mark.parametrize("puntajes,esperado", [
    ([85, 90, 95], 90.0),
    ([100], 100.0),
    ([0, 0, 0], 0.0),
    ([50, 60, 70, 80, 90], 70.0),
    ([1, 2, 3, 4, 5], 3.0)
])
def test_promedio_puntajes_parametrizado(puntajes, esperado):
    """Test parametrizado para promedio de puntajes"""
    assert promedio_puntajes(puntajes) == esperado


# ============================================================================
# TESTS DE EXCEPCIONES
# ============================================================================

@pytest.mark.parametrize("radio_invalido", [-1, -5, -10.5, -100])
def test_calcular_area_circulo_radio_negativo(radio_invalido):
    """Test para radios negativos"""
    with pytest.raises(ValueError, match="El radio no puede ser negativo"):
        calcular_area_circulo(radio_invalido)


def test_promedio_puntajes_lista_vacia():
    """Test para lista vacía"""
    with pytest.raises(ValueError, match="La lista de puntajes no puede estar vacía"):
        promedio_puntajes([])


def test_promedio_puntajes_none():
    """Test para entrada None"""
    with pytest.raises(TypeError):
        promedio_puntajes(None)


# ============================================================================
# TESTS DE INTEGRACIÓN
# ============================================================================

def test_flujo_completo_calificaciones():
    """Test de integración: flujo completo de calificaciones"""
    # Simular datos de estudiantes
    estudiantes = [
        {"nombre": "Ana", "puntaje": 85},
        {"nombre": "Juan", "puntaje": 92},
        {"nombre": "María", "puntaje": 78}
    ]
    
    # Ordenar estudiantes
    estudiantes_ordenados = ordenar_estudiantes(estudiantes)
    
    # Extraer puntajes
    puntajes = [est["puntaje"] for est in estudiantes_ordenados]
    
    # Calcular promedio
    promedio = promedio_puntajes(puntajes)
    
    # Verificaciones
    assert len(estudiantes_ordenados) == 3
    assert estudiantes_ordenados[0]["puntaje"] == 92  # Mayor
    assert promedio == pytest.approx(85.0, abs=0.01)


# ============================================================================
# TESTS DE RENDIMIENTO
# ============================================================================

def test_rendimiento_ordenamiento():
    """Test de rendimiento para ordenamiento"""
    # Generar lista grande
    estudiantes_grandes = [
        {"nombre": f"Estudiante{i}", "puntaje": random.randint(0, 100)}
        for i in range(1000)
    ]
    
    # Medir tiempo de ordenamiento
    import time
    inicio = time.time()
    resultado = ordenar_estudiantes(estudiantes_grandes)
    tiempo = time.time() - inicio
    
    # Verificar que se ordenó correctamente
    puntajes = [est["puntaje"] for est in resultado]
    assert puntajes == sorted(puntajes, reverse=True)
    
    # Verificar que no toma demasiado tiempo (menos de 1 segundo)
    assert tiempo < 1.0, f"Ordenamiento tomó {tiempo:.3f} segundos"


# ============================================================================
# TESTS DE EDGE CASES
# ============================================================================

def test_calcular_area_circulo_edge_cases():
    """Test para casos extremos de área de círculo"""
    # Radio muy pequeño
    assert calcular_area_circulo(0.001) > 0
    
    # Radio muy grande
    radio_grande = 1e6
    area_grande = calcular_area_circulo(radio_grande)
    assert area_grande > 0
    assert math.isinf(area_grande) == False


def test_validar_email_edge_cases():
    """Test para casos extremos de validación de email"""
    # Casos especiales
    assert validar_email("a@b.c") == True  # Email mínimo válido
    assert validar_email("usuario+tag@dominio.com") == True  # Con tag
    assert validar_email("usuario@dominio.co.uk") == True  # Dominio compuesto
    
    # Casos inválidos especiales
    assert validar_email("usuario..@dominio.com") == False  # Doble punto
    assert validar_email("usuario@dominio..com") == False  # Doble punto en dominio


# ============================================================================
# TESTS ADICIONALES PARA PRÁCTICA
# ============================================================================

def test_calcular_area_circulo_tipos():
    """Test para diferentes tipos de entrada"""
    # Enteros
    assert calcular_area_circulo(5) == pytest.approx(25 * math.pi, abs=0.01)
    
    # Flotantes
    assert calcular_area_circulo(2.5) == pytest.approx(6.25 * math.pi, abs=0.01)
    
    # Cero
    assert calcular_area_circulo(0) == 0


def test_calcular_descuento_limites():
    """Test para límites de la función de descuento"""
    # En el límite exacto
    assert calcular_descuento(5, 5, 10) == "Discount applied!"
    assert calcular_descuento(10, 5, 10) == "Big discount applied!"
    
    # Justo debajo del límite
    assert calcular_descuento(4, 5, 10) == "No discount."
    assert calcular_descuento(9, 5, 10) == "Discount applied!"


def test_promedio_puntajes_numeros_negativos():
    """Test para puntajes negativos"""
    assert promedio_puntajes([-10, 0, 10]) == 0.0
    assert promedio_puntajes([-5, -10, -15]) == -10.0


def test_validar_email_casos_especiales():
    """Test para casos especiales de email"""
    # Emails con números
    assert validar_email("usuario123@dominio.com") == True
    
    # Emails con guiones
    assert validar_email("usuario-nombre@dominio.com") == True
    
    # Emails con puntos en el usuario
    assert validar_email("usuario.nombre@dominio.com") == True


def test_ordenar_estudiantes_sin_puntaje():
    """Test para estudiantes sin puntaje"""
    estudiantes = [
        {"nombre": "Ana", "puntaje": 85},
        {"nombre": "Juan"},  # Sin puntaje
        {"nombre": "María", "puntaje": 78}
    ]
    
    resultado = ordenar_estudiantes(estudiantes)
    
    # El estudiante sin puntaje debería ir al final (puntaje = 0)
    assert resultado[0]["nombre"] == "Ana"
    assert resultado[1]["nombre"] == "María"
    assert resultado[2]["nombre"] == "Juan"


# ============================================================================
# FUNCIÓN PARA EJECUTAR TESTS MANUALMENTE
# ============================================================================

def ejecutar_tests_manualmente():
    """
    Función para ejecutar tests manualmente sin pytest
    Útil para demostración o cuando pytest no está disponible
    """
    print("Ejecutando tests manualmente...")
    
    # Tests básicos
    try:
        assert calcular_area_circulo(5) == pytest.approx(78.54, abs=0.01)
        print("✓ test_calcular_area_circulo")
    except AssertionError:
        print("✗ test_calcular_area_circulo")
    
    try:
        assert calcular_descuento(7, 5, 10) == "Discount applied!"
        print("✓ test_calcular_descuento")
    except AssertionError:
        print("✗ test_calcular_descuento")
    
    try:
        assert promedio_puntajes([85, 90, 95]) == 90.0
        print("✓ test_promedio_puntajes")
    except AssertionError:
        print("✗ test_promedio_puntajes")
    
    try:
        assert validar_email("usuario@dominio.com") == True
        print("✓ test_validar_email")
    except AssertionError:
        print("✗ test_validar_email")
    
    print("\nTests manuales completados!")


if __name__ == "__main__":
    # Si se ejecuta directamente, mostrar información
    print("Archivo de Tests para Módulo 5 - Testing con pytest")
    print("=" * 60)
    print("\nPara ejecutar con pytest:")
    print("  pytest test_funciones.py")
    print("  pytest test_funciones.py -v")
    print("  pytest test_funciones.py::test_calcular_area_circulo")
    print("\nPara ejecutar tests manualmente:")
    ejecutar_tests_manualmente() 