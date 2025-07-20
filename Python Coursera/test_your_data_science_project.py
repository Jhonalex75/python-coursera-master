import pytest
import pandas as pd
from your_data_science_project import clean_data, train_model, predict

# Sample test data
@pytest.fixture
def test_data():
    data = {'feature1': [1, 2, 3, None], 'feature2': ['A', 'B', 'C', 'D']}
    return pd.DataFrame(data)

def test_data_cleaning(test_data):
    """Verify if data cleaning handles missing values correctly."""
    cleaned_data = clean_data(test_data)
    assert cleaned_data['feature1'].isnull().sum() == 0  # Check if missing values are filled

def test_model_predictions():
    """Check if model predictions match expected outcomes."""
    # Creamos un dataset simple
    X = pd.DataFrame({'feature1': [1, 2, 3, 4, 5, 6], 'feature2': [0, 1, 0, 1, 0, 1]})
    y = [0, 1, 0, 1, 0, 1]
    model = train_model(X, y)
    predictions = predict(model, X)
    accuracy = (predictions == y).mean()
    assert accuracy > 0.8  # Set your desired accuracy threshold

def test_model_performance():
    """Evaluate model performance using relevant metrics."""
    from sklearn.metrics import precision_score, recall_score, f1_score

    X = pd.DataFrame({'feature1': [1, 2, 3, 4, 5, 6], 'feature2': [0, 1, 0, 1, 0, 1]})
    y = [0, 1, 0, 1, 0, 1]
    model = train_model(X, y)
    predictions = predict(model, X)

    precision = precision_score(y, predictions)
    recall = recall_score(y, predictions)
    f1 = f1_score(y, predictions)

    assert precision > 0.8
    assert recall > 0.8
    assert f1 > 0.8

# --- Nuevos casos de prueba ---
def test_clean_data_all_nulls():
    df = pd.DataFrame({'feature1': [None, None, None], 'feature2': ['A', 'B', 'C']})
    cleaned = clean_data(df)
    # Si todos son nulos, la media es NaN, así que la columna seguirá siendo NaN
    assert cleaned['feature1'].isnull().all()

def test_clean_data_no_nulls():
    df = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': ['A', 'B', 'C']})
    cleaned = clean_data(df)
    pd.testing.assert_frame_equal(df, cleaned)

def test_model_with_imbalanced_classes():
    X = pd.DataFrame({'feature1': [1, 2, 3, 4, 5, 6], 'feature2': [0, 1, 0, 1, 0, 1]})
    y = [0, 0, 0, 0, 0, 1]  # Muy desbalanceado
    model = train_model(X, y)
    predictions = predict(model, X)
    # No esperamos alta precisión, pero el modelo debe funcionar sin error
    assert len(predictions) == len(y)

def test_predict_on_new_data():
    X_train = pd.DataFrame({'feature1': [1, 2, 3, 4], 'feature2': [0, 1, 0, 1]})
    y_train = [0, 1, 0, 1]
    X_new = pd.DataFrame({'feature1': [5, 6], 'feature2': [0, 1]})
    model = train_model(X_train, y_train)
    predictions = predict(model, X_new)
    assert len(predictions) == len(X_new) 
    
def test_clean_data_all_nulls():
    df = pd.DataFrame({'feature1': [None, None, None], 'feature2': ['A', 'B', 'C']})
    cleaned = clean_data(df)
    # Si todos son nulos, la media es NaN, así que la columna seguirá siendo NaN
    assert cleaned['feature1'].isnull().all()

def test_clean_data_no_nulls():
    df = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': ['A', 'B', 'C']})
    cleaned = clean_data(df)
    pd.testing.assert_frame_equal(df, cleaned)

def test_model_with_imbalanced_classes():
    X = pd.DataFrame({'feature1': [1, 2, 3, 4, 5, 6], 'feature2': [0, 1, 0, 1, 0, 1]})
    y = [0, 0, 0, 0, 0, 1]  # Muy desbalanceado
    model = train_model(X, y)
    predictions = predict(model, X)
    # No esperamos alta precisión, pero el modelo debe funcionar sin error
    assert len(predictions) == len(y)

def test_predict_on_new_data():
    X_train = pd.DataFrame({'feature1': [1, 2, 3, 4], 'feature2': [0, 1, 0, 1]})
    y_train = [0, 1, 0, 1]
    X_new = pd.DataFrame({'feature1': [5, 6], 'feature2': [0, 1]})
    model = train_model(X_train, y_train)
    predictions = predict(model, X_new)
    assert len(predictions) == len(X_new)