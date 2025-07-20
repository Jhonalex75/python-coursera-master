"""
Módulo 3: Ordenamiento y Manejo de Errores
==========================================

Este módulo cubre:
- Algoritmos de ordenamiento (bubble sort, quick sort)
- Manejo de excepciones con try/except
- Validación de datos de entrada
- Análisis de datos con manejo de errores
- Casos prácticos de la vida real

Autor: Curso Python Coursera
Versión: 1.0
"""

import random
import time
from typing import List, Dict, Any, Optional


class AnalizadorPuntajes:
    """
    Clase para analizar puntajes de exámenes con manejo de errores
    """
    
    def __init__(self):
        self.estudiantes = []
        self.puntajes = {}
        self.historial_errores = []
    
    def agregar_estudiante(self, nombre: str, puntaje: int) -> bool:
        """
        Agregar un estudiante con su puntaje
        
        Args:
            nombre: Nombre del estudiante
            puntaje: Puntaje del examen (0-100)
            
        Returns:
            bool: True si se agregó correctamente, False si hubo error
        """
        try:
            # Validaciones
            if not nombre or not nombre.strip():
                raise ValueError("El nombre no puede estar vacío")
            
            if not isinstance(puntaje, (int, float)):
                raise ValueError("El puntaje debe ser un número")
            
            if not 0 <= puntaje <= 100:
                raise ValueError("El puntaje debe estar entre 0 y 100")
            
            # Agregar estudiante
            self.estudiantes.append(nombre)
            self.puntajes[nombre] = puntaje
            return True
            
        except Exception as e:
            self.historial_errores.append(f"Error al agregar {nombre}: {str(e)}")
            return False
    
    def obtener_puntajes(self) -> List[int]:
        """
        Extraer lista de puntajes de los estudiantes
        
        Returns:
            List[int]: Lista de puntajes
        """
        return list(self.puntajes.values())
    
    def bubble_sort(self, lista: List[int]) -> List[int]:
        """
        Implementación del algoritmo de ordenamiento burbuja
        
        Args:
            lista: Lista de números a ordenar
            
        Returns:
            List[int]: Lista ordenada de menor a mayor
        """
        lista_ordenada = lista.copy()
        n = len(lista_ordenada)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_ordenada[j] > lista_ordenada[j + 1]:
                    # Intercambiar elementos
                    lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
        
        return lista_ordenada
    
    def quick_sort(self, lista: List[int]) -> List[int]:
        """
        Implementación del algoritmo de ordenamiento rápido
        
        Args:
            lista: Lista de números a ordenar
            
        Returns:
            List[int]: Lista ordenada de menor a mayor
        """
        if len(lista) <= 1:
            return lista
        
        pivote = lista[len(lista) // 2]
        menores = [x for x in lista if x < pivote]
        iguales = [x for x in lista if x == pivote]
        mayores = [x for x in lista if x > pivote]
        
        return self.quick_sort(menores) + iguales + self.quick_sort(mayores)
    
    def calcular_estadisticas(self) -> Dict[str, Any]:
        """
        Calcular estadísticas de los puntajes con manejo de errores
        
        Returns:
            Dict con estadísticas o None si hay error
        """
        try:
            if not self.puntajes:
                raise ValueError("No hay puntajes para analizar")
            
            puntajes_lista = self.obtener_puntajes()
            puntajes_ordenados = self.bubble_sort(puntajes_lista)
            
            estadisticas = {
                'total_estudiantes': len(self.estudiantes),
                'puntaje_minimo': puntajes_ordenados[0],
                'puntaje_maximo': puntajes_ordenados[-1],
                'promedio': sum(puntajes_lista) / len(puntajes_lista),
                'mediana': self._calcular_mediana(puntajes_ordenados),
                'puntajes_ordenados': puntajes_ordenados,
                'estudiantes_ordenados': self._ordenar_estudiantes_por_puntaje()
            }
            
            return estadisticas
            
        except Exception as e:
            self.historial_errores.append(f"Error al calcular estadísticas: {str(e)}")
            return None
    
    def _calcular_mediana(self, lista_ordenada: List[int]) -> float:
        """
        Calcular la mediana de una lista ordenada
        
        Args:
            lista_ordenada: Lista de números ordenados
            
        Returns:
            float: Valor de la mediana
        """
        n = len(lista_ordenada)
        if n % 2 == 0:
            return (lista_ordenada[n//2 - 1] + lista_ordenada[n//2]) / 2
        else:
            return lista_ordenada[n//2]
    
    def _ordenar_estudiantes_por_puntaje(self) -> List[tuple]:
        """
        Ordenar estudiantes por puntaje de mayor a menor
        
        Returns:
            List[tuple]: Lista de tuplas (estudiante, puntaje) ordenadas
        """
        return sorted(self.puntajes.items(), key=lambda x: x[1], reverse=True)
    
    def obtener_errores(self) -> List[str]:
        """
        Obtener historial de errores
        
        Returns:
            List[str]: Lista de errores registrados
        """
        return self.historial_errores.copy()


def comparar_algoritmos_ordenamiento():
    """
    Comparar rendimiento de diferentes algoritmos de ordenamiento
    """
    print("=== Comparación de Algoritmos de Ordenamiento ===\n")
    
    # Generar datos de prueba
    tamanos = [100, 1000, 5000]
    
    for tamano in tamanos:
        print(f"Probando con {tamano} elementos:")
        
        # Generar lista aleatoria
        datos = [random.randint(1, 1000) for _ in range(tamano)]
        
        # Bubble Sort
        inicio = time.time()
        bubble_result = bubble_sort_simple(datos.copy())
        tiempo_bubble = time.time() - inicio
        
        # Quick Sort
        inicio = time.time()
        quick_result = quick_sort_simple(datos.copy())
        tiempo_quick = time.time() - inicio
        
        # Sort nativo de Python
        inicio = time.time()
        python_result = sorted(datos)
        tiempo_python = time.time() - inicio
        
        print(f"  Bubble Sort: {tiempo_bubble:.4f} segundos")
        print(f"  Quick Sort:  {tiempo_quick:.4f} segundos")
        print(f"  Python Sort: {tiempo_python:.4f} segundos")
        print()


def bubble_sort_simple(lista: List[int]) -> List[int]:
    """Versión simple de bubble sort para comparación"""
    lista_ordenada = lista.copy()
    n = len(lista_ordenada)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_ordenada[j] > lista_ordenada[j + 1]:
                lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
    
    return lista_ordenada


def quick_sort_simple(lista: List[int]) -> List[int]:
    """Versión simple de quick sort para comparación"""
    if len(lista) <= 1:
        return lista
    
    pivote = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    
    return quick_sort_simple(menores) + iguales + quick_sort_simple(mayores)


def ejemplo_manejo_errores_avanzado():
    """
    Ejemplo avanzado de manejo de errores con múltiples tipos de excepciones
    """
    print("=== Ejemplo Avanzado de Manejo de Errores ===\n")
    
    # Crear analizador
    analizador = AnalizadorPuntajes()
    
    # Casos de prueba con errores
    casos_prueba = [
        ("Juan", 85),      # Caso válido
        ("", 90),          # Nombre vacío
        ("María", -5),     # Puntaje negativo
        ("Pedro", 150),    # Puntaje muy alto
        ("Ana", "abc"),    # Puntaje no numérico
        ("Carlos", 92),    # Caso válido
        (None, 88),        # Nombre None
        ("Elena", 95),     # Caso válido
    ]
    
    print("Agregando estudiantes con posibles errores:")
    for nombre, puntaje in casos_prueba:
        resultado = analizador.agregar_estudiante(nombre, puntaje)
        if resultado:
            print(f"✓ {nombre}: {puntaje}")
        else:
            print(f"✗ Error con {nombre}: {puntaje}")
    
    print(f"\nEstudiantes agregados exitosamente: {len(analizador.estudiantes)}")
    print(f"Errores registrados: {len(analizador.historial_errores)}")
    
    # Mostrar errores
    if analizador.historial_errores:
        print("\nErrores registrados:")
        for error in analizador.historial_errores:
            print(f"  - {error}")
    
    # Calcular estadísticas
    print("\nCalculando estadísticas:")
    estadisticas = analizador.calcular_estadisticas()
    
    if estadisticas:
        print(f"Total estudiantes: {estadisticas['total_estudiantes']}")
        print(f"Puntaje mínimo: {estadisticas['puntaje_minimo']}")
        print(f"Puntaje máximo: {estadisticas['puntaje_maximo']}")
        print(f"Promedio: {estadisticas['promedio']:.2f}")
        print(f"Mediana: {estadisticas['mediana']}")
        
        print("\nEstudiantes ordenados por puntaje:")
        for estudiante, puntaje in estadisticas['estudiantes_ordenados']:
            print(f"  {estudiante}: {puntaje}")


def ejercicios_practicos():
    """
    Ejercicios prácticos para el módulo 3
    """
    print("\n=== Ejercicios Prácticos ===\n")
    
    # Ejercicio 1: Ordenamiento personalizado
    print("Ejercicio 1: Ordenamiento personalizado")
    productos = [
        ("Laptop", 1200, 4.5),
        ("Mouse", 25, 4.2),
        ("Teclado", 80, 4.8),
        ("Monitor", 300, 4.3),
        ("Auriculares", 150, 4.6)
    ]
    
    # Ordenar por precio
    productos_por_precio = sorted(productos, key=lambda x: x[1])
    print("Productos ordenados por precio:")
    for producto in productos_por_precio:
        print(f"  {producto[0]}: ${producto[1]} (Rating: {producto[2]})")
    
    # Ordenar por rating
    productos_por_rating = sorted(productos, key=lambda x: x[2], reverse=True)
    print("\nProductos ordenados por rating:")
    for producto in productos_por_rating:
        print(f"  {producto[0]}: Rating {producto[2]} (${producto[1]})")
    
    # Ejercicio 2: Manejo de errores en cálculos
    print("\nEjercicio 2: Calculadora con manejo de errores")
    
    def calculadora_segura(operacion, a, b):
        try:
            if operacion == "suma":
                return a + b
            elif operacion == "resta":
                return a - b
            elif operacion == "multiplicacion":
                return a * b
            elif operacion == "division":
                if b == 0:
                    raise ValueError("División por cero no permitida")
                return a / b
            else:
                raise ValueError(f"Operación '{operacion}' no reconocida")
        except Exception as e:
            return f"Error: {str(e)}"
    
    operaciones = [
        ("suma", 10, 5),
        ("resta", 10, 5),
        ("multiplicacion", 10, 5),
        ("division", 10, 5),
        ("division", 10, 0),
        ("potencia", 2, 3)
    ]
    
    for op, a, b in operaciones:
        resultado = calculadora_segura(op, a, b)
        print(f"  {op}({a}, {b}) = {resultado}")


def main():
    """
    Función principal del módulo 3
    """
    print("MÓDULO 3: ORDENAMIENTO Y MANEJO DE ERRORES")
    print("=" * 50)
    
    # Ejemplo básico
    print("\n1. Ejemplo básico de ordenamiento:")
    estudiantes = ["John", "Lisa", "Mary", "Chris", "Linda", "Matt"]
    puntajes = [87, 90, 75, 100, 100, 70]
    
    print(f"Estudiantes: {estudiantes}")
    print(f"Puntajes: {puntajes}")
    
    # Ordenar puntajes
    analizador = AnalizadorPuntajes()
    for estudiante, puntaje in zip(estudiantes, puntajes):
        analizador.agregar_estudiante(estudiante, puntaje)
    
    estadisticas = analizador.calcular_estadisticas()
    if estadisticas:
        print(f"Puntajes ordenados: {estadisticas['puntajes_ordenados']}")
        print(f"Promedio: {estadisticas['promedio']:.2f}")
    
    # Comparación de algoritmos
    print("\n2. Comparación de algoritmos de ordenamiento:")
    comparar_algoritmos_ordenamiento()
    
    # Manejo de errores avanzado
    print("\n3. Manejo de errores avanzado:")
    ejemplo_manejo_errores_avanzado()
    
    # Ejercicios prácticos
    ejercicios_practicos()
    
    print("\n" + "=" * 50)
    print("¡Módulo 3 completado exitosamente!")


if __name__ == "__main__":
    main() 