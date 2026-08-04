import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
 This multipage app displays maps and dashboards for the various mwache catchment restoration interventions (https://www.kwscrp.org/mwache-dam-project-watershed-management).
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Mwache Catchment Restoration")

st.markdown("""
    This multipage app displays maps and dashboards for the various mwache catchment restoration interventions (https://www.kwscrp.org/mwache-dam-project-watershed-management).
    """)

st.subheader("Background")

markdown = """
Mwache catchment covers an area of 3647 km² and stretches across coordinates 38.6327 west,
39.5416 East, and -3.53513 North, -4.10244 South and stretches across Taita Taveta, Kwale, and
Kilifi Counties.
This Catchment which is the source of water for the Mwache dam has undergone significant degradation

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
