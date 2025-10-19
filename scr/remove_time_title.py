import os
import re

def remove_studies_prefix(folder_path):
    """
    Remove prefix ending with '__Studies_' from subfolder names under folder_path.
    Skip if the target name already exists.
    """
    pattern = re.compile(r'^.+__Studies_')  # Match anything up to and including '__Studies_'

    for name in os.listdir(folder_path):
        current_path = os.path.join(folder_path, name)

        if os.path.isdir(current_path) and pattern.match(name):
            new_name = pattern.sub('', name)
            new_path = os.path.join(folder_path, new_name)

            if os.path.exists(new_path):
                print(f"Skipping rename (target exists): {new_name}")
                continue

            os.rename(current_path, new_path)
            print(f"Renamed: {name} -> {new_name}")

# Example usage
root_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2'
remove_studies_prefix(root_folder)