# -----------------------------------------------------------------------------
# Diagrama de Velocidad Límite de Sedimentación de Durand (Curvas Características)
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Graficar curvas características para análisis de ingeniería, como eficiencia,
# desempeño o parámetros de sistemas, usando el diagrama de Durand.
# Aplicación: Visualización de datos en estudios de ingeniería, mecánica de fluidos.
#
# Dependencias: numpy, matplotlib
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale las librerías necesarias si no las tiene:
#      pip install numpy matplotlib
#   3. Al ejecutar, se muestra la gráfica de curvas características.
# -----------------------------------------------------------------------------

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print("ERROR: Falta una dependencia. Instale con: pip install numpy matplotlib")
    raise e

# Crear figura y ejes
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111)

# Configurar los rangos principales de los ejes
ax.set_xlim(-0.6, 3)
ax.set_ylim(-6, 1.6)

# Curvas para el primer cuadrante (x positivo, y positivo): concentración por volumen
x_2 = [0, 0.25, 0.6, 1, 2, 3]
y_2 = [0, 1, 1.8, 1.25, 1.31, 1.34]

x_5 = [0, 0.2, 0.6, 1, 1.4, 2, 3]
y_5 = [0, 1.1, 1.35, 1.4, 1.38, 1.32, 1.34]

x_10 = [0, 0.4, 0.6, 1, 1.6, 2, 3]
y_10 = [0, 1.42, 1.44, 1.42, 1.35, 1.32, 1.34]

x_15 = [0, 0.2, 0.6, 1, 1.6, 2, 3]
y_15 = [0, 1.35, 1.5, 1.42, 1.35, 1.32, 1.34]

# Graficar las curvas con etiquetas
ax.plot(x_2, y_2, 'k-', label='2%')
ax.plot(x_5, y_5, 'k-', label='5%')
ax.plot(x_10, y_10, 'k-', label='10%')
ax.plot(x_15, y_15, 'k-', label='15%')

# Título para las curvas de concentración
ax.text(1.5, 1.5, 'CONCENTRACIÓN POR VOLUMEN REAL: Cv [%]\n(Para Cv>15% use 15%)', 
        ha='center', va='bottom', fontsize=10)

# Etiquetas para las curvas
ax.text(2.5, 1.2, '2', fontsize=10)
ax.text(2.5, 1.3, '5', fontsize=10)
ax.text(2.5, 1.35, '10', fontsize=10)
ax.text(2.5, 1.4, '15', fontsize=10)

# Líneas del segundo cuadrante (x negativo, y positivo): diámetro de tubería
pipe_diameters = [0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6]
for d in pipe_diameters:
    # Dibujar líneas desde el origen (0,0) hasta (x negativo, y máximo)
    ax.plot([0, -d], [0, 1.6], 'k-', linewidth=0.5)
    ax.text(-d, 1.55, str(d), rotation=90, fontsize=8)

# Líneas del tercer cuadrante (x negativo, y negativo): gravedad específica y velocidad
gravity_values = [0, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
velocity_values = np.linspace(0, 14, len(gravity_values))

for i, (g, v) in enumerate(zip(gravity_values, velocity_values)):
    ax.plot([-0.6, 0], [-g, 0], 'k-', linewidth=0.5)
    ax.text(-0.58, -g, f'{g}', ha='right', va='center', fontsize=8)
    ax.text(-0.02, -g, f'{v:.1f}', ha='right', va='center', fontsize=8)

# Etiquetas de los ejes y textos explicativos
ax.set_xlabel('DIÁMETRO DE PARTÍCULA: d50 [mm]')
ax.text(1.5, -0.5, 'DIÁMETRO DE PARTÍCULA: d50 [mm]', ha='center')
ax.text(-0.3, 0.8, 'DIÁMETRO DE TUBERÍA: D [m]', rotation=0)
ax.text(-0.55, -3, 'GRAVEDAD ESPECÍFICA DE SÓLIDOS: S [-]', rotation=90)
ax.text(-0.1, -3, 'VELOCIDAD LÍMITE DE SEDIMENTACIÓN: VL = FL√(gD(S-1)) [m/s]', rotation=90)

# Título principal
printf_title = "DIAGRAMA DE VELOCIDAD LÍMITE DE DURAND"
plt.title(printf_title)

# Cuadro de ejemplo
props = dict(boxstyle='square', facecolor='white', alpha=0.5)
example_text = 'EJEMPLO:\nd50 = 0.5 mm\nCv = 5%\nD = 0.2 m\nS = 2.65\n\nVL = 3.4 m/s\n(FL = 1.34)'
ax.text(2, -3, example_text, bbox=props)

# Configurar la cuadrícula
ax.grid(True, linestyle='--', alpha=0.3)

# Ocultar los ejes por defecto en x=0 y y=0
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.tight_layout()
plt.show()