"""
Sistema de Análisis Estadístico para Ingeniería
==============================================

Este módulo proporciona herramientas completas para análisis estadístico
específicamente diseñadas para aplicaciones de ingeniería.

Funcionalidades:
- Estadísticas descriptivas avanzadas
- Pruebas de normalidad y bondad de ajuste
- Análisis de correlación y regresión
- Control de calidad estadístico
- Análisis de capacidad de procesos
- Visualizaciones profesionales

Autor: Ingeniería Estadística
Versión: 2.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, t, chi2, f
from typing import Dict, List, Tuple, Optional, Union
import warnings
warnings.filterwarnings('ignore')


class AnalisisEstadistico:
    """
    Clase principal para análisis estadístico de datos de ingeniería
    """
    
    def __init__(self, datos: Optional[pd.DataFrame] = None):
        """
        Inicializa el analizador estadístico
        
        Args:
            datos: DataFrame de pandas con los datos a analizar (opcional)
        """
        self.datos = datos
        self.resultados = {}
        self.configuracion = {
            'nivel_confianza': 0.95,
            'alpha': 0.05,
            'decimales': 4
        }
    
    def cargar_datos(self, ruta_archivo: str, tipo: str = 'csv', **kwargs) -> bool:
        """
        Carga datos desde un archivo
        
        Args:
            ruta_archivo: Ruta al archivo de datos
            tipo: Tipo de archivo ('csv', 'excel', etc.)
            **kwargs: Argumentos adicionales para la función de lectura
            
        Returns:
            bool: True si se cargaron correctamente
        """
        try:
            if tipo.lower() == 'csv':
                self.datos = pd.read_csv(ruta_archivo, **kwargs)
            elif tipo.lower() in ['excel', 'xlsx', 'xls']:
                self.datos = pd.read_excel(ruta_archivo, **kwargs)
            elif tipo.lower() == 'json':
                self.datos = pd.read_json(ruta_archivo, **kwargs)
            else:
                raise ValueError(f"Tipo de archivo '{tipo}' no soportado.")
                
            print(f"✅ Datos cargados correctamente. Dimensiones: {self.datos.shape}")
            return True
        except Exception as e:
            print(f"❌ Error al cargar los datos: {str(e)}")
            return False
    
    def estadisticas_descriptivas(self, columnas: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Calcula estadísticas descriptivas completas para las columnas numéricas
        
        Args:
            columnas: Lista de columnas a analizar (None para todas las numéricas)
            
        Returns:
            DataFrame con estadísticas descriptivas
        """
        if self.datos is None:
            print("❌ No hay datos cargados.")
            return None
        
        # Seleccionar columnas numéricas si no se especifican
        if columnas is None:
            columnas_num = self.datos.select_dtypes(include=['number']).columns
        else:
            columnas_num = [col for col in columnas if col in self.datos.columns and 
                           np.issubdtype(self.datos[col].dtype, np.number)]
        
        if not columnas_num:
            print("❌ No hay columnas numéricas para analizar.")
            return None
        
        # Calcular estadísticas básicas
        stats_desc = self.datos[columnas_num].describe()
        
        # Añadir estadísticas avanzadas
        stats_desc.loc['varianza'] = self.datos[columnas_num].var()
        stats_desc.loc['asimetria'] = self.datos[columnas_num].skew()
        stats_desc.loc['curtosis'] = self.datos[columnas_num].kurtosis()
        stats_desc.loc['cv'] = stats_desc.loc['std'] / stats_desc.loc['mean'] * 100  # Coeficiente de variación
        stats_desc.loc['rango'] = stats_desc.loc['max'] - stats_desc.loc['min']
        stats_desc.loc['iqr'] = stats_desc.loc['75%'] - stats_desc.loc['25%']
        
        # Calcular intervalos de confianza para la media
        for col in columnas_num:
            datos_col = self.datos[col].dropna()
            if len(datos_col) > 0:
                n = len(datos_col)
                se = datos_col.std() / np.sqrt(n)
                t_critico = t.ppf((1 + self.configuracion['nivel_confianza']) / 2, n - 1)
                margen_error = t_critico * se
                stats_desc.loc[f'ic_inferior_{col}'] = datos_col.mean() - margen_error
                stats_desc.loc[f'ic_superior_{col}'] = datos_col.mean() + margen_error
        
        self.resultados['estadisticas_descriptivas'] = stats_desc
        return stats_desc
    
    def prueba_normalidad(self, columna: str) -> Dict:
        """
        Realiza pruebas de normalidad para una columna
        
        Args:
            columna: Nombre de la columna a analizar
            
        Returns:
            Diccionario con resultados de las pruebas
        """
        if self.datos is None or columna not in self.datos.columns:
            print("❌ Datos o columna no disponibles.")
            return None
        
        # Eliminar valores nulos
        datos_columna = self.datos[columna].dropna()
        
        if len(datos_columna) < 3:
            print("❌ Se necesitan al menos 3 observaciones para la prueba de normalidad.")
            return None
        
        resultados = {}
        
        # Prueba de Shapiro-Wilk
        shapiro_test = stats.shapiro(datos_columna)
        resultados['shapiro_wilk'] = {
            'estadistico': shapiro_test[0],
            'p_valor': shapiro_test[1],
            'es_normal': shapiro_test[1] > self.configuracion['alpha']
        }
        
        # Prueba de Kolmogorov-Smirnov
        ks_test = stats.kstest(datos_columna, 'norm', args=(datos_columna.mean(), datos_columna.std()))
        resultados['kolmogorov_smirnov'] = {
            'estadistico': ks_test[0],
            'p_valor': ks_test[1],
            'es_normal': ks_test[1] > self.configuracion['alpha']
        }
        
        # Prueba de Anderson-Darling
        anderson_test = stats.anderson(datos_columna)
        resultados['anderson_darling'] = {
            'estadistico': anderson_test.statistic,
            'valores_criticos': anderson_test.critical_values,
            'niveles_significancia': anderson_test.significance_level
        }
        
        # Resumen
        resultados['resumen'] = {
            'es_normal_shapiro': resultados['shapiro_wilk']['es_normal'],
            'es_normal_ks': resultados['kolmogorov_smirnov']['es_normal'],
            'recomendacion': 'Normal' if resultados['shapiro_wilk']['es_normal'] else 'No Normal'
        }
        
        self.resultados[f'normalidad_{columna}'] = resultados
        return resultados
    
    def analisis_correlacion(self, metodo: str = 'pearson', visualizar: bool = True) -> pd.DataFrame:
        """
        Calcula la matriz de correlación entre variables numéricas
        
        Args:
            metodo: Método de correlación ('pearson', 'spearman', 'kendall')
            visualizar: Si mostrar el mapa de calor
            
        Returns:
            DataFrame con matriz de correlación
        """
        if self.datos is None:
            print("❌ No hay datos cargados.")
            return None
        
        # Seleccionar columnas numéricas
        columnas_num = self.datos.select_dtypes(include=['number']).columns
        
        if len(columnas_num) < 2:
            print("❌ Se necesitan al menos dos columnas numéricas para calcular correlaciones.")
            return None
        
        # Calcular matriz de correlación
        corr_matrix = self.datos[columnas_num].corr(method=metodo)
        
        # Calcular p-valores para correlaciones significativas
        p_values = pd.DataFrame(index=columnas_num, columns=columnas_num)
        for i in columnas_num:
            for j in columnas_num:
                if i != j:
                    r, p = stats.pearsonr(self.datos[i].dropna(), self.datos[j].dropna())
                    p_values.loc[i, j] = p
                else:
                    p_values.loc[i, j] = 1.0
        
        self.resultados['correlacion'] = {
            'matriz': corr_matrix,
            'p_valores': p_values,
            'metodo': metodo
        }
        
        # Visualización
        if visualizar:
            self.visualizar_correlacion(corr_matrix, p_values)
        
        return corr_matrix
    
    def analisis_regresion(self, variable_dependiente: str, variables_independientes: List[str]) -> Dict:
        """
        Realiza análisis de regresión lineal múltiple
        
        Args:
            variable_dependiente: Nombre de la variable dependiente
            variables_independientes: Lista de variables independientes
            
        Returns:
            Diccionario con resultados del análisis de regresión
        """
        if self.datos is None:
            print("❌ No hay datos cargados.")
            return None
        
        # Verificar que todas las variables existan
        todas_variables = [variable_dependiente] + variables_independientes
        if not all(var in self.datos.columns for var in todas_variables):
            print("❌ Una o más variables no existen en el dataset.")
            return None
        
        # Eliminar filas con valores faltantes
        datos_limpios = self.datos[todas_variables].dropna()
        
        if len(datos_limpios) < len(variables_independientes) + 1:
            print("❌ Insuficientes datos para el análisis de regresión.")
            return None
        
        # Preparar datos para regresión
        X = datos_limpios[variables_independientes]
        y = datos_limpios[variable_dependiente]
        
        # Agregar constante para intercepto
        X = sm.add_constant(X)
        
        # Realizar regresión
        modelo = sm.OLS(y, X).fit()
        
        # Extraer resultados
        resultados = {
            'resumen': modelo.summary(),
            'r_cuadrado': modelo.rsquared,
            'r_cuadrado_ajustado': modelo.rsquared_adj,
            'f_statistic': modelo.fvalue,
            'f_pvalue': modelo.f_pvalue,
            'aic': modelo.aic,
            'bic': modelo.bic,
            'coeficientes': modelo.params,
            'p_valores': modelo.pvalues,
            'intervalos_confianza': modelo.conf_int(),
            'residuos': modelo.resid,
            'valores_predichos': modelo.fittedvalues
        }
        
        self.resultados['regresion'] = resultados
        return resultados
    
    def control_calidad_estadistico(self, columna: str, especificacion_superior: float = None,
                                   especificacion_inferior: float = None, 
                                   especificacion_objetivo: float = None) -> Dict:
        """
        Realiza análisis de control de calidad estadístico
        
        Args:
            columna: Nombre de la columna a analizar
            especificacion_superior: Límite superior de especificación
            especificacion_inferior: Límite inferior de especificación
            especificacion_objetivo: Valor objetivo
            
        Returns:
            Diccionario con análisis de capacidad
        """
        if self.datos is None or columna not in self.datos.columns:
            print("❌ Datos o columna no disponibles.")
            return None
        
        datos = self.datos[columna].dropna()
        
        if len(datos) < 30:
            print("⚠️ Se recomiendan al menos 30 observaciones para análisis de capacidad.")
        
        # Estadísticas básicas
        media = datos.mean()
        desv_est = datos.std()
        
        # Análisis de capacidad
        resultados = {
            'estadisticas_basicas': {
                'media': media,
                'desviacion_estandar': desv_est,
                'n': len(datos)
            }
        }
        
        # Cp y Cpk si se proporcionan especificaciones
        if especificacion_superior is not None and especificacion_inferior is not None:
            usl = especificacion_superior
            lsl = especificacion_inferior
            
            # Cp (Capacidad del proceso)
            cp = (usl - lsl) / (6 * desv_est)
            
            # Cpk (Capacidad del proceso considerando centrado)
            cpu = (usl - media) / (3 * desv_est)
            cpl = (media - lsl) / (3 * desv_est)
            cpk = min(cpu, cpl)
            
            # Pp y Ppk (Capacidad del proceso usando desviación estándar total)
            pp = (usl - lsl) / (6 * datos.std(ddof=1))
            ppu = (usl - media) / (3 * datos.std(ddof=1))
            ppl = (media - lsl) / (3 * datos.std(ddof=1))
            ppk = min(ppu, ppl)
            
            resultados['capacidad'] = {
                'cp': cp,
                'cpk': cpk,
                'pp': pp,
                'ppk': ppk,
                'cpu': cpu,
                'cpl': cpl,
                'usl': usl,
                'lsl': lsl
            }
            
            # Interpretación
            if cp >= 1.33 and cpk >= 1.33:
                interpretacion = "Excelente"
            elif cp >= 1.0 and cpk >= 1.0:
                interpretacion = "Adecuado"
            elif cp >= 0.83 and cpk >= 0.83:
                interpretacion = "Marginal"
            else:
                interpretacion = "Inadecuado"
            
            resultados['interpretacion'] = interpretacion
        
        # Análisis de outliers
        q1 = datos.quantile(0.25)
        q3 = datos.quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        
        outliers = datos[(datos < limite_inferior) | (datos > limite_superior)]
        
        resultados['outliers'] = {
            'cantidad': len(outliers),
            'porcentaje': len(outliers) / len(datos) * 100,
            'valores': outliers.tolist()
        }
        
        self.resultados[f'control_calidad_{columna}'] = resultados
        return resultados
    
    def visualizar_distribucion(self, columna: str, bins: int = 30) -> None:
        """
        Visualiza la distribución de una variable
        
        Args:
            columna: Nombre de la columna a visualizar
            bins: Número de bins para el histograma
        """
        if self.datos is None or columna not in self.datos.columns:
            print("❌ Datos o columna no disponibles.")
            return
        
        datos = self.datos[columna].dropna()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Histograma con curva normal
        ax1.hist(datos, bins=bins, density=True, alpha=0.7, color='skyblue', edgecolor='black')
        x = np.linspace(datos.min(), datos.max(), 100)
        y = norm.pdf(x, datos.mean(), datos.std())
        ax1.plot(x, y, 'r-', linewidth=2, label='Distribución Normal')
        ax1.set_title(f'Distribución de {columna}', fontweight='bold')
        ax1.set_xlabel(columna)
        ax1.set_ylabel('Densidad')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2.boxplot(datos, patch_artist=True, boxprops=dict(facecolor='lightgreen'))
        ax2.set_title(f'Diagrama de Caja - {columna}', fontweight='bold')
        ax2.set_ylabel(columna)
        ax2.grid(True, alpha=0.3)
        
        # Q-Q plot
        stats.probplot(datos, dist="norm", plot=ax3)
        ax3.set_title(f'Q-Q Plot - {columna}', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Estadísticas resumidas
        ax4.axis('off')
        stats_text = f"""
        Estadísticas de {columna}:
        
        Media: {datos.mean():.4f}
        Mediana: {datos.median():.4f}
        Desv. Est.: {datos.std():.4f}
        Mínimo: {datos.min():.4f}
        Máximo: {datos.max():.4f}
        Asimetría: {datos.skew():.4f}
        Curtosis: {datos.kurtosis():.4f}
        N: {len(datos)}
        """
        ax4.text(0.1, 0.5, stats_text, transform=ax4.transAxes, fontsize=12,
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def visualizar_correlacion(self, corr_matrix: pd.DataFrame, p_values: pd.DataFrame) -> None:
        """
        Visualiza la matriz de correlación
        
        Args:
            corr_matrix: Matriz de correlación
            p_values: Matriz de p-valores
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Mapa de calor de correlaciones
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, ax=ax1, fmt='.3f')
        ax1.set_title('Matriz de Correlación', fontweight='bold')
        
        # Mapa de calor de p-valores
        sns.heatmap(p_values, annot=True, cmap='RdYlGn_r', center=0.05, 
                   square=True, ax=ax2, fmt='.3f')
        ax2.set_title('P-valores de Correlación', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def generar_reporte_completo(self, columnas_numericas: Optional[List[str]] = None) -> None:
        """
        Genera un reporte completo de análisis estadístico
        
        Args:
            columnas_numericas: Lista de columnas numéricas a analizar
        """
        if self.datos is None:
            print("❌ No hay datos cargados.")
            return
        
        print("📊 REPORTE DE ANÁLISIS ESTADÍSTICO")
        print("=" * 60)
        
        # Información general
        print(f"\n📋 INFORMACIÓN GENERAL:")
        print(f"Dimensiones del dataset: {self.datos.shape}")
        print(f"Columnas: {list(self.datos.columns)}")
        print(f"Tipos de datos:")
        for col, dtype in self.datos.dtypes.items():
            print(f"  {col}: {dtype}")
        
        # Valores faltantes
        print(f"\n🔍 VALORES FALTANTES:")
        missing = self.datos.isnull().sum()
        for col, count in missing.items():
            if count > 0:
                print(f"  {col}: {count} ({count/len(self.datos)*100:.1f}%)")
        
        # Estadísticas descriptivas
        print(f"\n📈 ESTADÍSTICAS DESCRIPTIVAS:")
        stats_desc = self.estadisticas_descriptivas(columnas_numericas)
        if stats_desc is not None:
            print(stats_desc.round(4))
        
        # Pruebas de normalidad
        if columnas_numericas:
            print(f"\n📊 PRUEBAS DE NORMALIDAD:")
            for col in columnas_numericas:
                if col in self.datos.columns:
                    print(f"\n{col}:")
                    normalidad = self.prueba_normalidad(col)
                    if normalidad:
                        print(f"  Shapiro-Wilk: p = {normalidad['shapiro_wilk']['p_valor']:.4f}")
                        print(f"  Es normal: {normalidad['shapiro_wilk']['es_normal']}")
        
        # Análisis de correlación
        print(f"\n🔗 ANÁLISIS DE CORRELACIÓN:")
        corr = self.analisis_correlacion(visualizar=False)
        if corr is not None:
            print("Matriz de correlación (Pearson):")
            print(corr.round(4))
        
        print(f"\n✅ Reporte completado exitosamente!")


def crear_datos_ejemplo() -> pd.DataFrame:
    """
    Crea datos de ejemplo para demostración
    
    Returns:
        DataFrame con datos de ejemplo
    """
    np.random.seed(42)
    n = 100
    
    # Datos normales
    datos_normales = np.random.normal(100, 15, n)
    
    # Datos con tendencia
    tiempo = np.arange(n)
    datos_tendencia = 50 + 0.5 * tiempo + np.random.normal(0, 5, n)
    
    # Datos correlacionados
    x = np.random.normal(0, 1, n)
    y = 2 * x + np.random.normal(0, 0.5, n)
    
    # Datos categóricos
    categorias = np.random.choice(['A', 'B', 'C'], n)
    
    return pd.DataFrame({
        'Medicion_1': datos_normales,
        'Medicion_2': datos_tendencia,
        'Variable_X': x,
        'Variable_Y': y,
        'Categoria': categorias,
        'Tiempo': tiempo
    })


def ejemplo_analisis_completo():
    """
    Ejemplo completo de análisis estadístico
    """
    print("📊 ANÁLISIS ESTADÍSTICO COMPLETO")
    print("=" * 50)
    
    # Crear analizador
    analizador = AnalisisEstadistico()
    
    # Crear datos de ejemplo
    datos_ejemplo = crear_datos_ejemplo()
    analizador.datos = datos_ejemplo
    
    print(f"Datos de ejemplo creados: {datos_ejemplo.shape}")
    
    # Generar reporte completo
    columnas_numericas = ['Medicion_1', 'Medicion_2', 'Variable_X', 'Variable_Y']
    analizador.generar_reporte_completo(columnas_numericas)
    
    # Análisis específicos
    print(f"\n🔬 ANÁLISIS ESPECÍFICOS:")
    
    # Control de calidad para Medición_1
    print(f"\nControl de Calidad - Medición_1:")
    capacidad = analizador.control_calidad_estadistico(
        'Medicion_1', 
        especificacion_superior=130, 
        especificacion_inferior=70
    )
    if capacidad and 'capacidad' in capacidad:
        print(f"  Cp: {capacidad['capacidad']['cp']:.3f}")
        print(f"  Cpk: {capacidad['capacidad']['cpk']:.3f}")
        print(f"  Interpretación: {capacidad['interpretacion']}")
    
    # Visualización de distribución
    print(f"\n📊 Visualizando distribución de Medición_1...")
    analizador.visualizar_distribucion('Medicion_1')
    
    # Análisis de correlación
    print(f"\n🔗 Visualizando correlaciones...")
    analizador.analisis_correlacion(visualizar=True)


def main():
    """
    Función principal del módulo
    """
    print("📊 SISTEMA DE ANÁLISIS ESTADÍSTICO PARA INGENIERÍA")
    print("=" * 60)
    
    # Ejecutar ejemplo completo
    ejemplo_analisis_completo()
    
    print("\n" + "=" * 60)
    print("✅ Análisis estadístico completado exitosamente!")
    print("\n📚 Funcionalidades incluidas:")
    print("• Estadísticas descriptivas avanzadas")
    print("• Pruebas de normalidad múltiples")
    print("• Análisis de correlación y regresión")
    print("• Control de calidad estadístico")
    print("• Visualizaciones profesionales")
    print("• Reportes automatizados")


if __name__ == "__main__":
    main()
