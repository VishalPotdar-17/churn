import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style='whitegrid')

def perform_eda(file_path):
    print("Loading data for EDA...")
    df = pd.read_csv(file_path)
    
    # 1. Churn Distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Churn', data=df)
    plt.title('Distribution of Churn')
    plt.savefig('plots/churn_distribution.png')
    plt.close()
    
    # 2. Numerical Features Distribution
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    plt.figure(figsize=(15, 5))
    for i, col in enumerate(num_cols):
        plt.subplot(1, 3, i+1)
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f'Distribution of {col}')
    plt.tight_layout()
    plt.savefig('plots/numerical_distributions.png')
    plt.close()
    
    # 3. Correlation Matrix (Numerical)
    plt.figure(figsize=(8, 6))
    # Select only numeric columns for correlation matrix
    numeric_df = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.savefig('plots/correlation_matrix.png')
    plt.close()
    
    # 4. Categorical Features vs Churn
    cat_cols = ['Contract', 'InternetService', 'PaymentMethod']
    plt.figure(figsize=(15, 5))
    for i, col in enumerate(cat_cols):
        plt.subplot(1, 3, i+1)
        sns.countplot(x=col, hue='Churn', data=df)
        plt.title(f'{col} vs Churn')
        plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('plots/categorical_vs_churn.png')
    plt.close()

    print("EDA plots saved in 'plots/' directory.")

if __name__ == "__main__":
    if os.path.exists('data/telecom_churn.csv'):
        perform_eda('data/telecom_churn.csv')
    else:
        print("Data file not found!")
