import os
import pydicom
from scipy.io import loadmat

# Replace with your actual paths
mat_folder = '/path/to/mat/files'
dicom_root_folder = '/path/to/dicom/folder'

# Step 1: Read all .mat filenames (extract prefix before "_")
mat_ids = set()
for file in os.listdir(mat_folder):
    if file.endswith('.mat'):
        mat_id = file.split('_')[0]
        mat_ids.add(mat_id)

# Step 2: Walk through all subfolders for DICOM files
unmatched_dicom_folders = set()
dicom_id_to_folder = {}

for root, _, files in os.walk(dicom_root_folder):
    for file in files:
        if file.lower().endswith('.dcm'):
            dicom_path = os.path.join(root, file)
            try:
                dcm = pydicom.dcmread(dicom_path, stop_before_pixels=True)
                patient_name = str(dcm.get((0x0010, 0x0010), '')).strip()
                if patient_name not in mat_ids:
                    unmatched_dicom_folders.add(os.path.basename(root))
            except Exception as e:
                print(f"Could not read {dicom_path}: {e}")

# Output the unmatched folders
print("Subfolders with unmatched DICOM files:")
for folder in sorted(unmatched_dicom_folders):
    print(folder)