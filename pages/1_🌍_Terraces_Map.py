import streamlit as st
import leafmap.foliumap as leafmap

st.sidebar.title("About")
st.sidebar.info("""
    This map displays the location of terraces within the Mwache catchment.
""")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.subheader("Terraces Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:

    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)
    m.to_streamlit(height=700)

wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"


m.add_geojson(wruas_url, layer_name="mwache_wruas")


    