# -----------------------------------------------------------------------------
# Purpose: Plot sedimentation velocity curves for different particle and fluid parameters.
# Application: Fluid mechanics, sediment transport analysis.
# Dependencies: numpy, matplotlib
# Usage: Run the script to visualize sedimentation velocity for various conditions.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# Parámetros para el diagrama
D_values = [0.6, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.06, 0.025]
Cv_values = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]
d50_values = [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]
S_values = [1.6, 1.5, 1.4, 1.3, 1.2, 1.1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]

# Función para calcular la velocidad límite de sedimentación (VL)
def calculate_VL(FL, D, S):
    g = 9.81  # aceleración debido a la gravedad (m/s^2)
    if S <= 1:
        return 0  # Si S <= 1, la velocidad límite de sedimentación es cero
    return FL * np.sqrt(2 * g * D * (S - 1))

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 8))

# Dibujar las líneas para diferentes valores de D
for D in D_values:
    VL_values = []
    for S in S_values:
        # Aquí deberías calcular FL basado en d50 y Cv, pero como no tenemos la fórmula exacta,
        # asumiremos un valor constante para FL para este ejemplo.
        FL = 1.34  # Valor de ejemplo
        VL = calculate_VL(FL, D, S)
        VL_values.append(VL)
    
    ax.plot(S_values, VL_values, label=f'D={D} m')

# Configurar los ejes y etiquetas
ax.set_xlabel('SOLIDS SPECIFIC GRAVITY: S [-]')
ax.set_ylabel('LIMITING SETTLING VELOCITY: VL [m/s]')
ax.set_title("DURAND'S LIMITING SETTLING VELOCITY DIAGRAM")
ax.legend(title='PIPE DIAMETER: D [m]')

# Añadir la cuadrícula
ax.grid(True)

# Mostrar la gráfica
plt.show()