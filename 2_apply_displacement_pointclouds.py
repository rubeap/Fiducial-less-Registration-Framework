import os
import pandas as pd

# ============================================================
# GLOBAL CONFIGURATION
# ============================================================
working_dir = os.getcwd()
experiments_dir = os.path.join(working_dir, "Experiments")

experiment_start = 1
experiment_end   = 3


# ============================================================
# PHASE A: TVS POINT CLOUD PROCESSING
# ============================================================
results = []

print("Starting PHASE A: TVS point cloud processing\n")

for i in range(experiment_start, experiment_end + 1):

    subfolder = f"{i:03}"
    print(f"--- Processing experiment folder: {subfolder}")

    subfolder_path = os.path.join(experiments_dir, subfolder)
    raw_data_path = os.path.join(subfolder_path, "raw_data")
    processed_data_path = os.path.join(subfolder_path, "processed_data")

    if not (os.path.isdir(subfolder_path) and os.path.isdir(raw_data_path)):
        print("    Skipped: required directories not found\n")
        results.append((subfolder, "Missing experiment/raw_data folder"))
        continue

    os.makedirs(processed_data_path, exist_ok=True)
    print("    Output directory verified")

    displacement_path = os.path.join(raw_data_path, "displacement.csv")
    if not os.path.exists(displacement_path):
        print("    Missing displacement.csv\n")
        results.append((subfolder, "Missing displacement.csv"))
        continue

    # Read incremental displacements (cm → m)
    displacements = pd.read_csv(displacement_path, header=None).iloc[0].tolist()
    displacements = [d / 100.0 for d in displacements]
    print(f"    Read {len(displacements)} incremental displacements")

    # Compute accumulated displacements
    accumulated_displacements = [0.0]
    running_sum = 0.0
    for d in displacements:
        running_sum += d
        accumulated_displacements.append(running_sum)

    print(f"    Accumulated displacement count: {len(accumulated_displacements)}")

    # Load TVS CSV files
    tvs_files = sorted([
        f for f in os.listdir(raw_data_path)
        if f.startswith("tvs_") and f.endswith(".csv")
    ])

    print(f"    Found {len(tvs_files)} TVS CSV files")

    if len(tvs_files) != len(accumulated_displacements):
        print("    Configuration error: TVS files and displacement count mismatch\n")
        results.append((subfolder, "Configuration error (count mismatch)"))
        continue

    data_without_disp = []
    data_with_disp = []
    displacement_vector = []

    for idx, filename in enumerate(tvs_files):

        print(f"        Processing TVS file {idx+1}/{len(tvs_files)}: {filename}")

        csv_path = os.path.join(raw_data_path, filename)

        df = pd.read_csv(csv_path, usecols=[0, 1, 2], header=None)
        df = df.dropna(how="all")

        print(f"            Points read: {len(df)}")

        data_without_disp.append(df)

        df_shifted = df.copy()
        df_shifted[1] += accumulated_displacements[idx]
        data_with_disp.append(df_shifted)

        displacement_vector.extend([accumulated_displacements[idx]] * len(df))

    df_without_disp = pd.concat(data_without_disp, ignore_index=True)
    df_with_disp = pd.concat(data_with_disp, ignore_index=True)

    df_without_disp.columns = ["X", "Y", "Z"]
    df_with_disp.columns = ["X", "Y", "Z"]

    df_without_disp.to_csv(
        os.path.join(processed_data_path, "tvs_pointcloud_without_displacement.csv"),
        index=False
    )
    print("    Saved tvs_pointcloud_without_displacement.csv")

    df_with_disp.to_csv(
        os.path.join(processed_data_path, "tvs_pointcloud_with_displacement.csv"),
        index=False
    )
    print("    Saved tvs_pointcloud_with_displacement.csv")

    pd.DataFrame(displacement_vector).to_csv(
        os.path.join(processed_data_path, "DisplacementVector.csv"),
        index=False,
        header=False
    )
    print("    Saved DisplacementVector.csv")

    # Consistency check
    num_imgs = len([
        f for f in os.listdir(raw_data_path)
        if f.lower().endswith(".jpg")
    ])

    status = "Correct" if len(tvs_files) == num_imgs else "Mismatch"
    print(f"    Validation: TVS files = {len(tvs_files)}, images = {num_imgs} -> {status}\n")

    results.append((subfolder, status))


pd.DataFrame(results, columns=["Experiment", "Result"]).to_csv(
    os.path.join(experiments_dir, "Experiment_Results.csv"),
    index=False
)

print("PHASE A completed\n")


# ============================================================
# PHASE B: APPLY DISPLACEMENT TO CAMERA POINT CLOUD
# ============================================================
print("Starting PHASE B: Camera point cloud displacement\n")

for i in range(experiment_start, experiment_end + 1):

    folder = f"{i:03}"
    print(f"--- Processing camera data for experiment {folder}")

    base_path = os.path.join(experiments_dir, folder)
    processed_data_path = os.path.join(base_path, "processed_data")

    cam_path = os.path.join(processed_data_path, "camera_pointcloud.csv")
    vec_path = os.path.join(processed_data_path, "DisplacementVector.csv")
    out_path = os.path.join(processed_data_path, "camera_pointcloud_with_displacement.csv")

    if not (os.path.exists(cam_path) and os.path.exists(vec_path)):
        print("    Required files not found\n")
        continue

    df_cam = pd.read_csv(cam_path, header=None)
    displacement_vec = pd.read_csv(vec_path, header=None)[0].values

    print(f"    Camera points: {len(df_cam)}")
    print(f"    Displacement vector length: {len(displacement_vec)}")

    if len(df_cam) != len(displacement_vec):
        print("    Dimension mismatch\n")
        continue

    df_cam[1] += displacement_vec
    df_cam.columns = ["X", "Y", "Z"]

    df_cam.to_csv(out_path, index=False)
    print("    Saved camera_pointcloud_with_displacement.csv\n")

print("FULL PROCESS COMPLETED")
