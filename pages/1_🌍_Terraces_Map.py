import streamlit as st 
import leafmap.foliumap as leafmap
import geopandas as gpd
import folium


st.sidebar.title("About")
st.sidebar.info("""
    This map displays the location of terraces within the Mwache catchment.
""")

logo = "https://favpng.com/png_view/terraced-fields-colorful-terraced-farmlands-on-hillside-png/VNrebwaH"
st.sidebar.image(logo)


st.subheader("Terraces Map")

m = leafmap.Map(center=[40, -100], zoom=9)
m.add_basemap("HYBRID")

wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"
terraces6_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_6.geojson"
terraces14_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_14.geojson"
damterraces_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/MwacheDam_terraces.geojson"

# 1) Load geojson
gdf = gpd.read_file("data/mwache_wruas.geojson")
# 2) Pick the property/column to use for the label.
# Inspect columns if you're not sure what property contains the WRUA name:
# st.write("GeoDataFrame columns:", list(gdf.columns))
# Set this to the property/column that you want to show as label
label_field = "WRUA_NAME"  # <-- change this to the correct property, e.g. "WRUA_NAME" or similar

# style function (optional) — customize color/opacity as needed
def style_function(feature):
    return {
        "fillColor": "#ffffff00",
        "color": "#ffffff00",
        "weight": 1,
        "fillOpacity": 0.3,
    }

# Build a folium.GeoJson with a tooltip and NO popup
tooltip = folium.GeoJsonTooltip(
    fields=[label_field],
    aliases=[label_field.capitalize()],
    localize=True,
    sticky=False,        # False = tooltip follows mouse, True = sticky on hover
)

geojson = folium.GeoJson(
    data=gdf.__geo_interface__,  # GeoJSON mapping
    name="WRUAs",
    style_function=style_function,
    tooltip=tooltip,
    popup=None,  # ensure no popup is created
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




    