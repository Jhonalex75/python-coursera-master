from proyecto_montaje_molino import (
    crear_cronograma, plot_gantt, entrenar_modelo_prediccion,
    predecir_fecha_terminacion, analizar_retrasos, exportar_reporte
)

df = crear_cronograma()
plot_gantt(df, save_path="gantt_molino.png")
modelo = entrenar_modelo_prediccion(df)
fecha_predicha = predecir_fecha_terminacion(modelo, len(df))
resumen = analizar_retrasos(df)
exportar_reporte(df, fecha_predicha, resumen, path="reporte_montaje_molino.xlsx")

print(resumen)
print(f"Fecha tentativa de terminación del montaje (predicción): {fecha_predicha.date()}")
print("Reporte Excel generado: reporte_montaje_molino.xlsx")
print("Gráfica Gantt guardada como gantt_molino.png")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from proyecto_montaje_molino import crear_cronograma, entrenar_modelo_prediccion, predecir_fecha_terminacion

# 1. Genera el cronograma y entrena el modelo
df = crear_cronograma()
modelo = entrenar_modelo_prediccion(df)

# 2. Prepara los datos para graficar
X = np.arange(len(df)).reshape(-1, 1)
y = df['fin_real'].map(pd.Timestamp.toordinal).values

# 3. Predice la fecha para cada actividad (línea de regresión)
y_pred = modelo.predict(X)

# 4. Convierte fechas ordinales a fechas para graficar
fechas_reales = [pd.Timestamp.fromordinal(int(val)) for val in y]
fechas_predichas = [pd.Timestamp.fromordinal(int(val)) for val in y_pred]

# 5. Predicción para la última actividad
fecha_predicha_final = predecir_fecha_terminacion(modelo, len(df))

# 6. Gráfica
plt.figure(figsize=(12, 6))
plt.plot(X, fechas_reales, 'o', label='Fechas reales de fin', color='blue')
plt.plot(X, fechas_predichas, '-', label='Regresión lineal (tendencia)', color='red')
plt.plot([len(df)-1], [fecha_predicha_final], 's', label='Predicción de fin', color='green', markersize=10)
plt.xticks(X.flatten(), df['actividad'], rotation=45, ha='right')
plt.ylabel('Fecha de fin')
plt.title('Regresión lineal sobre fechas reales de fin de actividades')
plt.legend()
plt.tight_layout()
plt.show()