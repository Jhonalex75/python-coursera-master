import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_process_data(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encuentra el archivo en: {file_path}")
        
        data = pd.read_csv(file_path, sep=';', encoding='utf-8')

        column_mapping = {
            'AREA': 'Area',
            'ACTIVIDAD REALIZADA': 'Actividad_Realizada',
            'TURNO': 'Turno',
            'FECHA': 'Fecha'
        }
        data.columns = [col.upper() for col in data.columns]
        data = data.rename(columns=column_mapping)

        data['Fecha'] = pd.to_datetime(data['Fecha'], format='%d/%m/%Y')
        return data
    except FileNotFoundError as e:
        print(f"Error al cargar los datos: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al cargar los datos: {e}")
        return None

def analyze_data(data):
    area_frequencies = data['Area'].value_counts()
    total_fallas = len(data)
    area_probabilities = (area_frequencies / total_fallas) * 100
    turno_frequencies = data['Turno'].value_counts()

    return area_frequencies, area_probabilities, turno_frequencies

def create_plots(data):
    plt.figure(figsize=(12, 10))
    sns.countplot(y=data['Area'], order=data['Area'].value_counts().index, palette='viridis')
    plt.title('Frecuencia de Intervenciones por Area')
    plt.xlabel('Cantidad de Intervenciones')
    plt.ylabel('Area')
    plt.show()
    
    plt.figure(figsize=(8, 10))
    sns.countplot(x=data['Turno'], palette='coolwarm')
    plt.title('Distribucion de Fallas por Turno')
    plt.xlabel('Turno')
    plt.ylabel('Cantidad de Intervenciones')
    plt.show()
    
    # Mejorar la grafica de tendencia de fallos
    plt.figure(figsize=(8, 8))
    top_areas = data['Area'].value_counts().head(5).index  # Seleccionar las 5 areas con mas fallos
    filtered_data = data[data['Area'].isin(top_areas)]
    trend_data = filtered_data.groupby(['Fecha', 'Area']).size().unstack()
    trend_data.plot(kind='line', figsize=(14,7), marker='o', linewidth=2)
    plt.title('Tendencia de Fallas en las Principales Areas a lo largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad de Intervenciones')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Area', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def main():
    file_path = "2025_febrero_completo.csv"
    data = load_and_process_data(file_path)
    
    if data is not None:
        area_frequencies, area_probabilities, turno_frequencies = analyze_data(data)
        
        print("\nFrecuencia de fallas por Area:")
        print(area_frequencies)
        
        print("\nProbabilidad de falla por Area:")
        print(area_probabilities)
        
        print("\nFrecuencia de fallas por Turno:")
        print(turno_frequencies)
        
        create_plots(data)
    else:
        print("No se pudieron cargar los datos correctamente.")

if __name__ == "__main__":
    main()
