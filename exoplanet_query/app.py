import streamlit as st
import plotly.express as px
import numpy as np
from database.data_loader import get_exoplanet_data
from controller.controller import query_exoplanets
from plot import method_radius_boxplots, radius_vs_mass_plot, temperature_vs_distance_plot, discovery_year_bar_chart, distance_histogram, method_radius_boxplots

# Friendly labels for query filters
QUERY_LABELS = {
    "pl_name": "Planet Name",
    "disc_year": "Discovery Year",
    "discoverymethod": "Discovery Method",
    "hostname": "Host Star",
    "disc_facility": "Discovery Facility",
    "sy_dist": "Distance from Earth (pc)",
    "pl_rade": "Planet Radius (R⊕)",
    "pl_masse": "Planet Mass (M⊕)",
    "pl_orbper": "Orbital Period (days)",
    "st_rad": "Star Radius (R☉)",
    "pl_eqt": "Equilibrium Temperature (K)"
}

# -------------------------------
# 🚀 Page Setup
# -------------------------------
st.set_page_config(
    page_title="NASA Exoplanet Query App",
    layout="wide"
)

st.title("🔭 NASA Exoplanet Query App")

# -------------------------------
# 🚀 1. Load Data
# -------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    return get_exoplanet_data(save_to_db=False)

data = load_data()


# -------------------------------
# 🚀 2. TABS (Query + Plot)
# -------------------------------
tab_plot, tab_query = st.tabs(["📊 Plot", "🔍 Query"])


# ================================================================
# 📊 TAB 1 — PLANET RADIUS vs MASS (CURATED VISUAL)
# ================================================================
with tab_plot:

    st.header("📊 Planet Radius vs Planet Mass")

    st.markdown("""
    This classic exoplanet diagram reveals how planets group into different families:

    • **Rocky super-Earths** tend to have low mass and small radii  
    • **Mini-Neptunes** form a noticeable cluster with larger radii but not too high mass  
    • **Gas giants** dominate the upper-right area with huge radii and masses  
    • A subtle **radius gap** appears around ~1.5–2 R⊕  

    This is one of the most important charts in exoplanet science!
    """)

    # -------------------------------
    # Clean DF for plotting
    # -------------------------------
    plot_df = data[["pl_name", "pl_rade", "pl_masse"]].dropna()

    # Remove impossible zero values
    plot_df = plot_df[(plot_df["pl_rade"] > 0) & (plot_df["pl_masse"] > 0)]

    st.write(f"**Displaying {len(plot_df):,} planets**")

    fig = radius_vs_mass_plot(data, trendline=True)
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig, use_container_width=True)

    # ================================================================
    # 🌡️ TEMPERATURE vs ORBITAL DISTANCE SECTION
    # ================================================================
    st.header("🌡️ Orbital Distance vs Temperature")

    st.markdown("""
    This plot illustrates how a planet's temperature depends on how far it orbits from its star:

    • **Hot Jupiters** roast at thousands of degrees because they orbit extremely close  
    • **Warm Neptunes** sit in the middle regions  
    • **Cool giants** orbit far out, receiving little starlight  
    • Most *habitable-zone-like* planets fall into a narrow mid-temperature range

    This helps us understand where different kinds of worlds tend to form and survive.
    """)

    fig2 = temperature_vs_distance_plot(data)
    fig2.update_xaxes(fixedrange=True)
    fig2.update_yaxes(fixedrange=True)
    st.plotly_chart(fig2, use_container_width=True)

    # ================================================================
    #  DISCOVERY YEAR BAR CHART
    # ================================================================

    st.header("📅 Discovery Year")

    st.markdown("""
    This plot illustrates how a planet's temperature depends on how far it orbits from its star:

    • Before 2000, only a handful of planets were known    
    • Kepler (2010-2013) discovered *thousands*, causing the iconic spike
    • TESS (2018-present) continues adding new nearby planets              
    • Improved radial velocity and transit techniques increased discovery rates 
    """)

    fig3 = discovery_year_bar_chart(data)
    st.plotly_chart(fig3, use_container_width=True)

    # ================================================================
    #  DISTANCE FROM EARTH HISTOGRAM (LOG SCALE VERSION)
    # ================================================================
    st.header("📏 Distance from Earth")

    st.markdown("""
    This histogram shows how far the known exoplanets are from us.

    • Only a small number of planets are within 50-100 light-years  
    • Most known worlds are **hundreds** of light-years away  
    • Kepler surveyed a region roughly 1,000-3,000 light-years from Earth  
    • Telescopes discover whichever stars they *look at*; not necessarily the closest ones  

    This tells us that our exoplanet catalog is shaped more by **where we looked**  
    than by where planets actually are.
    """)

    # ------------------------------
    # Clean + transform data
    # ------------------------------
    clean = data[["sy_dist"]].dropna()
    clean = clean[clean["sy_dist"] > 0]  # remove invalid 0 values

    # log-transform distance
    clean["log_dist"] = np.log10(clean["sy_dist"])

    # ------------------------------
    # Create histogram
    # ------------------------------
    fig4 = px.histogram(
        clean,
        x="log_dist",
        nbins=60,
        title="Distance From Earth (log-scaled)",
        labels={
            "log_dist": "log₁₀(Distance in parsecs)",
        },
        template="plotly_dark"
    )

    fig4.update_traces(marker_color="#66C2FF", opacity=0.75)
    fig4.update_layout(
        xaxis_title="log₁₀(Distance [pc])",
        yaxis_title="Number of Planets",
    )

    # Disable zooming/panning
    fig4.update_xaxes(fixedrange=True)
    fig4.update_yaxes(fixedrange=True)

    # Display (mobile-friendly)
    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "doubleClick": False,
            "displayModeBar": False,
            "staticPlot": False,
        }
    )

    # -------------------------------------------------
    # DISCOVERY METHOD COMPARISON (BOX PLOTS)
    # -------------------------------------------------

    st.header("🔍 Discovery Method Comparison")

    st.markdown("""
    This section compares how different detection techniques influence  
    **which types of planets we’re most likely to find.**

    Each method has its own strengths — and its own biases:

    • **Transit** finds tons of small and medium planets because it detects tiny dips in starlight  
    • **Radial Velocity** excels at detecting massive planets tugging on their stars  
    • **Imaging** can spot huge, young, glowing planets far from their stars  
    • **Timing methods** detect planets in special, precise situations  
    • Rare or niche techniques are grouped as **Other**  

    Because every method favors certain planets, their radius distributions  
    look *wildly* different.

    This makes discovery methods one of the biggest factors shaping our exoplanet catalog.
    """)

    figs = method_radius_boxplots(data)

    st.subheader("Planet Radius by Discovery Method (Zoomed)")
    st.plotly_chart(figs["zoom"], use_container_width=True)

    st.subheader("Planet Radius by Discovery Method (Full Range)")
    st.plotly_chart(figs["full"], use_container_width=True)

# ================================================================
# 🔍 TAB 2 — QUERY PAGE
# ================================================================
with tab_query:

    st.header("🔍 Filter Options")

    # --- Filters inside the tab ---
    col1, col2 = st.columns(2)

    with col1:
        planet_name = st.text_input(QUERY_LABELS["pl_name"])
        method = st.selectbox(
            QUERY_LABELS["discoverymethod"],
            ["Any", *sorted(x for x in data["discoverymethod"].dropna().unique())]
        )
        facility = st.selectbox(
            QUERY_LABELS["disc_facility"],
            ["Any", *sorted(x for x in data["disc_facility"].dropna().unique())]
        )

    with col2:
        discovery_year = st.selectbox(
            QUERY_LABELS["disc_year"],
            ["Any", *sorted(x for x in data["disc_year"].dropna().unique())]
        )
        host_name = st.text_input(QUERY_LABELS["hostname"])

    # --- Run Query Button ---
    if st.button("Run Query"):
        filtered = query_exoplanets(
            data,
            name=planet_name,
            year=None if discovery_year == "Any" else discovery_year,
            method=None if method == "Any" else method,
            host=host_name,
            facility=None if facility == "Any" else facility,
        )

        renamed = filtered.rename(columns=QUERY_LABELS)

        st.subheader("Query Results")
        st.dataframe(renamed, use_container_width=True)
        