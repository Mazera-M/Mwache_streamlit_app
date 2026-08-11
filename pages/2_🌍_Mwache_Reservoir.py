import streamlit as st
import leafmap.foliumap as leafmap


st.sidebar.title("About")
st.sidebar.info("""
    This map displays all the catchment interventions within the Mwache dam reservoir.
""")

logo = "https://favpng.com/png_view/terraced-fields-colorful-terraced-farmlands-on-hillside-png/VNrebwaH"
st.sidebar.image(logo)


st.subheader("Mwache Dam ReservoirInterventions Map")

m = leafmap.Map(center=[40, -100], zoom=9)
m.add_basemap("HYBRID")

axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
reservoir_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/main/data/mwachedam_reservoir.geojson"


m.add_geojson(reservoir_url, layer_name="mwachedam_reservoir")
m.add_geojson(axes_url, layer_name="mwachedam_axes")


# display in Streamlit
m.to_streamlit(height=700)




    