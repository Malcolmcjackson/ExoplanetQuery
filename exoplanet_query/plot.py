import plotly.express as px
import numpy as np
import pandas as pd

# --------------------------------------------------------------
# 🌈 1. Optional binned scatter helper (if you still want it)
# --------------------------------------------------------------
def bin_and_aggregate_data(x, y, bins=200):
    """
    Bin and aggregate numeric data (optional helper for smoothed plots).

    Args:
        x (array-like): x-axis values
        y (array-like): y-axis values
        bins (int): number of bins

    Returns:
        DataFrame: with columns ["x", "y_mean"]
    """

    x = np.array(x)
    y = np.array(y)

    bin_edges = np.linspace(np.nanmin(x), np.nanmax(x), bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    bin_indices = np.digitize(x, bin_edges) - 1
    agg_y = np.zeros(bins)
    counts = np.zeros(bins)

    for xi, yi in zip(bin_indices, y):
        if 0 <= xi < bins:
            agg_y[xi] += yi
            counts[xi] += 1

    y_mean = np.divide(agg_y, counts, out=np.zeros_like(agg_y), where=counts > 0)

    return pd.DataFrame({"x": bin_centers, "y_mean": y_mean})


# --------------------------------------------------------------
# 🌈 2. Primary scatter plot function
# --------------------------------------------------------------
def build_plot(df, x="pl_rade", y="pl_masse", binned=False, trendline=True):
    """
    Create a Plotly scatter plot (with optional smoothing + trendline).

    Args:
        df (DataFrame): filtered exoplanet data
        x (str): x-axis column
        y (str): y-axis column
        binned (bool): whether to apply binning smoothing
        trendline (bool): whether to add a regression trendline

    Returns:
        Plotly Figure
    """

    plot_df = df.copy()

    # remove missing values
    plot_df = plot_df[[x, y, "pl_name"]].dropna()

    # optional binning
    if binned:
        binned_df = bin_and_aggregate_data(plot_df[x], plot_df[y])
        fig = px.scatter(
            binned_df,
            x="x",
            y="y_mean",
            title=f"Binned {x} vs {y}",
            labels={"x": x, "y_mean": f"Mean {y}"},
            template="plotly_dark",
        )
    else:
        fig = px.scatter(
            plot_df,
            x=x,
            y=y,
            hover_name="pl_name",
            title=f"{x} vs {y}",
            template="plotly_dark",
            opacity=0.7,
        )

    # optional regression trendline  
    if trendline and not binned:
        fig2 = px.scatter(
            plot_df,
            x=x,
            y=y,
            trendline="ols",
            opacity=0,
        )
        # add trendline trace only
        trend_trace = fig2.data[-1]
        trend_trace.opacity = 0.9
        trend_trace.line.width = 3
        fig.add_trace(trend_trace)

    return fig