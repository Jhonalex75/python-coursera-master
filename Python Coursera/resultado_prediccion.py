from proyecto_montaje_molino import crear_cronograma, entrenar_modelo_prediccion, predecir_fecha_terminacion

df = crear_cronograma()
modelo = entrenar_modelo_prediccion(df)
fecha_predicha = predecir_fecha_terminacion(modelo, len(df))
print(f"Fecha tentativa de terminación del montaje (predicción): {fecha_predicha.date()}")