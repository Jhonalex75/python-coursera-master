from vpython import *
import numpy as np

# Parámetros del mecanismo
L1 = 2     # Longitud barra 1
L2 = 1.5   # Longitud barra 2
L3 = 2     # Longitud barra 3
L4 = 1.5   # Longitud barra 4

# Ángulo de entrada (M2)
theta2 = 0

# Crear la escena
scene = canvas(title="Mecanismo de 4 barras", width=800, height=600)

# Crear barras y puntos
p1 = vector(0, 0, 0)
p2 = vector(L1, 0, 0)
joint1 = sphere(pos=p1, radius=0.05, color=color.red)
joint2 = sphere(pos=p2, radius=0.05, color=color.red)
bar1 = cylinder(pos=p1, axis=p2-p1, radius=0.03, color=color.blue)

# Inicializar posiciones de las otras barras
joint3 = sphere(radius=0.05, color=color.green)
joint4 = sphere(radius=0.05, color=color.green)
bar2 = cylinder(radius=0.03, color=color.orange)
bar3 = cylinder(radius=0.03, color=color.cyan)
bar4 = cylinder(radius=0.03, color=color.magenta)

# Control deslizante para M2
slider_M2 = slider(min=0, max=2*np.pi, value=0, length=300, right=15)
label_M2 = wtext(text=f"Ángulo M2: {slider_M2.value:.2f} rad")

# Cinemática simplificada de 4 barras
def fourbar_positions(theta2):
    # p1 y p2 son fijos
    # Calcula p3 y p4 usando geometría simplificada
    x3 = L1 + L2 * np.cos(theta2)
    y3 = L2 * np.sin(theta2)
    p3 = vector(x3, y3, 0)
    # Para p4, se puede usar el método de posición de cierre (simplificado aquí)
    x4 = x3 + L3
    y4 = y3
    p4 = vector(x4, y4, 0)
    return p3, p4

## Eliminado el uso de bind y la función update_M2

# Animación principal
while True:
    rate(60)
    theta2 = slider_M2.value
    label_M2.text = f"Ángulo M2: {theta2:.2f} rad"
    p3, p4 = fourbar_positions(theta2)
    joint3.pos = p3
    joint4.pos = p4
    bar2.pos = p2
    bar2.axis = p3 - p2
    bar3.pos = p3
    bar3.axis = p4 - p3
    bar4.pos = p4
    bar4.axis = p1 - p4
