import plotly.express as px
import numpy as np
import pandas as pd

# --------------------------------------------------------------
# 🌈 Units + Human-Friendly Axis Names
# --------------------------------------------------------------
AXIS_LABELS = {
    "sy_dist": "Distance from Earth (pc)",
    "pl_rade": "Planet Radius (R⊕)",
    "pl_masse": "Planet Mass (M⊕)",
    "pl_orbper": "Orbital Period (days)",
    "st_rad": "Star Radius (R☉)",
    "pl_eqt": "Equilibrium Temperature (K)",
    "disc_year": "Discovery Year",
}

def pretty(col):
    """Return a human-friendly axis label with units."""
    return AXIS_LABELS.get(col, col)


# --------------------------------------------------------------
# 🌈 1. Optional binned scatter helper
# --------------------------------------------------------------
def bin_and_aggregate_data(x, y, bins=200):

    x = np.array(x)
    y = np.array(y)

    bin_edges = np.linspace(np.nanmin(x), np.nanmax(x), bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    bin_indices = np.digitize(x, bin_edges) - 1

    # ⭐ Median aggregation (better for skewed planet data)
    y_med = np.array([
        np.nanmedian(y[(bin_indices == i)]) if np.any(bin_indices == i) else np.nan
        for i in range(bins)
    ])

    return pd.DataFrame({"x": bin_centers, "y_med": y_med})


# --------------------------------------------------------------
# 🌈 2. Primary scatter plot function WITH UNIT LABELS + BIN TRENDLINE
# --------------------------------------------------------------
def build_plot(df, x="pl_rade", y="pl_masse", binned=False, trendline=True):

    plot_df = df.copy()
    plot_df = plot_df[[x, y, "pl_name"]].dropna()

    # remove physically impossible zero-values
    bad_zero_columns = ["sy_dist", "pl_rade", "pl_masse", "pl_orbper", "st_rad", "pl_eqt"]
    for col in bad_zero_columns:
        if col in plot_df.columns:
            plot_df = plot_df[plot_df[col] > 0]

    # ==========================================================
    # ⭐ BINNED MODE
    # ==========================================================
    if binned:

        binned_df = bin_and_aggregate_data(plot_df[x], plot_df[y])
        binned_df = binned_df.dropna()  # remove empty bins

        fig = px.scatter(
            binned_df,
            x="x",
            y="y_med",
            title=f"{pretty(x)} vs {pretty(y)}",
            labels={"x": pretty(x), "y_med": f"Median {pretty(y)}"},
            template="plotly_dark",
        )

        # ⭐ MANUAL TRENDLINE FOR BINNED DATA ⭐
        if trendline and len(binned_df) > 2:
            # Fit linear regression
            slope, intercept = np.polyfit(binned_df["x"], binned_df["y_med"], 1)

            line_x = np.array([binned_df["x"].min(), binned_df["x"].max()])
            line_y = slope * line_x + intercept

            fig.add_scatter(
                x=line_x,
                y=line_y,
                mode="lines",
                name="Trendline",
                line=dict(color="red", width=3),
            )

        return fig

    # ==========================================================
    # ⭐ STANDARD SCATTER MODE
    # ==========================================================
    fig = px.scatter(
        plot_df,
        x=x,
        y=y,
        hover_name="pl_name",
        title=f"{pretty(x)} vs {pretty(y)}",
        labels={x: pretty(x), y: pretty(y)},
        template="plotly_dark",
        opacity=0.7,
    )

    # ⭐ Built-in OLS trendline for unbinned mode
    if trendline:
        fig2 = px.scatter(
            plot_df,
            x=x,
            y=y,
            trendline="ols",
            opacity=0,
        )
        trend = fig2.data[-1]
        trend.opacity = 0.9
        trend.line.width = 3
        fig.add_trace(trend)

    return fig