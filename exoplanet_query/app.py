import streamlit as st
from database.data_loader import get_exoplanet_data
from controller.controller import query_exoplanets
from plot import build_plot

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
tab_query, tab_plot = st.tabs(["🔍 Query", "📊 Plot"])


# ================================================================
# 🔍 TAB 1 — QUERY PAGE
# ================================================================
with tab_query:

    st.sidebar.header("Filter Options")

    planet_name = st.sidebar.text_input("Planet name:")
    discovery_year = st.sidebar.selectbox(
        "Discovery year:", 
        ["Any", *sorted(x for x in data["disc_year"].dropna().unique())]
    )

    method = st.sidebar.selectbox(
        "Discovery method:", 
        ["Any", *sorted(x for x in data["discoverymethod"].dropna().unique())]
    )

    host_name = st.sidebar.text_input("Host star:")

    facility = st.sidebar.selectbox(
        "Discovery facility:",
        ["Any", *sorted(x for x in data["disc_facility"].dropna().unique())]
    )

    if st.sidebar.button("Run Query"):

        filtered = query_exoplanets(
            data,
            name=planet_name,
            year=None if discovery_year == "Any" else discovery_year,
            method=None if method == "Any" else method,
            host=host_name,
            facility=None if facility == "Any" else facility,
        )

        st.subheader("Query Results")
        st.dataframe(filtered, use_container_width=True)


# ================================================================
# 📊 TAB 2 — PLOT PAGE
# ================================================================
with tab_plot:

    st.header("📊 Exoplanet Data Visualization")

    # -------------------------------
    # Axis selectors
    # -------------------------------
    numeric_cols = {
        "sy_dist": "Distance from Earth",
        "pl_rade": "Planet Radius",
        "pl_masse": "Planet Mass",
        "pl_orbper": "Orbital Period",
        "st_rad": "Star Radius",
        "pl_eqt": "Equilibrium Temperature",
        "disc_year": "Discovery Year"
    }
    
    # Reverse mapping for label -> column lookup
    label_to_col = {v: k for k, v in numeric_cols.items()}
    col_list = list(numeric_cols.keys())
    col_labels = list(numeric_cols.values())

    col1, col2 = st.columns(2)

    with col1:
        x_label = st.selectbox("X-axis", col_labels, index=col_labels.index("Planet Radius"))
        x_axis = label_to_col[x_label]

    # Filter y-axis to exclude the selected x-axis
    y_list = [col for col in col_list if col != x_axis]
    y_labels = [numeric_cols[col] for col in y_list]
    
    with col2:
        y_label = st.selectbox("Y-axis", y_labels, 
                              index=y_labels.index("Planet Mass") if "Planet Mass" in y_labels else 0)
        y_axis = label_to_col[y_label]

    # -------------------------------
    # Color-by (categorical options)
    # -------------------------------
    color_options = ["None", "discoverymethod", "disc_facility", "hostname"]

    color_by = st.selectbox("Color points by:", color_options)

    # -------------------------------
    # Toggles
    # -------------------------------
    binned = st.checkbox("Smooth / Bin data (200 bins)", value=False)
    trendline = st.checkbox("Show trendline", value=True)

    # -------------------------------
    # Filter dataset by columns that exist
    # -------------------------------
    plot_df = data[[c for c in data.columns if c in ["pl_name", x_axis, y_axis, *color_options]]].dropna()

    # -------------------------------
    # Show count
    # -------------------------------
    st.write(f"**Showing {len(plot_df):,} planets**")

    # -------------------------------
    # Build figure
    # -------------------------------
    fig = build_plot(
        plot_df,
        x=x_axis,
        y=y_axis,
        binned=binned,
        trendline=trendline
    )

    # Add color-by if applicable
    if color_by != "None":
        fig.update_traces(marker=dict(color=plot_df[color_by], colorscale="Turbo"), selector=dict(mode="markers"))

    # Display it
    st.plotly_chart(fig, use_container_width=True)