# 🐍 Curso de Python de Coursera - Materiales Organizados

## 📚 Descripción

Este repositorio contiene todos los materiales, ejemplos y ejercicios del curso de Python de Coursera, organizados por módulos y niveles de dificultad. Cada módulo incluye ejemplos prácticos, ejercicios y proyectos completos.

## 🎯 Estructura del Curso

### **Módulo 1: Fundamentos de Python** ✅
- Variables y tipos de datos
- Operadores y expresiones
- Entrada y salida básica
- Formateo de strings
- Conversión de tipos

### **Módulo 2: Control de Flujo** ✅
- Declaraciones condicionales (if, elif, else)
- Operadores lógicos (and, or, not)
- Decisiones y ramificación
- Anidamiento de condiciones

### **Módulo 3: Ordenamiento y Manejo de Errores** ✅
- Algoritmos de ordenamiento (bubble sort, quick sort)
- Manejo de excepciones con try/except
- Validación de datos de entrada
- Análisis de datos con manejo de errores

### **Módulo 4: Control de Versiones con Git** ✅
- Conceptos básicos de control de versiones
- Comandos Git fundamentales
- Flujo de trabajo con Git
- Colaboración en proyectos

### **Módulo 5: Testing con pytest** ✅
- Conceptos básicos de testing
- Framework pytest
- Tests unitarios
- Fixtures y parametrización
- Cobertura de código

### **Módulo 6: Manejo de Errores Avanzado** ✅
- Debugging avanzado
- Logging y monitoreo
- Assertions y validaciones
- Casos de estudio reales

## 📁 Estructura de Directorios

```
coursera-python-course/
├── modulo_1_fundamentos/
│   └── variables_tipos.py          # Variables, tipos, operaciones básicas
├── modulo_2_control_flujo/
│   └── condicionales.py            # Condicionales, operadores lógicos
├── modulo_3_ordenamiento_errores/
│   └── ordenamiento_errores.py     # Algoritmos de ordenamiento, manejo de errores
├── modulo_4_control_versiones/
│   └── git_basico.py               # Control de versiones con Git
├── modulo_5_testing/
│   ├── testing_pytest.py           # Framework pytest y testing
│   └── test_funciones.py           # Archivo de tests ejecutables
├── modulo_6_manejo_errores/
│   └── debugging.py                # Debugging avanzado y logging
├── herramientas_utilidad/
│   └── debugging_toolkit.py        # Kit de herramientas de debugging
├── setup_coursera.py               # Script de configuración del curso
├── ejecutar_curso.py               # Script principal para ejecutar módulos
├── requirements.txt                # Dependencias del curso
├── pytest.ini                     # Configuración de pytest
└── README.md                      # Documentación principal
```

## 🚀 Cómo Usar

### 1. **Instalación y Configuración**
```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd coursera-python-course

# Configurar el entorno del curso
python setup_coursera.py

# Instalar dependencias
pip install -r requirements.txt
```

### 2. **Ejecutar el Curso**
```bash
# Ejecutar el script principal (modo interactivo)
python ejecutar_curso.py

# Ejecutar un módulo específico
python ejecutar_curso.py 1    # Módulo 1
python ejecutar_curso.py 2    # Módulo 2
python ejecutar_curso.py 3    # Módulo 3
python ejecutar_curso.py 4    # Módulo 4
python ejecutar_curso.py 5    # Módulo 5
python ejecutar_curso.py 6    # Módulo 6

# Ejecutar todos los módulos
python ejecutar_curso.py todos

# Ejecutar tests
python ejecutar_curso.py tests
```

### 3. **Ejecutar Módulos Individuales**
```bash
# Módulo 1: Fundamentos
python modulo_1_fundamentos/variables_tipos.py

# Módulo 2: Control de Flujo
python modulo_2_control_flujo/condicionales.py

# Módulo 3: Ordenamiento y Errores
python modulo_3_ordenamiento_errores/ordenamiento_errores.py

# Módulo 4: Git
python modulo_4_control_versiones/git_basico.py

# Módulo 5: Testing
python modulo_5_testing/testing_pytest.py

# Módulo 6: Debugging Avanzado
python modulo_6_manejo_errores/debugging.py
```

### 4. **Ejecutar Tests**
```bash
# Ejecutar tests del módulo 5
pytest modulo_5_testing/test_funciones.py -v

# Ejecutar tests con cobertura
pytest modulo_5_testing/test_funciones.py --cov=. --cov-report=html
```

## 📖 Contenido de Cada Módulo

### **Módulo 1: Fundamentos**
- Variables y tipos de datos básicos
- Operadores aritméticos, de comparación y lógicos
- Entrada con `input()` y salida con `print()`
- Formateo de strings

### **Módulo 2: Control de Flujo**
- Estructuras if-elif-else
- Operadores lógicos (and, or, not)
- Anidamiento de condiciones
- Ejercicios prácticos de decisión

### **Módulo 3: Bucles**
- Bucles for con range() y secuencias
- Bucles while con condiciones
- Control de bucles (break, continue, else)
- Iteración sobre diferentes tipos de datos

### **Módulo 4: Estructuras de Datos**
- Listas: creación, modificación, métodos
- Tuplas: inmutabilidad y uso
- Diccionarios: claves, valores, métodos
- Conjuntos: operaciones de conjunto

### **Módulo 5: Funciones**
- Definición y llamada de funciones
- Parámetros posicionales y con nombre
- Valores por defecto
- Alcance local y global

### **Módulo 6: Manejo de Errores**
- Try-except básico y específico
- Tipos de excepciones comunes
- Debugging con print y logging
- Mejores prácticas

### **Módulo 7: Control de Versiones**
- Conceptos básicos de Git
- Comandos principales
- Repositorios locales y remotos
- Colaboración básica

### **Módulo 8: Testing**
- Conceptos de testing
- pytest básico
- Casos de prueba
- Cobertura de código

## 🛠️ Herramientas Incluidas

### **Debugging Toolkit** ✅
- Técnicas de debugging avanzadas
- Logging configurado con diferentes niveles
- Herramientas de diagnóstico interactivas
- Ejemplos de casos reales de debugging
- Assertions y validaciones automáticas

### **Testing Framework** ✅
- Framework pytest completo
- Tests unitarios con fixtures
- Parametrización de tests
- Cobertura de código
- Archivo de configuración pytest.ini

### **Control de Versiones** ✅
- Simulador de Git para aprendizaje
- Comandos Git reales
- Flujo de trabajo básico
- Mejores prácticas

### **Scripts de Utilidad** ✅
- `setup_coursera.py`: Configuración automática del entorno
- `ejecutar_curso.py`: Script principal interactivo
- `requirements.txt`: Dependencias organizadas
- Configuración de pytest

## 📊 Progreso del Curso

| Módulo | Estado | Archivos | Tests |
|--------|--------|----------|-------|
| 1. Fundamentos | ✅ Completo | `variables_tipos.py` | Incluidos |
| 2. Control de Flujo | ✅ Completo | `condicionales.py` | Incluidos |
| 3. Ordenamiento y Errores | ✅ Completo | `ordenamiento_errores.py` | Incluidos |
| 4. Control de Versiones | ✅ Completo | `git_basico.py` | Simulador |
| 5. Testing | ✅ Completo | `testing_pytest.py`, `test_funciones.py` | ✅ pytest |
| 6. Debugging Avanzado | ✅ Completo | `debugging.py` | Incluidos |

## 🎓 Aprendizaje Recomendado

### **Secuencia de Estudio**
1. **Módulo 1**: Fundamentos básicos de Python
2. **Módulo 2**: Control de flujo y decisiones
3. **Módulo 3**: Ordenamiento y manejo de errores
4. **Módulo 4**: Control de versiones con Git
5. **Módulo 5**: Testing con pytest
6. **Módulo 6**: Debugging avanzado

### **Prácticas Recomendadas**
- Ejecutar cada módulo en orden
- Experimentar con los ejemplos
- Modificar el código para aprender
- Ejecutar los tests para verificar comprensión
- Usar el debugging toolkit para resolver problemas

## 🔧 Configuración Avanzada

### **Entorno de Desarrollo**
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Configurar pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

### **IDE Recomendado**
- **VS Code** con extensiones Python
- **PyCharm** Community Edition
- **Jupyter Notebook** para experimentación

## 📝 Notas Importantes

- Todos los módulos son independientes pero complementarios
- Cada módulo incluye ejemplos prácticos y ejercicios
- Los tests están diseñados para verificar el aprendizaje
- El debugging toolkit es útil para proyectos reales
- Git es fundamental para el desarrollo profesional

## 🤝 Contribuciones

Este curso está diseñado para ser educativo y práctico. Si encuentras errores o tienes sugerencias de mejora:

1. Revisa los tests para entender el comportamiento esperado
2. Usa el debugging toolkit para identificar problemas
3. Documenta cualquier cambio o mejora
4. Mantén la estructura modular del curso

## 📚 Recursos Adicionales

- [Documentación oficial de Python](https://docs.python.org/)
- [Tutorial de pytest](https://docs.pytest.org/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Python Debugging Guide](https://docs.python.org/3/library/pdb.html)

## 📊 Proyectos Integrados

### **1. Calculadora Avanzada**
- Operaciones básicas y avanzadas
- Manejo de errores
- Interfaz de línea de comandos
- Testing completo

### **2. Gestor de Contactos**
- CRUD de contactos
- Persistencia de datos
- Búsqueda y filtrado
- Validación de datos

### **3. Analizador de Datos**
- Lectura de archivos CSV
- Análisis estadístico básico
- Visualización de datos
- Generación de reportes

### **4. Juego de Adivinanza**
- Lógica de juego
- Interacción con usuario
- Sistema de puntuación
- Diferentes niveles

## 🧪 Testing y Validación

### **Ejecutar Tests**
```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests de un módulo específico
pytest modulo_5_funciones/

# Ejecutar con cobertura
pytest --cov=.

# Ejecutar tests específicos
pytest -k "test_calculadora"
```

### **Cobertura de Código**
```bash
# Generar reporte de cobertura
pytest --cov=. --cov-report=html

# Ver cobertura en terminal
pytest --cov=. --cov-report=term-missing
```

## 📚 Recursos Adicionales

### **Documentación**
- Guías paso a paso para cada módulo
- Ejemplos de código comentados
- Soluciones a ejercicios
- Mejores prácticas

### **Datos de Ejemplo**
- Archivos CSV para análisis
- Datos de prueba para ejercicios
- Configuraciones de ejemplo

### **Plantillas**
- Plantillas para nuevos proyectos
- Configuraciones de testing
- Estructuras de archivos

## 🤝 Contribuciones

### **Cómo Contribuir**
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Enviar Pull Request

### **Estándares de Código**
- PEP 8 para estilo de código
- Docstrings para documentación
- Tests para nueva funcionalidad
- Comentarios explicativos

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autor

- **Ing. Jhon A. Valencia**
- **Especialidad**: Python, Ingeniería de Software
- **Contacto**: [email@ejemplo.com]

## 🔄 Historial de Versiones

### v1.0.0 (2024-01-15)
- ✅ Organización inicial de módulos
- ✅ Ejemplos completos para cada módulo
- ✅ Proyectos integrados
- ✅ Herramientas de debugging y testing

---

**⭐ Si este material te resulta útil, considera darle una estrella en GitHub!** 