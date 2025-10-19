import os
import numpy as np

def compute_sum_and_voxel_count(base_path, file_filter, shape=(64, 64, 30), dtype=np.float32):
    total_sum = 0.0
    total_voxels = 0
    matched_files = 0

    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if file_filter(filename):
                file_path = os.path.join(dirpath, filename)
                try:
                    data = np.fromfile(file_path, dtype=dtype)
                    if data.size != np.prod(shape):
                        print(f"Skipping {file_path}: unexpected size {data.size}")
                        continue
                    data = data.reshape(shape)
                    total_sum += data.sum()
                    total_voxels += data.size
                    matched_files += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if matched_files == 0:
        print(f"No valid matching files in: {base_path}")
        return 0.0, 0

    print(f"{matched_files} file(s) processed in {base_path}.")
    return total_sum, total_voxels

def task1_total(root_folder, subfolders):
    total_sum = 0.0
    total_voxels = 0
    for subfolder in subfolders:
        path = os.path.join(root_folder, subfolder)
        print(f"\nProcessing Task 1: {subfolder}")
        sub_sum, sub_voxels = compute_sum_and_voxel_count(
            base_path=path,
            file_filter=lambda f: "orig_" in f and "_d1.a00" in f
        )
        total_sum += sub_sum
        total_voxels += sub_voxels
    return total_sum, total_voxels

def task2_total(main_folder):
    print(f"\nProcessing Task 2: {main_folder}")
    return compute_sum_and_voxel_count(
        base_path=main_folder,
        file_filter=lambda f: f.endswith(".a00")
    )


# === USAGE ===
task1_root = "/data03/user-storage/y.zezhang/Ashequr/data_spie"
task1_subfolders = ["low_dose_proj_v2", "low_dose_proj_v2_hl"]

task2_main_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100"

sum1, voxels1 = task1_total(task1_root, task1_subfolders)
sum2, voxels2 = task2_total(task2_main_folder)

if voxels1 > 0 and voxels2 > 0:
    avg1 = sum1 / voxels1
    avg2 = sum2 / voxels2
    ratio = avg1 / avg2
    print(f"\nTask 1 Average: {avg1:.4f}")
    print(f"Task 2 Average: {avg2:.4f}")
    print(f"✅ Ratio (Task 1 Avg / Task 2 Avg): {ratio:.4f}")
else:
    print("\n❌ Unable to compute ratio due to missing or zero voxel counts.")