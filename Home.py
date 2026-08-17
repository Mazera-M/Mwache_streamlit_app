#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import leafmap.foliumap as leafmap

#######################
# Page configuration
st.set_page_config(
    page_title="Mwache Catchment Dashboard",
    layout="wide",
)

st.subheader("Mwache Catchment Restoration")

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

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#######################
# Load data
df_ = pd.read_csv('data/Mwache_Interventions.csv')
# Use raw GitHub URLs so the GeoJSON files can be loaded directly
axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
reservoir_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/main/data/mwachedam_reservoir.geojson"
wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"

m = leafmap.Map(center=[40, -100], zoom=4)     
# Customize the sidebar
st.sidebar.title("About")
st.sidebar.info("""
    This multipage app displays maps and dashboards for the various mwache catchment restoration interventions 
    (https://www.kwscrp.org/mwache-dam-project-watershed-management).
    
   """)

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

#######################
# Plots
m.add_geojson(reservoir_url, layer_name="mwachedam_reservoir")
m.add_geojson(axes_url, layer_name="mwachedam_axes")
m.add_geojson(
    wruas_url,
    layer_name="mwache_wruas",
    style_function=lambda feature: {
        "fillColor": "#ffffff00",
        "color": "black",
        "weight": 2,
    },
)

m.to_streamlit(height=700)

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Hectares", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="Interventions", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# Calculation year-over-year hectares cumulation for each intervention
df_['Cumulative_Hectares'] = df_.groupby('Intervention')['Hectares'].cumsum()

#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Total Hectares by Intervention')

    # Sum all hectare-based columns for each intervention
    ha_columns = [col for col in df_.columns if 'ha' in col.lower()]
    if not ha_columns:
        ha_columns = ['Hectares']

    for col_name in ha_columns:
        df_[col_name] = pd.to_numeric(df_[col_name].astype(str).str.replace(',', '', regex=False), errors='coerce')

    intervention_totals = (
        df_.groupby('Intervention', as_index=False)[ha_columns]
        .sum()
        .fillna(0)
    )
    st.dataframe(intervention_totals, use_container_width=True)

 