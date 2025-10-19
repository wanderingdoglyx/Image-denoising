import os
import shutil

def copy_subsubfolders(src_root, dst_root):
    """
    Copy all sub-subfolders (2 levels deep) from src_root to dst_root.
    """
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    for subfolder in os.listdir(src_root):
        subfolder_path = os.path.join(src_root, subfolder)
        if os.path.isdir(subfolder_path):
            for subsubfolder in os.listdir(subfolder_path):
                subsubfolder_path = os.path.join(subfolder_path, subsubfolder)
                if os.path.isdir(subsubfolder_path):
                    target_path = os.path.join(dst_root, f"{subfolder}/{subsubfolder}")
                    shutil.copytree(subsubfolder_path, target_path)
                    print(f"Copied: {subsubfolder_path} -> {target_path}")

# Example usage
source_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_SA_images/CTAC"
target_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/neural_network_data/training_v3"
copy_subsubfolders(source_folder, target_folder)
