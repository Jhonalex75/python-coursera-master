import math

def calculate_area_circle(radius):
    """Calcula el área de un círculo dado su radio."""
    return math.pi * radius**2

def calculate_circumference_circle(radius):
    """Calcula la circunferencia de un círculo dado su radio."""
    return 2 * math.pi * radius

class Rectangle:
    """Representa un rectángulo con ancho y alto."""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        """Calcula el área del rectángulo."""
        return self.width * self.height

    def calculate_perimeter(self):
        """Calcula el perímetro del rectángulo."""
        return 2 * (self.width + self.height)
