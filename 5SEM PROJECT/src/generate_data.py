import pandas as pd
import numpy as np
import random

def generate_telecom_data(n_samples=1000):
    np.random.seed(42)
    random.seed(42)

    data = {
        'customerID': [f'{random.randint(1000,9999)}-{random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")*5}' for _ in range(n_samples)],
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'SeniorCitizen': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'Partner': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['Yes', 'No'], n_samples),
        'tenure': np.random.randint(1, 73, n_samples),
        'PhoneService': np.random.choice(['Yes', 'No'], n_samples, p=[0.9, 0.1]),
        'MultipleLines': np.random.choice(['Yes', 'No', 'No phone service'], n_samples),
        'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
        'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_samples),
        'MonthlyCharges': np.random.uniform(18.25, 118.75, n_samples).round(2)
    }

    df = pd.DataFrame(data)

    # Calculate TotalCharges (approximate based on tenure and monthly charges with some noise)
    df['TotalCharges'] = df['tenure'] * df['MonthlyCharges'] + np.random.normal(0, 10, n_samples)
    df['TotalCharges'] = df['TotalCharges'].abs().round(2) # Ensure positive

    # Generate Churn based on some logic to make it learnable
    # Higher probability of churn if:
    # - Month-to-month contract
    # - Fiber optic internet
    # - Low tenure
    # - High monthly charges
    
    churn_prob = np.zeros(n_samples)
    churn_prob += np.where(df['Contract'] == 'Month-to-month', 0.4, 0.05)
    churn_prob += np.where(df['InternetService'] == 'Fiber optic', 0.2, 0.0)
    churn_prob += np.where(df['tenure'] < 12, 0.2, -0.1)
    churn_prob += np.where(df['MonthlyCharges'] > 70, 0.1, 0.0)
    
    # Clip probabilities to [0, 1]
    churn_prob = np.clip(churn_prob, 0, 1)
    
    df['Churn'] = [np.random.choice(['Yes', 'No'], p=[p, 1-p]) for p in churn_prob]

    return df

if __name__ == "__main__":
    print("Generating synthetic telecom churn data...")
    df = generate_telecom_data(3000)
    output_path = 'data/telecom_churn.csv'
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    print(df.head())
