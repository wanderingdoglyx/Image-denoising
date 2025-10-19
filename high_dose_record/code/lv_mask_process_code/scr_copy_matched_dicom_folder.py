import os
import shutil
import pydicom

# Paths (edit as needed)
mat_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/LV_mask/LV_mask_v2'
dicom_root_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/raw_data/SA_folder'
output_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_folder_match_v2'

# Step 1: Extract IDs from .mat filenames
mat_ids = set()
for file in os.listdir(mat_folder):
    if file.endswith('.mat'):
        mat_id = file.split('_')[0]
        mat_ids.add(mat_id)

# Step 2: Find matching DICOM files and record their folders
matched_folders = set()

for root, _, files in os.walk(dicom_root_folder):
    for file in files:
        if file.lower().endswith('.dcm'):
            dicom_path = os.path.join(root, file)
            try:
                dcm = pydicom.dcmread(dicom_path, stop_before_pixels=True)
                patient_name_elem = dcm.get((0x0010, 0x0010), None)
                if patient_name_elem is not None:
                    patient_name = str(patient_name_elem.value).split('^')[0]
                    if patient_name in mat_ids:
                        matched_folders.add(root)
                        break
            except Exception as e:
                print(f"Could not read {dicom_path}: {e}")

# Step 3: Copy matched folders to the output folder
os.makedirs(output_folder, exist_ok=True)

for folder in matched_folders:
    dest_path = os.path.join(output_folder, os.path.basename(folder))
    if not os.path.exists(dest_path):
        shutil.copytree(folder, dest_path)
        print(f"Copied: {folder} -> {dest_path}")
    else:
        print(f"Skipped (already exists): {dest_path}")