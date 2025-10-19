import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np
import os
from tempfile import TemporaryFile
import pandas as pd
import shutil 
import pydicom


def my_read_bin(cur_inp_file, data_type, input_shape):
    A = np.fromfile(cur_inp_file, dtype = data_type)
    A[np.isnan(A)] = 0
    A = np.reshape(A, input_shape)
    #A = np.transpose(A, [2, 1, 0])
    return A

def my_write_bin(cur_out_file, data_type, data):
    #data = np.transpose(data, [2, 1, 0])
    data.astype(data_type).tofile(cur_out_file)
    return

def convert_ct_to_mu(ct_array):
    mu = ct_array.astype(np.float64)
    
    neg_mask = ct_array < 0
    pos_mask = ct_array >= 0
    air_mask = ct_array == (-2000 - 1024)

    mu[neg_mask] = ct_array[neg_mask] * 1.52e-4 + 0.15
    mu[pos_mask] = ct_array[pos_mask] * 1.14e-4 + 0.15
    mu[air_mask] = 0
    mu[mu < 0] = 0

    return mu.astype(np.float32)



dose_level='dose_level_100'

outputFolder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2'

# Get the list of target patient 
#hl_patient_list_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments"
#hl_patient_list = os.listdir(hl_patient_list_path)

# Get the list of patient data and directories
#real_patient_data_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM"
#patient_list = os.listdir(real_patient_data_path)


# Define paths
root_ct_dir = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2'          # Folder containing all 'RegCT' folders
reference_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments_v2'   # Third-level folder with patient IDs (or other reference names)


output_dir = os.path.join(outputFolder,dose_level)
os.makedirs(output_dir, exist_ok=True)

# Get list of subfolder names from the reference folder
reference_ids = [
    name for name in os.listdir(reference_folder)
    if os.path.isdir(os.path.join(reference_folder, name))
]

# Loop over reference IDs and match corresponding RegCT folders
for ref_id in reference_ids:
    matched_folder = None

    # Search for a subfolder in root_ct_dir that contains both 'RegCT' and the reference ID
    for folder_name in os.listdir(root_ct_dir):
        if 'RegCT' in folder_name and ref_id in folder_name:
            matched_folder = os.path.join(root_ct_dir, folder_name)
            break

    if matched_folder is None or not os.path.isdir(matched_folder):
        print(f"No matching RegCT folder found for {ref_id}")
        continue

    # Load and sort CT slices
    slices = []
    for filename in os.listdir(matched_folder):
        if filename.lower().endswith('.dcm'):
            file_path = os.path.join(matched_folder, filename)
            try:
                ds = pydicom.dcmread(file_path)
                if hasattr(ds, 'SliceLocation'):
                    pixel_array = ds.pixel_array.astype(np.float32)
                    if hasattr(ds, 'RescaleSlope') and hasattr(ds, 'RescaleIntercept'):
                        pixel_array = pixel_array * float(ds.RescaleSlope) + float(ds.RescaleIntercept)
                        
                    slices.append((ds.SliceLocation, pixel_array))
            except Exception as e:
                print(f"Skipping {file_path}: {e}")

    if slices:
        slices.sort(key=lambda x: x[0])
        volume = np.stack([s[1] for s in slices], axis=0).astype(np.float32)
        mu_array=convert_ct_to_mu(volume)
        
        output_path = os.path.join(output_dir,ref_id ,f"{ref_id}.ict")
        mu_array.tofile(output_path)
        print(f"Saved {mu_array.shape} volume to {output_path}")
    else:
        print(f"No valid slices in folder {matched_folder}")


    