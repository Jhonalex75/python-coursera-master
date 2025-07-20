import numpy as np
import matplotlib.pyplot as plt

# Physical parameters
alpha = 1.172e-5  # thermal diffusivity [m²/s]
Lx, Ly = 0.5, 0.5  # plate dimensions [m]
Nx, Ny = 50, 50    # grid resolution
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)

# Time parameters
dt = 0.25 * min(dx, dy)**2 / alpha  # stability condition
tiempo_total = 1200
Nt = int(tiempo_total / dt)

# Create grid
T = np.ones((Nx, Ny)) * 20.0  # initial temperature inside
T[0, :] = 100.0  # top boundary
T[:, 0] = 100.0  # left boundary
T[-1, :] = 0.0   # bottom boundary
T[:, -1] = 0.0   # right boundary

# For plotting later
T_snapshots = [T.copy()]
tiempos = [0.0]

# Time evolution
for step in range(Nt):
    T_new = T.copy()
    # Update internal points using finite difference
    T_new[1:-1, 1:-1] = T[1:-1, 1:-1] + alpha * dt * (
        (T[2:, 1:-1] - 2*T[1:-1, 1:-1] + T[0:-2, 1:-1]) / dx**2 +
        (T[1:-1, 2:] - 2*T[1:-1, 1:-1] + T[1:-1, 0:-2]) / dy**2
    )
    T = T_new

    # Save every 10% of time
    if (step + 1) % (Nt // 10) == 0:
        T_snapshots.append(T.copy())
        tiempos.append((step + 1) * dt)

# Visualization
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for ax, T_plot, t in zip(axes.flat, T_snapshots, tiempos):
    c = ax.imshow(T_plot, origin='lower', cmap='hot', extent=[0, Lx, 0, Ly])
    ax.set_title(f"t = {int(t)} s")
    fig.colorbar(c, ax=ax, shrink=0.8)
plt.suptitle("2D Heat Diffusion Over Time", fontsize=16)
plt.tight_layout()
plt.show()
