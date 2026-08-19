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

top_left, top_right = st.columns([1, 2])

with top_left:
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
    st.info("Click on the left sidebar menu to navigate to the different mwache intervention map layers.")

with top_right:
    st.info("Mwache Catchment Location Map.")
    m = leafmap.Map(center=[40, -100], zoom=9)
    m.add_basemap("HYBRID")

    wruas_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwache_wruas.geojson"
    axes_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/refs/heads/main/data/mwachedam_axes.geojson"
    reservoir_url = "https://raw.githubusercontent.com/Mazera-M/Mwache_streamlit_app/main/data/mwachedam_reservoir.geojson"

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
    m.to_streamlit(height=500)

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
interventions_df = pd.read_csv("data/Mwache_Interventions.csv")
beneficiaries_df = pd.read_csv("data/Mwache_Beneficiaries.csv")

interventions_column, beneficiaries_column = st.columns(2)

with interventions_column:
    # Display intervention data
    df = interventions_df

    if "Intervention" in df.columns:
        intervention_options = sorted(df["Intervention"].dropna().unique().tolist())
        selected_interventions = st.multiselect(
            "Choose interventions",
            intervention_options,
            ["Terraces"]
        )

        filtered_df = df[df["Intervention"].isin(selected_interventions)].copy() if selected_interventions else df.iloc[0:0].copy()

        if not filtered_df.empty:
            st.write(f"Showing {len(filtered_df)} records for the selected intervention(s): {', '.join(selected_interventions)}")
            st.dataframe(filtered_df, use_container_width=True)

            if "Intervention" in filtered_df.columns:
                year_columns = ["Baseline", "15/16", "16/17", "17/18", "18/19", "19/20", "20/21", "21/22", "22/23", "23/24", "24/25", "25/26"]
                years_in_data = [col for col in year_columns if col in filtered_df.columns]
            
                if years_in_data:
                    all_years = [col for col in year_columns if col in df.columns]
                    melted_df = filtered_df.melt(id_vars=["Intervention"], value_vars=all_years, var_name="Financial Year", value_name="Hectares")
                    melted_df["Hectares"] = pd.to_numeric(melted_df["Hectares"], errors="coerce")
                    melted_df = melted_df[melted_df["Intervention"] != "Target area"].copy()
                    melted_df = melted_df.dropna(subset=["Hectares"])
                    melted_df["Financial Year"] = pd.Categorical(
                        melted_df["Financial Year"],
                        categories=year_columns,
                        ordered=True,
                    )

                    all_hectares = pd.to_numeric(
                        df[all_years].stack(), errors="coerce"
                    ).dropna()
                    chart = (
                        alt.Chart(melted_df)
                        .mark_rect()
                        .encode(
                            x=alt.X("Intervention:N", title="Intervention"),
                            y=alt.Y("Financial Year:O", title="Financial Year"),
                            color=alt.Color("Hectares:Q", title="Hectares"),
                            tooltip=["Intervention:N", "Financial Year:O", "Hectares:Q"],
                        )
                    )
                    st.altair_chart(chart, use_container_width=True)
        
with beneficiaries_column:
    # select multiple beneficiaries
    beneficiary_column = "Beneficiaries" if "Beneficiaries" in beneficiaries_df.columns else None

    if beneficiary_column:
        beneficiary_options = sorted(
            set(beneficiaries_df[beneficiary_column].dropna().astype(str).unique())
            | {"Direct Beneficiaries SLM", "Indirect Beneficiaries SLM"}
        )
        selected_beneficiaries = st.multiselect(
            "Choose beneficiaries",
            beneficiary_options,
            key="selected_beneficiaries",
        )

        if selected_beneficiaries:
            filtered_beneficiaries = beneficiaries_df[
                beneficiaries_df[beneficiary_column]
                .astype(str)
                .isin(selected_beneficiaries)
            ].copy()
            st.write(
                f"Showing {len(filtered_beneficiaries)} records for the selected beneficiary(ies)."
            )
            st.dataframe(filtered_beneficiaries, use_container_width=True)
    else:
        st.error("The beneficiaries CSV does not contain a beneficiary name column.")
    
