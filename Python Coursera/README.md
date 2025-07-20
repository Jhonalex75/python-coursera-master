# 🚀 PYTHON COURSERA MASTER - Paquete Educativo de Ingeniería Mecánica

## 📋 Descripción

**PYTHON COURSERA MASTER** es una plataforma educativa integral diseñada para ingeniería mecánica, que utiliza Python como herramienta sofisticada para realizar cualquier actividad en todas las áreas de la ingeniería mecánica. Este paquete combina teoría, práctica y herramientas computacionales avanzadas en una interfaz interactiva y educativa.

## 🎯 Propósito

El objetivo principal es proporcionar a estudiantes, profesionales e investigadores de ingeniería mecánica una herramienta completa que integre:

- **Análisis estructural** avanzado
- **Dinámica de máquinas** y mecanismos
- **Termodinámica y fluidos** computacional
- **Materiales y resistencia** de materiales
- **Control y automatización** de sistemas
- **Manufactura y procesos** industriales
- **Mantenimiento y confiabilidad** de equipos
- **Gestión de proyectos** de ingeniería

## 🏗️ Arquitectura del Sistema

### Estructura de Módulos

```
PYTHON_COURSERA_MASTER/
├── PYTHON_COURSERA_MASTER.py          # Aplicación principal
├── modulos/                           # Módulos de ingeniería
│   ├── __init__.py
│   ├── analisis_estructural.py        # Análisis estructural
│   ├── dinamica_maquinas.py          # Dinámica de máquinas
│   ├── termodinamica_fluidos.py      # Termodinámica y fluidos
│   └── materiales_resistencia.py     # Materiales y resistencia
├── herramientas/                      # Herramientas de cálculo
│   └── calculadora_avanzada.py       # Calculadora avanzada
├── github-organizado/                 # Módulos existentes
│   └── src/
│       ├── mantenimiento/            # Gestión de mantenimiento
│       ├── scripts/                  # Scripts de proyectos
│       └── ingenieria/               # Herramientas de ingeniería
└── requirements.txt                   # Dependencias
```

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd PYTHON_COURSERA_MASTER
   ```

2. **Crear entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

### Dependencias Principales

```
numpy>=1.21.0
matplotlib>=3.5.0
pandas>=1.3.0
scipy>=1.7.0
tkinter (incluido con Python)
```

## 🎮 Uso del Sistema

### Ejecutar la Aplicación Principal

```bash
python PYTHON_COURSERA_MASTER.py
```

### Interfaz Principal

La aplicación principal presenta una interfaz gráfica organizada en dos paneles:

#### Panel Izquierdo - Módulos Principales
- 🏗️ **Análisis Estructural**: Vigas, columnas, cerchas, elementos finitos
- ⚙️ **Dinámica de Máquinas**: Mecanismos, vibraciones, balanceo, cinemática
- 🌡️ **Termodinámica y Fluidos**: Ciclos termodinámicos, flujo de fluidos
- 🔧 **Materiales y Resistencia**: Propiedades mecánicas, esfuerzos, fatiga
- 🎛️ **Control y Automatización**: Sistemas de control, automatización
- 🏭 **Manufactura y Procesos**: Procesos de manufactura, optimización
- 🔧 **Mantenimiento y Confiabilidad**: Gestión de mantenimiento
- 📊 **Gestión de Proyectos**: Planificación y control de proyectos

#### Panel Derecho - Herramientas y Recursos
- **Herramientas de Cálculo**: Calculadora avanzada, conversores, generadores
- **Recursos Educativos**: Tutoriales, base de datos técnica, ejemplos
- **Desarrollo y Programación**: Editor, depurador, generador de reportes
- **Información del Sistema**: Estado, actualizaciones, ayuda

## 📚 Módulos Disponibles

### 1. 🏗️ Análisis Estructural
**Archivo:** `modulos/analisis_estructural.py`

**Funcionalidades:**
- Análisis de vigas (cortante, momento flector, deflexión)
- Análisis de columnas (pandeo, carga crítica)
- Análisis de cerchas (método de nodos, método de secciones)
- Elementos finitos básicos
- Generación de reportes y gráficos

**Ejemplo de uso:**
```python
from modulos.analisis_estructural import AnalisisEstructuralApp
app = AnalisisEstructuralApp()
app.ejecutar()
```

### 2. ⚙️ Dinámica de Máquinas
**Archivo:** `modulos/dinamica_maquinas.py`

**Funcionalidades:**
- Análisis de mecanismos de 4 barras
- Análisis de vibraciones (libre, forzada)
- Balanceo de rotores
- Análisis cinemático
- Simulación de movimiento

**Características:**
- Cálculo de condición de Grashof
- Análisis de frecuencias naturales
- Determinación de velocidades críticas
- Visualización de trayectorias

### 3. 🌡️ Termodinámica y Fluidos
**Archivo:** `modulos/termodinamica_fluidos.py`

**Funcionalidades:**
- Análisis de ciclos termodinámicos (Carnot, Otto, Diesel, Brayton)
- Análisis de flujo de fluidos
- Transferencia de calor (conducción, convección, radiación)
- Diagramas P-V y T-S

**Ciclos implementados:**
- Cálculo de eficiencia térmica
- Análisis de trabajo neto
- Optimización de parámetros

### 4. 🔧 Materiales y Resistencia
**Archivo:** `modulos/materiales_resistencia.py`

**Funcionalidades:**
- Base de datos de materiales
- Análisis de propiedades mecánicas
- Cálculo de esfuerzos y deformaciones
- Análisis de fatiga
- Curvas S-N

**Materiales incluidos:**
- Aceros (AISI 1020, 1045)
- Aluminio 6061-T6
- Titanio Ti-6Al-4V
- Cobre C11000

### 5. 🧮 Calculadora Avanzada
**Archivo:** `herramientas/calculadora_avanzada.py`

**Funcionalidades:**
- Operaciones matemáticas básicas y avanzadas
- Conversión de unidades
- Constantes físicas
- Fórmulas de ingeniería
- Historial de cálculos

## 🔧 Herramientas Integradas

### Módulos de github-organizado
El paquete integra módulos existentes del proyecto github-organizado:

- **Gestión de Mantenimiento**: Sistema completo de gestión de mantenimiento
- **Gestión de Proyectos**: Herramientas de planificación y control
- **Análisis de Bombas**: Curvas de bombas y análisis de flujo
- **Estadística y Análisis**: Herramientas estadísticas para ingeniería

## 📊 Características Técnicas

### Interfaz de Usuario
- **Tkinter**: Interfaz gráfica nativa de Python
- **Matplotlib**: Visualización de datos y gráficos
- **Tema personalizado**: Interfaz moderna y profesional
- **Navegación intuitiva**: Sistema de pestañas y botones

### Análisis Computacional
- **NumPy**: Cálculos numéricos avanzados
- **SciPy**: Funciones científicas y optimización
- **Pandas**: Manipulación y análisis de datos
- **Algoritmos especializados**: Métodos numéricos para ingeniería

### Generación de Reportes
- **Reportes automáticos**: Generación de reportes técnicos
- **Exportación de datos**: Formatos TXT, CSV, Excel
- **Gráficos profesionales**: Visualizaciones de alta calidad
- **Documentación técnica**: Explicaciones detalladas

## 🎓 Aplicaciones Educativas

### Para Estudiantes
- **Aprendizaje interactivo**: Experimentación con parámetros reales
- **Visualización de conceptos**: Gráficos y animaciones
- **Ejercicios prácticos**: Problemas resueltos paso a paso
- **Autoevaluación**: Verificación de resultados

### Para Profesores
- **Herramienta de enseñanza**: Demostraciones en clase
- **Generación de ejercicios**: Creación de problemas personalizados
- **Evaluación automática**: Verificación de soluciones
- **Recursos didácticos**: Material de apoyo

### Para Profesionales
- **Análisis rápido**: Cálculos de ingeniería inmediatos
- **Verificación de diseños**: Validación de conceptos
- **Optimización**: Búsqueda de parámetros óptimos
- **Documentación**: Generación de reportes técnicos

## 🔄 Desarrollo y Extensibilidad

### Estructura Modular
El sistema está diseñado con una arquitectura modular que permite:

- **Agregar nuevos módulos**: Fácil integración de nuevas funcionalidades
- **Modificar módulos existentes**: Actualización sin afectar otros componentes
- **Personalización**: Adaptación a necesidades específicas
- **Escalabilidad**: Crecimiento del sistema según requerimientos

### Estándares de Código
- **PEP 8**: Estilo de código Python estándar
- **Documentación**: Docstrings completos
- **Manejo de errores**: Excepciones robustas
- **Testing**: Pruebas unitarias (en desarrollo)

## 📈 Roadmap de Desarrollo

### Versión Actual (1.0)
- ✅ Módulos principales implementados
- ✅ Interfaz gráfica funcional
- ✅ Integración con módulos existentes
- ✅ Documentación básica

### Próximas Versiones
- 🔄 **Control y Automatización**: Sistemas de control, PID, automatización
- 🔄 **Manufactura y Procesos**: CNC, procesos de manufactura
- 🔄 **Herramientas Avanzadas**: Más calculadoras y conversores
- 🔄 **Base de Datos Técnica**: Catálogo de materiales y componentes
- 🔄 **Tutoriales Interactivos**: Guías paso a paso
- 🔄 **Testing Completo**: Suite de pruebas automatizadas

## 🤝 Contribuciones

### Cómo Contribuir
1. **Fork del repositorio**
2. **Crear rama de características**: `git checkout -b feature/nueva-funcionalidad`
3. **Realizar cambios**: Implementar mejoras o correcciones
4. **Commit de cambios**: `git commit -m 'Agregar nueva funcionalidad'`
5. **Push a la rama**: `git push origin feature/nueva-funcionalidad`
6. **Crear Pull Request**: Solicitar integración de cambios

### Áreas de Contribución
- **Nuevos módulos**: Implementación de nuevas áreas de ingeniería
- **Mejoras de interfaz**: Optimización de la experiencia de usuario
- **Documentación**: Mejora de guías y tutoriales
- **Testing**: Desarrollo de pruebas automatizadas
- **Optimización**: Mejora de rendimiento y eficiencia

## 📞 Soporte y Contacto

### Problemas y Errores
- **Issues de GitHub**: Reportar bugs y solicitar características
- **Documentación**: Consultar guías y tutoriales
- **Comunidad**: Participar en discusiones y foros

### Recursos Adicionales
- **Documentación técnica**: Manuales detallados de cada módulo
- **Ejemplos de uso**: Casos prácticos y aplicaciones
- **Videos tutoriales**: Guías visuales (en desarrollo)
- **Base de conocimientos**: FAQ y soluciones comunes

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **Comunidad Python**: Por proporcionar las herramientas base
- **Desarrolladores de librerías**: NumPy, Matplotlib, SciPy, Pandas
- **Contribuidores**: Todos aquellos que han aportado al proyecto
- **Usuarios**: Por el feedback y sugerencias de mejora

---

**PYTHON COURSERA MASTER** - Transformando la ingeniería mecánica con Python 🚀

*Desarrollado con ❤️ para la comunidad de ingeniería*
