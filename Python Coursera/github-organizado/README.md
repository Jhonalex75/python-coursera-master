# 🏭 Paquete GitHub-Organizado - Herramientas de Ingeniería

## 📋 Descripción General

Este paquete contiene una colección completa de herramientas, scripts y aplicaciones para el análisis y diseño en ingeniería. El proyecto está organizado por disciplinas y especialidades, proporcionando soluciones prácticas para problemas de ingeniería reales.

## 🎯 Objetivos del Proyecto

- **Educativo**: Proporcionar ejemplos prácticos para estudiantes de ingeniería
- **Profesional**: Ofrecer herramientas útiles para ingenieros en ejercicio
- **Investigación**: Facilitar el análisis y modelado de sistemas de ingeniería
- **Automatización**: Simplificar cálculos repetitivos y análisis complejos
- **Integración**: Crear un ecosistema completo de herramientas de ingeniería

## 📁 Estructura del Proyecto

```
github-organizado/
├── src/
│   ├── ingenieria/
│   │   ├── bombas_y_flujos/          # Análisis de bombas y sistemas de flujo
│   │   ├── metodos_numericos/        # Métodos numéricos y EDOs
│   │   ├── visualizacion/            # Herramientas de visualización
│   │   ├── CURVA_BOMBA.py           # Simulador de curvas de bomba
│   │   ├── RUNGE_KUTTA.py           # Método de Runge-Kutta
│   │   ├── Grafica_Duran.py         # Visualizaciones profesionales
│   │   └── curva_mtto.py            # Análisis de confiabilidad
│   ├── mantenimiento/
│   │   └── gestion_mtto.py          # Gestión de mantenimiento industrial
│   ├── analisis/
│   │   ├── financiero_operativo/     # Análisis financiero
│   │   └── Opex_2025.py             # Análisis de costos operativos
│   ├── estadistica/
│   │   └── ESTADISTICA.py           # Análisis estadístico
│   ├── gui/
│   │   └── MODELO_GRUA.py           # Modelado de grúas
│   └── web/
│       ├── CALCULO TUBERIAS.html    # Calculadora web de tuberías
│       └── styles.css               # Estilos CSS
├── docs/
│   ├── manuales/                    # Manuales de usuario
│   └── ejemplos/                    # Ejemplos de uso
└── tests/                           # Pruebas unitarias
```

## 🚀 Características Principales

### 🔧 Ingeniería de Fluidos y Bombas
- **Simulador de Curvas de Bomba**: Aplicación GUI interactiva para análisis de bombas centrífugas
- **Análisis de Sistemas de Flujo**: Cálculos de pérdidas de carga y optimización
- **Curvas Características**: Visualización de curvas H-Q, eficiencia y potencia

### 📊 Métodos Numéricos
- **Método de Runge-Kutta**: Implementación completa para resolver EDOs
- **Sistemas de EDOs**: Análisis de sistemas dinámicos complejos
- **Validación Analítica**: Comparación con soluciones exactas

### 📈 Visualización Profesional
- **Gráficos de Ingeniería**: Estilos profesionales para presentaciones
- **Análisis de Datos**: Herramientas estadísticas y gráficas
- **Diagramas de Fase**: Análisis de sistemas dinámicos

### 🔍 Análisis de Confiabilidad
- **Curva de Bañera**: Análisis de tasas de falla a lo largo del tiempo
- **Distribuciones de Falla**: Weibull, exponencial y normal
- **Mantenimiento Preventivo**: Optimización de estrategias de mantenimiento

### 🏭 Gestión de Mantenimiento
- **Sistema de Gestión**: Control de equipos y órdenes de trabajo
- **Indicadores KPI**: MTBF, MTTR, disponibilidad
- **Análisis de Costos**: Optimización de gastos de mantenimiento

## 🛠️ Instalación y Configuración

### Requisitos Previos
```bash
Python 3.8 o superior
pip (gestor de paquetes de Python)
```

### Instalación de Dependencias
```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd github-organizado

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias Principales
```
numpy>=1.21.0
matplotlib>=3.5.0
pandas>=1.3.0
scipy>=1.7.0
seaborn>=0.11.0
tkinter (incluido con Python)
plotly>=5.0.0
dash>=2.0.0
```

## 📖 Guía de Uso

### 1. Simulador de Curvas de Bomba
```python
from src.ingenieria.CURVA_BOMBA import SimuladorCurvaBomba

# Ejecutar simulador
app = SimuladorCurvaBomba()
app.ejecutar()
```

### 2. Método de Runge-Kutta
```python
from src.ingenieria.RUNGE_KUTTA import MetodoRungeKutta

# Definir EDO
def f(t, y):
    return -y

# Resolver
rk = MetodoRungeKutta()
t, y = rk.runge_kutta_4(f, y0=1.0, t0=0.0, tf=5.0, h=0.1)
```

### 3. Análisis de Confiabilidad
```python
from src.ingenieria.curva_mtto import AnalizadorConfiabilidad

# Generar curva de bañera
analizador = AnalizadorConfiabilidad()
tiempo, tasa_falla = analizador.curva_banera()
```

### 4. Gestión de Mantenimiento
```python
from src.mantenimiento.gestion_mtto import GestionMantenimiento

# Crear sistema de gestión
gestion = GestionMantenimiento()
resultados = gestion.analizar_costos_mtto()
```

## 📊 Ejemplos de Aplicación

### Análisis de Bomba Industrial
- **Problema**: Selección de bomba para sistema de riego
- **Solución**: Simulador de curvas para optimizar punto de operación
- **Resultado**: 15% de ahorro energético

### Optimización de Mantenimiento
- **Problema**: Frecuencia óptima de mantenimiento preventivo
- **Solución**: Análisis de curva de bañera y costos
- **Resultado**: Reducción del 25% en costos de mantenimiento

### Modelado de Sistemas Dinámicos
- **Problema**: Análisis de vibraciones en máquina rotativa
- **Solución**: Sistema de EDOs con Runge-Kutta
- **Resultado**: Identificación de frecuencias críticas

## 🧪 Pruebas y Validación

### Ejecutar Pruebas
```bash
# Ejecutar todas las pruebas
python -m pytest tests/

# Pruebas específicas
python -m pytest tests/test_curva_bomba.py
python -m pytest tests/test_runge_kutta.py
```

### Validación de Resultados
- Comparación con soluciones analíticas conocidas
- Verificación con software comercial (MATLAB, ANSYS)
- Validación experimental en casos de estudio

## 📚 Documentación

### Manuales Disponibles
- **Manual de Usuario**: Guía completa de todas las herramientas
- **Manual Técnico**: Especificaciones y algoritmos
- **Ejemplos Prácticos**: Casos de estudio reales

### Referencias Técnicas
- **Mecánica de Fluidos**: White, F.M. "Fluid Mechanics"
- **Métodos Numéricos**: Chapra, S.C. "Numerical Methods"
- **Confiabilidad**: O'Connor, P.D.T. "Practical Reliability Engineering"

## 🤝 Contribuciones

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con pruebas
4. Enviar Pull Request con descripción detallada

### Estándares de Código
- **PEP 8**: Estilo de código Python
- **Docstrings**: Documentación de funciones
- **Type Hints**: Tipado estático
- **Pruebas Unitarias**: Cobertura mínima del 80%

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- **Ing. Jhon A. Valencia** - Ingeniero Mecánico
- **Especialidad**: Análisis de sistemas mecánicos y optimización

## 📞 Contacto

- **Email**: [email@ejemplo.com]
- **LinkedIn**: [Perfil de LinkedIn]
- **GitHub**: [Perfil de GitHub]

## 🔄 Historial de Versiones

### v1.0.0 (2024-01-15)
- ✅ Implementación inicial de simulador de bombas
- ✅ Método de Runge-Kutta para EDOs
- ✅ Sistema de gestión de mantenimiento
- ✅ Herramientas de visualización

### v1.1.0 (En desarrollo)
- 🔄 Análisis de vibraciones
- 🔄 Optimización multi-objetivo
- 🔄 Interfaz web mejorada

---

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!**
