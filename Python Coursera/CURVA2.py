# -----------------------------------------------------------------------------
# Ajuste de Distribución Weibull 2P a Datos de Fallas
# Autor: [Tu Nombre]
# Fecha: [Fecha de última edición]
# Versión: 1.0
#
# Propósito: Ajustar una distribución Weibull de 2 parámetros a un conjunto de datos
# de fallas y mostrar los resultados y la gráfica del ajuste.
# Aplicación: Ingeniería de confiabilidad, análisis de fallas.
#
# Dependencias: reliability, matplotlib
# Uso:
#   1. Ejecute este script con Python 3.7+.
#   2. Instale las librerías necesarias si no las tiene:
#      pip install reliability matplotlib
#   3. Al ejecutar, se ajusta el modelo y se muestra la gráfica.
# -----------------------------------------------------------------------------

try:
    from reliability.Fitters import Fit_Weibull_2P
    import matplotlib.pyplot as plt
except ImportError as e:
    print("ERROR: Falta una dependencia. Instale con: pip install reliability matplotlib")
    raise e

# Datos de fallas (horas hasta la falla, por ejemplo)
data = [58,75,36,52,63,65,22,17,28,64,23,40,73,45,52,36,52,60,13,55,82,55,34,57,23,42,66,35,34,25] # generado con Weibull(alpha=50, beta=3)

# Ajuste Weibull 2P
wb = Fit_Weibull_2P(failures=data)

# Mostrar la gráfica del ajuste
plt.show()

'''
Resultados de ejemplo del ajuste Weibull 2P (95% CI):
Método de análisis: Maximum Likelihood Estimation (MLE)
Optimizador: TNC
Fallas / Censurados: 30/0 (0% censurados)

Parámetro  Estimación  Error estándar  IC Inferior  IC Superior
    Alpha      51.858         3.55628     45.3359     59.3183
     Beta      2.80086        0.41411     2.09624     3.74233

Bondad de ajuste    Valor
 Log-likelihood  -129.063
           AICc   262.57
            BIC  264.928
             AD  0.759805
'''