import streamlit as st
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

wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"
terraces6_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_6.geojson"
terraces14_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwacheterraces_14.geojson"

m.add_geojson(wruas_url, layer_name="mwache_wruas")
m.add_geojson(terraces6_url, layer_name="mwacheterraces_6")
m.add_geojson(terraces14_url, layer_name="mwacheterraces_14")

# display in Streamlit
m.to_streamlit(height=700)




    