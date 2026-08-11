import streamlit as st
import leafmap.foliumap as leafmap
import folium
import branca

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
    wruas_url,
    layer_name="mwache_wruas",
    style_function=lambda feature: {
        "fillColor": "#ffffff00",
        "color": "black",
        "weight": 2,
    },
)

# add simple HTML legend compatible with Streamlit display
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 10px; width: 160px; height: 110px; 
     background-color: white; z-index:9999; padding: 10px; 
     border:2px solid grey; border-radius:6px;">
  <h4 style="margin:0 0 6px 0; font-size:14px;">Legend</h4>
  <div><span style="display:inline-block;width:12px;height:12px;background:purple;margin-right:6px;"></span>Terraces (6m)</div>
  <div style="margin-top:6px;"><span style="display:inline-block;width:12px;height:12px;background:brown;margin-right:6px;"></span>Terraces (14m)</div>
  <div style="margin-top:6px;"><span style="display:inline-block;width:12px;height:12px;border:2px solid black;margin-right:6px;vertical-align:middle;"></span>WRUAs</div>
</div>
'''

# attach legend to the underlying folium map
# Use branca.Html to ensure the HTML is added correctly to the folium root
try:
    legend = branca.element.Html(legend_html, script=True)
    m.folium_map.get_root().html.add_child(legend)
except Exception:
    # fallback: try adding via folium Element
    try:
        m.folium_map.get_root().html.add_child(folium.Element(legend_html))
    except Exception:
        m.add_child(folium.Element(legend_html))
# display in Streamlit
m.to_streamlit(height=700)




    