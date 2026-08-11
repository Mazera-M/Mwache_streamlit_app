import streamlit as st
import leafmap.foliumap as leafmap
import folium

st.set_page_config(layout="wide")

# Customize the sidebar

st.sidebar.title("About")
st.sidebar.info("""
    This multipage app displays maps and dashboards for the various mwache catchment restoration interventions 
    (https://www.kwscrp.org/mwache-dam-project-watershed-management).
    
   """)

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Mwache Catchment Restoration")

st.subheader("Background")

st.markdown("""
Mwache catchment covers an area of 3647 km² and stretches across coordinates 38.6327 west,
39.5416 East, and -3.53513 North, -4.10244 South and stretches across Taita Taveta, Kwale, and
Kilifi Counties.
This Catchment which is the source of water for the Mwache dam has undergone significant degradation over the years 
necessitating the need for restoration interventions. 

Key Watershed interventions include:
1. Sustainable Land Management (SLM) techniques; Terracing and soil stabilization, Gabion Construction
2. Livelihood Enhancement; Support for WRUAs, Farmer Field Schools (FFS) and Farmer Led Irrigation Development (FLID)

""")

st.info("Click on the left sidebar menu to navigate to the different map layers.")

st.subheader("Mwache Catchment Location Map")

# Use raw GitHub URLs so the GeoJSON files can be loaded directly
m = leafmap.Map(center=[40, -100], zoom=4)
axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
reservoir_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/main/data/mwachedam_reservoir.geojson"
wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"

m.add_geojson(
    wruas_url,
    layer_name="mwache_wruas",
    style_function=lambda feature: {
        "fillColor": "#ffffff00",
        "color": "black",
        "weight": 2,
    },
)

# Add axes as GeoJSON but render point features as black circle icons
m.add_geojson(
    axes_url,
    layer_name="mwachedam_axes",
    point_to_layer=lambda feature, latlng: folium.CircleMarker(
        location=latlng,
        radius=6,
        color="black",
        fill=True,
        fill_color="black",
    ),
)

m.add_geojson(reservoir_url, layer_name="mwachedam_reservoir")

m.to_streamlit(height=700)

with st.expander("See source code"):
    st.code("""
# Use raw GitHub URLs so the GeoJSON files can be loaded directly
m = leafmap.Map(center=[40, -100], zoom=4)
axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"

m.add_geojson(
    wruas_url,
    layer_name="mwache_wruas",
    style_function=lambda feature: {
        "fillColor": "#ffffff00",
        "color": "black",
        "weight": 2,
    },
)
m.add_geojson(axes_url, layer_name="mwachedam_axes")
m.to_streamlit(height=700)
    """, language="python")        
        
       
