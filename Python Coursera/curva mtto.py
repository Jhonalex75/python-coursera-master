# -----------------------------------------------------------------------------
# Curva de la Bañera (Bathtub Curve) - Tasa de Fallos en Equipos
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Graficar la curva de la bañera, que representa la tasa de fallos a lo largo
# de la vida útil de un equipo (mortalidad infantil, vida útil, desgaste).
# Aplicación: Ingeniería de mantenimiento, análisis de confiabilidad.
#
# Dependencias: numpy, matplotlib
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale las librerías necesarias si no las tiene:
#      pip install numpy matplotlib
#   3. Al ejecutar, se muestra la gráfica de la curva de la bañera.
# -----------------------------------------------------------------------------

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError as e:
    print("ERROR: Falta una dependencia. Instale con: pip install numpy matplotlib")
    raise e

# Parámetros para cada región de la curva de la bañera
alpha1, beta1 = 1000, 0.5  # Mortalidad infantil (fallos decrecientes)
alpha2, beta2 = 1000, 1.0  # Vida útil (fallos constantes)
alpha3, beta3 = 1000, 3.0  # Desgaste (fallos crecientes)

# Tiempo (evitar t=0 para evitar división por cero)
t = np.linspace(0.1, 3000, 1000)

# Calcular tasas de fallo utilizando la función de riesgo de Weibull
h_infantil = (beta1 / alpha1) * (t / alpha1) ** (beta1 - 1)  # Mortalidad infantil
h_util = (beta2 / alpha2) * (t / alpha2) ** (beta2 - 1)      # Vida útil
h_desgaste = (beta3 / alpha3) * (t / alpha3) ** (beta3 - 1)  # Desgaste

# Inicializar arreglo de tasas de fallo
h_bathtub = np.zeros_like(t)

# Combinar por tramos:
# - Primer tramo: mortalidad infantil
# - Segundo tramo: vida útil
# - Tercer tramo: desgaste
h_bathtub[t < 1000] = h_infantil[t < 1000]
h_bathtub[(t >= 1000) & (t < 2000)] = h_util[(t >= 1000) & (t < 2000)]
h_bathtub[t >= 2000] = h_desgaste[t >= 2000]

# Graficar la curva de la bañera
plt.figure(figsize=(10, 6))
plt.plot(t, h_bathtub, label="Curva de la Bañera", color="blue")
plt.title("Curva de la Bañera (Tasa de Fallos)")
plt.xlabel("Tiempo (horas)")
plt.ylabel("Tasa de Fallos")
plt.legend()
plt.grid(True)
plt.show()
