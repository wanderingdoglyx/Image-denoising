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

dose_level='dose_level_100'

outputFolder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl'

# Get the list of target patient 
#hl_patient_list_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments"
#hl_patient_list = os.listdir(hl_patient_list_path)

# Get the list of patient data and directories
#real_patient_data_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM"
#patient_list = os.listdir(real_patient_data_path)


# Define paths
root_ct_dir = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM'          # Folder containing all 'RegCT' folders
reference_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments'   # Third-level folder with patient IDs (or other reference names)


output_dir = os.path.join(outputFolder,dose_level)
os.makedirs(output_dir, exist_ok=True)

# Reference IDs
reference_ids = [
    name for name in os.listdir(reference_folder)
    if os.path.isdir(os.path.join(reference_folder, name))
]

for ref_id in reference_ids:
    matched_folder = None

    # Find corresponding RegCT folder
    for folder_name in os.listdir(root_ct_dir):
        if 'RegCT' in folder_name and ref_id in folder_name:
            matched_folder = os.path.join(root_ct_dir, folder_name)
            break

    if matched_folder is None or not os.path.isdir(matched_folder):
        print(f"No matching RegCT folder found for {ref_id}")
        continue

    dcm_files = [
        os.path.join(matched_folder, f)
        for f in os.listdir(matched_folder)
        if f.lower().endswith('.dcm')
    ]

    if not dcm_files:
        print(f"No .dcm files found in {matched_folder}")
        continue

    # Case 1: Single volume-integrated DICOM
    if len(dcm_files) == 1:
        try:
            ds = pydicom.dcmread(dcm_files[0])
            pixel_array = ds.pixel_array.astype(np.float32)

            if hasattr(ds, 'RescaleSlope') and hasattr(ds, 'RescaleIntercept'):
                pixel_array = pixel_array * float(ds.RescaleSlope) + float(ds.RescaleIntercept)

            output_path = os.path.join(output_dir,ref_id ,f"{ref_id}.ict")
            pixel_array.tofile(output_path)
            print(f"Saved volume-integrated {pixel_array.shape} to {output_path}")
        except Exception as e:
            print(f"Error reading multi-frame DICOM: {dcm_files[0]}: {e}")

    # Case 2: Multiple 2D slices to be stacked
    else:
        slices = []
        for file_path in dcm_files:
            try:
                ds = pydicom.dcmread(file_path)
                if hasattr(ds, 'SliceLocation'):
                    slice_array = ds.pixel_array.astype(np.float32)
                    if hasattr(ds, 'RescaleSlope') and hasattr(ds, 'RescaleIntercept'):
                        slice_array = slice_array * float(ds.RescaleSlope) + float(ds.RescaleIntercept)
                    slices.append((ds.SliceLocation, slice_array))
            except Exception as e:
                print(f"Skipping {file_path}: {e}")

        if slices:
            slices.sort(key=lambda x: x[0])
            volume = np.stack([s[1] for s in slices], axis=0).astype(np.float32)
            output_path = os.path.join(output_dir, ref_id,f"{ref_id}.ict")
            volume.tofile(output_path)
            print(f"Saved stacked slices {volume.shape} to {output_path}")
        else:
            print(f"No valid slices found in {matched_folder}")


    