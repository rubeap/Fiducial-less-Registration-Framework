# Fiducial-less Registration Framework — Code Repository

This repository serves as a shared space for the review and verification of the code and data associated with the submitted paper entitled:

**“Fiducial-less Registration Framework for Multisensor Point Cloud Fusion of Laser Scanning and Stereo Vision for Autonomous Mining Tunnel Inspection.”**

The provided Python scripts reproduce the main stages of the proposed framework, including synchronized point cloud generation, controlled displacement simulation, row-wise registration, and quantitative evaluation using RMSE.

---

## Overview of the Evaluation Pipeline

Evaluation is organized into **three sequential steps**, which must be executed in order.  
Each step corresponds to one Python script in this repository.

---

## Step 1 : Stereo–Laser Point Cloud Generation  
**Script:** `1_stereo_laser_pointcloud.py`

This script generates synchronized and corresponding 3D point clouds from:

- The **Technical Vision System (TVS)** using dynamic laser triangulation, and  
- The **stereo camera system (CAM)** using stereo triangulation of detected laser spots.

### Main operations:
- Loads synchronized acquisition data.
- Reconstructs 3D points independently for:
  - TVS coordinate frame: \( P^{(TVS)}_{j,k} \)
  - Stereo camera frame: \( P^{(CAM)}_{j,k} \)
- Preserves point-to-point correspondence using shared indices \((j, k)\), where:
  - \( j \) = scan-line (vertical angle index)  
  - \( k \) = platform stop index

### Output:
Two structured and synchronized point clouds:

- `P_TVS.npy` — TVS point cloud  
- `P_CAM.npy` — Stereo point cloud  

These point clouds are still expressed in **different coordinate frames** and are not yet aligned.

---

## Step 2: Application of Controlled Displacements  
**Script:** `2_apply_displacement_pointclouds.py`

This step simulates relative motion between sensor frames by applying known rigid displacements to the point clouds.

This is used to:

- Emulate practical misalignment conditions,
- Test robustness of the proposed registration method under controlled perturbations.

### Main operations:
- Applies translational offsets corresponding to platform motion.
- Generates multiple acquisition configurations corresponding to:
  - Different scanning distances,
  - Different numbers of translational positions.

### Output:
Displaced point clouds saved as:

- `P_TVS_disp.npy`  
- `P_CAM_disp.npy`  

These datasets represent the **unaligned multisensor point clouds** used as input for the registration framework.

---

## Step 3: Row-wise Registration and RMSE Evaluation  
**Script:** `3_align_pointclouds_calculate_rmse.py`

This script implements the core contribution of the paper:  
**scan-line-wise rigid registration using PCA-based local frames.**

### Main operations:

1. **Row-wise segmentation**  
   - Each point cloud is partitioned into horizontal scan-lines corresponding to constant vertical angles.

2. **PCA-based line fitting**  
   - For each scan-line:
     - Centroid is computed.
     - Principal direction is estimated using PCA.

3. **Local reference frame construction**  
   - Local orthonormal bases are built for both TVS and CAM rows.

4. **Row-wise rigid transformation estimation**  
   - Rotation matrices \( R_j \) are computed independently per scan-line:
     \[
     R_j = M^{(TVS)}_j \cdot (M^{(CAM)}_j)^T
     \]

5. **Row-wise alignment**
   - CAM points are rotated and translated into the TVS frame:
     \[
     \hat{p}^{(CAM)}_{j,k} = R_j (p^{(CAM)}_{j,k} - c^{(CAM)}_j) + c^{(TVS)}_j
     \]

6. **Error computation**
   - Root Mean Square Error (RMSE) is computed point-wise:
     \[
     RMSE = \sqrt{\frac{1}{MN}\sum_{j=0}^{N-1}\sum_{k=0}^{M-1}
     \|\hat{p}^{(CAM)}_{j,k} - p^{(TVS)}_{j,k}\|^2}
     \]

### Output:
- Aligned point clouds for visualization.
- Numerical RMSE values per experimental configuration.

---

## Relation to Experimental Results in the Paper

The scripts reproduce the experiments reported in the manuscript, including:

- Scanning distances of **20 cm, 25 cm, and 30 cm**.
- Vertical angular steps \( \Delta \lambda \) between **1° and 10°**.
- Multiple translational platform positions per scan.

The resulting RMSE statistics correspond to those reported in:

- Average RMSE vs. angular step,
- RMSE vs. number of translational positions,
- Distributional statistics and ANOVA analysis.

---

## Expected Folder Structure

The repository is expected to follow the structure below:

```text
project_root/
│
├── data/
│   ├── raw/
│   │   ├── stereo_images/
│   │   │   ├── left/
│   │   │   └── right/
│   │   └── tvs_signals/
│   │       └── waveforms/
│   │
│   ├── processed/
│   │   ├── P_TVS.npy
│   │   ├── P_CAM.npy
│   │   ├── P_TVS_disp.npy
│   │   └── P_CAM_disp.npy
│
├── scripts/
│   ├── 1_stereo_laser_pointcloud.py
│   ├── 2_apply_displacement_pointclouds.py
│   └── 3_align_pointclouds_calculate_rmse.py
│
├── results/
│   ├── aligned_pointclouds/
│   └── rmse_tables/
│
├── figures/
│   └── plots/
│
└── README.md
