import streamlit as st
import leafmap.foliumap as leafmap


st.sidebar.title("About")
st.sidebar.info("""
    This map displays catchment interventions within the Mwache dam reservoir.
""")

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.subheader("Mwache Dam Reservoir Intervention Map")

m = leafmap.Map(center=[40, -100], zoom=9)
m.add_basemap("HYBRID")

axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
reservoir_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/main/data/mwachedam_reservoir.geojson"
damterraces_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/MwacheDam_terraces.geojson"
treeareas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/tree_areas.geojson"

m.add_geojson(reservoir_url, layer_name="mwachedam_reservoir")
m.add_geojson(axes_url, layer_name="mwachedam_axes")
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
m.add_geojson(
    treeareas_url,
    layer_name="tree_areas",
    style_function=lambda feature: {
        "fillColor": "darkgreen",
        "color": "darkgreen",
        "fillOpacity": 0.1,
        "weight": 4,
    },
)
# display in Streamlit
m.to_streamlit(height=700)




    