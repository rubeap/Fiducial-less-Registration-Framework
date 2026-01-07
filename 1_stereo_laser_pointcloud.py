import os
import cv2
import csv
import pandas as pd
import numpy as np
import re  # Used for numeric extraction from filenames
from collections import defaultdict  # grouping by base image name im_k_j
from data import stereo_rectification
from data import stereo_triangulation

# ============================================================
# EXPERIMENT RANGE
# ============================================================
experiment_start = 1
experiment_end   = 3


# ============================================================
# FUNCTION: Detect laser spot centroid
# ============================================================
def find_laser_centroid(image, image_name):
    """
    Detects the centroid of the magenta laser spot in an image.
    Saves a visualization with contour and centroid overlay.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_magenta = np.array([100, 0, 245])
    upper_magenta = np.array([170, 30, 255])

    mask = cv2.inRange(hsv, lower_magenta, upper_magenta)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        laser_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(laser_contour)

        if moments["m00"] != 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])

            cv2.drawContours(image, [laser_contour], -1, (0, 255, 0), 2)
            cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)

            save_path = os.path.join(laser_spot_detection_path, f"{image_name}_spot.jpg")
            cv2.imwrite(save_path, image)

            print(f"Laser spot image saved at: {save_path}")
            return (cx, cy)

    return None


# ============================================================
# NATURAL SORTING KEYS
# ============================================================

# Original images: im_<k>_<j>.jpg  -> (k, j)
def original_image_key(filename: str):
    match = re.search(r'im_(\d+)_(\d+)\.jpg$', filename, re.IGNORECASE)
    if match:
        return (int(match.group(1)), int(match.group(2)))
    nums = re.findall(r'\d+', filename)
    return tuple(map(int, nums)) if nums else (0,)


# Split images: im_<k>_<j>_(I|D).jpg -> (k, j, side) where I=0, D=1
def split_image_key(filename: str):
    match = re.search(r'im_(\d+)_(\d+)_(I|D)\.jpg$', filename, re.IGNORECASE)
    if match:
        k, j = int(match.group(1)), int(match.group(2))
        side = 0 if match.group(3).upper() == 'I' else 1
        return (k, j, side)

    nums = re.findall(r'\d+', filename)
    side = 0 if '_I' in filename.upper() else 1
    return (*map(int, nums), side) if nums else (0, side)


# ============================================================
# BASE WORKING DIRECTORY
# ============================================================
working_dir = os.getcwd()


# ============================================================
# MAIN PROCESSING LOOP
# ============================================================
for experiment_id in range(experiment_start, experiment_end + 1):

    experiment_folder = f"{experiment_id:03}"
    experiment_path = os.path.join(
        working_dir,
        "Experiments",
        experiment_folder
    )

    print(experiment_path)

    if not os.path.isdir(experiment_path):
        print(f"⚠️ Folder {experiment_folder} does not exist. Skipping...")
        continue

    # --------------------------------------------------------
    # DIRECTORY STRUCTURE
    # --------------------------------------------------------
    raw_data_path = os.path.join(experiment_path, "raw_data")
    processed_data_path = os.path.join(experiment_path, "processed_data")

    split_images_path = os.path.join(processed_data_path, "split_images")
    rectified_images_path = os.path.join(processed_data_path, "rectified_images")
    laser_spot_detection_path = os.path.join(processed_data_path, "laser_spot_detection")

    ordered_cloud_csv = os.path.join(processed_data_path, "camera_pointcloud_ordered.csv")
    cloud_csv = os.path.join(processed_data_path, "camera_pointcloud.csv")

    os.makedirs(split_images_path, exist_ok=True)
    os.makedirs(rectified_images_path, exist_ok=True)
    os.makedirs(laser_spot_detection_path, exist_ok=True)

    # --------------------------------------------------------
    # STEP 1: Split original stereo images
    # --------------------------------------------------------
    original_images = sorted(
        [f for f in os.listdir(raw_data_path) if f.lower().endswith(".jpg")],
        key=original_image_key
    )

    for image_name in original_images:
        image_path = os.path.join(raw_data_path, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Could not load image: {image_path}")
            continue

        height, width, _ = image.shape
        mid = width // 2

        left_image = image[:, :mid]
        right_image = image[:, mid:]

        base_name, ext = os.path.splitext(image_name)

        left_path = os.path.join(split_images_path, f"{base_name}_I{ext}")
        right_path = os.path.join(split_images_path, f"{base_name}_D{ext}")

        cv2.imwrite(left_path, left_image)
        cv2.imwrite(right_path, right_image)

        print(f"Image {image_name} split successfully.")

    # --------------------------------------------------------
    # STEP 2: Rectify stereo image pairs
    # --------------------------------------------------------
    split_images = sorted(
        [f for f in os.listdir(split_images_path) if f.lower().endswith(".jpg")],
        key=split_image_key
    )

    grouped_pairs = defaultdict(dict)

    for filename in split_images:
        match = re.search(r'(im_\d+_\d+)_(I|D)\.jpg$', filename, re.IGNORECASE)
        if not match:
            continue

        base_name, side = match.group(1), match.group(2).upper()
        grouped_pairs[base_name][side] = filename

    def base_key(base: str):
        k, j = map(int, re.findall(r'\d+', base))
        return (k, j)

    stereo_pairs = []
    for base in sorted(grouped_pairs.keys(), key=base_key):
        if 'I' in grouped_pairs[base] and 'D' in grouped_pairs[base]:
            stereo_pairs.append((grouped_pairs[base]['I'], grouped_pairs[base]['D']))

    for left_name, right_name in stereo_pairs:

        left_path = os.path.join(split_images_path, left_name)
        right_path = os.path.join(split_images_path, right_name)

        left_img = cv2.imread(left_path)
        right_img = cv2.imread(right_path)

        if left_img is None or right_img is None:
            print(f"Failed to load stereo pair: {left_name}, {right_name}")
            continue

        left_rect, right_rect = stereo_rectification.run(left_img, right_img)

        base_name = re.sub(r'_I$', '', os.path.splitext(left_name)[0])

        left_rect_path = os.path.join(rectified_images_path, f"{base_name}_I_rect.jpg")
        right_rect_path = os.path.join(rectified_images_path, f"{base_name}_D_rect.jpg")

        cv2.imwrite(left_rect_path, left_rect)
        cv2.imwrite(right_rect_path, right_rect)

        print(f"Rectified images saved for {base_name}")

    # --------------------------------------------------------
    # STEP 3: Generate ordered camera point cloud CSV
    # --------------------------------------------------------
    with open(ordered_cloud_csv, mode='w', newline='') as csv_ordered:

        writer = csv.writer(csv_ordered)

        for left_name, right_name in stereo_pairs:

            base_name = re.sub(r'_I$', '', os.path.splitext(left_name)[0])

            left_rect_path = os.path.join(rectified_images_path, f"{base_name}_I_rect.jpg")
            right_rect_path = os.path.join(rectified_images_path, f"{base_name}_D_rect.jpg")

            left_rect = cv2.imread(left_rect_path)
            right_rect = cv2.imread(right_rect_path)

            centroid_left = find_laser_centroid(left_rect, f"{base_name}_I_rect")
            centroid_right = find_laser_centroid(right_rect, f"{base_name}_D_rect")

            if centroid_left and centroid_right:

                xy_left = np.array([centroid_left], dtype=np.float32)
                xy_right = np.array([centroid_right], dtype=np.float32)

                laser_point_cam = stereo_triangulation.triangulation(
                    xy_left, xy_right, left_rect
                )

                laser_point_cam = np.array(laser_point_cam).flatten()

                writer.writerow([*laser_point_cam, left_name, right_name])

            else:
                print(f"Laser spot not detected in pair {base_name}")

    # --------------------------------------------------------
    # STEP 4: Generate final camera point cloud CSV
    # --------------------------------------------------------
    with open(ordered_cloud_csv, mode='r') as ordered_file, \
         open(cloud_csv, mode='w', newline='') as final_file:

        reader = csv.reader(ordered_file)
        writer = csv.writer(final_file)

        for row in reader:
            writer.writerow(row[:3])

    print("Processing completed: 'camera_pointcloud_ordered.csv' and 'camera_pointcloud.csv' generated successfully.")
