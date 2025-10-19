import os
import pydicom
from pathlib import Path

# === Define paths ===
reference_root = Path('/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2/dose_level_100')  # Target: where subfolders are written to
source_root = Path('/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2')        # Contains RegCT and PriPrj folders
template_dir = Path('/datastore01/user-storage/y.zezhang/2025_high_dose_project/supporting_file')     # Contains ct.hct and .h00 template

# === Load templates ===
with open(template_dir / 'mod_proj_da2130s100_obj_01927022_d1.h00', 'r') as f:
    h00_template = f.read()

with open(template_dir / 'ct.hct', 'r') as f:
    hct_template = f.read()

# === Process each reference subfolder ===
for subfolder in reference_root.iterdir():
    
    if not subfolder.is_dir():
        continue

    ref_id = subfolder.name
    
    # === Locate corresponding RegCT and PriPrj folders ===
    regct_folder = next((source_root / f for f in os.listdir(source_root)
                         if 'RegCT' in f and ref_id in f and (source_root / f).is_dir()), None)
    prj_folder = next((source_root / f for f in os.listdir(source_root)
                       if 'PriPrj' in f and ref_id in f and (source_root / f).is_dir()), None)
    
    if regct_folder is None or prj_folder is None:
        print(f"Skipping {ref_id}: missing RegCT or PriPrj folder.")
        continue

    # === Read any .dcm file from PriPrj and RegCT folders ===
    def read_first_dcm(folder):
        for file in os.listdir(folder):
            if file.lower().endswith('.dcm'):
                try:
                    return pydicom.dcmread(folder / file)
                except Exception as e:
                    print(f"Failed to read DICOM in {folder}: {e}")
                    return None
        return None

    prj_dcm = read_first_dcm(prj_folder)
    regct_dcm = read_first_dcm(regct_folder)

    
    
    if prj_dcm is None or regct_dcm is None:
        print(f"Skipping {ref_id}: could not read DICOMs.")
        continue

    # === Get needed DICOM fields ===
    try:
        num_frames = int(prj_dcm[0x0028, 0x0008].value)  # Number of Frames in Rotation
        prj_rows = int(prj_dcm.Rows)
        prj_cols = int(prj_dcm.Columns)
        start_angle=float(prj_dcm[0x0054,0x0022][0][0x0054,0x0200].value)
        scan_angle= float(prj_dcm[0x0054,0x0052][0][0x0018,0x1143].value)
        
    except:
        print(f"Skipping {ref_id}: missing PriPrj metadata.")
        continue

    try:
        regct_rows = int(regct_dcm.Rows)
        regct_cols=int(regct_dcm.Columns)
        slice_thickness=float(regct_dcm[0x0018,0x0050].value)
    except:
        print(f"Skipping {ref_id}: missing RegCT metadata.")
        continue

    # === Count .dcm files in RegCT folder ===
    regct_dcm_count = sum(1 for f in os.listdir(regct_folder) if f.lower().endswith('.dcm'))



    # === Modify .h00 content ===
    h00_modified = h00_template
    h00_modified = h00_modified.replace(
        '!name of data file := mod_proj_da2130s100_obj_01927022_d1.a00',
        f'!name of data file := {ref_id}.a00'
    )
    h00_modified = h00_modified.replace(
        'patient name := SMC_mod_proj_da2130s100_obj_01927022_d1.a00',
        f'patient name := SMC_{ref_id}.a00'
    )
    '''
    h00_modified = h00_modified.replace(
        '!total number of images := 30',
        f'!total number of images := {num_frames}'
    )
    h00_modified = h00_modified.replace(
        '!matrix size [1] := 64',
        f'!matrix size [1] := {prj_rows}'
    )
    h00_modified = h00_modified.replace(
        '!matrix size [2] := 64',
        f'!matrix size [2] := {prj_cols}'
    )
    '''
    h00_modified = h00_modified.replace(
        'start angle := 225.350',
        f'start angle := {round(start_angle,3)}'
    )
    '''
    h00_modified = h00_modified.replace(
        '!number of projections := 30',
        f'!number of projections := {num_frames}'
    )
    h00_modified = h00_modified.replace(
        '!number of images/energy window := 30',
        f'!number of images/energy window := {num_frames}'
    )
    h00_modified = h00_modified.replace(
        'image duration (sec) := 30.000',
        f'image duration (sec) := {num_frames}'
    )
    '''
    h00_modified = h00_modified.replace(
        'scaling factor (mm/pixel) [1] := 6.800',
        f'scaling factor (mm/pixel) [1] := {round(435.0090/prj_rows,2)}'
    )
    h00_modified = h00_modified.replace(
        'scaling factor (mm/pixel) [2] := 6.800',
        f'scaling factor (mm/pixel) [1] := {round(435.0090/prj_cols,2)}'
    )
    h00_modified = h00_modified.replace(
        'scaling factor (mm/pixel) [3] := 6.800',
        f'scaling factor (mm/pixel) [3] := {round((204/num_frames)*(scan_angle/180),2)}'
    )
    h00_modified = h00_modified.replace(
        '!extent of rotation := 180',
        f'!extent of rotation := {scan_angle}'
    )
    
    
    # === Modify .hct content ===
    hct_modified = hct_template
    hct_modified = hct_modified.replace(
        '!total number of images := 64',
        f'!total number of images := {regct_dcm_count}'
    )
    '''
    hct_modified = hct_modified.replace(
        '!matrix size [1] := 128',
        f'!matrix size [1] := {regct_rows}'
    )
    hct_modified = hct_modified.replace(
        '!matrix size [2] := 128',
        f'!matrix size [2] := {regct_cols}'
    )
    '''
    hct_modified = hct_modified.replace(
        '!matrix size [3] := 64',
        f'!matrix size [3] := {regct_dcm_count}'
    )
    '''
    hct_modified = hct_modified.replace(
        'scaling factor (mm/pixel) [1] := 3.4',
        f'scaling factor (mm/pixel) [1] := {round(435.1606/regct_rows,3)}'
    )
    hct_modified = hct_modified.replace(
        'scaling factor (mm/pixel) [2] := 3.4',
        f'scaling factor (mm/pixel) [2] := {round(435.1606/regct_cols,3)}'
    )
    '''
    hct_modified = hct_modified.replace(
        'scaling factor (mm/pixel) [3] := 6.8',
        f'scaling factor (mm/pixel) [3] := {round(float(regct_dcm[0x0018,0x0050].value),2)}'
    )
    hct_modified = hct_modified.replace(
        '!number of images/energy window := 64',
        f'!number of images/energy window := {regct_dcm_count}'
    )
    hct_modified = hct_modified.replace(
        '!name of data file := ct.ict',
        f'!name of data file := {ref_id}.ict'
    )
    # === Save modified files ===
    h00_path = subfolder / f"{ref_id}.h00"
    hct_path = subfolder / f"{ref_id}.hct"

    with open(h00_path, 'w') as f:
        f.write(h00_modified)

    with open(hct_path, 'w') as f:
        f.write(hct_modified)

    print(f"Processed {ref_id}: .h00 and .hct written to {subfolder}")