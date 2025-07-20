# -----------------------------------------------------------------------------
# Diagrama de Velocidad Límite de Sedimentación de Durand
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Graficar curvas de velocidad límite de sedimentación para diferentes
# diámetros de tubería y gravedad específica de sólidos, usando el modelo de Durand.
# Aplicación: Mecánica de fluidos, transporte de sedimentos.
#
# Dependencias: numpy, matplotlib
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale las librerías necesarias si no las tiene:
#      pip install numpy matplotlib
#   3. Al ejecutar, se muestra la gráfica del diagrama de Durand.
# -----------------------------------------------------------------------------

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError as e:
    print("ERROR: Falta una dependencia. Instale con: pip install numpy matplotlib")
    raise e

# Parámetros para el diagrama (valores de ejemplo)
D_values = [0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.06, 0.025]  # Diámetros de tubería (m)
Cv_values = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]  # Volumen de sólidos (no usado en este ejemplo)
d50_values = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]  # Tamaño medio de partícula (no usado en este ejemplo)
S_values = [1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]  # Gravedad específica de sólidos

# Función para calcular la velocidad límite de sedimentación (VL) según Durand
# FL es un factor adimensional (en este ejemplo se asume constante)
def calculate_VL(FL, D, S):
    g = 9.81  # aceleración debido a la gravedad (m/s^2)
    if S <= 1:
        return 0  # Si S <= 1, la velocidad límite de sedimentación es cero
    return FL * np.sqrt(2 * g * D * (S - 1))

# Crear la figura y los ejes para la gráfica
fig, ax = plt.subplots(figsize=(10, 8))

# Dibujar las líneas para diferentes valores de D (diámetro de tubería)
for D in D_values:
    VL_values = []
    for S in S_values:
        # Aquí deberías calcular FL basado en d50 y Cv, pero como no tenemos la fórmula exacta,
        # asumimos un valor constante para FL para este ejemplo.
        FL = 1.34  # Valor de ejemplo
        VL = calculate_VL(FL, D, S)
        VL_values.append(VL)
    ax.plot(S_values, VL_values, label=f'D={D} m')

# Configurar los ejes y etiquetas
ax.set_xlabel('GRAVEDAD ESPECÍFICA DE SÓLIDOS: S [-]')
ax.set_ylabel('VELOCIDAD LÍMITE DE SEDIMENTACIÓN: VL [m/s]')
ax.set_title("DIAGRAMA DE VELOCIDAD LÍMITE DE DURAND")
ax.legend(title='DIÁMETRO DE TUBERÍA: D [m]')

# Añadir la cuadrícula
ax.grid(True)

# Mostrar la gráfica
plt.show()