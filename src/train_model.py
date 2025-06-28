# This script is located in src/train_model.py
import pandas as pd
from prophet import Prophet
import joblib
from pathlib import Path
import warnings

# Ignore warnings to keep the output clean
warnings.filterwarnings('ignore')

print("--- Starting Model Training Script ---")

# --- Pathing ---
# When we run this script from the main project folder, Path.cwd() gives us the project root
PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / 'data'
MODELS_DIR = PROJECT_ROOT / 'models'

try:
    # --- Data Loading and Preparation ---
    print("Loading datasets...")
    train_df = pd.read_csv(DATA_DIR / 'train.csv')
    features_df = pd.read_csv(DATA_DIR / 'features.csv')
    stores_df = pd.read_csv(DATA_DIR / 'stores.csv')

    df = train_df.merge(features_df, on=['Store', 'Date', 'IsHoliday'], how='inner')
    df = df.merge(stores_df, on='Store', how='inner')
    print("Datasets loaded and merged.")

    # --- Data Cleaning and Feature Engineering ---
    df['Date'] = pd.to_datetime(df['Date'])
    df_filtered = df[(df['Store'] == 1) & (df['Dept'] == 1)].copy()
    print(f"Filtered data for Store 1, Dept 1. We have {len(df_filtered)} data points.")

    df_prophet = df_filtered[['Date', 'Weekly_Sales']].rename(columns={'Date': 'ds', 'Weekly_Sales': 'y'})

    # --- Model Training ---
    print("Training Prophet model... This will take a minute or two.")
    model = Prophet()
    model.fit(df_prophet)
    print("Model training complete.")

    # --- Save the Model ---
    MODELS_DIR.mkdir(exist_ok=True)
    model_path = MODELS_DIR / 'prophet_model.pkl'
    joblib.dump(model, model_path)
    print(f"\nSUCCESS: Model has been saved to: {model_path}")

except FileNotFoundError as e:
    print(f"\nERROR: Could not find a data file. {e}. Make sure the Kaggle CSV files are in the 'data' directory.")

print("--- Script Finished ---")