import os

def rename_subfolders(folder_path, prefix='2019-07__Studies_'):
    """
    Rename subfolders under folder_path by adding prefix if 'Studies' not in the name.
    """
    for name in os.listdir(folder_path):
        current_path = os.path.join(folder_path, name)

        if os.path.isdir(current_path) and 'Studies' not in name:
            new_name = prefix + name
            new_path = os.path.join(folder_path, new_name)

            # Rename the folder
            os.rename(current_path, new_path)
            print(f"Renamed: {name} -> {new_name}")

# Example usage
root_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2'
rename_subfolders(root_folder)