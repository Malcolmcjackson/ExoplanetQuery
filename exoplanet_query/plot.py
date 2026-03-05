import plotly.express as px
import numpy as np
import pandas as pd

# --------------------------------------------------------------
# 🌈 Human-friendly axis labels
# --------------------------------------------------------------
AXIS_LABELS = {
    "pl_rade": "Planet Radius (R⊕)",
    "pl_masse": "Planet Mass (M⊕)",
}

def pretty(col):
    return AXIS_LABELS.get(col, col)


# --------------------------------------------------------------
# 🌈 Median binning helper (kept lightweight)
# --------------------------------------------------------------
def bin_and_aggregate_data(x, y, bins=150):
    """
    Smooths noisy scatter data by computing median values in X-bins.
    """
    x = np.array(x)
    y = np.array(y)

    bin_edges = np.linspace(np.nanmin(x), np.nanmax(x), bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_indices = np.digitize(x, bin_edges) - 1

    y_med = np.array([
        np.nanmedian(y[bin_indices == i]) if np.any(bin_indices == i) else np.nan
        for i in range(bins)
    ])

    df = pd.DataFrame({"x": bin_centers, "y_med": y_med})
    return df.dropna()


# --------------------------------------------------------------
# 🌈 Curated Planet Radius vs Mass Plot
# --------------------------------------------------------------
def radius_vs_mass_plot(df, use_binning=False, trendline=True):
    """
    Creates the official curated plot: Planet Radius (R⊕) vs Mass (M⊕).
    """

    # Clean data
    clean = df[["pl_name", "pl_rade", "pl_masse"]].dropna()
    clean = clean[(clean["pl_rade"] > 0) & (clean["pl_masse"] > 0)]

    x = "pl_rade"
    y = "pl_masse"

    # =============================================================
    # ⭐ BINNED MODE (optional)
    # =============================================================
    if use_binning:
        binned = bin_and_aggregate_data(clean[x], clean[y])

        fig = px.scatter(
            binned,
            x="x",
            y="y_med",
            title=f"{pretty(x)} vs {pretty(y)} (Median Smoothed)",
            labels={"x": pretty(x), "y_med": pretty(y)},
            template="plotly_dark",
        )

        # Optional trendline applied to binned curve
        if trendline and len(binned) > 2:
            slope, intercept = np.polyfit(binned["x"], binned["y_med"], 1)
            lx = np.array([binned["x"].min(), binned["x"].max()])
            ly = slope * lx + intercept

            fig.add_scatter(x=lx, y=ly, mode="lines",
                            name="Trendline",
                            line=dict(color="red", width=3))

        return fig

    # =============================================================
    # ⭐ RAW SCATTER MODE (default)
    # =============================================================
    fig = px.scatter(
        clean,
        x=x,
        y=y,
        hover_name="pl_name",
        title=f"{pretty(x)} vs {pretty(y)}",
        labels={x: pretty(x), y: pretty(y)},
        template="plotly_dark",
        opacity=0.7,
    )

    # Add OLS regression trendline (Plotly built-in)
    if trendline:
        fit_df = px.scatter(
            clean,
            x=x,
            y=y,
            trendline="ols",
            opacity=0,
        )
        trend = fit_df.data[-1]
        trend.line.width = 3
        trend.opacity = 0.9
        fig.add_trace(trend)

    return fig

# --------------------------------------------------------------
# 🌈 Curated Temperature vs Orbital Distance Plot
# --------------------------------------------------------------
def temperature_vs_distance_plot(df, use_binning=True, trendline=True):

    clean = df[["pl_name", "pl_eqt", "pl_orbper"]].dropna()
    clean = clean[(clean["pl_eqt"] > 0) & (clean["pl_orbper"] > 0)]

    x = "pl_orbper"   # orbital period (proxy for distance)
    y = "pl_eqt"      # equilibrium temperature

    # =====================================================
    # ⭐ BINNED VERSION — reduces extreme skew
    # =====================================================
    if use_binning:
        # LOG-BIN the orbital periods
        clean["log_x"] = np.log10(clean[x])

        # Bin in log space
        bins = 120
        bin_edges = np.linspace(clean["log_x"].min(), clean["log_x"].max(), bins + 1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_idx = np.digitize(clean["log_x"], bin_edges) - 1

        temp_medians = []
        for i in range(bins):
            vals = clean[y][bin_idx == i]
            temp_medians.append(np.nanmedian(vals) if len(vals) else np.nan)

        binned_df = pd.DataFrame({
            "log_x": bin_centers,
            "temp_med": temp_medians
        }).dropna()

        fig = px.scatter(
            binned_df,
            x="log_x",
            y="temp_med",
            title="Orbital Distance vs Temperature (log-binned)",
            labels={
                "log_x": "log₁₀(Orbital Period in days)",
                "temp_med": "Median Temperature (K)"
            },
            template="plotly_dark",
        )

        # Add trendline to binned data
        if trendline:
            slope, intercept = np.polyfit(binned_df["log_x"], binned_df["temp_med"], 1)
            lx = np.array([binned_df["log_x"].min(), binned_df["log_x"].max()])
            ly = slope * lx + intercept

            fig.add_scatter(
                x=lx, y=ly,
                mode="lines",
                name="Trendline",
                line=dict(color="red", width=3)
            )

        return fig

    # =====================================================
    # ⭐ RAW SCATTER (log x-axis)
    # =====================================================
    fig = px.scatter(
        clean,
        x=x,
        y=y,
        hover_name="pl_name",
        title="Orbital Distance vs Temperature",
        labels={x: "Orbital Period (days)", y: "Equilibrium Temperature (K)"},
        template="plotly_dark",
        opacity=0.7,
    )

    fig.update_xaxes(type="log")

    return fig

def discovery_year_bar_chart(df):
    """
    Exoplanet discoveries per year.
    A classic plot showing mission-driven spikes.
    """

    # Keep only valid years
    clean = df[["disc_year"]].dropna()
    clean = clean[clean["disc_year"] > 1980]   # removes weird old placeholder values

    # Count discoveries per year
    counts = clean["disc_year"].value_counts().sort_index()

    fig = px.bar(
        x=counts.index,
        y=counts.values,
        labels={"x": "Discovery Year", "y": "Number of Planets Discovered"},
        title="Exoplanet Discoveries Per Year",
        template="plotly_dark"
    )

    fig.update_traces(marker_color="#7FDBFF")  # pretty blue

    return fig

import plotly.express as px
import numpy as np
import pandas as pd

def distance_histogram(df):
    """
    Histogram of exoplanet distances from Earth.
    Shows how many planets are nearby vs far away.
    """

    clean = df[["sy_dist"]].dropna()
    clean = clean[clean["sy_dist"] > 0]  # remove invalid zeros

    fig = px.histogram(
        clean,
        x="sy_dist",
        nbins=80,
        title="Distance From Earth (pc)",
        labels={"sy_dist": "Distance From Earth (pc)"},
        template="plotly_dark"
    )

    fig.update_traces(marker_color="#66C2FF", opacity=0.75)
    fig.update_layout(
        xaxis_title="Distance (parsecs)",
        yaxis_title="Number of Planets",
    )

    return fig

def method_radius_boxplots(df):
    clean = df[["pl_rade", "discoverymethod"]].dropna()
    clean = clean[clean["pl_rade"] > 0]

    # Group rare methods into "Other"
    method_counts = clean["discoverymethod"].value_counts()
    keep = method_counts[method_counts > 30].index
    clean["method_group"] = clean["discoverymethod"].apply(
        lambda m: m if m in keep else "Other"
    )

    figs = {}

    # 1️⃣ ZOOMED PLOT (0–30 R⊕)
    zoom = clean[clean["pl_rade"] <= 30]
    fig_zoom = px.box(
        zoom,
        x="method_group",
        y="pl_rade",
        title="Planet Radius by Discovery Method (Zoomed: ≤ 30 R⊕)",
        labels={"pl_rade": "Planet Radius (R⊕)"},
        template="plotly_dark",
        points="outliers"
    )
    figs["zoom"] = fig_zoom

    # 2️⃣ FULL RANGE PLOT
    fig_full = px.box(
        clean,
        x="method_group",
        y="pl_rade",
        title="Planet Radius by Discovery Method (Full Range)",
        labels={"pl_rade": "Planet Radius (R⊕)"},
        template="plotly_dark",
        points="outliers"
    )
    figs["full"] = fig_full

    return figs