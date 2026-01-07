def split_rows(df, step):
    """
    Splits a DataFrame into multiple sub-DataFrames using a fixed step and
    different initial offsets.

    Parameters:
        df: pandas DataFrame containing the point cloud
        step: integer step size used for row-wise subsampling

    Returns:
        subclouds: list of DataFrames, one per offset
    """
    subclouds = []

    for offset in range(step):
        # Extract each subsampling with fixed step and initial offset
        sub_df = df.iloc[offset::step, :].reset_index(drop=True)
        subclouds.append(sub_df)

    return subclouds
