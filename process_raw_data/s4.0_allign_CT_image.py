import numpy as np
from scipy.ndimage import zoom
import os
from skimage.transform import resize

# Define the input and output directories
input_directory = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2/dose_level_100'
output_directory ='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2/dose_level_100'

#output_directory = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/processed_hl/dose_level_100'

patient_list = os.listdir(input_directory )
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)


for pat_id in patient_list:
    
    input_directory_folder=os.path.join(input_directory,pat_id)
    
    for filename in os.listdir(input_directory_folder):
        if filename.endswith('.ict'):
            input_filepath = os.path.join(input_directory_folder, filename)
            # === Path to the saved CT binary file ===
            ict_path=input_filepath
            # === Specify original shape ===
           
            height = 128
            width = 128
            num_elements = os.path.getsize(ict_path) // 4
            print(f"Total elements: {num_elements}")
            num_slices = num_elements // (height * width)
            print(f"Inferred shape: ({num_slices}, {height}, {width})")
            # === Load the .ict file ===
            ct_array = np.fromfile(ict_path, dtype=np.float32).reshape((num_slices, height, width))

            # === Reverse slice order (axis 0) ===
            ct_array = ct_array[::-1, :, :]

            # === Mirror left-right (flip horizontally, axis 2) ===
            ct_array = ct_array[:, :, ::-1]

            # === Save to new file ===
            #output_path = 'reversed_and_flipped.ict'

            
            output_directory_folder = os.path.join(output_directory,pat_id )
            os.makedirs(output_directory_folder, exist_ok=True)
            output_filepath = os.path.join(output_directory_folder,filename)
            
            ct_array.astype(np.float32).tofile(output_filepath)

            print(f"Saved flipped and reversed CT to: {output_filepath}")





