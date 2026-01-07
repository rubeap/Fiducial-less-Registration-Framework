import os
import pandas as pd
import matplotlib.pyplot as plt

from data.split_rows import split_rows
from data.pointcloud_plotting import (
    plot_pointcloud,
    plot_pointcloud_with_lines,
    plot_pointcloud_with_lines_and_vectors,
    plot_two_pointclouds
)
from data.line_fitting import fit_lines
from data.planes_from_lines import planes_from_lines
from data.line_vectors import compute_line_vectors
from data.line_rotations import estimate_line_rotations
from data.rotate_rows import rotate_rows
from data.rmse_rows import compute_rmse_rows


# ============================================================
# GLOBAL CONFIGURATION
# ============================================================
working_dir = os.getcwd()
experiments_dir = os.path.join(working_dir, "Experiments")


# ============================================================
# EXPERIMENT RANGE
# ============================================================
experiment_start = 1
experiment_end   = 3


# ============================================================
# PARAMETERS
# ============================================================
step = 40  # row split size


# ============================================================
# RMSE RESULTS ACCUMULATOR
# ============================================================
rmse_results = []


# ============================================================
# PHASE C: LINE-BASED ALIGNMENT + RMSE (CAM vs TVS)
#   - Reads:
#       • camera_pointcloud_with_displacement.csv
#       • tvs_pointcloud_with_displacement.csv
#   - Splits into rows
#   - Fits lines and vectors
#   - Estimates per-row rotations
#   - Aligns CAM rows to TVS rows
#   - Writes:
#       • camera_pointcloud_aligned.csv
#       • RMSE_<exp>.csv
#       • RMSE_Summary.csv (global)
# ============================================================
print("Starting PHASE C: CAM vs TVS alignment + RMSE\n")


# ============================================================
# MAIN LOOP OVER EXPERIMENTS
# ============================================================
for experiment_id in range(experiment_start, experiment_end + 1):

    experiment_folder = f"{experiment_id:03}"
    print(f"--- Processing experiment folder: {experiment_folder}")

    experiment_path = os.path.join(experiments_dir, experiment_folder)
    processed_data_path = os.path.join(experiment_path, "processed_data")

    # File names aligned with previous scripts
    cam_csv = os.path.join(processed_data_path, "camera_pointcloud_with_displacement.csv")
    tvs_csv = os.path.join(processed_data_path, "tvs_pointcloud_with_displacement.csv")

    if not os.path.exists(cam_csv):
        print(f"    Missing file: {cam_csv}\n")
        continue

    if not os.path.exists(tvs_csv):
        print(f"    Missing file: {tvs_csv}\n")
        continue

    try:
        # --------------------------------------------------------
        # 1) Load point clouds
        # --------------------------------------------------------
        cloud_cam = pd.read_csv(cam_csv)
        cloud_tvs = pd.read_csv(tvs_csv)

        print(f"    CAM points: {len(cloud_cam)}")
        print(f"    TVS points: {len(cloud_tvs)}")

        # --------------------------------------------------------
        # 2) Split into rows
        # --------------------------------------------------------
        cam_rows = split_rows(cloud_cam, step)
        tvs_rows = split_rows(cloud_tvs, step)

        print(f"    CAM rows: {len(cam_rows)} (step={step})")
        print(f"    TVS rows: {len(tvs_rows)} (step={step})")

        # --------------------------------------------------------
        # 3) Visualize raw point clouds (optional figures)
        # --------------------------------------------------------
        plot_pointcloud(cam_rows, title=f"CAM point cloud {experiment_folder}")
        plot_pointcloud(tvs_rows, title=f"TVS point cloud {experiment_folder}")

        # --------------------------------------------------------
        # 4) Fit lines per row
        # --------------------------------------------------------
        cam_lines = fit_lines(cam_rows)
        tvs_lines = fit_lines(tvs_rows)

        print(f"    CAM fitted lines: {len(cam_lines)}")
        print(f"    TVS fitted lines: {len(tvs_lines)}")

        plot_pointcloud_with_lines(cam_rows, cam_lines, title=f"CAM lines {experiment_folder}")
        plot_pointcloud_with_lines(tvs_rows, tvs_lines, title=f"TVS lines {experiment_folder}")

        # --------------------------------------------------------
        # 5) Compute line direction vectors
        # --------------------------------------------------------
        cam_vectors = compute_line_vectors(cam_lines)
        tvs_vectors = compute_line_vectors(tvs_lines)

        plot_pointcloud_with_lines_and_vectors(
            cam_rows, cam_lines, cam_vectors, title=f"CAM vectors {experiment_folder}"
        )
        plot_pointcloud_with_lines_and_vectors(
            tvs_rows, tvs_lines, tvs_vectors, title=f"TVS vectors {experiment_folder}"
        )

        # --------------------------------------------------------
        # 6) Estimate rotations (CAM → TVS)
        # --------------------------------------------------------
        rotations = estimate_line_rotations(cam_vectors, tvs_vectors)
        print(f"    Rotations estimated: {len(rotations)}")

        # --------------------------------------------------------
        # 7) Rotate / align CAM rows to TVS rows
        # --------------------------------------------------------
        cam_rows_aligned = rotate_rows(cam_rows, tvs_rows, rotations)

        aligned_csv = os.path.join(processed_data_path, "camera_pointcloud_aligned.csv")
        pd.concat(cam_rows_aligned).to_csv(aligned_csv, index=False)
        print("    Saved camera_pointcloud_aligned.csv")

        # --------------------------------------------------------
        # 8) Compare aligned CAM vs TVS
        # --------------------------------------------------------
        plot_two_pointclouds(
            cam_rows_aligned, tvs_rows, title=f"CAM vs TVS comparison {experiment_folder}"
        )

        # --------------------------------------------------------
        # 9) RMSE computation
        # --------------------------------------------------------
        rmse = compute_rmse_rows(cam_rows_aligned, tvs_rows)
        print(f"    RMSE: {rmse:.6f}")

        # Save per-experiment RMSE inside the experiment folder
        rmse_csv_individual = os.path.join(processed_data_path, f"RMSE_{experiment_folder}.csv")
        pd.DataFrame([{"Experiment": experiment_folder, "RMSE": rmse}]).to_csv(
            rmse_csv_individual,
            index=False
        )
        print(f"    Saved RMSE_{experiment_folder}.csv")

        # Accumulate global summary
        rmse_results.append({"Experiment": experiment_folder, "RMSE": rmse})

        # Show and close figures to free memory
        plt.show()
        plt.close("all")

        print("    Completed\n")

    except Exception as e:
        print(f"    Error: {e}\n")


# ============================================================
# SAVE GLOBAL RMSE SUMMARY
# ============================================================
df_rmse = pd.DataFrame(rmse_results)
rmse_summary_csv = os.path.join(experiments_dir, "RMSE_Summary.csv")
df_rmse.to_csv(rmse_summary_csv, index=False)

print("PHASE C completed")
print(f"Saved RMSE_Summary.csv at: {rmse_summary_csv}")
