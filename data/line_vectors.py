import numpy as np
import pandas as pd

def compute_line_vectors(lines):
    """
    Computes an orthonormal triad (e1, e2, e3) for each fitted 3D line.

    Each line is defined by a centroid and a direction vector.
    The output is a DataFrame containing the centroid and the three
    orthonormal basis vectors.
    """
    data = []

    for centroid, e1 in lines:
        # Normalize primary direction vector
        e1 = e1 / np.linalg.norm(e1)

        # Enforce e1 orientation toward positive Y
        if np.dot(e1, np.array([0, 1, 0])) < 0:
            e1 = -e1

        # Use a fixed reference vector to construct e2
        reference = np.array([0, 0, 1])
        if np.abs(np.dot(e1, reference)) > 0.95:
            reference = np.array([1, 0, 0])

        # Compute e2 orthogonal to e1
        v_proj = reference - np.dot(reference, e1) * e1
        e2 = v_proj / np.linalg.norm(v_proj)

        # Compute e3 as the cross product
        e3 = np.cross(e1, e2)
        e3 /= np.linalg.norm(e3)

        row = list(centroid) + list(e1) + list(e2) + list(e3)
        data.append(row)

    columns = [
        'cx', 'cy', 'cz',
        'e1x', 'e1y', 'e1z',
        'e2x', 'e2y', 'e2z',
        'e3x', 'e3y', 'e3z'
    ]

    return pd.DataFrame(data, columns=columns)
