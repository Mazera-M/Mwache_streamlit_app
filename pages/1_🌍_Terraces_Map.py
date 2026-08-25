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
all_terraces_df = pd.read_csv("data/all_terraces.csv", encoding="utf-8-sig")
# CSV exports can contain a BOM or extra whitespace in column names.
all_terraces_df.columns = all_terraces_df.columns.astype(str).str.replace("\ufeff", "", regex=False).str.strip()

def display_financial_year_filter():
    financial_year_column = next(
        (column for column in all_terraces_df.columns
         if column.lower().replace(" ", "_") == "financial_year"),
        None,
    )
    if financial_year_column is None:
        st.sidebar.error(
            "The data does not contain a 'Financial_Year' column. "
            f"Available columns: {', '.join(all_terraces_df.columns)}"
        )
        st.stop()

    financial_years = (
        all_terraces_df[financial_year_column]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    if not financial_years:
        st.sidebar.warning("No financial years are available.")
        return None

    return financial_year_column, st.sidebar.selectbox('Financial Year', financial_years)

financial_year_column, selected_financial_year = display_financial_year_filter()
filtered_terraces_df = all_terraces_df[
    all_terraces_df[financial_year_column].astype(str) == selected_financial_year
]
wrua_counts = filtered_terraces_df['WRUA Name'].value_counts().to_dict()
maximum_count = max(wrua_counts.values(), default=0)

def wrua_style(feature):
    wrua_name = feature.get('properties', {}).get('name')
    count = wrua_counts.get(wrua_name, 0)
    ratio = count / maximum_count if maximum_count else 0
    if ratio == 0:
        color = '#f7fbff'
    elif ratio <= 0.25:
        color = '#c6dbef'
    elif ratio <= 0.5:
        color = '#6baed6'
    elif ratio <= 0.75:
        color = '#2171b5'
    else:
        color = '#08306b'
    return {
        'fillColor': color,
        'color': '#555555',
        'weight': 1,
        'fillOpacity': 0.7,
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




    