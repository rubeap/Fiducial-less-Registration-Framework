import numpy as np
import pandas as pd

def planes_from_lines(lines, global_centroid=None):
    """
    Computes local planes between consecutive fitted lines.

    Each plane is defined by an orthonormal basis (e1, e2, e3) and
    a reference point lying midway between consecutive line centroids.
    """
    data = []

    if global_centroid is None:
        global_centroid = np.mean([p for p, _ in lines], axis=0)

    for i in range(len(lines) - 1):
        p1, v1 = lines[i]
        p2, _  = lines[i + 1]

        d1 = p2 - p1
        norm_d1 = np.linalg.norm(d1)
        if norm_d1 < 1e-6:
            continue

        # e1: direction between consecutive centroids
        e1 = d1 / norm_d1

        # e2: direction of the first line
        e2 = v1 / np.linalg.norm(v1)

        # e3: plane normal
        e3 = np.cross(e1, e2)
        e3 /= np.linalg.norm(e3)

        # Enforce consistent outward orientation
        radial_vector = p1 - global_centroid
        if np.dot(e3, radial_vector) < 0:
            e3 = -e3
            e2 = np.cross(e3, e1)

        plane_point = (p1 + p2) / 2

        data.append([
            *plane_point,
            *e1, *e2, *e3
        ])

    columns = [
        'px', 'py', 'pz',
        'e1x', 'e1y', 'e1z',
        'e2x', 'e2y', 'e2z',
        'e3x', 'e3y', 'e3z'
    ]

    return pd.DataFrame(data, columns=columns)
