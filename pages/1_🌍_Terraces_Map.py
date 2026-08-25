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

# Display totals for conserved terrace length and area.
def find_column(candidates):
    normalized_columns = {
        column.lower().replace("_", " ").replace("-", " "): column
        for column in all_terraces_df.columns
    }
    for candidate in candidates:
        for normalized, original in normalized_columns.items():
            if candidate in normalized:
                return original
    return None


km_column = find_column(["km", "kilometre", "kilometer", "length"])
hectare_column = find_column(["hectare", "hectares", "ha", "area"])

if km_column and hectare_column:
    totals_df = pd.DataFrame(
        {
            "Measure": ["Total conserved length (km)", "Total conserved area (ha)"],
            "Total": [
                pd.to_numeric(all_terraces_df[km_column], errors="coerce").sum(),
                pd.to_numeric(all_terraces_df[hectare_column], errors="coerce").sum(),
            ],
        }
    )
    st.subheader("Hectares Conserved")
    conservation_chart = alt.Chart(totals_df).mark_bar().encode(
        x=alt.X("Total:Q", title="Total"),
        y=alt.Y("Measure:N", sort="-x", title=None),
        color=alt.Color("Measure:N", legend=None),
        tooltip=[alt.Tooltip("Total:Q", format=",.2f")],
    )
    st.altair_chart(conservation_chart, use_container_width=True)



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
        "fillOpacity": 0.1,
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




    