import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_process_data(file_path):
    try:
        # Cargar datos con separador punto y coma
        data = pd.read_csv(file_path, sep=';')
        
        # Renombrar las columnas
        column_mapping = {
            'AREA': 'Área',
            'ACTIVIDAD REALIZADA': 'Actividad realizada',
            'TURNO': 'Turno',
            'FECHA': 'Fecha'
        }
        
        # Verificar si las columnas existen
        missing_columns = [col for col in column_mapping.keys() if col not in data.columns]
        if missing_columns:
            print(f"Columnas en el archivo: {data.columns.tolist()}")
            raise KeyError(f"Faltan las siguientes columnas: {', '.join(missing_columns)}")
            
        # Renombrar columnas
        data = data.rename(columns=column_mapping)
        return data
        
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

def create_plots(data):
    try:
        # Contar frecuencia de áreas
        area_frequencies = data['Área'].value_counts()

        # Filtrar datos de la trituradora cónica
        trituradora_data = data[data['Área'] == 'Trituración']
        trituradora_turno = trituradora_data['Turno'].value_counts()

        # Gráfico 1: Frecuencia de áreas
        plt.figure(figsize=(10, 6))
        sns.barplot(x=area_frequencies.index, y=area_frequencies.values, palette='viridis')
        plt.title('Frecuencia de Intervenciones por Área', fontsize=16)
        plt.xlabel('Área', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Gráfico 2: Intervenciones en la trituradora cónica (día vs. noche)
        plt.figure(figsize=(8, 6))
        sns.barplot(x=trituradora_turno.index, y=trituradora_turno.values, palette='coolwarm')
        plt.title('Intervenciones en la Trituradora Cónica (Día vs. Noche)', fontsize=16)
        plt.xlabel('Turno', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.tight_layout()
        plt.show()

        # Gráfico 3: Actividades más comunes
        activity_frequencies = data['Actividad realizada'].value_counts().head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=activity_frequencies.values, y=activity_frequencies.index, palette='magma')
        plt.title('Actividades Más Comunes', fontsize=16)
        plt.xlabel('Frecuencia', fontsize=12)
        plt.ylabel('Actividad', fontsize=12)
        plt.tight_layout()
        plt.show()

        # Análisis estadístico
        total_interventions = data.shape[0]
        trituradora_proportion = trituradora_data.shape[0] / total_interventions * 100

        print(f"Total de intervenciones: {total_interventions}")
        print(f"Proporción de intervenciones en la trituradora cónica: {trituradora_proportion:.2f}%")
        print("\nFrecuencia de intervenciones por área:")
        print(area_frequencies)
        print("\nFrecuencia de intervenciones en la trituradora cónica por turno:")
        print(trituradora_turno)
        
    except Exception as e:
        print(f"Error al crear los gráficos: {e}")

def main():
    file_path = r"C:\Users\User\OneDrive\Documents\ARCHIVOS PYTHON\INFORME FEBRERO\2025_febrero.csv"
    print(f"Buscando archivo en: {file_path}")
    
    # Mostrar las primeras filas y columnas del CSV
    try:
        raw_data = pd.read_csv(file_path)
        print("\nColumnas en el archivo CSV:")
        print(raw_data.columns.tolist())
        print("\nPrimeras 5 filas del archivo:")
        print(raw_data.head())
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    data = load_and_process_data(file_path)
    if data is not None:
        print(data.columns)  # Ver nombres de columnas
        print(data.head())   # Ver primeras filas
        create_plots(data)
    else:
        print("No se pudieron cargar los datos correctamente")

if __name__ == "__main__":
    main()