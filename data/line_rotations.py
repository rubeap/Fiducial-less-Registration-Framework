import numpy as np

def estimate_line_rotations(cam_vectors, tvs_vectors):
    """
    Computes a 3x3 rotation matrix for each pair of corresponding lines
    between CAM vectors and TVS vectors.

    Each row of the input DataFrames represents an orthonormal triad.
    """
    rotations = []

    for i in range(len(cam_vectors)):
        # Extract orthonormal vectors from CAM
        e1_cam = cam_vectors.loc[i, ['e1x', 'e1y', 'e1z']].to_numpy()
        e2_cam = cam_vectors.loc[i, ['e2x', 'e2y', 'e2z']].to_numpy()
        e3_cam = cam_vectors.loc[i, ['e3x', 'e3y', 'e3z']].to_numpy()
        E_cam = np.column_stack([e1_cam, e2_cam, e3_cam])

        # Extract orthonormal vectors from TVS
        e1_tvs = tvs_vectors.loc[i, ['e1x', 'e1y', 'e1z']].to_numpy()
        e2_tvs = tvs_vectors.loc[i, ['e2x', 'e2y', 'e2z']].to_numpy()
        e3_tvs = tvs_vectors.loc[i, ['e3x', 'e3y', 'e3z']].to_numpy()
        E_tvs = np.column_stack([e1_tvs, e2_tvs, e3_tvs])

        # Compute the rotation that aligns CAM with TVS
        R_i = E_tvs @ E_cam.T
        rotations.append(R_i)

    return rotations
