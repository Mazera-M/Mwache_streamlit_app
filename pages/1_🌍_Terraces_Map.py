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

st.markdown("**Financial Year**")
st.dataframe(all_terraces_df[["financial_year"]], use_container_width=True)

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
        "fillOpacity": 0.5,
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




    