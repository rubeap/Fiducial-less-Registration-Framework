import numpy as np

def fit_lines(list_of_dfs):
    """
    Fits a 3D line to each DataFrame using SVD.
    Each line is represented by a centroid and a direction vector.
    """
    lines = []

    for df in list_of_dfs:
        points = df[['X', 'Y', 'Z']].to_numpy()

        centroid = points.mean(axis=0)
        centered_points = points - centroid

        _, _, Vt = np.linalg.svd(centered_points)
        direction = Vt[0]  # Principal direction vector

        # Each element is a tuple: (centroid, direction)
        lines.append((centroid, direction))

    return lines
