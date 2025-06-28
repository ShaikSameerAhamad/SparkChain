import streamlit as st
import pandas as pd
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="SparkChain",
    page_icon="🔗"
)

# --- Title of the Application ---
st.title('SparkChain: Walmart Supply Chain Control Tower')

# --- Pathing ---
# This makes our file paths work robustly, regardless of where the script is run
# __file__ is the path to the current script (dashboard.py)
# .parent gives us the directory of the script (the 'app' folder)
# .parent again goes up one more level to the project root ('SparkChain/')
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "locations.csv"

# --- Data Loading ---
@st.cache_data
def load_data(filepath):
    """Loads data from a specified CSV file."""
    if filepath.exists():
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=['LocationName', 'LocationType', 'Latitude', 'Longitude'])

# Load the location data
locations_df = load_data(DATA_PATH)

# --- Main Dashboard Display ---
st.header('Live Supply Chain Map')

# Check if the DataFrame is empty. If so, show an error.
if locations_df.empty:
    st.error(f"Error: Could not load location data from the path: {DATA_PATH}. Please ensure the file exists.")
else:
    # Display the map using the 'latitude' and 'longitude' columns
    st.map(locations_df, latitude='Latitude', longitude='Longitude')