import streamlit as st 
import pandas as pd
import altair as alt
import plotly.express as px
import leafmap.foliumap as leafmap

st.sidebar.title("About")
st.sidebar.info("""
    This map displays the location of terraces within the Mwache catchment.
""")

logo = "https://favpng.com/png_view/terraced-fields-colorful-terraced-farmlands-on-hillside-png/VNrebwaH"
st.sidebar.image(logo)

st.subheader("Terraces Map")

m = leafmap.Map(center=[40, -100], zoom=9)
m.add_basemap("HYBRID")

# Load data
all_terraces_df = pd.read_csv("data/all_terraces.csv")

def display_financial_year_filter():
    financial_years = all_terraces_df['Financial_Year'].unique()
    return st.sidebar.selectbox('Financial Year', financial_years)

selected_financial_year = display_financial_year_filter()
filtered_terraces = all_terraces_df[
    all_terraces_df['Financial_Year'] == selected_financial_year
]

def normalise(value):
    return str(value).strip().casefold()

# Collect WRUA names from the filtered records.  This supports CSV columns
# such as WRUA, WRUA_Name, or WRUA Name without requiring a fixed schema.
wrua_columns = [
    column for column in filtered_terraces.columns
    if 'wrua' in str(column).casefold()
]
filtered_wruas = {
    normalise(value)
    for column in wrua_columns
    for value in filtered_terraces[column].dropna()
}


def wrua_style(feature):
    properties = feature.get('properties', {})
    matched = any(
        normalise(value) in filtered_wruas
        for key, value in properties.items()
        if 'wrua' in str(key).casefold()
    )
    return {
        'fillColor': '#00ff00' if matched else '#ffffff00',
        'color': '#008000' if matched else 'black',
        'weight': 4 if matched else 2,
        'fillOpacity': 0.45 if matched else 0,
    }

wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"
terraces6_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_6.geojson"
terraces14_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_14.geojson"
damterraces_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/MwacheDam_terraces.geojson"

m.add_geojson(
    wruas_url,
    layer_name="mwache_wruas",
    style_function=wrua_style,
)

m.add_geojson(
    terraces6_url,
    layer_name="mwacheterraces_6",
    style_function=lambda feature: {
        "fillColor": "purple",
        "color": "purple",
        "weight": 2,
    },
)

m.add_geojson(
    terraces14_url,
    layer_name="mwacheterraces_14",
    style_function=lambda feature: {
        "fillColor": "brown",
        "color": "brown",
        "weight": 2,
    },
)

m.add_geojson(
    damterraces_url,
    layer_name="mwachedam_terraces",
    style_function=lambda feature: {
        "fillColor": "#ffc0cb",
        "color": "#ffc0cb",
        "fillOpacity": 0.6,
        "weight": 2,
    },
)
# display in Streamlit
m.to_streamlit(height=700)




    