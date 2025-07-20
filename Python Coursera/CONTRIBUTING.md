# 🤝 Guía de Contribución - PYTHON COURSERA MASTER

¡Gracias por tu interés en contribuir al proyecto PYTHON COURSERA MASTER! Este documento proporciona las pautas para contribuir al desarrollo de este paquete educativo de ingeniería mecánica.

## 📋 Índice

- [¿Cómo Contribuir?](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Contribución](#proceso-de-contribución)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Características](#solicitar-características)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## 🚀 ¿Cómo Contribuir?

### Tipos de Contribuciones

Aceptamos diferentes tipos de contribuciones:

- **🐛 Reportar Bugs**: Encontrar y reportar errores
- **✨ Nuevas Características**: Implementar nuevas funcionalidades
- **📚 Mejoras de Documentación**: Mejorar guías, tutoriales y documentación
- **🎨 Mejoras de Interfaz**: Optimizar la experiencia de usuario
- **⚡ Optimizaciones**: Mejorar rendimiento y eficiencia
- **🧪 Testing**: Agregar pruebas y mejorar cobertura
- **🌐 Traducciones**: Traducir a otros idiomas

### Áreas de Contribución Específicas

#### Módulos de Ingeniería
- **Análisis Estructural**: Vigas, columnas, cerchas, elementos finitos
- **Dinámica de Máquinas**: Mecanismos, vibraciones, balanceo
- **Termodinámica y Fluidos**: Ciclos termodinámicos, flujo de fluidos
- **Materiales y Resistencia**: Propiedades mecánicas, esfuerzos, fatiga
- **Control y Automatización**: Sistemas de control, PID, automatización
- **Manufactura y Procesos**: Procesos de manufactura, optimización

#### Herramientas y Utilidades
- **Calculadoras**: Herramientas de cálculo especializadas
- **Conversores**: Conversión de unidades de ingeniería
- **Generadores**: Generación de gráficos y reportes
- **Base de Datos**: Catálogos de materiales y componentes

## 🔧 Configuración del Entorno

### Requisitos Previos

- Python 3.8 o superior
- Git
- pip (gestor de paquetes de Python)

### Configuración Local

1. **Fork del repositorio**
   ```bash
   # En GitHub, haz fork del repositorio
   # Luego clona tu fork localmente
   git clone https://github.com/tu-usuario/python-coursera-master.git
   cd python-coursera-master
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar pre-commit hooks (opcional)**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## 📁 Estructura del Proyecto

```
python-coursera-master/
├── PYTHON_COURSERA_MASTER.py      # Aplicación principal
├── modulos/                       # Módulos de ingeniería
│   ├── __init__.py
│   ├── analisis_estructural.py
│   ├── dinamica_maquinas.py
│   ├── termodinamica_fluidos.py
│   └── materiales_resistencia.py
├── herramientas/                  # Herramientas de cálculo
│   └── calculadora_avanzada.py
├── tests/                        # Pruebas unitarias
├── docs/                         # Documentación
├── examples/                     # Ejemplos de uso
├── requirements.txt              # Dependencias
├── README.md                     # Documentación principal
├── LICENSE                       # Licencia del proyecto
└── CONTRIBUTING.md               # Esta guía
```

## 📝 Estándares de Código

### Estilo de Código Python

Seguimos las convenciones PEP 8:

```python
# ✅ Correcto
def calcular_esfuerzo_viga(longitud, carga, modulo_elasticidad):
    """Calcula el esfuerzo en una viga simplemente apoyada."""
    momento_maximo = carga * longitud**2 / 8
    esfuerzo = momento_maximo / modulo_elasticidad
    return esfuerzo

# ❌ Incorrecto
def calcularEsfuerzoViga(l,c,m):
    M=c*l**2/8
    return M/m
```

### Convenciones de Nomenclatura

- **Funciones y variables**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Archivos**: `snake_case.py`

### Documentación

#### Docstrings
```python
def analizar_viga(longitud, carga, material):
    """
    Analiza una viga sometida a carga distribuida.
    
    Args:
        longitud (float): Longitud de la viga en metros
        carga (float): Carga distribuida en N/m
        material (dict): Propiedades del material
        
    Returns:
        dict: Resultados del análisis con claves:
            - 'momento_maximo': Momento flector máximo (N·m)
            - 'deflexion_maxima': Deflexión máxima (m)
            - 'esfuerzo_maximo': Esfuerzo máximo (Pa)
            
    Raises:
        ValueError: Si los parámetros son negativos
    """
    # Implementación...
```

#### Comentarios
```python
# Calcular momento flector máximo en el centro
momento_maximo = carga * longitud**2 / 8

# Verificar que el esfuerzo no exceda el límite de fluencia
if esfuerzo > material['limite_fluencia']:
    raise ValueError("El esfuerzo excede el límite de fluencia")
```

### Manejo de Errores

```python
def cargar_material(nombre_material):
    """Carga las propiedades de un material desde la base de datos."""
    try:
        with open(f"materiales/{nombre_material}.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise MaterialNotFoundError(f"Material '{nombre_material}' no encontrado")
    except json.JSONDecodeError:
        raise InvalidMaterialFileError(f"Archivo de material '{nombre_material}' corrupto")
```

## 🔄 Proceso de Contribución

### 1. Crear una Rama

```bash
# Asegúrate de estar en la rama principal
git checkout main
git pull origin main

# Crea una nueva rama para tu contribución
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 2. Realizar Cambios

- Haz los cambios necesarios
- Sigue los estándares de código
- Agrega pruebas si es necesario
- Actualiza la documentación

### 3. Commit de Cambios

```bash
# Agregar archivos modificados
git add .

# Crear commit con mensaje descriptivo
git commit -m "feat: agregar análisis de columnas con pandeo

- Implementar cálculo de carga crítica de pandeo
- Agregar visualización de modos de pandeo
- Incluir validación de parámetros de entrada
- Actualizar documentación del módulo"
```

### 4. Push y Pull Request

```bash
# Subir cambios a tu fork
git push origin feature/nueva-funcionalidad

# Crear Pull Request en GitHub
```

### 5. Revisión y Merge

- Los mantenedores revisarán tu código
- Se pueden solicitar cambios
- Una vez aprobado, se hará merge

## 🐛 Reportar Bugs

### Antes de Reportar

1. Verifica que el bug no haya sido reportado ya
2. Asegúrate de usar la versión más reciente
3. Intenta reproducir el bug en un entorno limpio

### Información Requerida

```markdown
**Descripción del Bug**
Descripción clara y concisa del problema.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Desplazarse hacia abajo hasta '...'
4. Ver error

**Comportamiento Esperado**
Lo que debería suceder.

**Comportamiento Actual**
Lo que realmente sucede.

**Capturas de Pantalla**
Si aplica, agregar capturas de pantalla.

**Información del Sistema**
- Sistema Operativo: [ej. Windows 10]
- Versión de Python: [ej. 3.9.0]
- Versión del paquete: [ej. 1.0.0]

**Información Adicional**
Cualquier contexto adicional sobre el problema.
```

## ✨ Solicitar Características

### Antes de Solicitar

1. Verifica que la característica no exista ya
2. Considera si la característica es apropiada para el proyecto
3. Piensa en cómo implementarla

### Información Requerida

```markdown
**Descripción de la Característica**
Descripción clara de la funcionalidad deseada.

**Problema que Resuelve**
Explicar por qué esta característica es necesaria.

**Solución Propuesta**
Descripción de cómo debería funcionar.

**Alternativas Consideradas**
Otras soluciones que se han considerado.

**Contexto Adicional**
Cualquier información adicional relevante.
```

## ❓ Preguntas Frecuentes

### ¿Cómo puedo empezar a contribuir?

1. Lee esta guía completa
2. Explora el código existente
3. Identifica un área de interés
4. Comienza con issues marcados como "good first issue"

### ¿Qué hago si no estoy seguro de algo?

- Abre una discusión en GitHub
- Pregunta en los issues existentes
- Contacta a los mantenedores

### ¿Cómo puedo mejorar la documentación?

- Corrige errores tipográficos
- Mejora la claridad de las explicaciones
- Agrega ejemplos de uso
- Traduce a otros idiomas

### ¿Puedo contribuir sin conocimientos de ingeniería?

¡Sí! Necesitamos ayuda con:
- Mejoras de interfaz de usuario
- Testing y calidad de código
- Documentación y tutoriales
- Optimización de rendimiento

## 📞 Contacto

- **Issues de GitHub**: Para bugs y solicitudes de características
- **Discussions**: Para preguntas y discusiones generales
- **Email**: [tu-email@ejemplo.com]

## 🙏 Agradecimientos

Gracias a todos los contribuidores que hacen posible este proyecto. Cada contribución, por pequeña que sea, ayuda a mejorar la educación en ingeniería mecánica.

---

**¡Gracias por contribuir a PYTHON COURSERA MASTER!** 🚀 