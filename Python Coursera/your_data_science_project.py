import pandas as pd
from sklearn.linear_model import LogisticRegression

def clean_data(df):
    # Rellena los valores faltantes con la media de la columna (solo para numéricos)
    df = df.copy()
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].fillna(df[col].mean())
    return df

def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    return model

def predict(model, X):
    return model.predict(X) 