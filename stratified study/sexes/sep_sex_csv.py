import pandas as pd
import os
from glob import glob
import re

# === CONFIG ===
name_map_path = "name_changes.xlsx"  # Excel file with OldName, NewName
csv_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/observer_study_04_main/stratified study/sexes/csv_results"  # Path to folder with .csv files
male_ids_path = "male.txt"
female_ids_path = "female.txt"

# === STEP 1: Load name map ===
name_map_df = pd.read_excel(name_map_path)
name_map = dict(zip(name_map_df['OldName'], name_map_df['NewName']))  # old → new

# Reverse map to get NewName → OldName
reverse_map = {v: k for k, v in name_map.items()}

# === STEP 2: Load sex info ===
with open(male_ids_path, "r") as f:
    male_ids = set(line.strip() for line in f if line.strip())

with open(female_ids_path, "r") as f:
    female_ids = set(line.strip() for line in f if line.strip())

# === STEP 3: Process each .csv file ===
csv_files = glob(os.path.join(csv_folder, "*.csv"))

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    # Extract image name (NewName), then map back to OldName
    if 'ImageName' not in df.columns:
        df['ImageName'] = df.apply(
            lambda row: f"h1_img{int(row['ImageID'])}.png" if str(row['Defect_Present']).strip().upper() == "TRUE"
                        else f"h2_img{int(row['ImageID'])}.png",
            axis=1
        )

    # Map new name to old name using the Excel file
    df['OldName'] = df['ImageName'].map(reverse_map)

    # Extract ID from old name (e.g., "pat03324602_d1_di2130s250.png" → "03324602")
    def extract_id(old_name):
        if pd.isna(old_name):
            return None
        match = re.search(r'pat(\d+)_', old_name)
        return match.group(1) if match else None

    df['PatientID'] = df['OldName'].apply(extract_id)

    # Filter by sex
    male_df = df[df['PatientID'].isin(male_ids)]
    female_df = df[df['PatientID'].isin(female_ids)]

    # Save outputs
    base = os.path.splitext(os.path.basename(csv_file))[0]
    male_df.to_csv(os.path.join(csv_folder, f"{base}_male.csv"), index=False)
    female_df.to_csv(os.path.join(csv_folder, f"{base}_female.csv"), index=False)

    print(f"Saved: {base}_male.csv and {base}_female.csv")

