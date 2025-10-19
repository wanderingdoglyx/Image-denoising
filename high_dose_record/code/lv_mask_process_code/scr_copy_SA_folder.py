import os
import shutil

def copy_matching_folders(src_root, dst_root, keyword="Short.Axis.ReconSA"):
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    for root, dirs, files in os.walk(src_root):
        for dirname in dirs:
            if keyword in dirname:
                src_folder_path = os.path.join(root, dirname)
                dst_folder_path = os.path.join(dst_root, dirname)

                print(f"Copying: {src_folder_path} -> {dst_folder_path}")
                shutil.copytree(src_folder_path, dst_folder_path, dirs_exist_ok=True)

# Example usage
source_directory = r"/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/raw_data/MIM_data_v2"
destination_directory = r"/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/raw_data/SA_folder"

copy_matching_folders(source_directory, destination_directory)