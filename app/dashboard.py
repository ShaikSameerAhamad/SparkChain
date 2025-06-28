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
PROJECT_ROOT = Path(__file__).parent.parent
LOCATIONS_PATH = PROJECT_ROOT / "data" / "locations.csv"
INVENTORY_PATH = PROJECT_ROOT / "data" / "inventory.csv"

# --- Data Loading ---
@st.cache_data
def load_data(filepath):
    if filepath.exists():
        return pd.read_csv(filepath)
    return None

locations_df = load_data(LOCATIONS_PATH)
inventory_df = load_data(INVENTORY_PATH)

# --- Sidebar for User Input ---
st.sidebar.header('Location Selector')
# Create a dropdown menu with location names. Prepend a 'Select a Location' option.
location_list = ["Select a Location"] + locations_df["LocationName"].unique().tolist()
selected_location = st.sidebar.selectbox("Choose a location to view details:", location_list)


# --- Main Dashboard Display ---
col1, col2 = st.columns([2, 1])  # Make the first column twice as wide as the second

with col1:
    st.header('Live Supply Chain Map')
    st.map(locations_df, latitude='Latitude', longitude='Longitude')

with col2:
    st.header('Inventory Levels')
    if selected_location != "Select a Location" and inventory_df is not None:
        # Filter the inventory data for the selected location
        location_inventory_df = inventory_df[inventory_df["LocationName"] == selected_location]

        # Display the filtered data in a table
        st.dataframe(location_inventory_df)
    else:
        st.info("Select a location from the sidebar to see its inventory.")