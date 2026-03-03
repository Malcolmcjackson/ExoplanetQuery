# --------------------------------------------------------------
# 💫 1. Query/filtering logic
# --------------------------------------------------------------
def query_exoplanets(
    df,
    name=None,
    year=None,
    method=None,
    host=None,
    facility=None,
):
    """
    Filter the exoplanet DataFrame based on user selections.

    Args:
        df (DataFrame): full dataset
        name (str): substring match
        year (int or None)
        method (str or None)
        host (str): substring match
        facility (str or None)

    Returns:
        DataFrame: filtered dataset
    """

    filtered = df.copy()

    if name:
        filtered = filtered[filtered["pl_name"].str.contains(name, case=False, na=False)]

    if year:
        filtered = filtered[filtered["disc_year"] == int(year)]

    if method:
        filtered = filtered[filtered["discoverymethod"] == method]

    if host:
        filtered = filtered[filtered["hostname"].str.contains(host, case=False, na=False)]

    if facility:
        filtered = filtered[filtered["disc_facility"] == facility]

    return filtered