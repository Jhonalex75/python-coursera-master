# Ejemplo de script de utilidad

Puedes agregar aquí scripts en Python, JavaScript u otros lenguajes para automatizar tareas o procesar datos relacionados con la estimación de costos.

Ejemplo de script Python:

```python
# calculo_area_tuberia.py
def area_tuberia(diametro_pulg, longitud_m):
    import math
    diametro_m = diametro_pulg * 0.0254
    return math.pi * diametro_m * longitud_m

if __name__ == "__main__":
    print("Área de tubería de 6'' y 10m:", area_tuberia(6, 10), "m²")
```
