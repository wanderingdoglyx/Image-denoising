import os
import shutil

def merge_subfolders(folder1, folder2, destination):
    # Get all unique subfolder names from both folders
    subfolders = set(os.listdir(folder1)) | set(os.listdir(folder2))

    for subfolder in subfolders:
        path1 = os.path.join(folder1, subfolder)
        path2 = os.path.join(folder2, subfolder)
        dest_path = os.path.join(destination, subfolder)

        # Create destination subfolder if it doesn't exist
        os.makedirs(dest_path, exist_ok=True)

        # Copy from folder1 if subfolder exists
        if os.path.isdir(path1):
            for item in os.listdir(path1):
                src = os.path.join(path1, item)
                dst = os.path.join(dest_path, item)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)

        # Copy from folder2 if subfolder exists
        if os.path.isdir(path2):
            for item in os.listdir(path2):
                src = os.path.join(path2, item)
                dst = os.path.join(dest_path, item)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)

if __name__ == "__main__":
    folder1 = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM"
    folder2 = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2"
    destination = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_total"

    merge_subfolders(folder1, folder2, destination)
    print("Merge complete.")