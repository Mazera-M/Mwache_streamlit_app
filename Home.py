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
1. Sustainable Land Management (SLM) techniques; Terracing and soil stabilization, Gabion Construction, Afforestation
2. Livelihood Enhancement; Support for WRUAs, Farmer Field Schools (FFS) and Farmer Led Irrigation Development (FLID)

""")

st.info("Click on the left sidebar menu to navigate to the different map layers.")

alt.themes.enable("dark")

# Customize the sidebar
st.sidebar.title("About")
st.sidebar.info("""
    This multipage app displays maps and dashboards for the various mwache catchment restoration interventions 
    (https://www.kwscrp.org/mwache-dam-project-watershed-management).
    
   """)

logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

#######################
# Load data

df = pd.read_csv("data/Mwache_Interventions.csv")

if "Intervention" in df.columns:
    intervention_options = sorted(df["Intervention"].dropna().unique().tolist())
    selected_interventions = st.multiselect(
        "Choose interventions",
        intervention_options,
        ["Target area", "Terraces"],
    )

    filtered_df = df[df["Intervention"].isin(selected_interventions)].copy() if selected_interventions else df.iloc[0:0].copy()

    if not filtered_df.empty:
        st.write(f"Showing {len(filtered_df)} records for the selected intervention(s): {', '.join(selected_interventions)}")
        st.dataframe(filtered_df, use_container_width=True)

        if "Intervention" in filtered_df.columns:
            # Display bar chart for selected interventions
            year_columns = ["Baseline", "15/16", "16/17", "17/18", "18/19", "19/20", "20/21", "21/22", "22/23", "23/24", "24/25", "25/26"]
            years_in_data = [col for col in year_columns if col in filtered_df.columns]
            
            if years_in_data:
                melted_df = filtered_df.melt(id_vars=["Intervention"], value_vars=years_in_data, var_name="Financial Year", value_name="Hectares")
                chart = alt.Chart(melted_df).mark_bar().encode(
                    x=alt.X("Intervention:N", title="Intervention Type"),
                    y=alt.Y("Hectares:Q", title="Hectares Restored"),
                    color="Financial Year:N"
                ).properties(width=700, height=400)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("Financial year columns not found in the data.")
    else:
        st.info("No intervention selected or no matching records found.")
else:
    st.error("The CSV file does not contain an 'Intervention' column.")  