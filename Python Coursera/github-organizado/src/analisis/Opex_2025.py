# -----------------------------------------------------------------------------
# Proyección de Opex para el año 2025
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Ejemplo de proyección de costos operativos (Opex) para el año 2025
# usando una tasa de crecimiento anual.
# Dependencias: pandas
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale pandas si no lo tiene: pip install pandas
# -----------------------------------------------------------------------------

try:
    import pandas as pd
except ImportError as e:
    print("ERROR: Falta la dependencia pandas. Instale con: pip install pandas")
    raise e

# Función de ejemplo: proyectar Opex para el año siguiente

def proyectar_opex(df, tasa_crecimiento=0.05):
    """
    Proyecta el Opex para el año siguiente usando una tasa de crecimiento.
    Args:
        df (pd.DataFrame): DataFrame con columna 'Opex'.
        tasa_crecimiento (float): Tasa de crecimiento anual (por defecto 5%).
    Returns:
        float: Opex proyectado para el año siguiente.
    """
    opex_actual = df['Opex'].sum()
    return opex_actual * (1 + tasa_crecimiento)

# Ejemplo de uso
if __name__ == "__main__":
    datos = {
        'Mes': ['Enero', 'Febrero', 'Marzo'],
        'Opex': [12000, 13500, 12800]
    }
    df = pd.DataFrame(datos)
    opex_2025 = proyectar_opex(df, tasa_crecimiento=0.07)
    print(f"Opex proyectado para 2025: {opex_2025:.2f}")
