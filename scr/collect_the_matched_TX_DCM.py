import os
import re
import shutil

def extract_key(folder_name):
    """Extract the key (6-digit number) from folder name."""
    match = re.search(r'_(\d{8})_', folder_name)
    if match:
        return match.group(1)
    return None

def find_matching_folder(key, search_root):
    """Search for a folder containing the key AND '_ReconPrimDS_' under search_root and its subfolders."""
    for root, dirs, files in os.walk(search_root):
        for dir_name in dirs:
            if key in dir_name and "_ReconPrimDS_n64" in dir_name:
                return os.path.join(root, dir_name)
    return None

def main(source_root, target_root, destination_root):
    # Make sure destination_root exists
    os.makedirs(destination_root, exist_ok=True)

    # List subfolders in source_root
    source_folders = [name for name in os.listdir(source_root)
                      if os.path.isdir(os.path.join(source_root, name))]

    for folder_name in source_folders:
        key = extract_key(folder_name)
        if key:
            matching_folder = find_matching_folder(key, target_root)
            if matching_folder:
                dest_folder_path = os.path.join(destination_root, os.path.basename(matching_folder))
                if not os.path.exists(dest_folder_path):
                    print(f"Copying: {matching_folder} --> {dest_folder_path}")
                    shutil.copytree(matching_folder, dest_folder_path)
                else:
                    print(f"Destination folder already exists: {dest_folder_path}")
            else:
                print(f"No match found for {folder_name}")
        else:
            print(f"No key found in folder name: {folder_name}")

if __name__ == "__main__":
    source_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_folder_match_v2"        # folder with the first type of names
    target_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2"         # folder where to search matching folders
    destination_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/TX_folder_match_v2"  # folder where matched folders will be copied
    main(source_root, target_root, destination_root)