import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def train_models(data_path):
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Drop customerID
    df = df.drop('customerID', axis=1)
    
    # Separate features and target
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    # Encode target
    le = LabelEncoder()
    y = le.fit_transform(y) # Yes -> 1, No -> 0
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
    
    print(f"Categorical columns: {list(categorical_cols)}")
    print(f"Numerical columns: {list(numerical_cols)}")
    
    # Preprocessing for numerical data
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    # Preprocessing for categorical data
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_score = 0
    best_model_name = ""
    
    results = {}
    
    print("\nTraining models...")
    for name, model in models.items():
        # Create pipeline
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', model)])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        score = accuracy_score(y_test, y_pred)
        results[name] = score
        
        print(f"\n{name} Accuracy: {score:.4f}")
        print(classification_report(y_test, y_pred))
        
        if score > best_score:
            best_score = score
            best_model = clf
            best_model_name = name
            
    print(f"\nBest model: {best_model_name} with accuracy: {best_score:.4f}")
    
    # Save the best model
    model_path = 'models/best_churn_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Best model saved to {model_path}")

    # Also save the label encoder logic if needed, but for binary classification (0/1) it's usually standard.
    # However, we might want to know what 1 means. 1 is usually the second class in sorted order (No, Yes -> Yes=1).
    # Let's verify and print it.
    print(f"Target classes: {le.classes_}")
    
if __name__ == "__main__":
    if os.path.exists('data/telecom_churn.csv'):
        train_models('data/telecom_churn.csv')
    else:
        print("Data file not found!")
