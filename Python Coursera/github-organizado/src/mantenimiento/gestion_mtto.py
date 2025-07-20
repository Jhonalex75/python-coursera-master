# Script de gestión de mantenimiento
# Especialidad: Mantenimiento industrial

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class GestionMantenimiento:
    def __init__(self):
        """Inicializa el sistema de gestión de mantenimiento."""
        self.equipos = {}
        self.ordenes_trabajo = []
        self.historial_mtto = []
        self.inicializar_datos_ejemplo()
    
    def inicializar_datos_ejemplo(self):
        """Crea datos de ejemplo para demostración."""
        # Crear equipos de ejemplo
        equipos_ejemplo = [
            {"id": "BOM-001", "nombre": "Bomba Centrífuga Principal", "ubicacion": "Planta 1", "criticidad": "Alta"},
            {"id": "MOT-002", "nombre": "Motor Eléctrico 75HP", "ubicacion": "Planta 1", "criticidad": "Alta"},
            {"id": "VLV-003", "nombre": "Válvula de Control 8\"", "ubicacion": "Planta 2", "criticidad": "Media"},
            {"id": "COM-004", "nombre": "Compresor de Aire", "ubicacion": "Planta 2", "criticidad": "Alta"},
            {"id": "TRN-005", "nombre": "Transportador de Banda", "ubicacion": "Planta 1", "criticidad": "Media"},
        ]
        
        for equipo in equipos_ejemplo:
            self.equipos[equipo["id"]] = equipo
        
        # Crear historial de mantenimiento
        fecha_actual = datetime.now()
        tipos_mtto = ["Preventivo", "Correctivo", "Predictivo"]
        estados = ["Completado", "Pendiente", "En Progreso"]
        
        for i in range(50):  # Generar 50 registros históricos
            dias_atras = np.random.randint(1, 365)  # Hasta un año atrás
            fecha = fecha_actual - timedelta(days=dias_atras)
            
            equipo_id = list(self.equipos.keys())[np.random.randint(0, len(self.equipos))]
            tipo = tipos_mtto[np.random.randint(0, len(tipos_mtto))]
            duracion = np.random.randint(1, 8)  # Horas
            costo = np.random.randint(100, 2000)  # Dólares
            estado = estados[0] if dias_atras > 7 else estados[np.random.randint(0, len(estados))]
            
            registro = {
                "id": f"OT-{1000+i}",
                "equipo_id": equipo_id,
                "fecha": fecha,
                "tipo": tipo,
                "descripcion": f"Mantenimiento {tipo.lower()} de {self.equipos[equipo_id]['nombre']}",
                "duracion_horas": duracion,
                "costo": costo,
                "estado": estado
            }
            
            self.historial_mtto.append(registro)
    
    def obtener_historial_equipo(self, equipo_id):
        """Obtiene el historial de mantenimiento para un equipo específico.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            DataFrame con el historial de mantenimiento
        """
        if equipo_id not in self.equipos:
            return f"El equipo con ID {equipo_id} no existe."
        
        # Filtrar historial para el equipo específico
        historial_equipo = [reg for reg in self.historial_mtto if reg["equipo_id"] == equipo_id]
        
        # Convertir a DataFrame
        df = pd.DataFrame(historial_equipo)
        if not df.empty:
            df = df.sort_values(by="fecha", ascending=False)
        
        return df
    
    def analizar_costos_mtto(self):
        """Analiza los costos de mantenimiento por equipo y tipo."""
        # Convertir historial a DataFrame
        df = pd.DataFrame(self.historial_mtto)
        
        if df.empty:
            return "No hay datos de mantenimiento para analizar."
        
        # Análisis por equipo
        costos_por_equipo = df.groupby("equipo_id")["costo"].sum().sort_values(ascending=False)
        
        # Análisis por tipo de mantenimiento
        costos_por_tipo = df.groupby("tipo")["costo"].sum()
        
        # Visualización
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Gráfico de costos por equipo
        costos_por_equipo.plot(kind="bar", ax=ax1, color="skyblue")
        ax1.set_title("Costos de Mantenimiento por Equipo")
        ax1.set_xlabel("Equipo")
        ax1.set_ylabel("Costo Total ($)")
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico de costos por tipo
        costos_por_tipo.plot(kind="pie", ax=ax2, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax2.set_title("Distribución de Costos por Tipo de Mantenimiento")
        ax2.set_ylabel("")
        
        plt.tight_layout()
        plt.show()
        
        return {
            "costos_por_equipo": costos_por_equipo,
            "costos_por_tipo": costos_por_tipo,
            "costo_total": df["costo"].sum()
        }
    
    def calcular_indicadores_mtto(self):
        """Calcula indicadores clave de mantenimiento (MTBF, MTTR, disponibilidad)."""
        # Convertir historial a DataFrame
        df = pd.DataFrame(self.historial_mtto)
        
        if df.empty:
            return "No hay datos de mantenimiento para analizar."
        
        # Filtrar solo mantenimientos completados
        df_completados = df[df["estado"] == "Completado"].copy()
        
        # Ordenar por fecha
        df_completados = df_completados.sort_values(by=["equipo_id", "fecha"])
        
        # Calcular tiempo entre fallos (solo para mantenimientos correctivos)
        df_correctivos = df_completados[df_completados["tipo"] == "Correctivo"].copy()
        
        resultados = {}
        
        for equipo_id in self.equipos.keys():
            df_equipo = df_correctivos[df_correctivos["equipo_id"] == equipo_id]
            
            if len(df_equipo) > 1:
                # Calcular diferencias de tiempo entre fallos
                df_equipo = df_equipo.sort_values(by="fecha")
                tiempos_entre_fallos = []
                
                for i in range(1, len(df_equipo)):
                    delta = (df_equipo.iloc[i]["fecha"] - df_equipo.iloc[i-1]["fecha"]).total_seconds() / 3600  # en horas
                    tiempos_entre_fallos.append(delta)
                
                mtbf = np.mean(tiempos_entre_fallos) if tiempos_entre_fallos else 0
                
                # Tiempo medio de reparación (MTTR)
                mttr = df_equipo["duracion_horas"].mean()
                
                # Disponibilidad
                if mtbf + mttr > 0:
                    disponibilidad = mtbf / (mtbf + mttr) * 100
                else:
                    disponibilidad = 0
                
                resultados[equipo_id] = {
                    "MTBF (horas)": mtbf,
                    "MTTR (horas)": mttr,
                    "Disponibilidad (%)": disponibilidad
                }
        
        # Convertir a DataFrame para mejor visualización
        df_resultados = pd.DataFrame(resultados).T
        
        # Visualizar resultados
        if not df_resultados.empty:
            plt.figure(figsize=(10, 6))
            ax = df_resultados[["MTBF (horas)", "MTTR (horas)"]].plot(kind="bar")
            ax.set_title("MTBF y MTTR por Equipo")
            ax.set_ylabel("Horas")
            ax.set_xlabel("Equipo")
            plt.tight_layout()
            plt.show()
            
            plt.figure(figsize=(8, 6))
            df_resultados["Disponibilidad (%)"].plot(kind="bar", color="green")
            plt.title("Disponibilidad por Equipo")
            plt.ylabel("Disponibilidad (%)")
            plt.xlabel("Equipo")
            plt.axhline(y=95, color='r', linestyle='--', label="Objetivo (95%)")
            plt.legend()
            plt.tight_layout()
            plt.show()
        
        return df_resultados

# Ejecutar análisis de ejemplo
if __name__ == "__main__":
    gestion = GestionMantenimiento()
    print("Análisis de costos de mantenimiento:")
    resultados_costos = gestion.analizar_costos_mtto()
    
    print("\nIndicadores de mantenimiento:")
    indicadores = gestion.calcular_indicadores_mtto()
    print(indicadores)
