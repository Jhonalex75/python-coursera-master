# -----------------------------------------------------------------------------
# Cálculo de Requerimiento Mensual de Recursos
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Ejemplo de cálculo de requerimiento mensual de recursos (materiales, mano de obra, etc.)
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

# Función de ejemplo: calcular el requerimiento total por mes

def requerimiento_mensual(df):
    """
    Calcula el requerimiento total de recursos por mes a partir de un DataFrame.
    Args:
        df (pd.DataFrame): DataFrame con columnas 'Mes' y 'Cantidad'.
    Returns:
        pd.Series: Requerimiento total por mes.
    """
    return df.groupby('Mes')['Cantidad'].sum()

# Ejemplo de uso
if __name__ == "__main__":
    datos = {
        'Mes': ['Enero', 'Febrero', 'Febrero', 'Marzo'],
        'Cantidad': [100, 150, 200, 120]
    }
    df = pd.DataFrame(datos)
    print("Requerimiento total por mes:")
    print(requerimiento_mensual(df))
