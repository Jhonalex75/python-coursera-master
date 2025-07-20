# -----------------------------------------------------------------------------
# Simulación y Análisis de Cronograma de Montaje de Proyecto
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Simular un cronograma de actividades de montaje, analizar retrasos y
# predecir la fecha de terminación usando regresión lineal.
# Aplicación: Gestión de proyectos, ingeniería de montaje, análisis de cronogramas.
#
# Dependencias: pandas, numpy, scikit-learn
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale las librerías necesarias si no las tiene:
#      pip install pandas numpy scikit-learn
#   3. Importe las funciones y utilícelas en su análisis o notebook.
# -----------------------------------------------------------------------------

try:
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LinearRegression
except ImportError as e:
    print("ERROR: Falta una dependencia. Instale con: pip install pandas numpy scikit-learn")
    raise e

# Función para crear un cronograma simulado de actividades
# Incluye fechas planificadas y reales, duraciones, retrasos y causas
# Si no se pasan retrasos o causas, se generan aleatoriamente

def crear_cronograma(actividades, retrasos=None, causas=None):
    fechas_inicio_plan = pd.date_range("2024-07-01", periods=len(actividades), freq="7D")
    duraciones = np.random.randint(5, 10, size=len(actividades))
    fechas_fin_plan = fechas_inicio_plan + pd.to_timedelta(duraciones, unit="D")
    if retrasos is None:
        retrasos = np.random.choice([0, 3, 7, 15], size=len(actividades), p=[0.3, 0.3, 0.3, 0.1])
    if causas is None:
        causas = ["No aplica"] * len(actividades)
    # Simular que todo inicia 15 días después de lo planificado
    fechas_inicio_real = fechas_inicio_plan + pd.to_timedelta(15, unit="D")
    fechas_fin_real = fechas_fin_plan + pd.to_timedelta(15 + np.array(retrasos), unit="D")
    df = pd.DataFrame({
        "actividad": actividades,
        "inicio_plan": fechas_inicio_plan,
        "fin_plan": fechas_fin_plan,
        "inicio_real": fechas_inicio_real,
        "fin_real": fechas_fin_real,
        "duracion_plan": duraciones,
        "duracion_real": duraciones + np.array(retrasos),
        "retraso_dias": retrasos,
        "causa_retraso": causas
    })
    return df

# Función para entrenar un modelo de regresión lineal para predecir la fecha de terminación

def entrenar_modelo_prediccion(df):
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['fin_real'].map(pd.Timestamp.toordinal).values
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo

# Función para predecir la fecha de terminación de la última actividad

def predecir_fecha_terminacion(modelo, num_actividades):
    pred_ordinal = modelo.predict(np.array([[num_actividades-1]]))[0]
    return pd.Timestamp.fromordinal(int(round(pred_ordinal)))

# Función para analizar los retrasos totales y promedio

def analizar_retrasos(df):
    return df['retraso_dias'].sum(), df['retraso_dias'].mean() 