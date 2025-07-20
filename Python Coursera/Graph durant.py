# -----------------------------------------------------------------------------
# Purpose: Plot characteristic curves for engineering analysis (e.g., efficiency, performance, or other system parameters).
# Application: Data visualization in engineering studies.
# Dependencies: numpy, matplotlib
# Usage: Run the script to display the characteristic curves.
# -----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

# Create figure and axes
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111)

# Set up the main axes ranges
ax.set_xlim(-0.6, 3)
ax.set_ylim(-6, 1.6)

# Create the curves for first quadrant (positive x, positive y)
x_2 = [0, 0.25, 0.6, 1, 2, 3]
y_2 = [0, 1, 1.8, 1.25, 1.31, 1.34]

x_5 = [0, 0.2, 0.6, 1, 1.4, 2, 3]
y_5 = [0, 1.1, 1.35, 1.4, 1.38, 1.32, 1.34]

x_10 = [0, 0.4, 0.6, 1, 1.6, 2, 3]
y_10 = [0, 1.42, 1.44, 1.42, 1.35, 1.32, 1.34]

x_15 = [0, 0.2, 0.6, 1, 1.6, 2, 3]
y_15 = [0, 1.35, 1.5, 1.42, 1.35, 1.32, 1.34]

# Plot the curves with labels
ax.plot(x_2, y_2, 'r-', label='2%')
ax.plot(x_5, y_5, 'b-', label='5%')
ax.plot(x_10, y_10, 'g-', label='10%')
ax.plot(x_15, y_15, 'm-', label='15%')

# Add title for concentration curves
ax.text(1.5, 1.5, 'CONCENTRATION BY TRUE VOLUME: Cv [%]\n(For Cv>15% use 15%)', 
        ha='center', va='bottom', fontsize=10)

# Add labels for curves
ax.text(2.5, 1.2, '2', fontsize=10)
ax.text(2.5, 1.3, '5', fontsize=10)
ax.text(2.5, 1.35, '10', fontsize=10)
ax.text(2.5, 1.4, '15', fontsize=10)

# Second quadrant lines (negative x, positive y)
pipe_diameters = [0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6]
for d in pipe_diameters:
    # Draw lines from origin (0,0) to (negative x, max y)
    ax.plot([0, -d], [0, 1.6], 'k-', linewidth=0.5)
    ax.text(-d, 1.55, str(d), rotation=90, fontsize=8)

# Third quadrant lines (negative x, negative y)
gravity_values = [0, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
velocity_values = np.linspace(0, 14, len(gravity_values))

for i, (g, v) in enumerate(zip(gravity_values, velocity_values)):
    ax.plot([-0.6, 0], [-g, 0], 'k-', linewidth=0.5)
    ax.text(-0.58, -g, f'{g}', ha='right', va='center', fontsize=8)
    ax.text(-0.02, -g, f'{v:.1f}', ha='right', va='center', fontsize=8)

# Set up axis labels
ax.set_xlabel('PARTICLE DIAMETER: d50 [mm]')
ax.text(1.5, -0.5, 'PARTICLE DIAMETER: d50 [mm]', ha='center')
ax.text(-1, 1.8, 'PIPE DIAMETER: D [m]', rotation=0)
ax.text(-1, -3, 'SOLIDS SPECIFIC GRAVITY: S [-]', rotation=90)
ax.text(0.1, -4, 'LIMITING SETTLING VELOCITY: VL = FL√(gD(S-1)) [m/s]', rotation=90)

# Add title
plt.title("DURAND'S LIMITING SETTLING VELOCITY DIAGRAM")

# Add example box
props = dict(boxstyle='square', facecolor='white', alpha=0.5)
example_text = 'EXAMPLE:\nd50 = 0.5 mm\nCv = 5%\nD = 0.2 m\nS = 2.65\n\nVL = 3.4 m/s\n(FL = 1.34)'
ax.text(2, -3, example_text, bbox=props)

# Configure grid
ax.grid(True, linestyle='--', alpha=0.3)

# Hide the default axes at x=0 and y=0
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.tight_layout()
plt.show()