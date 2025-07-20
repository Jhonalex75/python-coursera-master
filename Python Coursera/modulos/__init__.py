# =============================================================================
# MÓDULOS DE INGENIERÍA MECÁNICA
# =============================================================================
# Paquete que contiene todos los módulos especializados de ingeniería mecánica
# =============================================================================

__version__ = "1.0.0"
__author__ = "Sistema de Ingeniería Mecánica con Python"

# Lista de módulos disponibles
MODULOS_DISPONIBLES = [
    "analisis_estructural",
    "dinamica_maquinas", 
    "termo_fluidos",
    "materiales",
    "control",
    "manufactura",
    "mantenimiento",
    "gestion_proyectos"
]

# Descripción de cada módulo
DESCRIPCION_MODULOS = {
    "analisis_estructural": "Análisis de estructuras, vigas, columnas y elementos mecánicos",
    "dinamica_maquinas": "Análisis dinámico de máquinas, vibraciones y balanceo",
    "termo_fluidos": "Termodinámica, transferencia de calor y mecánica de fluidos",
    "materiales": "Propiedades de materiales, resistencia y selección",
    "control": "Sistemas de control, automatización y robótica",
    "manufactura": "Procesos de manufactura, CNC y control de calidad",
    "mantenimiento": "Mantenimiento preventivo, predictivo y gestión de activos",
    "gestion_proyectos": "Planificación, programación y control de proyectos"
}

def obtener_modulo_info(nombre_modulo):
    """Obtiene información sobre un módulo específico"""
    if nombre_modulo in DESCRIPCION_MODULOS:
        return {
            "nombre": nombre_modulo,
            "descripcion": DESCRIPCION_MODULOS[nombre_modulo],
            "disponible": True
        }
    else:
        return {
            "nombre": nombre_modulo,
            "descripcion": "Módulo no encontrado",
            "disponible": False
        }

def listar_modulos():
    """Lista todos los módulos disponibles"""
    return MODULOS_DISPONIBLES

def obtener_descripciones():
    """Obtiene las descripciones de todos los módulos"""
    return DESCRIPCION_MODULOS 