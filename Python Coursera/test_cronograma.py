import pytest
from montaje import crear_cronograma, entrenar_modelo_prediccion, predecir_fecha_terminacion

@pytest.fixture
def actividades():
    return [
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

def test_cronograma_columnas(actividades):
    df = crear_cronograma(actividades)
    assert set(['actividad', 'inicio_plan', 'fin_plan', 'inicio_real', 'fin_real', 'duracion_plan', 'duracion_real', 'retraso_dias', 'causa_retraso']).issubset(df.columns)

def test_prediccion_fecha_terminacion(actividades):
    df = crear_cronograma(actividades)
    modelo = entrenar_modelo_prediccion(df)
    fecha_predicha = predecir_fecha_terminacion(modelo, len(df))
    assert fecha_predicha > df['inicio_real'].min() 