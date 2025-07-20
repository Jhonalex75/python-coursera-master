# -----------------------------------------------------------------------------
# Análisis de Opex y Proyecciones Financieras (Ejemplo 2)
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Ejemplo adicional de análisis de costos operativos (Opex) y proyecciones
# para proyectos de ingeniería.
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

# Función de ejemplo: calcular el Opex acumulado mes a mes

def opex_acumulado(df):
    """
    Calcula el Opex acumulado mes a mes a partir de un DataFrame con columna 'Opex'.
    Args:
        df (pd.DataFrame): DataFrame con columna 'Opex'.
    Returns:
        pd.Series: Opex acumulado por mes.
    """
    return df['Opex'].cumsum()

# Ejemplo de uso
if __name__ == "__main__":
    datos = {
        'Mes': ['Enero', 'Febrero', 'Marzo'],
        'Opex': [12000, 13500, 12800]
    }
    df = pd.DataFrame(datos)
    print("Opex acumulado por mes:")
    print(opex_acumulado(df))
