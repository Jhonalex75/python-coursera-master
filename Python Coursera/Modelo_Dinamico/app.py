from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde el navegador
CORS(app)

# --- Parámetros del Mecanismo ---
L1 = 7.0
L2 = 3.0
L3 = 5.0
L4 = 5.0
L5 = 4.0

def solve_kinematics_python(theta2_deg, theta5_deg):
    """
    Esta es la versión en Python de la lógica de cinemática.
    """
    theta2_rad = np.deg2rad(theta2_deg)
    theta5_rad = np.deg2rad(theta5_deg)

    p1 = np.array([0, 0])
    p6 = np.array([L1, 0])

    p2 = np.array([L2 * np.cos(theta2_rad), L2 * np.sin(theta2_rad)])
    p4 = np.array([L1 + L5 * np.cos(theta5_rad), L5 * np.sin(theta5_rad)])

    d = np.linalg.norm(p4 - p2)

    if d > L3 + L4 or d < np.abs(L3 - L4) or d == 0:
        return {"error": "Configuración imposible.", "points": None}

    # Manejo de posible valor negativo en la raíz cuadrada
    a_squared_component = (L3**2 - L4**2 + d**2) / (2 * d)
    if a_squared_component**2 > L3**2:
        return {"error": "Configuración imposible (cálculo h).", "points": None}
    
    a = (L3**2 - L4**2 + d**2) / (2 * d)
    h = np.sqrt(L3**2 - a**2)

    p_mid = p2 + a * (p4 - p2) / d
    
    p3_1 = np.array([
        p_mid[0] + h * (p4[1] - p2[1]) / d,
        p_mid[1] - h * (p4[0] - p2[0]) / d
    ])
    
    positions = {
        "p1": p1.tolist(),
        "p2": p2.tolist(),
        "p3": p3_1.tolist(),
        "p4": p4.tolist(),
        "p5": p6.tolist()
    }
    
    return {"error": None, "points": positions}

@app.route('/calculate')
def calculate():
    """Punto de API para calcular las posiciones."""
    theta2 = request.args.get('theta2', default=45, type=float)
    theta5 = request.args.get('theta5', default=120, type=float)
    result = solve_kinematics_python(theta2, theta5)
    return jsonify(result)

@app.route('/')
def index():
    """Ruta principal que podría servir el HTML si fuera necesario."""
    return "Servidor del mecanismo de 5 barras funcionando. La interfaz es un archivo HTML autónomo."

if __name__ == '__main__':
    # Ejecutar el servidor para que sea visible en la red local.
    # Necesario si el HTML hiciera peticiones a este servidor.
    app.run(debug=True, host='0.0.0.0', port=5000)
