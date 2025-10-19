import os
import numpy as np

def compute_average_total_count(base_path, file_filter, shape=(64, 64, 30), dtype=np.float32):
    total_image_sum = 0.0
    num_images = 0

    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if file_filter(filename):
                file_path = os.path.join(dirpath, filename)
                try:
                    data = np.fromfile(file_path, dtype=dtype)
                    if data.size != np.prod(shape):
                        print(f"Skipping {file_path}: unexpected size {data.size}")
                        continue
                    total_image_sum += np.sum(data)
                    num_images += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if num_images == 0:
        print(f"No valid matching files in: {base_path}")
        return None, 0

    avg_total_count = total_image_sum / num_images
    print(f"{num_images} file(s) processed in {base_path}. Average total count per image: {avg_total_count:.2f}")
    return avg_total_count, num_images

def task1_average_total_count(root_folder, subfolders):
    total_sum = 0.0
    total_images = 0
    for subfolder in subfolders:
        path = os.path.join(root_folder, subfolder)
        print(f"\nProcessing Task 1: {subfolder}")
        avg, num = compute_average_total_count(
            base_path=path,
            file_filter=lambda f: "orig_" in f and "_d1.a00" in f
        )
        if avg is not None:
            total_sum += avg * num
            total_images += num
    overall_avg = total_sum / total_images if total_images > 0 else None
    return overall_avg

def task2_average_total_count(main_folder):
    print(f"\nProcessing Task 2: {main_folder}")
    avg, _ = compute_average_total_count(
        base_path=main_folder,
        file_filter=lambda f: f.endswith(".a00")
    )
    return avg


# === USAGE ===
task1_root = "/data03/user-storage/y.zezhang/Ashequr/data_spie"
task1_subfolders = ["low_dose_proj_v2", "low_dose_proj_v2_hl"]

task2_main_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100"


avg1 = task1_average_total_count(task1_root, task1_subfolders)
avg2 = task2_average_total_count(task2_main_folder)

if avg1 is not None and avg2 is not None and avg2 != 0:
    ratio = avg1 / avg2
    print(f"\nTask 1 Avg Total Count per Image: {avg1:.2f}")
    print(f"Task 2 Avg Total Count per Image: {avg2:.2f}")
    print(f"✅ Ratio (Task 1 / Task 2): {ratio:.4f}")
else:
    print("\n❌ Unable to compute ratio due to missing or zero values.")