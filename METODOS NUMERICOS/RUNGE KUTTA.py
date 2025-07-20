# -----------------------------------------------------------------------------
# Purpose: Solve a second-order differential equation (mass-spring-damper system) using the 4th order Runge-Kutta method and plot the results.
# Application: Numerical methods, dynamic systems simulation.
# Dependencies: numpy, matplotlib
# Usage: Run the script to simulate and visualize the system response.
# -----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# Parameters
m = 1.0  # mass (kg)
c = 0.2  # damping coefficient (kg/s)
k = 1.0  # spring constant (N/m)

# Initial conditions
x0 = 1.0  # initial displacement (m)
v0 = 0.0  # initial velocity (m/s)

# Time parameters
t0 = 0.0  # initial time (s)
tf = 20.0  # final time (s)
dt = 0.01  # time step (s)

# Differential equation system
def derivatives(t, y):
    x, v = y
    dxdt = v
    dvdt = -(c/m) * v - (k/m) * x
    return np.array([dxdt, dvdt])

# Runge-Kutta 4th order method
def rk4_step(f, t, y, dt):
    k1 = f(t, y)
    k2 = f(t + 0.5*dt, y + 0.5*dt*k1)
    k3 = f(t + 0.5*dt, y + 0.5*dt*k2)
    k4 = f(t + dt, y + dt*k3)
    return y + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

# Time integration
t_values = np.arange(t0, tf, dt)
y_values = np.zeros((len(t_values), 2))
y_values[0] = [x0, v0]

for i in range(1, len(t_values)):
    t = t_values[i-1]
    y = y_values[i-1]
    y_values[i] = rk4_step(derivatives, t, y, dt)

# Extract displacement and velocity
x_values = y_values[:, 0]
v_values = y_values[:, 1]

# Plot results
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t_values, x_values, label='Displacement (x)')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t_values, v_values, label='Velocity (v)', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()