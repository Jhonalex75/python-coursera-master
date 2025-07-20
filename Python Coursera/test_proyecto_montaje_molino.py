import pytest
from proyecto_montaje_molino import crear_cronograma, plot_gantt, entrenar_modelo_prediccion, predecir_fecha_terminacion

def test_crear_cronograma():
    df = crear_cronograma()
    assert not df.empty
    assert "actividad" in df.columns
    assert len(df) >= 10  # Debe haber al menos 10 actividades

def test_plot_gantt_crea_archivo(tmp_path):
    df = crear_cronograma()
    plot_path = tmp_path / "gantt.png"
    plot_gantt(df, save_path=str(plot_path))
    assert plot_path.exists()

def test_prediccion_fecha_terminacion():
    df = crear_cronograma()
    modelo = entrenar_modelo_prediccion(df)
    fecha_predicha = predecir_fecha_terminacion(modelo, len(df))
    # La fecha predicha debe ser una fecha posterior a la fecha de inicio real
    assert fecha_predicha > df['inicio_real'].min() 