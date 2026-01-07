import numpy as np

def compute_rmse_rows(cam_rows, tvs_rows):
    """
    Computes the global RMSE between two 3D point clouds segmented by rows (offsets).
    Point-to-point correspondence is assumed between corresponding rows.

    Parameters:
        cam_rows: list of DataFrames (one per offset) from the CAM point cloud
        tvs_rows: list of DataFrames (one per offset) from the TVS point cloud

    Returns:
        global_rmse: scalar value of the global root mean square error
    """
    squared_errors = []

    for i in range(len(cam_rows)):
        cam_points = cam_rows[i][['X', 'Y', 'Z']].to_numpy()
        tvs_points = tvs_rows[i][['X', 'Y', 'Z']].to_numpy()

        if cam_points.shape != tvs_points.shape:
            raise ValueError(
                f"Row {i} does not contain the same number of points in both point clouds"
            )

        diff = cam_points - tvs_points
        distances = np.linalg.norm(diff, axis=1)
        squared_errors.extend(distances ** 2)

    global_rmse = np.sqrt(np.mean(squared_errors))
    return global_rmse
