import pytest
from montaje import crear_cronograma, analizar_retrasos

@pytest.fixture
def actividades():
    return [
        "Inspección obra civil",
        "Retiro del equipo del almacén",
        "Interpretación de planos mecánicos"
    ]

def test_analisis_retrasos_total_y_promedio(actividades):
    retrasos = [3, 7, 0]
    causas = ["Falta de personal", "Fallas en equipos", "No aplica"]
    df = crear_cronograma(actividades, retrasos=retrasos, causas=causas)
    total, promedio = analizar_retrasos(df)
    assert total == 10
    assert promedio == pytest.approx(10/3) 