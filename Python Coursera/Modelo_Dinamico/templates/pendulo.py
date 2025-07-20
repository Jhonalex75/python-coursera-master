
from vpython import *

# Péndulo Doble - Versión Didáctica Mejorada y Corregida

# El análisis se basa en la mecánica Lagrangiana.
# Las variables son el ángulo de la barra superior (theta1) y el ángulo de la
# barra inferior (theta2), medidos desde la vertical.

scene.width = 800
scene.height = 600
scene.range = 1.8
scene.title = "Péndulo Doble Interactivo"
scene.caption = "\n<b>Controles de la Simulación:</b>\n"

# --- Variables Globales y Controles ---

g = 9.8
run = False  # La simulación comienza pausada
dt = 2e-5    # Paso de tiempo: debe ser pequeño para estabilidad
t = 0        # Tiempo de la simulación

# Variables para los objetos del péndulo (se declaran como None inicialmente)
pedestal, base, axle1, bar1, bar1b, axle2, bar2 = (None,) * 7
pendulum_objects = [] # Lista para contener todos los objetos y borrarlos fácilmente

# --- Funciones de la Interfaz de Usuario (UI) ---

def set_run(b):
    """Inicia o pausa la simulación."""
    global run
    run = not run
    if run:
        b.text = 'Pausa'
    else:
        b.text = 'Continuar'

def reset_simulation():
    """Crea o reinicia el péndulo con los valores de los sliders."""
    global t, run, M1, M2, L1, L2, theta1, theta2, thetadot1, thetadot2, p1, p2
    global bar1, bar2 # Necesitamos acceso global para las energías
    
    # Detener la simulación para reconstruir
    run = False
    run_button.text = 'Ejecutar'
    t = 0
    
    # Leer valores de los sliders
    M1 = M1_slider.value
    M2 = M2_slider.value
    L1 = L1_slider.value
    L2 = L2_slider.value
    M1_label.text = f'Masa 1: {M1:.2f} kg'
    M2_label.text = f'Masa 2: {M2:.2f} kg'
    L1_label.text = f'Longitud 1: {L1:.2f} m'
    L2_label.text = f'Longitud 2: {L2:.2f} m'
    
    # Limpiar objetos anteriores
    for obj in pendulum_objects:
        obj.visible = False
        del obj
    pendulum_objects.clear()

    # Condiciones iniciales
    theta1 = 1.3 * pi / 2
    theta2 = 0
    thetadot1 = 0
    thetadot2 = 0
    p1 = 0
    p2 = 0
    
    crear_pendulo_visual()
    
    # Reiniciar gráficos (con la corrección del error)
    if energy_graph is not None:
        energy_graph.delete()
    reset_graphs()


def crear_pendulo_visual():
    """Construye todos los objetos 3D del péndulo."""
    global pedestal, base, axle1, bar1, bar1b, axle2, bar2, pendulum_objects

    d = 0.05
    gap = 2 * d
    L1display = L1 + d
    L2display = L2 + d / 2
    hpedestal = 1.1 * (L1 + L2)
    wpedestal = 0.1
    tbase = 0.05
    wbase = 8 * gap
    offset = 2 * gap
    pedestal_top = vec(0, hpedestal / 2, 0)
    pivot1 = vec(pedestal_top.x, pedestal_top.y, 0)

    # Crear y almacenar objetos
    base = box(pos=pedestal_top - vec(0, hpedestal + tbase / 2, offset), size=vec(wbase, tbase, wbase), color=vec(0.4, 0.4, 0.5))
    pedestal = box(pos=pedestal_top - vec(0, hpedestal / 2, offset), size=vec(wpedestal, 1.1 * hpedestal, wpedestal), color=base.color)
    axle1 = cylinder(pos=pedestal_top - vec(0, 0, gap / 2 - d / 4), axis=vec(0, 0, -1), size=vec(offset, d / 4, d / 4), color=color.yellow)
    bar1 = box(pos=pivot1 + vec(L1 / 2, 0, -(gap + d) / 2), size=vec(L1display, d, d), color=color.red, axis=vec(sin(theta1), -cos(theta1), 0))
    bar1b = box(pos=pivot1 + vec(L1 / 2, 0, (gap + d) / 2), size=vec(L1display, d, d), color=bar1.color, axis=bar1.axis)
    
    pivot2_pos = pivot1 + L1 * bar1.axis.norm()
    axle2 = cylinder(pos=pivot2_pos, axis=vec(0, 0, 1), size=vec(gap + d, axle1.radius / 2, axle1.radius / 2), color=axle1.color)
    
    bar2_pos = pivot2_pos + (L2 / 2) * vec(sin(theta2), -cos(theta2), 0)
    bar2 = box(pos=bar2_pos, size=vec(L2display, d, d), color=color.green, axis=vec(sin(theta2), -cos(theta2), 0))
    
    # ✨ MEJORA DIDÁCTICA: Añadir un rastro a la segunda barra ✨
    attach_trail(bar2, type='curve', color=color.orange, radius=0.005, retain=200)

    pendulum_objects.extend([base, pedestal, axle1, bar1, bar1b, axle2, bar2])

# --- Botones y Sliders ---
scene.append_to_caption('   ')
run_button = button(text='Ejecutar', bind=set_run)
scene.append_to_caption('   ')
button(text='Reiniciar Simulación', bind=reset_simulation)
scene.append_to_caption('\n\n')

# ✨ MEJORA DIDÁCTICA: Sliders para control interactivo ✨
M1_slider = slider(min=0.1, max=5, value=1, step=0.1, bind=lambda: None)
M1_label = wtext(text=f'Masa 1: {M1_slider.value:.2f} kg\n')
scene.append_to_caption('\n')
M2_slider = slider(min=0.1, max=5, value=2, step=0.1, bind=lambda: None)
M2_label = wtext(text=f'Masa 2: {M2_slider.value:.2f} kg\n')
scene.append_to_caption('\n')
L1_slider = slider(min=0.1, max=2, value=0.5, step=0.05, bind=lambda: None)
L1_label = wtext(text=f'Longitud 1: {L1_slider.value:.2f} m\n')
scene.append_to_caption('\n')
L2_slider = slider(min=0.1, max=2, value=1, step=0.05, bind=lambda: None)
L2_label = wtext(text=f'Longitud 2: {L2_slider.value:.2f} m\n')


# --- Gráficos de Energía ---
energy_graph = None # Declarar la variable del gráfico
E_total_curve, K_trans_curve, K_rot_curve, U_grav_curve = (None,)*4

def reset_graphs():
    """Crea o reinicia las curvas del gráfico de energía."""
    global energy_graph, E_total_curve, K_trans_curve, K_rot_curve, U_grav_curve
    energy_graph = graph(width=600, height=300, title="<b>Análisis de Energía</b>",
                         xtitle="Tiempo (s)", ytitle="Energía (J)", scroll=True, xmin=0, xmax=10)
    E_total_curve = gcurve(color=color.black, label="E<sub>total</sub>")
    K_trans_curve = gcurve(color=color.red, label="K<sub>traslación</sub>")
    K_rot_curve = gcurve(color=color.purple, label="K<sub>rotación</sub>")
    U_grav_curve = gcurve(color=color.blue, label="U<sub>potencial</sub>")

# --- Funciones de Física y Actualización ---

def actualizar_fisica():
    """Calcula un paso de la simulación física."""
    global p1, p2, thetadot1, thetadot2, theta1, theta2
    
    # Ecuaciones de movimiento (Mecánica Lagrangiana)
    I1 = (1/12) * M1 * L1**2
    I2 = (1/12) * M2 * L2**2

    # Actualizar momentos generalizados (p1, p2)
    dp1_dt = -(1/2)*M2*L1*L2*thetadot1*thetadot2*sin(theta1-theta2) - ((1/2)*M1+M2)*g*L1*sin(theta1)
    dp2_dt = (1/2)*M2*L1*L2*thetadot1*thetadot2*sin(theta1-theta2) - (1/2)*M2*g*L2*sin(theta2)
    p1 += dp1_dt * dt
    p2 += dp2_dt * dt
    
    # Calcular velocidades angulares (thetadot1, thetadot2)
    den = 4*(M1+3*M2) - 9*M2*(cos(theta1-theta2))**2
    thetadot1 = (6/(L1**2))*(2*p1 - 3*(L1/L2)*cos(theta1-theta2)*p2) / den
    thetadot2 = (6/(M2*L2**2))*(2*p2*(M1+3*M2) - 3*M2*(L2/L1)*cos(theta1-theta2)*p1) / den
    
    # Actualizar ángulos
    theta1 += thetadot1 * dt
    theta2 += thetadot2 * dt

def actualizar_visuales_y_graficos():
    """Actualiza la posición de los objetos 3D y los gráficos."""
    
    # Guardar posiciones anteriores para calcular energía cinética
    pos1_old = vec(bar1.pos)
    pos2_old = vec(bar2.pos)

    # Actualizar posiciones y orientaciones
    pivot1 = vec(axle1.pos.x, axle1.pos.y, 0)
    bar1.axis = L1 * vec(sin(theta1), -cos(theta1), 0)
    bar1.pos = pivot1 + bar1.axis / 2
    bar1b.axis = bar1.axis
    bar1b.pos = bar1.pos + vec(0, 0, bar1b.pos.z - bar1.pos.z)
    
    pivot2 = pivot1 + bar1.axis
    axle2.pos = pivot2
    bar2.axis = L2 * vec(sin(theta2), -cos(theta2), 0)
    bar2.pos = pivot2 + bar2.axis / 2
    
    # Calcular energías
    I1 = (1/12) * M1 * L1**2
    I2 = (1/12) * M2 * L2**2
    
    v1 = (bar1.pos - pos1_old) / dt
    v2 = (bar2.pos - pos2_old) / dt
    
    K_trans = 0.5 * M1 * mag2(v1) + 0.5 * M2 * mag2(v2)
    K_rot = 0.5 * I1 * thetadot1**2 + 0.5 * I2 * thetadot2**2
    U_grav = M1 * g * bar1.pos.y + M2 * g * bar2.pos.y
    E_total = K_trans + K_rot + U_grav
    
    # Graficar energías
    E_total_curve.plot(t, E_total)
    K_trans_curve.plot(t, K_trans)
    K_rot_curve.plot(t, K_rot)
    U_grav_curve.plot(t, U_grav)

# --- Bucle Principal ---

reset_simulation() # Crear la configuración inicial

while True:
    rate(1 / dt)
    if not run:
        continue  # Si está en pausa, no hacer nada

    actualizar_fisica()
    actualizar_visuales_y_graficos()
    
    t += dt