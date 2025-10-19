import os

# Set the path to the main folder
main_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_SA_images/CTAC'

# Set the output file name
output_file = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/document/patient_list/patient_names_total_clear.txt'

# Get all subfolder names
subfolders = [name for name in os.listdir(main_folder)
              if os.path.isdir(os.path.join(main_folder, name))]

# Write subfolder names to a text file
with open(output_file, 'w') as f:
    for folder in subfolders:
        f.write(folder + '\n')

print(f"Saved {len(subfolders)} subfolder names to {output_file}")