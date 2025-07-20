# Web VPython 3.2
from vpython import *

# ===================================================================
# 1. DEFINICIÓN DE FUNCIONES
# ===================================================================

def ajustar_angulo(slider_widget):
    """Actualiza el texto que muestra el ángulo seleccionado."""
    texto_angulo.text = f'{slider_widget.value}°'

def lanzar_esfera():
    """Ejecuta la simulación del movimiento parabólico."""
    global simulacion_activa
    
    # Detiene la simulación anterior si estuviera activa
    simulacion_activa = False 
    sleep(0.02) # Pequeña pausa para asegurar que el bucle anterior termine

    # Inicia la nueva simulación
    simulacion_activa = True

    # Resetea la posición y el rastro de la esfera
    esfera.pos = vec(0, 0, 0)
    esfera.clear_trail()

    # Lee el ángulo y calcula la velocidad inicial
    angulo_rad = radians(angulo_slider.value)
    v_x = velocidad_inicial * cos(angulo_rad)
    v_y = velocidad_inicial * sin(angulo_rad)
    esfera.velocity = vec(v_x, v_y, 0)
    
    # Bucle de física: se ejecuta mientras la esfera esté sobre el suelo
    while esfera.pos.y >= 0:
        # Si simulacion_activa se vuelve False, se detiene este lanzamiento
        if not simulacion_activa:
            break
            
        rate(100) # Controla la velocidad de la animación

        # Aplica la gravedad para actualizar la velocidad y luego la posición
        esfera.velocity += fuerza_gravedad * dt
        esfera.pos += esfera.velocity * dt

    simulacion_activa = False


# ===================================================================
# 2. CONFIGURACIÓN DE LA ESCENA Y OBJETOS
# ===================================================================

scene.width = 800
scene.height = 500
scene.autoscale = False
scene.range = 20
scene.center = vec(15, 5, 0)
scene.caption = "Usa el deslizador para cambiar el ángulo y presiona 'Lanzar'.\n\n"

suelo = box(pos=vec(15, -0.5, 0), size=vec(40, 1, 10), color=color.green)
esfera = sphere(pos=vec(0, 0, 0), radius=0.5, color=color.yellow, make_trail=False) # Trail se controla manualmente
attach_trail(esfera, color=color.cyan, radius=0.1)


# ===================================================================
# 3. PARÁMETROS Y CONTROLES
# ===================================================================

# Parámetros Físicos
g = 9.8
velocidad_inicial = 20
dt = 0.01
fuerza_gravedad = vec(0, -g, 0)
simulacion_activa = False

# Controles Interactivos (Sliders y Botones)
angulo_slider = slider(min=0, max=90, value=45, step=1, bind=ajustar_angulo)
texto_angulo = wtext(text=f'{angulo_slider.value}°')
scene.append_to_caption("   ")
lanzar_boton = button(text="Lanzar", bind=lanzar_esfera)


# ===================================================================
# 4. BUCLE PRINCIPAL PARA MANTENER EL PROGRAMA ACTIVO
# ===================================================================

while True:
    rate(100) # Espera y procesa eventos (como clics de botón)