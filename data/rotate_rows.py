import pandas as pd

def rotate_rows(cam_rows, tvs_rows, rotations):
    """
    Applies an individual rotation to each row of the CAM point cloud, aligning it
    with the corresponding row in the TVS point cloud. Uses the local centroid and
    the per-row rotation matrix.
    """
    aligned_cam_rows = []

    for i in range(len(cam_rows)):
        df_cam = cam_rows[i].copy()
        df_tvs = tvs_rows[i]
        R_i = rotations[i]

        # Compute centroids
        cam_centroid = df_cam[['X', 'Y', 'Z']].mean().to_numpy()
        tvs_centroid = df_tvs[['X', 'Y', 'Z']].mean().to_numpy()

        # Center CAM points
        cam_points = df_cam[['X', 'Y', 'Z']].to_numpy()
        centered_points = cam_points - cam_centroid

        # Apply rotation
        rotated_points = (R_i @ centered_points.T).T

        # Translate to TVS frame
        aligned_points = rotated_points + tvs_centroid

        # Store aligned DataFrame
        df_aligned = pd.DataFrame(aligned_points, columns=['X', 'Y', 'Z'])
        aligned_cam_rows.append(df_aligned)

    return aligned_cam_rows
