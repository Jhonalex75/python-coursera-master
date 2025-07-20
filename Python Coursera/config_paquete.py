# =============================================================================
# CONFIGURACIÓN GLOBAL DEL PAQUETE PYTHON COURSERA MASTER
# =============================================================================
# Archivo de configuración central para todos los módulos
# Autor: Sistema de Ingeniería Mecánica con Python
# Versión: 1.0
# =============================================================================

import os
import json
from pathlib import Path

class ConfiguracionPaquete:
    """
    Clase para manejar la configuración global del paquete
    """
    
    def __init__(self):
        self.config_file = "config_paquete.json"
        self.config = self.cargar_configuracion()
    
    def cargar_configuracion(self):
        """Carga la configuración desde archivo o crea una por defecto"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
                return self.configuracion_por_defecto()
        else:
            return self.configuracion_por_defecto()
    
    def configuracion_por_defecto(self):
        """Retorna la configuración por defecto"""
        return {
            "paquete": {
                "nombre": "PYTHON COURSERA MASTER",
                "version": "1.0",
                "descripcion": "Paquete Educativo de Ingeniería Mecánica",
                "autor": "Sistema de Ingeniería Mecánica con Python",
                "fecha_creacion": "2024"
            },
            "interfaz": {
                "tema": "clam",
                "color_fondo": "#2c3e50",
                "color_primario": "#3498db",
                "color_secundario": "#ecf0f1",
                "fuente_principal": "Arial",
                "tamaño_fuente_titulo": 16,
                "tamaño_fuente_normal": 10
            },
            "modulos": {
                "analisis_estructural": {
                    "activo": True,
                    "version": "1.0",
                    "descripcion": "Análisis de estructuras, vigas, columnas y cerchas"
                },
                "dinamica_maquinas": {
                    "activo": True,
                    "version": "1.0",
                    "descripcion": "Análisis de mecanismos, vibraciones y balanceo"
                },
                "termodinamica_fluidos": {
                    "activo": True,
                    "version": "1.0",
                    "descripcion": "Ciclos termodinámicos y análisis de fluidos"
                },
                "materiales_resistencia": {
                    "activo": True,
                    "version": "1.0",
                    "descripcion": "Propiedades de materiales y análisis de resistencia"
                },
                "control_automatizacion": {
                    "activo": False,
                    "version": "0.1",
                    "descripcion": "Sistemas de control y automatización"
                },
                "manufactura_procesos": {
                    "activo": False,
                    "version": "0.1",
                    "descripcion": "Procesos de manufactura y optimización"
                }
            },
            "herramientas": {
                "calculadora_avanzada": {
                    "activo": True,
                    "version": "1.0",
                    "descripcion": "Calculadora con funciones de ingeniería"
                },
                "conversor_unidades": {
                    "activo": False,
                    "version": "0.1",
                    "descripcion": "Conversor de unidades de ingeniería"
                },
                "generador_graficos": {
                    "activo": False,
                    "version": "0.1",
                    "descripcion": "Generador de gráficos especializados"
                }
            },
            "archivos": {
                "directorio_datos": "datos/",
                "directorio_reportes": "reportes/",
                "directorio_logs": "logs/",
                "formato_reporte": "txt",
                "formato_datos": "csv"
            },
            "constantes_fisicas": {
                "gravedad": 9.81,
                "pi": 3.14159265359,
                "e": 2.71828182846,
                "velocidad_luz": 299792458,
                "constante_boltzmann": 1.380649e-23,
                "constante_avogadro": 6.02214076e23
            },
            "unidades": {
                "longitud": "m",
                "masa": "kg",
                "tiempo": "s",
                "temperatura": "K",
                "presion": "Pa",
                "energia": "J",
                "potencia": "W",
                "fuerza": "N"
            },
            "materiales": {
                "acero_1020": {
                    "nombre": "Acero AISI 1020",
                    "modulo_elasticidad": 200e9,
                    "modulo_poisson": 0.3,
                    "limite_fluencia": 250e6,
                    "resistencia_ultima": 400e6,
                    "densidad": 7850,
                    "coef_expansion_termica": 12e-6,
                    "conductividad_termica": 50
                },
                "aluminio_6061": {
                    "nombre": "Aluminio 6061-T6",
                    "modulo_elasticidad": 69e9,
                    "modulo_poisson": 0.33,
                    "limite_fluencia": 240e6,
                    "resistencia_ultima": 310e6,
                    "densidad": 2700,
                    "coef_expansion_termica": 23e-6,
                    "conductividad_termica": 167
                },
                "titanio_ti6al4v": {
                    "nombre": "Titanio Ti-6Al-4V",
                    "modulo_elasticidad": 114e9,
                    "modulo_poisson": 0.34,
                    "limite_fluencia": 825e6,
                    "resistencia_ultima": 950e6,
                    "densidad": 4430,
                    "coef_expansion_termica": 8.6e-6,
                    "conductividad_termica": 7
                }
            },
            "configuracion_graficos": {
                "estilo": "default",
                "tamaño_figura": [10, 6],
                "dpi": 100,
                "color_fondo": "white",
                "color_linea": "blue",
                "grosor_linea": 2,
                "tamaño_marcador": 6
            },
            "configuracion_reportes": {
                "incluir_graficos": True,
                "incluir_datos": True,
                "incluir_analisis": True,
                "formato_fecha": "%Y-%m-%d %H:%M:%S",
                "idioma": "español"
            }
        }
    
    def guardar_configuracion(self):
        """Guarda la configuración actual en archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def obtener_valor(self, ruta):
        """Obtiene un valor de configuración usando ruta con puntos"""
        try:
            valor = self.config
            for clave in ruta.split('.'):
                valor = valor[clave]
            return valor
        except KeyError:
            return None
    
    def establecer_valor(self, ruta, valor):
        """Establece un valor de configuración usando ruta con puntos"""
        try:
            claves = ruta.split('.')
            config = self.config
            
            # Navegar hasta el penúltimo nivel
            for clave in claves[:-1]:
                if clave not in config:
                    config[clave] = {}
                config = config[clave]
            
            # Establecer el valor
            config[claves[-1]] = valor
            return True
        except Exception as e:
            print(f"Error al establecer valor: {e}")
            return False
    
    def obtener_modulo_config(self, nombre_modulo):
        """Obtiene la configuración de un módulo específico"""
        return self.config.get("modulos", {}).get(nombre_modulo, {})
    
    def obtener_material_config(self, nombre_material):
        """Obtiene la configuración de un material específico"""
        return self.config.get("materiales", {}).get(nombre_material, {})
    
    def listar_modulos_activos(self):
        """Lista todos los módulos activos"""
        modulos_activos = []
        for nombre, config in self.config.get("modulos", {}).items():
            if config.get("activo", False):
                modulos_activos.append({
                    "nombre": nombre,
                    "version": config.get("version", "0.0"),
                    "descripcion": config.get("descripcion", "")
                })
        return modulos_activos
    
    def listar_herramientas_activas(self):
        """Lista todas las herramientas activas"""
        herramientas_activas = []
        for nombre, config in self.config.get("herramientas", {}).items():
            if config.get("activo", False):
                herramientas_activas.append({
                    "nombre": nombre,
                    "version": config.get("version", "0.0"),
                    "descripcion": config.get("descripcion", "")
                })
        return herramientas_activas
    
    def crear_directorios(self):
        """Crea los directorios necesarios para el paquete"""
        directorios = [
            self.config["archivos"]["directorio_datos"],
            self.config["archivos"]["directorio_reportes"],
            self.config["archivos"]["directorio_logs"]
        ]
        
        for directorio in directorios:
            Path(directorio).mkdir(parents=True, exist_ok=True)
    
    def obtener_info_paquete(self):
        """Obtiene información general del paquete"""
        return self.config.get("paquete", {})
    
    def obtener_configuracion_interfaz(self):
        """Obtiene la configuración de la interfaz"""
        return self.config.get("interfaz", {})
    
    def obtener_constantes_fisicas(self):
        """Obtiene las constantes físicas"""
        return self.config.get("constantes_fisicas", {})
    
    def obtener_unidades(self):
        """Obtiene las unidades por defecto"""
        return self.config.get("unidades", {})
    
    def obtener_configuracion_graficos(self):
        """Obtiene la configuración de gráficos"""
        return self.config.get("configuracion_graficos", {})
    
    def obtener_configuracion_reportes(self):
        """Obtiene la configuración de reportes"""
        return self.config.get("configuracion_reportes", {})

# Instancia global de configuración
config_paquete = ConfiguracionPaquete()

def obtener_configuracion():
    """Función de conveniencia para obtener la configuración global"""
    return config_paquete

def obtener_valor_config(ruta):
    """Función de conveniencia para obtener un valor de configuración"""
    return config_paquete.obtener_valor(ruta)

def establecer_valor_config(ruta, valor):
    """Función de conveniencia para establecer un valor de configuración"""
    return config_paquete.establecer_valor(ruta, valor)

if __name__ == "__main__":
    # Crear directorios necesarios
    config_paquete.crear_directorios()
    
    # Mostrar información del paquete
    info = config_paquete.obtener_info_paquete()
    print(f"Paquete: {info['nombre']} v{info['version']}")
    print(f"Descripción: {info['descripcion']}")
    
    # Mostrar módulos activos
    modulos = config_paquete.listar_modulos_activos()
    print(f"\nMódulos activos ({len(modulos)}):")
    for modulo in modulos:
        print(f"  - {modulo['nombre']} v{modulo['version']}")
    
    # Mostrar herramientas activas
    herramientas = config_paquete.listar_herramientas_activas()
    print(f"\nHerramientas activas ({len(herramientas)}):")
    for herramienta in herramientas:
        print(f"  - {herramienta['nombre']} v{herramienta['version']}")
    
    # Guardar configuración
    if config_paquete.guardar_configuracion():
        print("\n✅ Configuración guardada exitosamente")
    else:
        print("\n❌ Error al guardar configuración") 