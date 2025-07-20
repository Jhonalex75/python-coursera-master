# -----------------------------------------------------------------------------
# Análisis y Visualización de Cronograma de Montaje de Molino de Bolas
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Simular, analizar y visualizar el cronograma de montaje de un molino,
# analizar retrasos, predecir fecha de terminación y exportar reportes.
# Aplicación: Gestión de proyectos, ingeniería de montaje, análisis de cronogramas.
#
# Dependencias: pandas, numpy, matplotlib, seaborn, scikit-learn
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale las librerías necesarias si no las tiene:
#      pip install pandas numpy matplotlib seaborn scikit-learn
#   3. Importe las funciones y utilícelas en su análisis o notebook.
# -----------------------------------------------------------------------------

try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    import numpy as np
except ImportError as e:
    print("ERROR: Falta una dependencia. Instale con: pip install pandas numpy matplotlib seaborn scikit-learn")
    raise e

# Función para crear un cronograma simulado de montaje de molino
# Incluye fechas planificadas y reales, duraciones, retrasos y causas

def crear_cronograma():
    actividades = [
        "Inspección obra civil",
        "Retiro del equipo del almacén",
        "Interpretación de planos mecánicos",
        "Instalación de grúa para izaje",
        "Montaje de base del molino",
        "Montaje de componentes principales",
        "Alineación de ejes",
        "Montaje de sistema de transmisión",
        "Montaje de sistema de lubricación",
        "Montaje de sistema eléctrico",
        "Pruebas de vacío",
        "Comisionamiento"
    ]
    causas = [
        "Retraso en entrega de materiales",
        "Condiciones climáticas",
        "Falta de personal",
        "Problemas logísticos",
        "Demoras en permisos",
        "Fallas en equipos",
        "Retraso en inspección",
        "No aplica"
    ]
    fechas_inicio_plan = pd.date_range("2024-07-01", periods=len(actividades), freq="7D")
    duraciones = np.random.randint(5, 10, size=len(actividades))
    fechas_fin_plan = fechas_inicio_plan + pd.to_timedelta(duraciones, unit="D")
    # Fechas reales con desfase de 15 días + retraso aleatorio
    retrasos = np.random.choice([0, 3, 7, 15], size=len(actividades), p=[0.3, 0.3, 0.3, 0.1])
    causas_retraso = np.random.choice(causas, size=len(actividades))
    fechas_inicio_real = fechas_inicio_plan + pd.to_timedelta(15, unit="D")
    fechas_fin_real = fechas_fin_plan + pd.to_timedelta(15 + retrasos, unit="D")
    df = pd.DataFrame({
        "actividad": actividades,
        "inicio_plan": fechas_inicio_plan,
        "fin_plan": fechas_fin_plan,
        "inicio_real": fechas_inicio_real,
        "fin_real": fechas_fin_real,
        "duracion_plan": duraciones,
        "duracion_real": duraciones + retrasos,
        "retraso_dias": retrasos,
        "causa_retraso": causas_retraso
    })
    return df

# Función para graficar el diagrama de Gantt (planificado vs real)
def plot_gantt(df, save_path="gantt_molino.png"):
    plt.figure(figsize=(12, 6))
    for i, row in df.iterrows():
        plt.plot([row['inicio_plan'], row['fin_plan']], [i+0.2, i+0.2], color='blue', linewidth=8, label='Planificado' if i==0 else "")
    for i, row in df.iterrows():
        plt.plot([row['inicio_real'], row['fin_real']], [i-0.2, i-0.2], color='orange', linewidth=8, label='Real' if i==0 else "")
    plt.yticks(range(len(df)), df['actividad'])
    plt.xlabel("Fecha")
    plt.title("Cronograma de Montaje Molino de Bolas (Planificado vs Real)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

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

# Función para analizar los retrasos y causas principales
def analizar_retrasos(df):
    total_retraso = df['retraso_dias'].sum()
    promedio_retraso = df['retraso_dias'].mean()
    max_retraso = df['retraso_dias'].max()
    actividad_max = df.loc[df['retraso_dias'].idxmax(), 'actividad']
    causas = df.groupby('causa_retraso')['retraso_dias'].sum().sort_values(ascending=False)
    resumen = (
        f"--- Análisis de Retrasos ---\n"
        f"Total de días de retraso acumulados: {total_retraso}\n"
        f"Promedio de retraso por actividad: {promedio_retraso:.2f} días\n"
        f"Mayor retraso: {max_retraso} días en la actividad '{actividad_max}'\n"
        f"Principales causas de retraso:\n{causas.to_string()}\n"
    )
    return resumen

# Función para exportar el cronograma y resumen a un archivo Excel
def exportar_reporte(df, fecha_predicha, resumen, path="reporte_montaje_molino.xlsx"):
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name="Cronograma", index=False)
        resumen_df = pd.DataFrame({
            "Resumen": [resumen],
            "Fecha_predicha_terminacion": [str(fecha_predicha.date())]
        })
        resumen_df.to_excel(writer, sheet_name="Resumen", index=False)

# Función para graficar las causas de retraso (barras)
def plot_causas_retraso(df, save_path="causas_retraso.png"):
    import matplotlib.pyplot as plt
    causas = df.groupby('causa_retraso')['retraso_dias'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    causas.plot(kind='bar', color='tomato')
    plt.title("Retraso total por causa")
    plt.ylabel("Días de retraso")
    plt.xlabel("Causa")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# Función para graficar el diagrama de Pareto de causas de retraso
def plot_pareto_causas(df, save_path="pareto_causas.png"):
    import matplotlib.pyplot as plt
    causas = df.groupby('causa_retraso')['retraso_dias'].sum().sort_values(ascending=False)
    total = causas.sum()
    porcentaje_acumulado = causas.cumsum() / total * 100

    fig, ax1 = plt.subplots(figsize=(10, 5))
    causas.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_ylabel("Días de retraso")
    ax1.set_xlabel("Causa")
    ax1.set_title("Diagrama de Pareto de causas de retraso")

    ax2 = ax1.twinx()
    porcentaje_acumulado.plot(color='red', marker='o', ax=ax2)
    ax2.set_ylabel("% acumulado")
    ax2.set_ylim(0, 110)
    ax2.axhline(80, color='gray', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close() 