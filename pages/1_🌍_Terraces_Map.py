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

# Load data
all_terraces_df = pd.read_csv("data/all_terraces.csv")

# Filter the terrace records by financial year.
if "financial_year" not in all_terraces_df.columns:
    st.error("The terraces dataset must contain a 'financial_year' column.")
    st.stop()

financial_years = sorted(
    all_terraces_df["financial_year"].dropna().astype(str).unique()
)
selected_financial_year = st.sidebar.selectbox(
    "Filter by financial year", ["All"] + financial_years
)

if selected_financial_year == "All":
    terraces_df = all_terraces_df
else:
    terraces_df = all_terraces_df[
        all_terraces_df["financial_year"].astype(str) == selected_financial_year
    ]

st.caption(f"Showing {len(terraces_df)} terrace records")

m = leafmap.Map(center=[40, -100], zoom=9)
m.add_basemap("HYBRID")

wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"
terraces6_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_6.geojson"
terraces14_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_14.geojson"
damterraces_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/MwacheDam_terraces.geojson"

m.add_geojson(
    wruas_url,
    layer_name="mwache_wruas",
    style_function=lambda feature: {
        "fillColor": "black",
        "color": "black",
        "fillOpacity": 0.1,
        "weight": 2,
    },
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




    