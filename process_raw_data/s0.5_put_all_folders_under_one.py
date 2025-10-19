import os
import shutil

def copy_subsubfolders(src_root, dst_root):
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    # Walk through the source root folder
    for subfolder in os.listdir(src_root):
        subfolder_path = os.path.join(src_root, subfolder)
        if os.path.isdir(subfolder_path):
            # Look for sub-subfolders
            for subsubfolder in os.listdir(subfolder_path):
                subsubfolder_path = os.path.join(subfolder_path, subsubfolder)
                if os.path.isdir(subsubfolder_path):
                    dst_path = os.path.join(dst_root, f"{subfolder}_{subsubfolder}")
                    shutil.copytree(subsubfolder_path, dst_path)
                    print(f"Copied: {subsubfolder_path} -> {dst_path}")

# Example usage
source_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/raw_data/MIM_data_ze"
destination_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM"

copy_subsubfolders(source_folder, destination_folder)
