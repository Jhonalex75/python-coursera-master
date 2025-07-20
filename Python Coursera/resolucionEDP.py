import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros de la simulación ---
# Propiedades del material (acero)
alpha = 1.172e-5  # Difusividad térmica en m^2/s

# Dimensiones de la barra
L = 0.5          # Longitud de la barra en metros
tiempo_total = 1200 # Tiempo total de simulación en segundos

# Parámetros de discretización
Nx = 50          # Número de puntos en el espacio
dx = L / (Nx - 1)  # Distancia entre puntos

# Paso de tiempo (asegurando la estabilidad)
factor_estabilidad = 0.5
dt = factor_estabilidad * dx**2 / alpha
Nt = int(tiempo_total / dt)

# --- Condiciones iniciales y de contorno ---
# Arreglo para la temperatura
T = np.zeros(Nx)

# Condición inicial: toda la barra a 20°C
T.fill(20.0)

# Condiciones de contorno (fijas en el tiempo)
T[0] = 100.0     # Extremo izquierdo a 100°C
T[-1] = 0.0      # Extremo derecho a 0°C

# Lista para guardar la solución en diferentes instantes
T_solucion = [T.copy()]
tiempos_guardados = [0.0]

# --- Bucle de simulación ---
for j in range(Nt):
    T_anterior = T.copy()
    for i in range(1, Nx - 1):
        # Aplicar la ecuación de actualización de diferencias finitas
        T[i] = T_anterior[i] + (alpha * dt / dx**2) * \
               (T_anterior[i+1] - 2*T_anterior[i] + T_anterior[i-1])

    # Guardar la solución en ciertos instantes para graficarla
    if (j + 1) % (Nt // 10) == 0:
        T_solucion.append(T.copy())
        tiempos_guardados.append((j + 1) * dt)

# --- Visualización ---
x_puntos = np.linspace(0, L, Nx)
plt.figure(figsize=(12, 7))

for i, T_perfil in enumerate(T_solucion):
    plt.plot(x_puntos, T_perfil, label=f't = {tiempos_guardados[i]:.0f} s')

plt.title('Evolución de la Temperatura en una Barra Metálica (Método de Diferencias Finitas)', fontsize=16)
plt.xlabel('Posición a lo largo de la barra (m)', fontsize=12)
plt.ylabel('Temperatura (°C)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, L)
plt.ylim(-5, 105)
plt.show()