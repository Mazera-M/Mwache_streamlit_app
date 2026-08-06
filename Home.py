import streamlit as st
import leafmap.foliumap as leafmap

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

with st.expander("See source code"):
    with st.echo():
        
# Use raw GitHub URLs so the GeoJSON files can be loaded directly
       m = leafmap.Map(center=[40, -100], zoom=4)
       axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
       wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"

       m.add_geojson(wruas_url, layer_name="mwache_wruas")
       m.add_geojson(axes_url, layer_name="mwachedam_axes")
    
    m.to_streamlit(height=500)        
        
       
